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

import sys
import codecs
from collections import defaultdict

class PronunciationDictionary(object):
    """Basic implementation...
    """
    def __init__(self, prond=None):
        if prond:
            self.prond = prond
        else:
            self.prond = {}

    def __iter__(self):
        return self.prond.__iter__()

    def __contains__(self, word):
        """Simpler, without possibility to consider POS, but sometimes
           convenient and maintaining compatibility...
        """
        return word in self.prond

    def contains(self, word, tag=None):
        if word in self.prond:
            if tag is not None:
                return tag in self.prond[word]
            return True
        return False

    def __check_consistency(self):
        """Assert that all info is consistent"""
        try:
            for word in self.prond:
                for tag in self.prond[word]:
                    _pron, _tone, _syll = self.prond[word][tag]
                    if _syll:
                        assert sum(map(int, _syll)) == len(_pron.split())
                    if _tone:
                        assert len(_tone) == len(_syll)
        except Exception as e:
            print("OFFENDING ENTRY:", word.encode("utf-8"), file=sys.stderr)
            raise

    def check_against_phoneset(self, phset):
        """check all dictionary entries are compatible with a specific
           phoneset...
        """
        phset = set(phset)
        dphset = set()
        for word in self.prond:
            for tag in self.prond[word]:
                dphset.update(self.prond[word][tag].split())
        uset = dphset.union(phset)
        assert uset == phset

    def lookup(self, word, tag=None):
        try:
            return self.prond[word][tag]
        except KeyError:
            return None

    def pron_lookup(self, word, tag=None):
        try:
            return self.prond[word][tag][0].split()
        except KeyError:
            return None

    def _flatphones2nestedsyl(self, phones, sylspec):
        sylls = []
        c = 0
        for l in map(int, sylspec):
            sylls.append(phones[c:c+l])
            c += l
        return sylls
        
    def syll_lookup(self, word, tag=None):
        try:
            _pron, _tone, _syll = self.lookup(word, tag)
        except TypeError:
            return None
        if _syll is not None:
            return self._flatphones2nestedsyl(_pron.split(), _syll)
        else:
            return None

    def tone_lookup(self, word, tag=None):
        try:
            _pron, _tone, _syll = self.lookup(word, tag)
        except TypeError:
            return None
        return _tone

    def _to_writeable_entries(self):
        entries = []
        for word in sorted(self.prond):
            wordentries = []
            writedefault = True
            for tag in [t for t in self.prond[word] if t is not None]:
                if self.prond[word][tag] == self.prond[word][None]:
                    wordentries.insert(0, [word, tag] + self.prond[word][tag])
                    writedefault = False
                else:
                    wordentries.append([word, tag] + self.prond[word][tag])
            if writedefault:
                wordentries.append([word, None] + self.prond[word][None])
            entries.extend(wordentries)
        return entries
    
    def toscmfile(self, fn, phonemap=None):
        entries = self._to_writeable_entries()
        with codecs.open(fn, "w", encoding="utf-8") as outfh:
            for word, tag, pron, tone, syll in entries:
                if syll is not None:
                    sylls = self._flatphones2nestedsyl(pron.split(), syll)
                    if tone is None:
                        tones = [0] * len(sylls)
                    else:
                        tones = tone
                    if phonemap:
                        prontext = " ".join(["((%s) %s)" % (" ".join([phonemap[p] for p in syl]), tone) for syl, tone in zip(sylls, tones)])
                    else:
                        prontext = " ".join(["((%s) %s)" % (" ".join(syl), tone) for syl, tone in zip(sylls, tones)])
                else:
                    if phonemap:
                        prontext = " ".join([phonemap[p] for p in pron.split()])
                    else:
                        prontext = pron
                text = '("%s" %s (%s))\n' % (word, tag, prontext)
                outfh.write(text)

    def totextfile(self, fn, phonemap=None):
        entries = self._to_writeable_entries()
        with codecs.open(fn, "w", encoding="utf-8") as outfh:
            for word, tag, pron, tone, syll in entries:
                if phonemap:
                    pron = " ".join([phonemap[p] for p in pron.split()])
                else:
                    pron = pron
                outfh.write(" ".join([word, str(tag), str(tone), str(syll), pron]) + "\n")

    def fromsimpletextfile(self, fn, phonemap=None):
        """ abandon q b a n d q n
        """
        prond = defaultdict(dict)
        with codecs.open(fn, encoding="utf-8") as infh:
            for line in infh:
                fields = line.split()
                word = fields[0]
                phones = fields[1:]
                if phonemap:
                    phones = [phonemap[p] for p in phones]
                prond[word][None] = [" ".join(phones), None, None]
        self.prond = dict(prond)
        return self

    def updatefromsimpledict(self, d):
        for k in d:
            if not k in self.prond:
                self.prond[k] = {}
            if type(d[k]) is list:
                self.prond[k][None] = [" ".join(d[k]), None, None]
            else:
                self.prond[k][None] = [" ".join(d[k].split()), None, None]

    def fromtextfile(self, fn, phonemap=None, nonestring="None"):
        """ abandon VERB 010 133 q b a n d q n
        """
        prond = defaultdict(dict)
        with codecs.open(fn, encoding="utf-8") as infh:
            for line in infh:
                fields = line.split()
                word = fields[0]
                tag = fields[1]
                tones = fields[2]
                if tones == nonestring:
                    tones = None
                sylls = fields[3]
                if sylls == nonestring:
                    sylls = None
                phones = fields[4:]
                if phonemap:
                    phones = [phonemap[p] for p in phones]
                if tag != nonestring:
                    prond[word][tag] = [" ".join(phones), tones, sylls]
                    if None not in prond[word]: #First tagged word will be retained as entry for "None" if no explicit untagged
                        prond[word][None] = prond[word][tag]
                else:
                    prond[word][None] = [" ".join(phones), tones, sylls]
        self.prond = dict(prond)
        self.__check_consistency()
        return self
