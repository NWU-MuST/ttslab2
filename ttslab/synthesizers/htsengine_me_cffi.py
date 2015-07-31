#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A very simple class wrapper for the HTS Engine API modified for
   mixed excitation (ME) in ../hts_engine

   At the moment the ME filters are loaded separately and carried
   around in Python, in future we could integrate this into the
   HTS_Engine struct in C.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os
import locale
locale.setlocale(locale.LC_NUMERIC, ("C", "UTF-8")) #for C atof calls to recognize "." as floating point
import cffi #from cffi import FFI

# setup FFI and library module-globally
MODULE_DIR = os.path.abspath(os.path.dirname(__file__)) #the htsengine .h and .so files need to be in this directory
FFI = cffi.FFI()
with open(os.path.join(MODULE_DIR, "HTS_engine_cffi.h")) as infh:
    FFI.cdef(infh.read() + "\n" + "\n".join(["FILE *fmemopen(void *buf, size_t size, const char *mode);",
                                             "int fclose(FILE *fp);"]) + "\n")
LIBHTS = FFI.dlopen(os.path.join(MODULE_DIR, "libHTSEngine.so"))
LIBC = FFI.dlopen(None)

import numpy as np

from ttslab.waveform import Waveform, normrange


def castdouble_np_2d_arr(x):
    """ from: http://arjones6.blogspot.com/2013/05/passing-multidimensional-numpy-arrays.html
    """
    if not x.dtype == np.float64:
        x = x.astype(np.float64)
    ap = FFI.new("double* [%d]" % (x.shape[0]))
    ptr = FFI.cast("double *", x.ctypes.data)
    for i in range(x.shape[0]):
        ap[i] = ptr + i*x.shape[1]
    return ap

def castdouble_np_flat_arr(x):
    """ from: http://arjones6.blogspot.com/2013/05/passing-multidimensional-numpy-arrays.html
    """
    if not x.dtype == np.float64:
        x = x.astype(np.float64)
    return FFI.cast("double *", x.ctypes.data)

def label_add_durs(htslabel, durs):
    """ seconds "end times" to HTK int start end times
    """
    htslabel = [l.split()[-1] for l in htslabel] #strip times if exist
    assert len(htslabel) == len(durs)
    starttime = 0
    for i in xrange(len(htslabel)):
        htkdur = int(durs[i] * 1e7)
        htslabel[i] = b" ".join([str(starttime), str(starttime + htkdur), htslabel[i]])
        starttime += htkdur
    return htslabel

def label_to_durs(htslabel):
    """label to simple list of durations in seconds...
    """
    durs = []
    for l in htslabel.splitlines():
        durs.append(int(l.split()[1]) / 1e7)
    return durs

def tof0(lf0):
    return np.exp(lf0)

def tolf0(f0):
    tmp = np.log(f0)
    tmp[tmp == -np.inf] = -1.0e+10
    return tmp


class HTSError(Exception):
    pass

class HTS_EngineME(object):
    SPEECHPARMS = {"mgc": 0,
                   "lf0": 1,
                   "str": 2}
    HTS_TRUE = 1
    HTS_FALSE = 0
    def __init__(self, voice, mefilt, pdfilt): #these are python bytestrings obtained from the original files...
        # init HTS_Engine and load voice...
        self.engine = FFI.new("HTS_Engine *")
        LIBHTS.HTS_Engine_initialize(self.engine)
        voicebuf = FFI.new("char[]", voice)
        mode = FFI.new("char[]", b"r")
        voicefp = LIBC.fmemopen(voicebuf, len(voice), mode)
        ok = bool(ord(LIBHTS.HTS_Engine_load_fp(self.engine, voicefp))) #LIBC.fclose(voicefp) --- WILL BE CLOSED INTERNALLY
        if not ok:
            raise HTSError("HTS_Engine: failed to load voice file...")
        # load mixed excitation bandpass filters and pulse dispersion filter from text files...
        mefiltlines = mefilt.split()
        self.me_nfilters = int(mefiltlines[0])
        self.me_filtorder = int(mefiltlines[1])
        self.me_filters = np.zeros((self.me_nfilters, self.me_filtorder), dtype=np.float64)
        for i in range(self.me_nfilters):
            self.me_filters[i,:] = map(float, mefiltlines[i*self.me_filtorder+2:i*self.me_filtorder+2+self.me_filtorder])
        self.me_filterpointers = castdouble_np_2d_arr(self.me_filters)
        pdfiltlines = pdfilt.split()
        self.pd_filtorder = int(pdfiltlines[0])
        self.pd_filter = np.array(map(float, pdfiltlines[1:]))
        self.pd_filterpointer = castdouble_np_flat_arr(self.pd_filter)
        # allocate buffers for ME vocoder's excitation signals
        self.xp_sig = FFI.new("double[]", self.me_filtorder)
        self.xn_sig = FFI.new("double[]", self.me_filtorder)
        self.hp = FFI.new("double[]", self.me_filtorder)
        self.hn = FFI.new("double[]", self.me_filtorder)
        #flag to check whether some requests can be serviced
        self.donesynth = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        LIBHTS.HTS_Engine_refresh(self.engine)
        LIBHTS.HTS_Engine_clear(self.engine)
        #Other allocations get free'd automatically by CFFI when out of scope

    def synth(self, htslabel, lf0=None, use_labalignments=False):
        """ htslabel is a sequence of strings...
        """
        self.htslabel = htslabel
        htslabelc = []
        for line in htslabel:
            htslabelc.append(FFI.new("char[]", line))
        htslabelc = tuple(htslabelc)
        #prep lf0 input
        if lf0 is not None:
            ilf0_nframes = len(lf0)
            ilf0 = castdouble_np_flat_arr(lf0)
        else:
            ilf0_nframes = 0
            ilf0 = FFI.NULL
        if use_labalignments:
            LIBHTS.HTS_Engine_set_phoneme_alignment_flag(self.engine, bytes(bytearray((self.HTS_TRUE,))))
        LIBHTS.HTS_Engine_synthesize_me_with_lf0_from_strings(self.engine, htslabelc, len(htslabelc),
                                                              self.me_nfilters, self.me_filtorder, self.me_filterpointers,
                                                              self.pd_filtorder, self.pd_filterpointer,
                                                              self.xp_sig, self.xn_sig, self.hp, self.hn,
                                                              ilf0, ilf0_nframes)
        LIBHTS.HTS_Engine_set_phoneme_alignment_flag(self.engine, bytes(bytearray((self.HTS_FALSE,)))) #Reset...
        self.donesynth = True

    def get_wav(self):
        assert self.donesynth
        waveform = Waveform()
        waveform.samples = np.zeros(LIBHTS.HTS_Engine_get_nsamples(self.engine), np.int16) #16-bit samples
        waveform.samplerate = int(LIBHTS.HTS_Engine_get_sampling_frequency(self.engine))
        waveform.channels = 1
        for i in range(len(waveform.samples)):
            waveform.samples[i] = LIBHTS.HTS_Engine_get_generated_speech(self.engine, i) #copy
        return waveform

    def get_parm(self, parm):
        """Can get generated parameter streams by index from HTS, we also
           allow parm specification as defined in SPEECHPARMS...
        """
        assert self.donesynth
        if parm in self.SPEECHPARMS:
            parmidx = self.SPEECHPARMS[parm]
        else:
            parmidx = int(parm)
        veclength = LIBHTS.HTS_GStreamSet_get_vector_length(FFI.new("HTS_GStreamSet *", self.engine.gss), parmidx)
        length = LIBHTS.HTS_GStreamSet_get_total_frame(FFI.new("HTS_GStreamSet *", self.engine.gss))
        x = np.zeros((veclength, length), dtype=np.float64)
        for i in xrange(veclength):
            for j in xrange(length):
                x[i, j] = LIBHTS.HTS_Engine_get_generated_parameter(self.engine, parmidx, j, i) #copy
        return x

    def get_dur(self):
        assert self.donesynth
        durs = np.zeros(len(self.htslabel), dtype=np.float64)
        states_per_model = LIBHTS.HTS_ModelSet_get_nstate(FFI.new("HTS_ModelSet *", self.engine.ms))
        statei = 0
        for i in range(len(self.htslabel)):
            for j in range(states_per_model):
                durs[i] += LIBHTS.HTS_SStreamSet_get_duration(FFI.new("HTS_SStreamSet *", self.engine.sss), statei)
                statei += 1
        durs *= self.engine.condition.fperiod / LIBHTS.HTS_Engine_get_sampling_frequency(self.engine)
        return durs

    def get_segtimes(self):
        assert self.donesynth
        durs = self.get_dur()
        starttime = 0.0
        segtimes = []
        for dur in durs:
            segtimes.append([starttime, starttime+dur])
            starttime += dur
        return segtimes

    def get_f0(self, log=False):
        lf0 = self.get_parm("lf0")
        if log:
            return lf0.flatten()
        else:
            return tof0(lf0).flatten()
        

def maintest():
    """Brute-force method to check for memory leaks...
    """
    import sys
    voicefn = sys.argv[1]
    mefiltfn = sys.argv[2]
    pdfiltfn = sys.argv[3]
    labfn = sys.argv[4]
    with open(voicefn, "rb") as infh:
        voice = infh.read()
    with open(labfn) as infh:
        label = infh.read().splitlines()
    with open(mefiltfn) as infh:
        mefilt = infh.read()
    with open(pdfiltfn) as infh:
        pdfilt = infh.read()
    while True:
        print(".", end="", file=sys.stderr)
        with HTS_EngineME(voice, mefilt, pdfilt) as htsengine:
            htsengine.synth(label)
            # import pylab as pl
            # waveform = htsengine.get_wav()
            # spectrum = htsengine.get_parm("mgc")
            # bandpass = htsengine.get_parm("str")
            # f0 = tof0(htsengine.get_f0("lf0"))
            # durs = htsengine.get_dur()
            # pl.subplot(511)
            # pl.plot(waveform.samples)
            # pl.subplot(512)
            # pl.imshow(spectrum)
            # pl.subplot(513)
            # pl.imshow(bandpass)
            # pl.subplot(514)
            # pl.plot(f0)
            # pl.subplot(515)
            # pl.plot(durs)
            # pl.show()

if __name__ == "__main__":
    maintest()
