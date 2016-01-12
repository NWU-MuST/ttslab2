# -*- coding: utf-8 -*-
"""As with the Voice implementation, the Synthesizer instance MUST
   STAY CONSTANT DURING SYNTHESIS and be instantiated by loading all
   the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import ttslab.synthesizers.hts
from ttslab.synthesizers.hts_labels_tone import * #all feature funcs (p, a, b, ...) and htk number conversion
from ttslab.synthesizers.htsengine_me_cffi import HTS_EngineME

class Synthesizer(ttslab.synthesizers.hts.Synthesizer):
    """Simple HTS synthesizer implementation with "standard" labels +
       additional labels for tone contexts. We use the modified HTS
       engine which is capable of mixed excitation synthesis.
    """

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
                       j(phone_item),
                       k(phone_item),
                       l(phone_item),
                       m(phone_item),
                       n(phone_item)]
            if endtime is not None:
                lab.append(" ".join([str(starttime), str(endtime), "/".join(phlabel)]))
                #lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime
        utt["hts_label"] = lab
        return utt

