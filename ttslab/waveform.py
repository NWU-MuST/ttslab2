# -*- coding: utf-8 -*-
""" A simple Waveform class to manage audio as numpy arrays.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import numpy as np
import wave
try:
    import scikits.audiolab as AL
except ImportError:
    AL = None
    import scipy.io.wavfile as wavfile
try:
    import cStringIO as StringIO
except ImportError:
    import io.StringIO as StringIO

def normrange(values, minval=-0.8, maxval=0.8):
    values = values.astype(np.float64)
    if len(values.shape) == 1:
        newvalues = values / (np.max(values) - np.min(values)) * (maxval - minval)
        newvalues = newvalues - np.min(newvalues) + minval
    else:
        for i in range(values.shape[1]):
            newvalues[:,i] = values[:,i] / (np.max(values[:,i]) - np.min(values[:,i])) * (maxval - minval)
            newvalues[:,i] = newvalues[:,i] - np.min(newvalues[:,i]) + minval
    return newvalues - np.mean(newvalues)

def riffstring(waveform):
    f = StringIO.StringIO()
    if waveform.samples.dtype == np.int16:
        s = waveform.samples.tostring()
    else:
        s = (waveform.samples * 32767).astype(np.int16).tostring()
    wf = wave.open(f, "w")
    wf.setparams((1, 2, waveform.samplerate, len(waveform.samples), "NONE", "No compression"))
    wf.writeframes(s)            
    wf.close()
    return f.getvalue()

if AL:
    class Waveform(object):
        """ Simply holds waveforms in numpy arrays...
        """
        def __init__(self, filename=None):
            self.samplerate = None
            self.samples = None
            self.channels = None
            if filename:
                self.read(filename)

        def __len__(self):
            return len(self.samples)

        def read(self, filename, dtype=np.float64):
            f = AL.Sndfile(filename, 'r')
            self.samplerate = f.samplerate
            self.samples = f.read_frames(f.nframes, dtype=dtype)
            if len(self.samples.shape) == 2:
                self.channels = self.samples.shape[1]
            else:
                self.channels = 1
            f.close()

        def write(self, filename, encoding="pcm16", endianness="file", fileformat=None):
            if not fileformat:
                fileformat = os.path.basename(filename).split(".")[-1]
            format = AL.Format(fileformat, encoding, endianness)
            f = AL.Sndfile(filename, "w", format, self.channels, self.samplerate)
            f.write_frames(self.samples)
            f.close()

        def play(self, norm=True):
            if norm:
                samples = normrange(self.samples)
            else:
                samples = self.samples
            AL.play(samples, self.samplerate)
    Waveform.riffstring = riffstring
else:
    class Waveform(object):
        """ Simply holds waveforms in numpy arrays...
        """
        def __init__(self, filename=None):
            self.samplerate = None
            self.samples = None
            self.channels = None
            if filename:
                self.read(filename)

        def __len__(self):
            return len(self.samples)

        def read(self, filename):
            self.samplerate, self.samples = wavfile.read(filename)
            try:
                numsamples, self.channels = self.samples.shape
            except ValueError:
                self.channels = 1

        def write(self, filename):
            wavfile.write(filename, self.samplerate, self.samples)

        def play(self):
            raise NotImplementedError
    Waveform.riffstring = riffstring
