# -*- coding: utf-8 -*-
"""This file contains language-specific implementation for US English
    (based on CMUdict).
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re

import ttslab.lang.englishZA
from ttslab.lang.englishZA import Voice

class Phoneset(ttslab.lang.englishZA.Phoneset):
    """ Based on ARPAbet... see: http://en.wikipedia.org/wiki/Arpabet

        Phoneme Example Translation
        ------- ------- -----------
        AA	odd     AA D
        AE	at	AE T
        AH	hut	HH AH T
        AO	ought	AO T
        AW	cow	K AW
        AY	hide	HH AY D
        B 	be	B IY
        CH	cheese	CH IY Z
        D 	dee	D IY
        DH	thee	DH IY
        EH	Ed	EH D
        ER	hurt	HH ER T
        EY	ate	EY T
        F 	fee	F IY
        G 	green	G R IY N
        HH	he	HH IY
        IH	it	IH T
        IY	eat	IY T
        JH	gee	JH IY
        K 	key	K IY
        L 	lee	L IY
        M 	me	M IY
        N 	knee	N IY
        NG	ping	P IH NG
        OW	oat	OW T
        OY	toy	T OY
        P 	pee	P IY
        R 	read	R IY D
        S 	sea	S IY
        SH	she	SH IY
        T 	tea	T IY
        TH	theta	TH EY T AH
        UH	hood	HH UH D
        UW	two	T UW
        V 	vee	V IY
        W 	we	W IY
        Y 	yield	Y IY L D
        Z 	zee	Z IY
        ZH	seizure	S IY ZH ER
    """
    def __init__(self):
        #syllable_clusters are processed in order, thus a list, not a set...
        self.features = {"name": "CMU English Phoneset",
                         "syllable_clusters": ["VCV", "VCCV", "VCCCV", "VCCCCV",
                                                "VCGV", "VCCGV", "VCCCGV", "VV"],
                         "wellformed_plosive_clusters": [["p","l"], ["b","l"], ["k","l"], ["g","l"], ["p","r"],
                                                         ["b","r"], ["t","r"], ["d","r"], ["k","r"], ["g","r"],
                                                         ["t","w"], ["d","w"], ["g","w"], ["k","w"], ["p","y"],
                                                         ["b","y"], ["t","y"], ["d","y"], ["k","y"], ["g","y"]],
                         "wellformed_fricative_clusters": [["f","l"], ["f","r"], ["th","r"], ["sh","r"],
                                                           ["th","w"], ["hh","w"], ["f","y"], ["v","y"],
                                                           ["th","y"], ["z","y"], ["hh","y"]],
                         "wellformed_other_clusters": [["m","y"], ["n","y"], ["l","y"]],
                         "wellformed_s_clusters": [["s","p"], ["s","t"], ["s","k"], ["s","m"], ["s","n"],
                                                   ["s","f"], ["s","w"], ["s","l"], ["s","y"], ["s","p","l"],
                                                   ["s","p","r"], ["s","p","y"], ["s","m","y"], ["s","t","r"],
                                                   ["s","t","y"], ["s","k","l"], ["s","k","r"], ["s","k","w"],
                                                   ["s","k","y"]]
                         }
        self.features["wellformed_clusters"] = (self.features["wellformed_plosive_clusters"] +
                                                self.features["wellformed_fricative_clusters"] +
                                                self.features["wellformed_other_clusters"] +
                                                self.features["wellformed_s_clusters"])
        self.features["silence_phone"] = "pau"
        self.features["closure_phone"] = "pau_cl"
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "pau_gs" : set(["glottal-stop"]),
                       "aa" : set(["duration_short", "position_back", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "iy" : set(["position_front", "duration_long", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "ch" : set(["place_alveolar", "class_consonantal", "manner_affricate", "consonant", "manner_strident", "place_post-alveolar"]),
                       "ae" : set(["duration_short", "position_front", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "eh" : set(["duration_short", "position_front", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ah" : set(["duration_short", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ao" : set(["duration_long", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ih" : set(["duration_short", "position_front", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "ey" : set(["position_front", "duration_diphthong", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "aw" : set(["position_front", "duration_diphthong", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "ay" : set(["position_front", "duration_diphthong", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "zh" : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "place_post-alveolar"]),
                       "er" : set(["position_central", "duration_short", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ng" : set(["class_consonantal", "voiced", "manner_nasal", "place_velar", "consonant", "class_sonorant"]),
                       "r"  : set(["place_alveolar", "class_consonantal", "manner_liquid", "voiced", "manner_approximant", "consonant", "class_sonorant"]),
                       "th" : set(["class_consonantal", "manner_fricative", "consonant", "place_dental"]),
                       "uh" : set(["duration_short", "position_back", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "oy" : set(["duration_diphthong", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "dh" : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "place_dental"]),
                       "ow" : set(["duration_diphthong", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "hh" : set(["manner_fricative", "consonant", "place_glottal"]),
                       "jh" : set(["place_alveolar", "class_consonantal", "manner_affricate", "voiced", "consonant", "manner_strident", "place_post-alveolar"]),
                       "b"  : set(["class_consonantal", "place_bilabial", "voiced", "manner_plosive", "consonant"]),
                       "d"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_plosive", "consonant"]),
                       "g"  : set(["class_consonantal", "voiced", "place_velar", "manner_plosive", "consonant"]),
                       "f"  : set(["class_consonantal", "manner_fricative", "consonant", "manner_strident", "place_labiodental"]),
                       "uw" : set(["duration_long", "articulation_round", "position_back", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "m"  : set(["class_consonantal", "voiced", "manner_nasal", "consonant", "place_labial", "class_sonorant"]),
                       "l"  : set(["place_alveolar", "class_consonantal", "manner_liquid", "voiced", "manner_approximant", "consonant", "manner_lateral", "class_sonorant"]),
                       "n"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_nasal", "consonant", "class_sonorant"]),
                       "p"  : set(["class_consonantal", "place_bilabial", "manner_plosive", "consonant"]),
                       "s"  : set(["place_alveolar", "class_consonantal", "manner_fricative", "consonant", "manner_strident"]),
                       "sh" : set(["class_consonantal", "manner_fricative", "consonant", "place_post-alveolar"]),
                       "t"  : set(["place_alveolar", "class_consonantal", "manner_plosive", "consonant"]),
                       "w"  : set(["voiced", "place_velar", "manner_approximant", "manner_glide", "consonant", "place_labial", "class_sonorant"]),
                       "v"  : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "manner_strident", "place_labiodental"]),
                       "y"  : set(["voiced", "place_palatal", "manner_approximant", "manner_glide", "consonant", "class_sonorant"]),
                       "z"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_fricative", "consonant", "manner_strident"]),
                       "k"  : set(["class_consonantal", "place_velar", "manner_plosive", "consonant"])
                       }        
        self.map = dict((k, k) for k in self.phones) # redundant mapping

    def guess_syltonestress(self, syllables):
        """ Try to guess stress pattern for an unknown word...
        """
        if len(syllables) == 1:
            if "ah" not in syllables[0]: #schwa
                return "1"
            else:
                return "0"
        else:
            return "0" * len(syllables) #implement other cases later
