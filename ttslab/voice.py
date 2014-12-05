# -*- coding: utf-8 -*-
"""This is the abstract Voice class.. The idea is that the whole
   synthesis process is defined within this structure with different
   implementations (for instance for synthesis techniques or language
   specific routines) be derived from this as needed..

   A Voice instance contains methods and attributes (UttProcessors
   objects) which process utterances with a standard interface...

   A Voice instance MUST STAY CONSTANT DURING SYNTHESIS and be
   instantiated by loading all the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import types

import hrg
import uttprocessor

class Voice(object):
    """ Abstract voice class
    """
    def __init__(self):
        self.features = {}
    
    def __getitem__(self, featname):
        """ Returns the requested feature from self.features
            This raises KeyError when featname is not available..
        """
        return self.features[featname]
    
    def __setitem__(self, featname, feat):
        """ Sets the specific feature in self.features
        """
        self.features[featname] = feat

    def __delitem__(self, featname):
        """ Deletes the specific feature in self.features
        """
        del self.features[featname]
    
    def __iter__(self):
        """ Iterate over features.
        """
        return self.features.__iter__()

    def __contains__(self, featname):
        """ Contains feature?
        """
        return featname in self.features

    def __getattribute__(self, name):
        """This is to allow attached UttProcessor or derived instances to run
           seemlessly as if methods of the voice, we do this on the
           fly to preserve the original type of the attribute
           (assuming this is necessary for pickling correctly)
        """
        if issubclass(type(object.__getattribute__(self, name)), uttprocessor.UttProcessor):
            return types.MethodType(object.__getattribute__(self, name), self)
        return object.__getattribute__(self, name)

    def _create_utterance(self):
        """Create Utterance with info about this voice...
        """
        return hrg.Utterance(repr(self).split()[0][1:])

    def process(self, utt, args):
        """This will now contain the top-level logic for the synthesis
           process, 'process pipelines' defined before are now
           explicit here (in code) and may be switched via 'args'
           input.
        """
        raise NotImplementedError
        return utt

    #################### User API:
    def synthesize(self, inputstring, processname="text-to-wave"):
        """ Render the inputstring...
        """
        utt = self._create_utterance()
        utt["inputtext"] = inputstring
        utt = self.process(utt, processname)
        return utt

    #removed "resynthesize" function: we should now call voice.process directly

####################################################################################
#####FOR TESTING:
class UttProcessorA(uttprocessor.UttProcessor):
    def __init__(self, somedata):
        self.somedata = somedata
    def process(self, voice, utt, args):
        print("Running " + self.somedata)
        print(" ".join([repr(self), repr(voice), repr(utt), args]))
        return utt

class UttProcessorB(uttprocessor.UttProcessor):
    def __init__(self, somedata):
        self.somedata = somedata
    def process(self, voice, utt, args):
        print("Running " + self.somedata)
        print(" ".join([repr(self), repr(voice), repr(utt), args]))
        return utt

class VoiceA(Voice):
    def __init__(self, somedata="Daniel"):
        Voice.__init__(self)
        self.features["somedata"] = somedata
        self.uttproc_a = UttProcessorA("Louis")
        self.uttproc_b = UttProcessorB("Philip")

    def uttproc_c(self, utt, args):
        print("Running Vincent")
        print(" ".join([repr(self), repr(utt), args]))
        return utt

    def process(self, utt, args):
        print("Running voice process with args: " + args)
        self.uttproc_a(utt, args)
        self.uttproc_b(utt, args)
        self.uttproc_c(utt, args)
        print(utt)
        return utt

def test():
    import ttslab
    import voice
    import os
            
    v = voice.VoiceA()
    print()
    print("SYNTHESIS PROCESS..........................")
    print()
    v.synthesize("Hello!")
    print()
    print("CHECK ATTRIBUTES..........................")
    print()
    print("v.features", v.features)
    print("v.uttproc_a", v.uttproc_a)
    print("v.uttproc_b", v.uttproc_b)
    print("v.uttproc_a.somedata", v.uttproc_a.somedata)
    print("v.uttproc_b.somedata", v.uttproc_b.somedata)

    if not os.path.exists("testvoice.pickle"):
        ttslab.tofile(v, "testvoice.pickle")
        v = ttslab.fromfile("testvoice.pickle")
        print()
        print("PICKLED AND LOADED..........................")
        print()
        print("v.features", v.features)
        print("v.uttproc_a", v.uttproc_a)
        print("v.uttproc_b", v.uttproc_b)
        print("v.uttproc_a.somedata", v.uttproc_a.somedata)
        print("v.uttproc_b.somedata", v.uttproc_b.somedata)
        os.remove("testvoice.pickle")
    
if __name__ == "__main__":
    test()
