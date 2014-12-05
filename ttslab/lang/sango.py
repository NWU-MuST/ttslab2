#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.phoneset

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for PhD studies, based on Sango data received from
        Etienne Barnard...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """
    def __init__(self):
        self.features = {"name": "Sango Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       #vowels
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ã"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front", "articulation_nasalized"]),
#                      "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front", "articulation_nasalized"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ĩ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front", "articulation_nasalized"]),
#                      "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]), 
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ɔ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded", "articulation_nasalized"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "ũ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_nasalized"]),
                       #consonants
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "gb"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ʒ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "kp"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "mb"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_plosive", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "nd"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_plosive", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋg"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_plosive", "manner_nasal", "place_velar", "voiced"]),
                       "ŋgb"    : set(["class_sonorant", "class_consonantal", "consonant", "manner_plosive", "manner_nasal", "place_velar", "place_bilabial", "voiced"]),
                       "nʒ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_nasal", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "nz"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_nasal", "place_alveolar", "voiced"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau"    : "pau",
                    "paucl" : "paucl",
                    "ʔ"      : "paugs",
                    "a"      : "a",
                    "ã"      : "an",
#                    "e"      : "e",
                    "ɛ"      : "e",
                    "ɛ̃"      : "en",
                    "i"      : "i",
                    "ĩ"      : "in",
#                    "o"      : "o",
                    "ɔ"      : "o",
                    "ɔ̃"      : "on",
                    "u"      : "u",
                    "ũ"      : "un",
                    "b"      : "b",
                    "tʃ"     : "tS",
                    "d"      : "d",
                    "dʒ"     : "dZ",
                    "f"      : "f",
                    "g"      : "g",
                    "gb"     : "gb",
                    "h"      : "h",
                    "ʒ"      : "Z",
                    "j"      : "j",
                    "k"      : "k",
                    "kp"     : "kp",
                    "l"      : "l",
                    "m"      : "m",
                    "mb"     : "mb",
                    "n"      : "n",
                    "nd"     : "nd",
                    "ŋg"     : "Ng",
                    "ŋgb"    : "Ngb",
                    "nʒ"     : "nZ",
                    "ɲ"      : "J",
                    "nz"     : "nz",
                    "p"      : "p",
                    "r"      : "r",
                    "s"      : "s",
                    "t"      : "t",
                    "ʃ"      : "S",
                    "v"      : "v",
                    "w"      : "w",
                    "z"      : "z"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabic_consonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic syllabification, based on the syllabification scheme
            devised by Etienne Barnard for isiZulu (Nguni language).
        """
        sylls = [[]]
        phlist = list(phonelist)
        while phlist:
            phone = phlist[0]
            if self.is_syllabic_consonant(phone):
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
