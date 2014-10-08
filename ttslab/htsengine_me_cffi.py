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

import locale
locale.setlocale(locale.LC_NUMERIC, ("C", "UTF-8")) #for C atof calls to recognize "." as floating point
from cffi import FFI

import numpy as np

from ttslab.waveform import Waveform, normrange

def castdouble_np_2d_arr(ffi, x):
    """ from: http://arjones6.blogspot.com/2013/05/passing-multidimensional-numpy-arrays.html
    """
    if not x.dtype == np.float64:
        x = x.astype(np.float64)
    ap = ffi.new("double* [%d]" % (x.shape[0]))
    ptr = ffi.cast("double *", x.ctypes.data)
    for i in range(x.shape[0]):
        ap[i] = ptr + i*x.shape[1]
    return ap

def castdouble_np_flat_arr(ffi, x):
    """ from: http://arjones6.blogspot.com/2013/05/passing-multidimensional-numpy-arrays.html
    """
    if not x.dtype == np.float64:
        x = x.astype(np.float64)
    return ffi.cast("double *", x.ctypes.data)

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
    def __init__(self, voicefn, mefiltfn, pdfiltfn):
        # setup FFI, library, init HTS_Engine and load voice...
        self.ffi = FFI()
        with open("HTS_engine_cffi.h") as infh:
            self.ffi.cdef(infh.read())
        self.libhts = self.ffi.dlopen("./libHTSEngine.so")
        self.engine = self.ffi.new("HTS_Engine *")
        self.libhts.HTS_Engine_initialize(self.engine)
        cvoicefn = self.ffi.new("char[]", voicefn)
        ok = bool(ord(self.libhts.HTS_Engine_load(self.engine, (cvoicefn, ), 1)))
        if not ok:
            raise HTSError("HTS_Engine: failed to load voice file...")
        # load mixed excitation bandpass filters and pulse dispersion filter from text files...
        with open(mefiltfn) as infh:
            lines = infh.read().split()
        self.me_nfilters = int(lines[0])
        self.me_filtorder = int(lines[1])
        self.me_filters = np.zeros((self.me_nfilters, self.me_filtorder), dtype=np.float64)
        for i in range(self.me_nfilters):
            self.me_filters[i,:] = map(float, lines[i*self.me_filtorder+2:i*self.me_filtorder+2+self.me_filtorder])
        self.me_filterpointers = castdouble_np_2d_arr(self.ffi, self.me_filters)
        with open(pdfiltfn) as infh:
            lines = infh.read().split()
        self.pd_filtorder = int(lines[0])
        self.pd_filter = np.array(map(float, lines[1:]))
        self.pd_filterpointer = castdouble_np_flat_arr(self.ffi, self.pd_filter)
        # allocate buffers for ME vocoder's excitation signals
        self.xp_sig = self.ffi.new("double[]", self.me_filtorder)
        self.xn_sig = self.ffi.new("double[]", self.me_filtorder)
        self.hp = self.ffi.new("double[]", self.me_filtorder)
        self.hn = self.ffi.new("double[]", self.me_filtorder)

    def _synth(self, htslabel, use_labalignments=False, lf0=None):
        """ htslabel is a sequence of strings...
        """
        htslabelc = []
        for line in htslabel:
            htslabelc.append(self.ffi.new("char[]", line))
        htslabelc = tuple(htslabelc)
        if not lf0 is None:
            ilf0_nframes = len(lf0)
            ilf0 = castdouble_np_flat_arr(self.ffi, lf0)
        else:
            ilf0_nframes = 0
            ilf0 = self.ffi.NULL
        if use_labalignments:
            self.libhts.HTS_Engine_set_phoneme_alignment_flag(self.engine, bytes(bytearray((self.HTS_TRUE,))))
        self.libhts.HTS_Engine_synthesize_me_with_lf0_from_strings(self.engine, htslabelc, len(htslabelc),
                                                                   self.me_nfilters, self.me_filtorder, self.me_filterpointers,
                                                                   self.pd_filtorder, self.pd_filterpointer,
                                                                   self.xp_sig, self.xn_sig, self.hp, self.hn,
                                                                   ilf0, ilf0_nframes)
        self.libhts.HTS_Engine_set_phoneme_alignment_flag(self.engine, bytes(bytearray((self.HTS_FALSE,)))) #Reset...

    def _synth_with_dur(self, htslabel, dur=None, lf0=None):
        if dur is not None:
            htslabel = label_add_durs(htslabel, dur)
            use_labalignments = True
        else:
            use_labalignments = False
        self._synth(htslabel, use_labalignments=use_labalignments, lf0=lf0)

    def synth_get_wav(self, htslabel, dur=None, lf0=None):
        self._synth_with_dur(htslabel, dur, lf0)
        waveform = Waveform()
        waveform.samples = np.zeros(self.libhts.HTS_Engine_get_nsamples(self.engine), np.int16) #16-bit samples
        waveform.samplerate = int(self.libhts.HTS_Engine_get_sampling_frequency(self.engine))
        waveform.channels = 1
        for i in range(len(waveform.samples)):
            waveform.samples[i] = self.libhts.HTS_Engine_get_generated_speech(self.engine, i)
        return waveform

    def synth_get_parm(self, htslabel, parm, dur=None, lf0=None):
        self._synth_with_dur(htslabel, dur, lf0)
        if parm in self.SPEECHPARMS:
            parmidx = self.SPEECHPARMS[parm]
        else:
            parmidx = int(parm)
        veclength = self.libhts.HTS_GStreamSet_get_vector_length(self.ffi.new("HTS_GStreamSet *", self.engine.gss), parmidx)
        length = self.libhts.HTS_GStreamSet_get_total_frame(self.ffi.new("HTS_GStreamSet *", self.engine.gss))
        x = np.zeros((veclength, length), dtype=np.float64)
        for i in xrange(veclength):
            for j in xrange(length):
                x[i, j] = self.libhts.HTS_Engine_get_generated_parameter(self.engine, parmidx, j, i)
        return x

    def synth_get_dur(self, htslabel):
        self._synth(htslabel)
        durs = np.zeros(len(htslabel), dtype=np.float64)
        states_per_model = self.libhts.HTS_ModelSet_get_nstate(self.ffi.new("HTS_ModelSet *", self.engine.ms))
        statei = 0
        for i in range(len(htslabel)):
            for j in range(states_per_model):
                durs[i] += self.libhts.HTS_SStreamSet_get_duration(self.ffi.new("HTS_SStreamSet *", self.engine.sss), statei)
                statei += 1
        durs *= self.engine.condition.fperiod / self.libhts.HTS_Engine_get_sampling_frequency(self.engine)
        return durs


def maintest():
    import sys
    voicefn = sys.argv[1]
    mefiltfn = sys.argv[2]
    pdfiltfn = sys.argv[3]
    labfn = sys.argv[4]
    htsengine = HTS_EngineME(voicefn, mefiltfn, pdfiltfn)
    wave = htsengine.synth(open(labfn).read().splitlines())


if __name__ == "__main__":
    maintest()
