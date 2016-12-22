#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

import ttslab.phoneset
from ttslab.lang.zulu import Voice as ZuluVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Xhosa Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl",
                         "foreign_CC_cluster_1split": [["l", "s"], ["l", "f"], ["l", "tʰ"], ["l", "tʼ"],
                                                     ["kʼ", "s"], ["kʼ", "f"], ["kʼ", "tʰ"], ["kʼ", "tʼ"],
                                                     ["pʼ", "tʼ"], ["pʼ", "tʰ"],
                                                     ["r", "n"], ["r", "m"]],
                         "foreign_CC_onsets": [["ɡ", "r"], ["ɡ", "l"],
                                             ["f", "r"], ["f", "l"],
                                             ["ɓ", "r"], ["bʰ", "r"], ["ɓ", "l"], ["bʰ", "l"],
                                             ["kʼ", "r"], ["kʰ", "r"], ["kʼ", "l"], ["kʰ", "l"], ["kʼ", "j"], ["kʰ", "j"],
                                             ["d", "r"],
                                             ["pʼ", "r"], ["pʼ", "l"],
                                             ["tʼ", "r"], ["tʰ", "r"],
                                             ["s", "kʼ"], ["s", "kʰ"], ["s", "tʼ"], ["s", "tʰ"]],
                         "foreign_CCC_onsets": [["s", "tʼ", "r"]]}
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "paugs"  : set(["glottal-stop"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_back"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɣ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "ɲʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced", "aspirated"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "ŋ"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "ǀ"      : set(["class_consonantal", "consonant", "manner_click", "place_alveolar", "place_dental"]),
                       "ǀʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_alveolar", "place_dental", "aspirated"]),
                       "ɡ͡ǀ"     : set(["class_consonantal", "consonant", "manner_click", "place_velar", "place_dental", "voiced"]),
                       "ɟ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "voiced"]),
                       "ɮ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_alveolar", "place_post-alveolar"]),
                       "ǃʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "ɡ͡ǃ"     : set(["class_consonantal", "consonant", "manner_click", "place_velar", "place_post-alveolar", "voiced"]),
                       "ǁ"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar"]),
                       "ǁʰ"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "aspirated"]),
                       "ɡ͡ǁ"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_velar", "place_alveolar", "voiced"]),
                       "bʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "aspirated"]),
                       "ɓ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "cʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "ejective"]),
                       "cʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "aspirated"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "d͡ʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_palatal", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "ɡ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "kʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "k͡xʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_velar", "ejective"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "mʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced", "aspirated"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "nʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced", "aspirated"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t͡ɬʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "ejective"]),
                       "t͡ʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "t͡ʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "t͡sʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "voiced"]),
                       "x"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "paugs":"paugs",
                    "a":"a",
                    "ɛ":"E",
                    "ɣ":"G",
                    "ɲ":"J",
                    "ɲʰ":"Jh",
                    "ɬ":"K",
                    "ŋ":"N",
                    "ɔ":"O",
                    "ʃ":"S",
                    "ǀ":"cc",
                    "ǀʰ":"cch",
                    "ɡ͡ǀ":"gcc",
                    "ɟ":"dy",
                    "ɮ":"lZ",
                    "ǃ":"qq",
                    "ǃʰ":"qqh",
                    "ɡ͡ǃ":"gqq",
                    "ǁ":"xx",
                    "ǁʰ":"xxh",
                    "ɡ͡ǁ":"gxx",
                    "bʰ":"bh",
                    "ɓ":"bE",
                    "cʼ":"ce",
                    "cʰ":"ch",
                    "d":"d",
                    "d͡ʒ":"dZ",
                    "f":"f",
                    "ɡ":"g",
                    "h":"h",
                    "i":"i",
                    "j":"j",
                    "kʼ":"ke",
                    "kʰ":"kh",
                    "k͡xʼ":"kxe",
                    "l":"l",
                    "m":"m",
                    "mʰ":"mh",
                    "n":"n",
                    "nʰ":"nh",
                    "pʼ":"pe",
                    "pʰ":"ph",
                    "r":"r",
                    "s":"s",
                    "t͡ɬʼ":"tKe",
                    "t͡ʃʼ":"tSe",
                    "t͡ʃʰ":"tSh",
                    "tʼ":"te",
                    "tʰ":"th",
                    "t͡sʼ":"tse",
                    "u":"u",
                    "v":"v",
                    "w":"w",
                    "x":"x",
                    "z":"z"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabic(self, phonename):
        return "class_syllabic" in self.phones[phonename]

    def is_affricate(self, phonename):
        return "manner_affricate" in self.phones[phonename]

    def is_fricative(self, phonename):
        return "manner_fricative" in self.phones[phonename]

    def is_plosive(self, phonename):
        return "manner_plosive" in self.phones[phonename]

    def is_click(self, phonename):
        return "manner_click" in self.phones[phonename]

    def is_plosivelike(self, phonename):
        return self.is_plosive(phonename) or self.is_affricate(phonename) or self.is_click(phonename)

    def is_nasal(self, phonename):
        return "manner_nasal" in self.phones[phonename]

    def is_approximant(self, phonename):
        return "manner_approximant" in self.phones[phonename]

    def is_homorganic(self, phn1, phn2):
        place1 = set([e for e in self.phones[phn1] if e.startswith("place_")])
        place2 = set([e for e in self.phones[phn2] if e.startswith("place_")])
        return bool(place1.intersection(place2))

    def is_valid_CC(self, cluster, consider_foreign=True):
        """Mostly from the book by Philip Hoole (see below)..
        """
        if cluster[1] == "w" and any(isf(cluster[0]) for isf in [self.is_plosivelike, self.is_fricative, self.is_nasal, self.is_approximant]):
            #print("CC1:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        if cluster[0] in ["n", "ŋ"] and (self.is_plosivelike(cluster[1]) or self.is_fricative(cluster[1])) and self.is_homorganic(cluster[0], cluster[1]):
            #print("CC2:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        if cluster[0] == "ɲ" and self.is_homorganic(cluster[0], cluster[1]):
            #print("CC3:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        if cluster[0] == "m" and cluster[1] in ["ɓ", "pʼ", "pʰ", "tʼ", "tʰ",
                                                "d", "s", "ʃ", "t͡ʃʼ", "t͡ʃʰ",
                                                "z", "ɬ", "ɮ", "n", "ɲ", "ɲʰ",
                                                "j", "ŋ", "kʼ", "kʰ"]:
            #print("CC4:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        elif consider_foreign and cluster in self.features["foreign_CC_onsets"]:
            #print("CC5:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            print("syllabify(): WARNING: foreign onset cluster: '{}'".format("".join(cluster)).encode("utf-8"), file=sys.stderr)
            return True
        return False

    def _vowelindices(self, phones):
        return [i for i, ph in enumerate(phones) if self.is_vowel(ph)]

    def syllabify(self, phones):
        """Syllabification algorithm for Nguni languages based on notes
           pp. 349 of "Consonant Clusters and Structural Complexity"
           by Philip Hoole
        """
        def breakcluster(cluster):
            if not cluster:
                print("syllabify(): WARNING: VV context found: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #Always V.V
            elif len(cluster) == 1:
                bounds.append(ci) #Always V.CV (open syllables)
            elif len(cluster) == 2:
                if self.is_valid_CC(cluster):
                    bounds.append(ci) #V.CCV
                    return
                if self.is_syllabic(cluster[0]):
                    #V.N.CV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                if cluster in self.features["foreign_CC_cluster_1split"]:
                    print("syllabify(): WARNING: foreign cluster was split: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CV
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster),"".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #V.CCV
            elif len(cluster) == 3:
                if cluster[2] == "w":
                    if self.is_valid_CC(cluster[:2], consider_foreign=False):
                        bounds.append(ci) #V.CCWV
                        return
                if self.is_syllabic(cluster[0]) and self.is_valid_CC(cluster[1:]):
                    #V.N.CWV
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                    return
                if cluster in self.features["foreign_CCC_onsets"]:
                    bounds.append(ci) #V.CCCV
                if cluster[1:] in self.features["foreign_CC_onsets"]:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CCV  (foreign)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #V.CCCV
            elif len(cluster) == 4:
                if cluster[-1] == "w" and self.is_syllabic(cluster[0]) and self.is_valid_CC(cluster[1:3], consider_foreign=False):
                    #V.N.CCWV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)                
                bounds.append(ci) #V.CCCCV
            else:
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #V.*V (generally: prefer open syllables)

        v_inds = self._vowelindices(phones)
        bounds = []
        if v_inds:
            #Onset cluster (syllabic nasal?)
            if not 0 in v_inds:
                span = phones[0:v_inds[0]+1]
                cluster = phones[0:v_inds[0]]
                ci = 0
                breakcluster(cluster)
                bounds.pop(0)
            #Other clusters
            for i, j in zip(v_inds, v_inds[1:]):
                span = phones[i:j+1]
                cluster = span[1:-1]
                ci = i+1
                breakcluster(cluster)
            #Word-final cluster?
            cluster = phones[v_inds[-1]+1:]
            if cluster:
                ci = v_inds[-1]+1
                if len(cluster) == 1 and self.is_syllabic(cluster[0]):
                    bounds.append(ci)
                else:
                    print("syllabify(): WARNING: word-final cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
        else:
            print("syllabify(): WARNING: no vowels found in word '{}'".format("".join(phones)).encode("utf-8"), file=sys.stderr)
                
        #Convert sylbounds to syllable lists
        sylls = []
        startbound = 0
        for bound in bounds:
            sylls.append(phones[startbound:bound])
            startbound = bound
        sylls.append(phones[startbound:])
        return sylls

    def guess_syltonestress(self, word, syllables):
        """ Try to guess tone/stress pattern for an unknown word...
        """
        return "L" * len(syllables)

class Voice(ZuluVoice): #Xhosa is also a Nguni language...
    pass
