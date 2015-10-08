#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Initial phoneset implementation for a Soninke voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.phoneset
from ttslab.lang.default import DefaultVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Defined according to:
        http://phoible.org/inventories/view/820#tsegments
    """
    def __init__(self):
        self.features = {"name": "Soninke Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl" : set(["closure"]),
                       #vowels
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "iː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_front"]),
                       "aː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_low", "position_front"]),
                       "uː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_back"]),
                       "oː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_back", "articulation_rounded"]),
                       "eː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_front"]),
                       "ĩ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ã"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ũ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "õ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ẽ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       #consonants
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "ʔ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_glottal"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "χ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_uvular"]),
                       "pː"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "tʃː"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "ʔː"      : set(["class_consonantal", "consonant", "manner_plosive", "place_glottal"])
                       }
        self.map = {"pau"    : "pau",
                    "paucl" : "paucl",
                    #vowels
                    "a"      : "a",
                    "e"      : "e",
                    "i"      : "i",
                    "o"      : "o",
                    "u"      : "u",
                    "iː"     : "il",
                    "aː"     : "al",
                    "uː"     : "ul",
                    "oː"     : "ol",
                    "eː"     : "el",
                    "ĩ"      : "in",
                    "ã"      : "an",
                    "ũ"      : "un",
                    "õ"      : "on",
                    "ẽ"      : "en",
                    #consonants
                    "ʔ"      : "paugs",
                    "b"      : "b",
                    "p"      : "p",
                    "d"      : "d",
                    "f"      : "f",
                    "g"      : "g",
                    "h"      : "h",
                    "j"      : "j",
                    "k"      : "k",
                    "l"      : "l",
                    "m"      : "m",
                    "n"      : "n",
                    "ɲ"      : "J",
                    "ŋ"      : "N",
                    "dʒ"     : "dZ",
                    "tʃ"     : "tS",
                    "r"      : "r",
                    "s"      : "s",
                    "t"      : "t",
                    "w"      : "w",
                    "χ"      : "X",
                    "pː"     : "pl",
                    "tʃː"    : "tSl",
                    "ʔː"     : "paugsl"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_consonant(self, phonename):
        return "consonant" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic syllabification, based on the syllabification scheme
            devised by Etienne Barnard for isiZulu (Nguni language).
        """
        sylls = [[]]
        phlist = list(phonelist)
        while phlist:
            phone = phlist[0]
            if self.is_syllabicconsonant(phone):
                #sC.Any
                sylls[-1].append(phlist.pop(0))
                if phlist: sylls.append([])
                continue
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

    def guess_syltonestress(self, word, syllables):
        """ Try to guess tone/stress pattern for an unknown word...
        """
        return "M" * len(syllables)


############################## TODO: Implement Voice --> start with defining orthography
VALID_GRAPHS = set("ŋ'abcdefghijklmnopqrstuwxy") #specify only lowercase NFC -- used for pronunciation/language determination

class Voice(DefaultVoice):
    pass

Voice.VALID_GRAPHS = VALID_GRAPHS
