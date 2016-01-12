# -*- coding: utf-8 -*-
"""This implementation synthesises the utterance using a full set of
   HTS models, extracts the f0 and synthesises a replacement using the
   voice's PitchModel synthesiser, then re-running the HTS vocoder
   with the new contour. The f0 contour need not have unvoiced
   sections zeroed since we are using a mixed excitation vocoder with
   bandpass strengths.

   As with the Voice implementation, the Synthesizer instance MUST
   STAY CONSTANT DURING SYNTHESIS and be instantiated by loading all
   the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

import ttslab.synthesizers.hts
from ttslab.synthesizers.htsengine_me_cffi import HTS_EngineME, tolf0
from ttslab.trackfile import Track
from ttslab.hrg import Utterance
ttslab.extend(Utterance, "ttslab.ufuncs.analysis")

STEPSIZE = 0.005
BACKOFF_STARTPITCH = 12.0 * np.log2(100.0) #100 Hz


class Synthesizer(ttslab.synthesizers.hts.Synthesizer):
    """F0 in semitones relative to 1Hz.
    """
    def synth(self, voice, utt, args):
        synthparms = args #not yet implemented...
        htslabel = "\n".join(utt["hts_label"]).encode("utf-8").splitlines() #to utf-8 bytestring
        if synthparms and "use_labalignments" in synthparms:
            use_labalignments = True
        else:
            use_labalignments = False
        with HTS_EngineME(self.htsvoice_bin, self.mixfilter_bin, self.pdfilter_bin) as htsengine:
            htsengine.synth(htslabel, use_labalignments=use_labalignments)
            for segt, seg in zip(htsengine.get_segtimes(), utt.gr("Segment")):
                seg["start"], seg["end"] = segt
#            utt["debug_waveform"] = htsengine.get_wav()
            f0st = 12.0 * np.log2(htsengine.get_f0())
            f0st[f0st == -np.inf] = 0.0
            f0times = np.arange(len(f0st)) * STEPSIZE
            f0track = Track()
            f0track.times = f0times
            f0track.values = f0st.reshape((-1, 1))
#            utt["debug_f0track"] = f0track
            utt.fill_startendtimes()
            #add qta_startpitch
            for phr in utt.gr("Phrase"):
                syl = phr.first_daughter.gir("SylStructure").first_daughter
                syltrackvals = f0track.slice(f0track.index_at(syl["start"]), f0track.index_at(syl["end"])).values.flatten()
                validvals = syltrackvals[syltrackvals.nonzero()]
                if len(validvals) > 3:
                    phr["qta_startpitch"] = np.mean(validvals[:len(validvals)//4])
                else:
                    phr["qta_startpitch"] = BACKOFF_STARTPITCH
            utt = voice.pitchmodel(utt, ("synth", None))
            f0spline = InterpolatedUnivariateSpline(utt["f0track"].times, utt["f0track"].values)
            newf0 = f0spline(f0track.times)
            #HEURISTIC ADJUSTMENT CLOSER TO HTS DYNAMICS
            m = np.mean(f0track.values[f0track.values.nonzero()])
            newf0 *= 1.3 #more dynamic
            m2 = np.mean(newf0)
            newf0 += m - m2
            ### TRANSFER UNVOICED SECTIONS
            # newf0[f0track.values.flatten() == 0.0] = 0.0
            # import pylab as pl
            # pl.plot(f0track.times, f0track.values)
            # pl.plot(f0track.times, newf0)
            ###
            newf0 = 2 ** (newf0 / 12.0)
            newf0 = tolf0(newf0)
            htsengine.synth(htslabel, lf0=newf0, use_labalignments=use_labalignments)
            #populate utt with waveform and segment alignments
            utt["waveform"] = htsengine.get_wav()
        return utt
