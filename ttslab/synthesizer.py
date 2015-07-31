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

from ttslab.uttprocessor import UttProcessor

class Synthesizer(UttProcessor):
    """ Abstract synthesizer class
    """

    def feats(self, voice, utt, args):
        raise NotImplementedError

    def synth(self, voice, utt, args):
        raise NotImplementedError

    def process(self, voice, utt, args):
        """Our synthesiser implementation will generally perform two things:
           extract relevant _feats_ from the utterance and actually
           perform _synthesis_.
        """
        processname, synthparms = args
        if processname in ["feats", "synth"]:
            utt = self.feats(voice, utt, synthparms)
        if processname in ["synth"]:
            utt = self.synth(voice, utt, synthparms)
        return utt
