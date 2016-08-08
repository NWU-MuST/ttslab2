#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""G2P implementation using LSTM sequence-to-sequence model...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os
import tarfile
import tempfile
import shutil

import ttslab.g2p as g2p

try:
    import g2p_seq2seq.g2p
except ImportError:
    print("WARNING: Failed to import g2p import implementation")

class G2P_LSTM(g2p.G2P):
    def __init__(self, modeldir):
        tempfh = tempfile.NamedTemporaryFile()
        with tarfile.open(fileobj=tempfh, mode="w") as tarfh:
            tarfh.add(modeldir, arcname=os.path.basename(modeldir))
        with open(tempfh.name) as infh:
            self.modeldirblob = infh.read()
        tempfh.close()
        self.model = g2p_seq2seq.g2p.G2PModel(modeldir)

    def __getstate__(self):
        return {"modeldirblob": self.modeldirblob}

    def __setstate__(self, d):
        self.__dict__ = d
        tempdir = tempfile.mkdtemp()
        tempfh = tempfile.NamedTemporaryFile(suffix=".tar.gz")
        tempfh.write(self.modeldirblob)
        tempfh.flush()
        t = tarfile.open(tempfh.name, "r")
        t.extractall(tempdir)
        self.model = g2p_seq2seq.g2p.G2PModel(tempdir)
        tempfh.close()
        shutil.rmtree(tempdir)

    def predict_word(self, word):
        s = self.model.decode_word(word)
        if s:
            return s.split()
        else:
            raise Exception("G2P Error")


if __name__ == "__main__":
    import sys, argparse, pickle
    import ttslab.g2p_lstm
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modeldir', metavar='MODELDIR', type=str, default=None, help="Load from model directory")
    parser.add_argument('--dumpmodel', dest='dumpmodel', action='store_true', help="Just dump G2P model (pickle format)")
    parser.set_defaults(dumpmodel=False)
    args = parser.parse_args()

    g2p = ttslab.g2p_lstm.G2P_LSTM(args.modeldir)

    if args.dumpmodel:
        print(pickle.dumps(g2p))
    else:
        for line in sys.stdin:
            word = unicode(line, encoding="utf-8").strip()
            try:
                print("{}\t{}".format(word, " ".join(g2p.predict_word(word))).encode("utf-8"))
            except Exception as e:
                print("WARNING: '{}' not converted".format(word), file=sys.stderr)
