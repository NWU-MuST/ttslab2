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
    def __init__(self, jsmmodel, graphtranstable):
        self.gmap = graphtranstable
        self.model = jsmmodel
        self.translator = Translator(self.model)

    def __getstate__(self):
        return {"model": self.model,
                "gmap": self.gmap}

    def __setstate__(self, d):
        self.__dict__ = d
        self.translator = Translator(self.model)

    def predict_word(self, word):
        if self.gmap is not None:
            phones = self.translator(word.translate(self.gmap))
        else:
            phones = self.translator(word)
        return phones

if __name__ == "__main__":
    import sys, codecs, argparse, pickle
    import ttslab.g2p_jsm
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from Sequitur model file (pickle)")
    parser.add_argument('--graphmapfn', dest="graphmapfn", type=str, default=None, help="Load grapheme map from file (tsv)")
    parser.add_argument('--dumpmodel', dest='dumpmodel', action='store_true', help="Just dump G2P model (pickle)")
    parser.set_defaults(dumpmodel=False)
    args = parser.parse_args()

    if args.graphmapfn is not None:
        c1 = []
        c2 = []
        with codecs.open(args.graphmapfn, encoding="utf-8") as infh:
            for line in infh:
                a, b = line.split()
                c1.append(a)
                c2.append(b)
        gtranstable = dict((ord(inchar), ord(outchar))
                           for inchar, outchar
                           in zip(c1, c2))
    else:
        gtranstable = None

    with open(args.modelfn) as infh:
        g2p = ttslab.g2p_jsm.G2P_JSM(pickle.load(infh), gtranstable)

    if args.dumpmodel:
        print(pickle.dumps(g2p))
    else:
        for line in sys.stdin:
            word = unicode(line, encoding="utf-8").strip()
            try:
                print("{}\t{}".format(word, " ".join(g2p.predict_word(word))).encode("utf-8"))
            except Exception as e:
                print("WARNING: '{}' not converted".format(word), file=sys.stderr)
                print(e, file=sys.stderr)
