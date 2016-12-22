#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re

import ttslab.phoneset
from ttslab.lang.default import DefaultTokenizer, DefaultVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        self.features = {"name": "Lwazi Zulu Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl",
                         "foreign_CC_cluster_1split": [["l", "s"], ["l", "f"], ["l", "tʰ"], ["l", "tʼ"],
                                                       ["k", "s"], ["k", "f"], ["k", "tʰ"], ["k", "tʼ"],
                                                       ["pʼ", "tʼ"], ["pʼ", "tʰ"],
                                                       ["r", "n"], ["r", "m"]],
                         "foreign_CC_onsets": [["ɡ", "r"], ["ɡ", "l"],
                                               ["f", "r"], ["f", "l"],
                                               ["ɓ", "r"], ["b", "r"], ["ɓ", "l"], ["b", "l"],
                                               ["k", "r"], ["kʰ", "r"], ["k", "l"], ["kʰ", "l"], ["k", "j"], ["kʰ", "j"],
                                               ["d", "r"],
                                               ["pʼ", "r"], ["pʼ", "l"],
                                               ["tʼ", "r"], ["tʰ", "r"],
                                               ["s", "k"], ["s", "kʰ"], ["s", "tʼ"], ["s", "tʰ"]],
                         "foreign_CCC_onsets": [["s", "tʼ", "r"]]}
        self.phones = {"pau"    : set(["pause"]),
                       "paucl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "ɓ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "ɮ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "t͡sʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "t͡ʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "d͡ʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "k͡ɬʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_velar", "place_alveolar", "ejective"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "ǀ"      : set(["class_consonantal", "consonant", "manner_click", "place_dental"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ǁ"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "ɡ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "ǀʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_dental", "aspirated"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ǃʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "aspirated"]),
                       "ǁʰ"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "aspirated"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "ɡ͡ǀ"      : set(["class_consonantal", "consonant", "manner_click", "place_dental", "voiced"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "ɡ͡ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "class_syllabic", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɡ͡ǁ"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "d͡z"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "voiced"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "pʼ":"pe",
                    "pʰ":"ph",
                    "ɓ":"bE",
                    "tʼ":"te",
                    "tʰ":"th",
                    "ɮ":"lZ",
                    "t͡sʼ":"tse",
                    "t͡ʃʼ":"tSe",
                    "d͡ʒ":"dZ",
                    "a":"a",
                    "kʰ":"kh",
                    "b":"b",
                    "k͡ɬʼ":"kKe",
                    "ɦ":"hv",
                    "ǀ":"cc",
                    "d":"d",
                    "ǃ":"qq",
                    "ɛ":"E",
                    "ǁ":"xx",
                    "f":"f",
                    "ɡ":"g",
                    "ǀʰ":"cch",
                    "h":"h",
                    "ǃʰ":"qqh",
                    "ǁʰ":"xxh",
                    "i":"i",
                    "j":"j",
                    "ɲ":"J",
                    "k":"k",
                    "ɬ":"K",
                    "ɡ͡ǀ":"gcc",
                    "l":"l",
                    "ɡ͡ǃ":"gqq",
                    "m":"m",
                    "n":"n",
                    "ŋ":"N",
                    "ɡ͡ǁ":"gxx",
                    "ɔ":"O",
                    "d͡z":"dz",
                    "r":"r",
                    "s":"s",
                    "ʃ":"S",
                    "u":"u",
                    "v":"v",
                    "w":"w",
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
                                                "z", "ɬ", "ɮ", "n", "ɲ", "ŋ",
                                                "j", "k", "kʰ"]:
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

PHRASEBREAK_TOKENS = set()
# #These are not all strictly conjunctions (some are motivated by
# #simple analysis of pauses between breath groups in the Lwazi2 TTS
# #corpus).
# PHRASEBREAK_TOKENS = set(["ukuti", #that, in order that
#                           "kuko", "kumbe", #or either
#                           "nokuba", "nakuba", #whether
#                           "noko", "kantinoko", #yet, however, notwithstanding, still,
#                           "kepa", #but
#                           "funa", #lest
#                           "ngokuba", #for, because
#                           "nxa", "inxa", "umauxa", #if
#                           "ngako", #therefore
#                           "njengoba", #because; since
#                           "kube", "ukube" #that; so that; in order that; if
#                           "sase", #and then
#                           # the following added based on stats from the Lwazi2 TTS corpus:
#                           "noma", #or either (38%)
#                           "bese", #and then (65%)
#                           "uma", #if (18%)
#                           "kufanele", # -fanele + sjnc. or inf. must; need to; have to; ought to; should (40%)
#                           "ukuze", #so that; in order that (40%)
#                           "futhi", #and (24%)
#                           "kanye", #once (34%)
#                           "kumele", #represent; stand for (30%)
#                           "kodwa", #only, excepting that (50%)
#                           "ukuthi", #so that; in order that (3%)
#                           "ngoba", #for, because (35%)
#                           "kanti", #whereas (50%)
#                           "ngaphandle", # ~ kwa-/kuka- apart from; besides; except; without; unless
#                           # ~ kwalokho apart from that; besides; otherwise (32%)
#                           "ngaphambi", #ahead; before; in front (33%)
#                           "lapho", #when, where (11%)
#                           "ukuba", #that; so that; in order that; if (12%)
#                           "nokuthi", #and; also; even to say (44%)
#                           "ikakhulukazi", "kakhulukazi" #especially; particularly; in particular (60%)
#                           "kuze", #so that; in order that (38%)
#                           "naye", #and him; and her; even he/him; even she/her; he too; she too; with him; with her (27%)
#                           "ngenxa" #~ ya- because of; on behalf of (21%)
#                       ])


class Tokenizer(DefaultTokenizer):
    def _split_token(self, token, simplemarkupchars):
        splitchars = "-" + "".join(simplemarkupchars)
        temp = token
        temp = re.sub(r"(\w)([%s]+)(\w)" % re.escape(splitchars), "\\1 \\2\\3", temp, flags=re.UNICODE)
        temp = re.sub(r"([a-z']+)([^a-z'_])", "\\1 \\2", temp, flags=re.UNICODE)
        temp = temp.replace("-", "")
        #print(token, temp.split())
        return temp.split()

class Voice(DefaultVoice):
    pass
#const data
Voice.PHRASEBREAK_TOKENS = PHRASEBREAK_TOKENS
#uttprocs
Voice.tokenize_text = Tokenizer()

if __name__ == "__main__":
    from ttslab.lang.zulu import Voice
    v = Voice()
#    u = v.synthesize("“Uma ubuka ukuthi inhlangano enkulu yezempilo, iWorld Health Organisation, ithe kungenzeka isifo siphathe abantu abawu-10 000 kusukela ngoDisemba uyabona ukuthi besidinga ukwenza umnyakazo ngokushesha,” kusho u-Annets.", "text-to-words")
    u = v.synthesize("Abaculi base-Afrika abawu-70 abahlanganiswe yiMTN enikele ngo-$10 million, kubalwa kubo abakuleli oDonald, Mafikizolo, Lloyd Cele, Loyiso, Matthew Gold, Elvis Blue, Kurt Darren, The Arrows, MTN Joyous Celebration noRebecca Malope bangabanye abazocula leli culo.", "text-to-words")
    print(u)
