#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.phoneset

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for PhD studies, based on Igbo data received from
        Ola Iheanetu...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """
    def __init__(self):
        self.features = {"name": "Igbo Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl" : set(["closure"]),
                       "paugs" : set(["glottal-stop"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]), 
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "tS"    : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_postal-veolar", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "place_labio-dental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "gb"    : set(["class_consonantal", "consonant", "manner_implosive", "manner_plosive", "place_labio-velar", "voiced", "bilabial"]),
                       "G"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar", "voiced"]),
                       "gw"    : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "labial", "voiced"]),
                       "hh"    : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "Iq"    : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_near-front"]),
                       "dZ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_plosive", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "k"      : set(["class_constantal", "consonant", "manner_plosive", "place_velar"]),
                       "kp"    : set(["class_constantal", "consonant", "manner_plosive", "place_velar", "place_bilabial"]),
                       "kw"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_approximant", "place_velar", "voiced", "labialized"]),
                       "l"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "Nw"    : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "labialized", "voiced"]),
                       "J"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "N"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "Oq"    : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial","ejective"]),
                       "rr"    : set(["class_consonantal", "consonant", "manner_approximant", "manner_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "S"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "Uq"    : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "position_near-back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_glide", "place_velar", "place_labial", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])        
}
        self.map = {"pau"    : "pau",
                    "paucl" : "paucl",
                    "paugs" : "paugs",
                    "a"      :  "a",
                    "b"      :  "b",
                    "tS"    :  "tS",
                    "d"      :  "d",
                    "f"      :  "f",
                    "g"      :  "g",
                    "gb"    :  "gb",
                    "G"      :  "G",
                    "gw"    :  "gw",
                    "hh"    :  "hh",
                    "e"      :  "e",
                    "i"      :  "i",
                    "Iq"    :  "Iq",
                    "dZ"    :  "dZ",
                    "k"      :  "k",
                    "kp"    :  "kp",
                    "kw"    :  "kw",
                    "l"      :  "l",
                    "m"      :  "m",
                    "n"      :  "n",
                    "Nw"    :  "Nw",
                    "J"      :  "J",
                    "N"      :  "N",
                    "o"      :  "o",
                    "Oq"    :  "Oq",
                    "p"      :  "p",
                    "rr"    :  "rr",
                    "s"      :  "s",
                    "S"      :  "S",
                    "t"      :  "t",
                    "u"      :  "u",
                    "Uq"    :  "Uq",
                    "v"      :  "v",
                    "w"      :  "w",
                    "j"      :  "j",
                    "z"      :  "z"    
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
