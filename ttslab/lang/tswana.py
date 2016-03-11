# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

import ttslab.phoneset
from ttslab.lang.sotho import Voice as SothoVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Tswana Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl",
                         "foreign_CC_cluster_1split": [["l", "s"], ["l", "f"], ["l", "tʰ"], ["l", "tʼ"],
                                                       ["kʼ", "s"], ["kʼ", "f"], ["kʼ", "tʰ"], ["kʼ", "tʼ"],
                                                       ["kʰ", "s"], ["kʰ", "f"], ["kʰ", "tʰ"], ["kʰ", "tʼ"],
                                                       ["pʼ", "tʼ"], ["pʼ", "tʰ"],
                                                       ["pʰ", "tʼ"], ["pʰ", "tʰ"],
                                                       ["r", "n"], ["r", "m"]],
                         "foreign_CC_onsets": [["f", "r"], ["f", "l"],
                                               ["b", "l"], ["b", "r"],
                                               ["kʼ", "r"], ["kʰ", "r"], ["kʼ", "l"], ["kʰ", "l"], ["kʼ", "j"], ["kʰ", "j"],
                                               ["d", "r"],
                                               ["pʼ", "r"], ["pʼ", "l"],
                                               ["tʼ", "r"], ["tʰ", "r"],
                                               ["s", "kʼ"], ["s", "kʰ"], ["s", "tʼ"], ["s", "tʰ"]],
                         "foreign_CCC_onsets": [["s", "tʼ", "r"]]
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "kʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "k͡x"     : set(["class_consonantal", "consonant", "manner_affricate", "place_velar"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "x"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "m"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "l"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "r"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "d͡ʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "t͡sʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "t͡sʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "aspirated"]),
                       "t͡ʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "t͡ʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "t͡lʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "ejective"]),
                       "t͡lʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "aspirated"]),
                       }
        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "b":"b",
                    "d":"d",
                    "pʼ":"pe",
                    "pʰ":"ph",
                    "tʼ":"te",
                    "tʰ":"th",
                    "kʼ":"ke",
                    "kʰ":"kh",
                    "k͡x":"kx",
                    "f":"f",
                    "s":"s",
                    "ʃ":"S",
                    "x":"x",
                    "h":"h",
                    "m":"m",
                    "n":"n",
                    "ŋ":"N",
                    "ɲ":"J",
                    "l":"l",
                    "r":"r",
                    "j":"j",
                    "w":"w",
                    "u":"u",
                    "ɛ":"E",
                    "ɔ":"O",
                    "i":"i",
                    "a":"a",
                    "d͡ʒ":"dZ",
                    "t͡sʼ":"tse",
                    "t͡sʰ":"tsh",
                    "t͡ʃʼ":"tSe",
                    "t͡ʃʰ":"tSh",
                    "t͡lʼ":"tle",
                    "t͡lʰ":"tlh"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabic(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def is_consonant(self, phonename):
        return "consonant" in self.phones[phonename]

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

    def is_trill(self, phonename):
        return "manner_trill" in self.phones[phonename]

    def guess_syltonestress(self, word, syllables):
        """ Try to guess tone pattern for an unknown word...
        """
        return "L" * len(syllables)

    def _vowelindices(self, phones):
        return [i for i, ph in enumerate(phones) if self.is_vowel(ph)]

    def is_valid_CC(self, cluster, consider_foreign=True):
        """ We only explicitly check for Cw and Ch
        """
        if cluster[1] == "w" and any(isf(cluster[0]) for isf in [self.is_plosivelike, self.is_fricative, self.is_nasal, self.is_approximant, self.is_trill]):
            #print("CC1:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        elif consider_foreign and cluster in self.features["foreign_CC_onsets"]:
            #print("CC5:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            print("syllabify(): WARNING: foreign onset cluster: '{}'".format("".join(cluster)).encode("utf-8"), file=sys.stderr)
            return True
        return False

    def syllabify(self, phones):
        """ Basic Tswana syllabification...
        """
        def breakcluster(cluster):
            if not cluster:
                bounds.append(ci) #Always V.V
            elif len(cluster) == 1:
                bounds.append(ci) #Always V.CV (open syllables)
            elif len(cluster) == 2:
                if self.is_valid_CC(cluster):
                    bounds.append(ci) #V.CCV
                    return
                if self.is_syllabic(cluster[0]):
                    #V.sC.CV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                if cluster in self.features["foreign_CC_cluster_1split"]:
                    print("syllabify(): WARNING: foreign cluster was split: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CV
                    return
                #DEFAULT: V.CCV
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster),"".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci)
            elif len(cluster) == 3:
                if self.is_syllabic(cluster[0]):
                    if self.is_valid_CC(cluster[1:]): #V.sC.CWV
                        pass
                    else:
                        print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster[1:]), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                    return
                if cluster in self.features["foreign_CCC_onsets"]:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci) #V.CCCV
                if cluster[1:] in self.features["foreign_CC_onsets"]:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster[1:]), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CCV  (foreign)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #V.CCCV
            else:
                print("syllabify(): WARNING: unexpectedly long consonant cluster found: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)                
                if self.is_syllabic(cluster[0]):
                    #V.sC.*V
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                else:
                    #V.*V (generally: prefer open syllables)
                    bounds.append(ci)                

        v_inds = self._vowelindices(phones)
        bounds = []
        if v_inds:
            #Onset cluster (syllabic consonant?)
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


class Voice(SothoVoice): #orthography of Sotho-Tswana languages...
    pass
