# -*- coding: utf-8 -*-
"""This is the abstract Synthesizer class.. The idea is that all the
   back-end-specific computation takes place in the synthesizer
   implementation so that different back-ends can be bolted onto any
   front-end (Voice) implementation..

   As with the Voice implementation, the Synthesizer instance MUST
   STAY CONSTANT DURING SYNTHESIS and be instantiated by loading all
   the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import ttslab.synthesizer
from ttslab.synthesizers.hts_labels import * #all feature funcs (p, a, b, ...) and htk number conversion
from ttslab.synthesizers.htsengine_me_cffi import HTS_EngineME

class Synthesizer(ttslab.synthesizer.Synthesizer):
    """Simple HTS synthesizer implementation with "standard" labels. We
       use the modified HTS engine which is capable of mixed
       excitation synthesis.
    """

    def __init__(self, modelsdir=None):
        if modelsdir:
            self._loadmodels(modelsdir)

    def _loadmodels(self, modelsdir):
        with open(os.path.join(modelsdir, "htsvoice"), "rb") as infh:
            self.htsvoice_bin = infh.read()
        with open(os.path.join(modelsdir, "mixfilter"), "rb") as infh:
            self.mixfilter_bin = infh.read()
        with open(os.path.join(modelsdir, "pdfilter"), "rb") as infh:
            self.pdfilter_bin = infh.read()

    def feats(self, voice, utt, args):
        lab = []
        starttime = 0
        for phone_item in utt.get_relation("Segment"):
            if "end" in phone_item:
                endtime = float_to_htk_int(phone_item["end"])
            else:
                endtime = None
            phlabel = [p(phone_item, voice.phonemap),
                       a(phone_item),
                       b(phone_item, voice.phones, voice.phonemap),
                       c(phone_item),
                       d(phone_item),
                       e(phone_item),
                       f(phone_item),
                       g(phone_item),
                       h(phone_item),
                       i(phone_item),
                       j(phone_item)]
            if endtime is not None:
                lab.append(" ".join([str(starttime), str(endtime), "/".join(phlabel)]))
                #lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime
        utt["hts_label"] = lab
        return utt

    def synth(self, voice, utt, args):
        synthparms = args #not yet implemented...
        htslabel = "\n".join(utt["hts_label"]).encode("utf-8").splitlines() #to utf-8 bytestring
        if synthparms and "use_labalignments" in synthparms:
            use_labalignments = True
        else:
            use_labalignments = False
        with HTS_EngineME(self.htsvoice_bin, self.mixfilter_bin, self.pdfilter_bin) as htsengine:
            htsengine.synth(htslabel, use_labalignments=use_labalignments)
            utt["waveform"] = htsengine.get_wav()
            for segt, seg in zip(htsengine.get_segtimes(), utt.gr("Segment")):
                seg["start"], seg["end"] = segt
        return utt
