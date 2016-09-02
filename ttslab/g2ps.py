#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" G2PS interface: Grapheme to phone + syl. The command line interface can be
   used to load any G2PS model and apply it to a list of words input
   via STDIN.
"""
from __future__ import unicode_literals, division, print_function #Py2


class G2PS(object):
    def predict_word(self, word):
        """Output a list of lists (syllables and phonemes)
        """
        raise NotImplementedError

    def __call__(self, word):
        return self.predict_word(word)

if __name__ == "__main__":
    import sys, pickle, itertools
    g2ps = pickle.load(open(sys.argv[1]))
    
    for line in sys.stdin:
        word = unicode(line.strip(), encoding="utf-8")
        try:
            syllables = g2ps(word)
            syllens = "".join(map(str, map(len, syllables)))
            print(" ".join([word, syllens, " ".join(itertools.chain(*syllables))]).encode("utf-8"))
        except Exception as e:
            print("WARNING: Could not G2PS '{}'".format(word).encode("utf-8"), file=sys.stderr)
            print(unicode(e).encode("utf-8"), file=sys.stderr)
