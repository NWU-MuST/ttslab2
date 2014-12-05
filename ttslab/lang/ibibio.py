#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.phoneset

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for PhD studies, based on Ibibio data received from
        Etienne Barnard...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """
    def __init__(self):
        self.features = {"name": "Ibibio Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       #vowels:
                       "a"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "aː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_low", "position_front"]),
                       "e"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "eː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_front"]),
                       "i"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "iː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_front"]),
                       "ɪ"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "o"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back"]),
                       "oː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_back"]),
                       "ɔ"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back"]),
                       "ɔː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_back"]),
                       "u"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "uː" : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_back"]),
                       "ʉ"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "ə"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_mid"]),
                       "ʌ"  : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back"]),
                       #consonants:
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "ʀ"      : set(["class_consonantal", "consonant", "manner_trill", "place_uvular", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "articulation_aspirated"]),
                       "kp"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "articulation_aspirated"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "articulation_aspirated"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"])
                       }


        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "a":"a",
                    "aː":"aa",
                    "e":"e",
                    "eː":"ee",
                    "i":"i",
                    "iː":"ii",
                    "ɪ":"I",
                    "o":"o",
                    "oː":"oo",
                    "ɔ":"O",
                    "ɔː":"OO",
                    "u":"u",
                    "uː":"uu",
                    "ʉ":"uq",
                    "ə":"@",
                    "ʌ":"V",
                    "b":"b",
                    "d":"d",
                    "f":"f",
                    "ʀ":"R",
                    "h":"h",
                    "k":"k",
                    "kʰ":"kk",
                    "kp":"kp",
                    "m":"m",
                    "n":"n",
                    "ɲ":"J",
                    "ŋ":"N",
                    "p":"p",
                    "pʰ":"pp",
                    "r":"r",
                    "s":"s",
                    "t":"t",
                    "tʰ":"tt",
                    "w":"w",
                    "j":"j"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabic_consonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def is_consonant(self, phonename):
        return "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic syllabification implementation derived from a few
            rewrite rules defined by Gibbon et al.
        """
        sylls = [[]]
        phlist = list(phonelist)

        while phlist:
            phone = phlist[0]

            try:
                nphone = phlist[1]
                #C[r|w]?.
                if (self.is_consonant(phone) and
                    nphone in ["r", "w"]):
                    try:
                        nnphone = phlist[2]
                        sylls[-1].append(phlist.pop(0))#phone
                        sylls[-1].append(phlist.pop(0))#nphone
                        sylls[-1].append(phlist.pop(0))#nnphone
                        if phlist: sylls.append([])
                    except IndexError:
                        pass
                    continue
                if (self.is_consonant(phone) and 
                    self.is_consonant(nphone)):
                    #C.C
                    sylls[-1].append(phlist.pop(0))
                    if phlist: sylls.append([])
                    continue
                if (self.is_vowel(phone) and
                    self.is_consonant(nphone)):
                    #V.C
                    sylls[-1].append(phlist.pop(0))
                    if phlist: sylls.append([])
                    continue
                if (self.is_consonant(phone) and
                    self.is_vowel(nphone)):
                    #CV.?
                    sylls[-1].append(phlist.pop(0))#phone
                    sylls[-1].append(phlist.pop(0))#nphone
                    if phlist: sylls.append([])
                    continue
                if (self.is_vowel(phone) and
                    self.is_vowel(nphone)):
                    #V.V
                    sylls[-1].append(phlist.pop(0))
                    if phlist: sylls.append([])
                    continue
            except IndexError: #this is the last phone, add to syl if
                               #C add to prev syl, else on its own
                if self.is_consonant(phone):
                    try:
                        sylls[-2].append(phlist.pop(0))
                        sylls.pop()
                        continue
                    except IndexError:
                        pass
            sylls[-1].append(phlist.pop(0))
        return sylls

    def guess_syltonestress(self, word, syllables):
        """ Try to guess tone/stress pattern for an unknown word...
        """
        return "M" * len(syllables)


############################## TODO: Implement Voice --> start with defining orthography
