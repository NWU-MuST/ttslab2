# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re

import ttslab.phoneset
from ttslab.lang.default import DefaultVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Tsonga Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "pjʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "place_palatal", "ejective"]),
                       "pjʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "place_palatal", "aspirated"]),
                       "bj"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "place_palatal", "voice"]),
                       "dj"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "place_palatal", "voice"]),
                       "ɓ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "mɦ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced", "aspirated"]),
                       "ʂ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_retroflex"]),
                       "dʐ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_retroflex", "voiced"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "β"      : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial", "voiced"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "tj"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "place_palatal"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "tjʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "place_palatal", "aspirated"]),
                       "ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "dɦ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced", "aspirated"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "nɦ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced", "aspirated"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "tlʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "ejective"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "tlʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "manner_lateral", "place_alveolar", "aspirated"]),
                       "dɬ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "dlʒ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "voiced", "aspirated"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "rɦ"     : set(["class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced", "aspirated"]),
                       "dʐɦ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_retroflex", "voiced", "aspirated"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "ɳ"      : set(["class_consonantal", "class_sonorant", "consonant", "manner_nasal", "place_retroflex", "voiced"]),
                       "tʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "tʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "dʒɦ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "aspirated", "voiced"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "gɦ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }

        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "pʰ":"ph",
                    "pjʼ":"pje",
                    "pjʰ":"pjh",
                    "bj":"bj",
                    "dj":"dj",
                    "ɓ":"bE",
                    "mɦ":"mh",
                    "ʂ":"sq",
                    "dʐ":"dzq",
                    "tʼ":"te",
                    "a":"a",
                    "tʰ":"th",
                    "b":"b",
                    "β":"B",
                    "ɦ":"hv",
                    "tj":"tj",
                    "d":"d",
                    "tjʰ":"tjh",
                    "ǃ":"q",
                    "ɛ":"E",
                    "dɦ":"dhv",
                    "f":"f",
                    "g":"g",
                    "nɦ":"nhv",
                    "i":"i",
                    "tlʼ":"tle",
                    "j":"j",
                    "ɲ":"J",
                    "k":"k",
                    "ɬ":"K",
                    "l":"l",
                    "tlʰ":"tlh",
                    "dɬ":"dK",
                    "m":"m",
                    "n":"n",
                    "ŋ":"N",
                    "ɔ":"O",
                    "dlʒ":"dKv",
                    "p":"p",
                    "rɦ":"rhv",
                    "dʐɦ":"dzhv",
                    "r":"r",
                    "s":"s",
                    "ʃ":"S",
                    "ɳ":"nq",
                    "tʃʼ":"tSe",
                    "u":"u",
                    "tʃʰ":"tSh",
                    "v":"v",
                    "dʒ":"dZ",
                    "w":"w",
                    "dʒɦ":"dZh",
                    "kʰ":"kh",
                    "gɦ":"ghv",
                    "z":"z"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def syllabify(self, phonelist):
        """ Basic Tsonga syllabification, based on the syllabification
            scheme devised by Etienne Barnard for isiZulu (Nguni
            language).
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

##############################
VALID_GRAPHS = set("abcdefghijklmnopqrstuvwxyz'") #specify only lowercase NFC -- used for pronunciation/language determination

class Voice(DefaultVoice):
    pass

Voice.VALID_GRAPHS = VALID_GRAPHS
