# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re

import ttslab.phoneset
from ttslab.lang.sotho import Voice as SothoVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Nsotho Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "kʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "kx"     : set(["class_consonantal", "consonant", "manner_affricate", "place_velar"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "ɣ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar", "voiced"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "βʒ"     : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial", "place_post-alveolar", "voiced"]),
                       "β"      : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial", "voiced"]),
                       "ɸs"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_bilabial", "place_alveolar"]), #strident?
                       "ɸʃ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_bilabial", "place_post-alveolar"]), #strident?
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "ɱ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_labiodental", "voiced"]),
                       "ɭ"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_retroflex", "voiced"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "tsʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "tsʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "aspirated"]),
                       "tʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "tʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "tlʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "ejective"]),
                       "tlʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "aspirated"]),
                       "psʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_bilabial", "place_alveolar", "aspirated"]),
                       "psʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_bilabial", "place_alveolar", "ejective"]),
                       "pʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_bilabial", "place_post-alveolar", "aspirated"])
                       }

        self.map = {"pau"     :"pau",
                    "paucl"   :"paucl",
                    "ʔ"       :"paugs",
                    "pʼ"      :"pe",
                    "pʰ"      :"ph",
                    "tʼ"      :"te",
                    "tʰ"      :"th",
                    "kʼ"      :"ke",
                    "kʰ"      :"kh",
                    "kx"      :"kx",
                    "f"       :"f",
                    "s"       :"s",
                    "ʃ"       :"S",
                    "h"       :"h",
                    "ɦ"       :"hv",
                    "ɣ"       :"G",
                    "ɬ"       :"K",
                    "βʒ"      :"BZ",
                    "β"       :"B",
                    "ɸs"      :"qs",
                    "ɸʃ"      :"qS",
                    "m"       :"m",
                    "n"       :"n",
                    "ŋ"       :"N",
                    "ɲ"       :"J",
                    "ɱ"       :"mj",
                    "ɭ"       :"lq",
                    "l"       :"l",
                    "r"       :"r",
                    "j"       :"j",
                    "w"       :"w",
                    "u"       :"u",
                    "ɛ"       :"E",
                    "ɔ"       :"O",
                    "i"       :"i",
                    "a"       :"a",
                    "dʒ"      :"dZ",
                    "tsʼ"     :"tse",
                    "tsʰ"     :"tsh",
                    "tʃʼ"     :"tSe",
                    "tʃʰ"     :"tSh",
                    "tlʼ"     :"tle",
                    "tlʰ"     :"tlh",
                    "psʰ"     :"psh",
                    "psʼ"     :"pse",
                    "pʃʰ"     :"pSh"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def is_consonant(self, phonename):
        return "consonant" in self.phones[phonename]

    def guess_syltonestress(self, word, syllables):
        """ Try to guess tone pattern for an unknown word...
        """
        return "0" * len(syllables)

    def syllabify(self, phonelist):
        """ Basic Sotho syllabification...
        """
        sylls = [[]]
        phlist = phonelist[:]
        while phlist:
            phone = phlist[0]
            if self.is_syllabicconsonant(phone):
                try:
                    nphone = phlist[1]
                    #syllabicC.C
                    if self.is_consonant(nphone):
                        sylls[-1].append(phlist.pop(0))
                        if phlist: sylls.append([])
                        continue
                except IndexError:
                    pass
            try:
                nphone = phlist[1]
                nnphone = phlist[2]
                #If there is a three phone cluster:
                if (self.is_vowel(phone) and
                    not self.is_vowel(nphone) and
                    not self.is_vowel(nnphone)):
                    #VC.C
                    sylls[-1].append(phlist.pop(0))#phone
                    sylls[-1].append(phlist.pop(0))#nphone
                    if phlist: sylls.append([])
                    continue
            except IndexError:
                pass
            if self.is_vowel(phone):
                #V.Any
                sylls[-1].append(phlist.pop(0))
                if phlist: sylls.append([])
                continue
            #anything not caught above is added to current syl...
            sylls[-1].append(phlist.pop(0))
        return sylls


class Voice(SothoVoice): #orthography of Sotho-Tswana languages...
    pass
