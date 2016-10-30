#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the generic Morphparse class/tool. The command line
   interface can be used to load any Morphparse model and apply it to
   a list of words input via STDIN.
"""
from __future__ import unicode_literals, print_function, division

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

class Morphparse(object):
    """Abstract class just to define the required interface...
    """
    def parse_word(self, word):
        """Takes a string and returns a list of "parses" where morph labels
        encapsulated by <> precede the string associated with it, for
        example:
             ["<word><noun><iv>u<nst1><npf><n1>m<nst2><nr>numzana",
              "<word><noun><iv_n11>u<nst2><nr>mnumzana",
              ...
             ]
        """
        raise NotImplementedError
        
    def __call__(self, word):
        return self.parse_word(word)
    
if __name__ == "__main__":
    import sys, codecs, argparse, pickle
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from model file (pickle format)")
    args = parser.parse_args()
    
    with open(args.modelfn) as infh:
        morphparse = pickle.load(infh)
    
    for line in sys.stdin:
        word = unicode(line, encoding="utf-8").strip()
        #try:
        print("{} {}".format(word, " ".join(morphparse(word)).encode("utf-8")))
        #except Exception as e:
        #    print("WARNING: '{}' not parsed".format(word).encode("utf-8"), file=sys.stderr)
        #    print(e, file=sys.stderr)
