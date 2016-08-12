#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the generic G2P class/tool. The command line interface can be
   used to load any G2P model and apply it to a list of words input
   via STDIN.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import codecs
import re

class NoRuleFound(Exception):
    pass

class GraphemeNotDefined(Exception):
    pass

class G2P(object):
    """Abstract class just to define the required interface...
    """
    def predict_word(self, word):
        """ Takes a string and returns a list of phonemes...
        """
        raise NotImplementedError

    def __call__(self, word):
        return self.predict_word(word)


if __name__ == "__main__":
    import sys, argparse, pickle
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from model file (pickle format)")
    args = parser.parse_args()
    
    with open(args.modelfn) as infh:
        g2p = pickle.load(infh)

    for line in sys.stdin:
        word = unicode(line, encoding="utf-8").strip()
        try:
            print("{} {}".format(word, " ".join(g2p.predict_word(word))).encode("utf-8"))
        except Exception as e:
            print("WARNING: '{}' not converted".format(word).encode("utf-8"), file=sys.stderr)
