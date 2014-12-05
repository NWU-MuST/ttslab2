# -*- coding: utf-8 -*-
"""Second try at implementation of a pronunciation dictionary for
   TTS, keep it simple with the following ideas:

    -- Only one pronunciation per word-tag pair is necessary (TTS)

    -- Tags are primarily designed for POS info but may represent
       other significant contexts

    -- Dictionaries may contain phoneme strings, syllable structure
       and a syllable feature such as tone or stress

    -- Simplest cases may only contain phoneme strings

    -- Return None when entry not found instead of raising KeyError

"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import codecs

#Special character not allowed in dictionary
SEP = "*"

class PronunciationDictionary(object):
    """Basic implementation...
    """
    def __init__(self, prond=None, sylld=None, toned=None):
        if prond:
            self.prond = prond
        else:
            self.prond = {}
        if sylld:
            self.sylld = sylld
        else:
            self.sylld = {}
        if toned:
            self.toned = toned
        else:
            self.toned = {}

    def __iter__(self):
        l = sorted(set([entry.split(SEP)[0] for entry in self.prond]))
        return l.__iter__()

    def __contains__(self, word):
        """Simpler, without possibility to consider POS, but sometimes
           convenient and maintaining compatibility...
        """
        return self.contains(word)

    def contains(self, word, pos=None):
        if pos:
            return SEP.join(word, pos) in self.prond
        return word in self.prond

    def __check_consistency(self):
        """Assert that all info is consistent"""
        try:
            for k in self.prond:
                if k in self.sylld:
                    assert sum(map(int, list(self.sylld[k]))) == len(self.prond[k].split())
            for k in self.sylld:
                assert k in self.prond
                if k in self.toned:
                    assert len(self.toned[k]) == len(self.sylld[k])
        except Exception as e:
            print("Offending entry:", k)
            raise

    def check_against_phoneset(self, phset):
        """check all dictionary entries are compatible with a specific
           phoneset...
        """
        phset = set(phset)
        dphset = set()
        for k in self.prond:
            dphset.update(self.prond[k].split())
        uset = dphset.union(phset)
        assert uset == phset

    def pron_lookup(self, word, tag=None):
        if tag:
            k = SEP.join([word, tag])
        else:
            k = word
        if k in self.prond:
            return self.prond[k].split()
        return None
        
    def syll_lookup(self, word, tag=None):
        _pron = self.pron_lookup(word, tag)
        if tag:
            k = SEP.join([word, tag])
        else:
            k = word
        if k in self.sylld:
            _syll = []
            c = 0
            for l in map(int, list(self.sylld[k])):
                _syll.append(_pron[c:c+l])  #_pron is not None
                c += l
            return _syll
        return None

    def tone_lookup(self, word, tag=None):
        if tag:
            k = SEP.join([word, tag])
        else:
            k = word
        if k in self.toned:
            return list(self.toned[k])
        return None

    def toscmfile(self, fn, phonemap=None):
        with codecs.open(fn, "w", encoding="utf-8") as outfh:
            for k in sorted(self.prond):
                if SEP in k:
                    word, tag = k.split(SEP)
                else:
                    word, tag = (k, None)
                sylls = self.syll_lookup(word, tag)
                if sylls:
                    tones = self.tone_lookup(word, tag)
                    if not tones:
                        tones = [0] * len(sylls)
                    if phonemap:
                        prontext = " ".join(["((%s) %s)" % (" ".join([phonemap[p] for p in syl]), tone) for syl, tone in zip(sylls, tones)])
                    else:
                        prontext = " ".join(["((%s) %s)" % (" ".join(syl), tone) for syl, tone in zip(sylls, tones)])
                else:
                    if phonemap:
                        prontext = " ".join([phonemap[p] for p in self.prond[word].split()])
                    else:
                        prontext = self.prond[k]
                text = '("%s" %s (%s))\n' % (word, tag, prontext)
                outfh.write(text)

    def totextfile(self, fn, phonemap=None):
        with codecs.open(fn, "w", encoding="utf-8") as outfh:
            for k in sorted(self.prond):
                if SEP in k:
                    word, tag = k.split(SEP)
                else:
                    word, tag = (k, None)
                if k in self.sylld:
                    syls = self.sylld[k]
                else:
                    syls = None
                if k in self.toned:
                    tones = self.toned[k]
                else:
                    tones = None
                if phonemap:
                    phones = " ".join([phonemap[p] for p in self.pron_lookup(word, tag)])
                else:
                    phones = self.prond[k]
                outfh.write(" ".join([word, str(tag), str(tones), str(syls), phones]) + "\n")

    def fromsimpletextfile(self, fn, phonemap=None):
        """ abandon q b a n d q n
        """
        with codecs.open(fn, encoding="utf-8") as infh:
            for line in infh:
                fields = line.split()
                word = fields[0]
                if SEP in word:
                    raise Exception("Asterisk character (*) not allowed in word: " + word)
                phones = fields[1:]
                if phonemap:
                    phones = [phonemap[p] for p in phones]
                self.prond[word] = " ".join(phones)
        return self

    def updatefromsimpledict(self, d):
        for k in d:
            if type(d[k]) is list:
                self.prond[k] = " ".join(d[k])
            else:
                self.prond[k] = " ".join(d[k].split())

    def fromtextfile(self, fn, phonemap=None, nonestring="None"):
        """ abandon VERB 010 133 q b a n d q n
        """
        with codecs.open(fn, encoding="utf-8") as infh:
            for line in infh:
                fields = line.split()
                word = fields[0]
                if SEP in word:
                    raise Exception("Asterisk character (*) not allowed in word: " + word)
                tag = fields[1]
                tones = fields[2]
                sylls = fields[3]
                phones = fields[4:]
                if tag == nonestring:
                    k = word
                else:
                    k = SEP.join([word, tag])
                if tones != nonestring:
                    self.toned[k] = tones
                if sylls != nonestring:
                    self.sylld[k] = sylls
                if phonemap:
                    phones = [phonemap[p] for p in phones]
                self.prond[k] = " ".join(phones)
        self.__check_consistency()
        return self
