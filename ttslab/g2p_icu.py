#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" G2P implementation using ICU transliteration rules...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import codecs
import re

import ttslab.g2p as g2p

import icu  # Debian/Ubuntu: apt-get install python-pyicu


class G2P_ICURules(g2p.G2P):
    def __init__(self, phonesfn, rulesfn):
        with codecs.open(phonesfn, encoding="utf-8") as infh:
            phones = infh.read().split()
        assert not any(["|" in ph for ph in phones])
        phones.sort(key=lambda x:len(x), reverse=True)
        self.phonesre = re.compile("|".join(phones), flags=re.UNICODE)
        with codecs.open(rulesfn, encoding="utf-8") as infh:
            self.rules = infh.read()
        self.transliterator = icu.Transliterator.createFromRules("noname", self.rules, icu.UTransDirection.FORWARD)

    def __getstate__(self):
        return {"phonesre": self.phonesre,
                "rules": self.rules}

    def __setstate__(self, d):
        self.__dict__ = d
        self.transliterator = icu.Transliterator.createFromRules("noname", self.rules, icu.UTransDirection.FORWARD)

    def predict_word(self, word):
        pronun = self.transliterator.transliterate(word)
        return [e.group(0) for e in self.phonesre.finditer(pronun)]


if __name__ == "__main__":
    import sys

    try:
        phonesfn = sys.argv[1]
        rulesfn = sys.argv[2]
    except IndexError:
        print("USAGE: g2p_icu.py PHONESFN RULESFN")
        sys.exit(1)

    g2p = G2P_ICURules(phonesfn, rulesfn)
    for line in sys.stdin:
        word = unicode(line.strip(), encoding="utf-8")
        print("{}\t{}".format(word, " ".join(g2p.predict_word(word))).encode("utf-8"))
