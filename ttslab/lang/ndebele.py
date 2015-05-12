#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.phoneset
from ttslab.lang.zulu import Voice as ZuluVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Ndebele Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"   : set(["pause"]),
                       "paucl" : set(["closure"]),
                       "ʔ"     : set(["glottal-stop"]),
                       "kʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "tʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "pʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "ɓ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "lʒ"    : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "tsʼ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "tsʰ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "aspirated"]),
                       "tʃʼ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "tʃʰ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "dʒ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "a"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "b"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "dz"    : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "voiced"]),
                       "tɬʼ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "ejective"]),
                       "tɬʰ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "aspirated"]),
                       "ǀ"     : set(["class_consonantal", "consonant", "manner_click", "place_dental"]),
                       "d"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ǃ"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ɛ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "f"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "ǀʰ"    : set(["class_consonantal", "consonant", "manner_click", "place_dental", "aspirated"]),
                       "h"     : set(["consonant", "manner_fricative", "place_glottal"]),
                       "kx"    : set(["class_consonantal", "consonant", "manner_affricate", "place_velar"]),
                       "i"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"     : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "ɲ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "k"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "ɬ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "l"     : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "ǁ̬"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "r"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ǃʰ"    : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "aspirated"]),
                       "ǃ̬"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "voiced"]),
                       "u"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"     : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "x"     : set(["class_consonantal", "consonant", "manner_fricative", "place_velar"]),
                       "z"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map={"pau":"pau",
                  "paucl":"paucl",
                  "ʔ":"paugs",
                  "kʼ":"ke",
                  "kʰ":"kh",
                  "tʼ":"te",
                  "tʰ":"th",
                  "pʼ":"pe",
                  "pʰ":"ph",
                  "ɓ":"bE",
                  "lʒ":"lZ",
                  "tsʼ":"tse",
                  "tsʰ":"tsh",
                  "tʃʼ":"tSe",
                  "tʃʰ":"tSh",
                  "dʒ":"dZ",
                  "a":"a",
                  "b":"b",
                  "dz":"dz",
                  "tɬʼ":"tKe",
                  "tɬʰ":"tKh",
                  "ǀ":"c",
                  "d":"d",
                  "ǃ":"q",
                  "ɛ":"E",
                  "f":"f",
                  "g":"g",
                  "ǀʰ":"ch",
                  "h":"h",
                  "kx":"kx",
                  "i":"i",
                  "j":"j",
                  "ɲ":"J",
                  "k":"k",
                  "ɬ":"K",
                  "l":"l",
                  "ǁ̬":"xv",
                  "m":"m",
                  "n":"n",
                  "ŋ":"N",
                  "ɔ":"O",
                  "r":"r",
                  "s":"s",
                  "ǃʰ":"qh",
                  "ǃ̬":"qv",
                  "u":"u",
                  "v":"v",
                  "w":"w",
                  "x":"x",
                  "z":"z"
                  }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def syllabify(self, phonelist):
        """ Basic isiNdebele syllabification, based on the
            syllabification scheme devised by Etienne Barnard for
            isiZulu (Nguni language).
        """
        sylls = [[]]
        phlist = phonelist[:]
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
        return "0" * len(syllables)

class Voice(ZuluVoice): #Ndebele is also a Nguni language... TODO: Separate Nguni from Zulu
    pass
