# -*- coding: utf-8 -*-
"""This is the abstract PitchModel class.. We just try to define an
   interface here..

   A PitchModel is a synthesizer utterance processor operating on
   syllables...

   A PitchModel instance MUST STAY CONSTANT DURING SYNTHESIS and be
   instantiated by loading all the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from synthesizer import Synthesizer

class PitchModel(Synthesizer):
    pass
