# -*- coding: utf-8 -*-
"""An utterance processor implements an independent module that can be
   used during synthesis. This leaves two mechanisms whereby a voice
   can manipulate an utterance: methods of the voice itsself or
   utterance processors.

   UttProcessor instances MUST STAY CONSTANT DURING SYNTHESIS and be
   instantiated by loading all the required data.

"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

class UttProcessor(object):
    """This is the base UttProcessor class..

       An UttProcessor is instantiated at voice instantiation time and
       MUST STAY CONSTANT DURING SYNTHESIS (lifetime of the voice)...
    """
    def process(self, voice, utt, args):
        """Implement the actual processing logic, this method just to keep
           consistency with Voice method by the same name, and for
           clearer code when calling the processor external to the
           voice, with explicit passing in of a Voice instance.
        """
        raise NotImplementedError
        return utt

    def __call__(self, voice, utt, args=None):
        """Make object callable, receiving the voice as first parameter, meant
           to be attached to a Voice instance and used as would a
           method of the voice.
        """
        return self.process(voice, utt, args)
