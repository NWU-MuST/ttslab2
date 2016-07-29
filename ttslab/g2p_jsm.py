#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""G2P implementation using Sequitur joint-sequence-models (JSMs)...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.g2p as g2p

from sequitur import Translator #Get it from: https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html

class G2P_JSM(g2p.G2P):
    def __init__(self, jsmmodel):
        self.model = jsmmodel
        self.translator = Translator(self.model)

    def __getstate__(self):
        return {"model": self.model}

    def __setstate__(self, d):
        self.__dict__ = d
        self.translator = Translator(self.model)

    def predict_word(self, word):
        return self.translator(word)


if __name__ == "__main__":
    import sys, argparse, pickle
    import ttslab.g2p_jsm
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from Sequitur model file")
    parser.add_argument('--dumpmodel', dest='dumpmodel', action='store_true', help="Just dump G2P model (pickle format)")
    parser.set_defaults(dumpmodel=False)
    args = parser.parse_args()

    with open(args.modelfn) as infh:
        g2p = ttslab.g2p_jsm.G2P_JSM(pickle.load(infh))

    if args.dumpmodel:
        print(pickle.dumps(g2p))
    else:
        for line in sys.stdin:
            word = unicode(line, encoding="utf-8").strip()
            try:
                print("{}\t{}".format(word, " ".join(g2p.predict_word(word))).encode("utf-8"))
            except Exception as e:
                print("WARNING: '{}' not converted".format(word), file=sys.stderr)
