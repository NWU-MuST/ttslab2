#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" G2PS implementation using Sequitur JSM model
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.g2ps as g2ps

from sequitur import Translator #Get it from: https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html

SYLBOUNDCHAR = "."

class G2PS_JSM(g2ps.G2PS):
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
            phonesylbounds = self.translator(word.translate(self.gmap))
        else:
            phonesylbounds = self.translator(word)
        candsyls = [[]]
        for e in phonesylbounds:
            if not e == SYLBOUNDCHAR:
                candsyls[-1].append(e)
            else:
                candsyls.append([])
        return [s for s in candsyls if s]

if __name__ == "__main__":
    import sys, codecs, argparse, pickle, itertools
    import ttslab.g2ps_jsm
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from Sequitur model file (pickle)")
    parser.add_argument('--graphmapfn', dest="graphmapfn", type=str, default=None, help="Load grapheme map from file (tsv)")
    parser.add_argument('--dumpmodel', dest='dumpmodel', action='store_true', help="Just dump G2PS model (pickle)")
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
        g2ps = ttslab.g2ps_jsm.G2PS_JSM(pickle.load(infh), gtranstable)

    if args.dumpmodel:
        print(pickle.dumps(g2ps))
    else:
        for line in sys.stdin:
            word = unicode(line, encoding="utf-8").strip()
            try:
                syls = g2ps(word)
                print("{} {} {}".format(word,
                                        "".join(map(str, map(len, syls))),
                                        " ".join(itertools.chain(*syls))).encode("utf-8"))
            except Exception as e:
                print("WARNING: '{}' not converted".format(word), file=sys.stderr)
                print(e, file=sys.stderr)
