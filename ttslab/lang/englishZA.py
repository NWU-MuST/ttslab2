# -*- coding: utf-8 -*-
"""This file contains language-specific implementation for South
    African English (based on Lwazi -- which was derived from OALD).
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
import ttslab.phoneset
from ttslab.lang.default import DefaultVoice

class Phoneset(ttslab.phoneset.Phoneset):
    """ Based on MRPA...
    """
    def __init__(self):
        #syllable_clusters are processed in order, thus a list, not a set...
        self.features = {"name": "Lwazi English Phoneset",
                         "syllable_clusters": ["VCV", "VGV", "VCCV", "VCCCV", "VCCCCV",
                                                "VCGV", "VCCGV", "VCCCGV", "VV"],
                         "wellformed_plosive_clusters": [["p","l"], ["b","l"], ["k","l"], ["g","l"], ["p","ɹ"],
                                                         ["b","ɹ"], ["t","ɹ"], ["d","ɹ"], ["k","ɹ"], ["g","ɹ"],
                                                         ["t","w"], ["d","w"], ["g","w"], ["k","w"], ["p","j"],
                                                         ["b","j"], ["t","j"], ["d","j"], ["k","j"], ["g","j"]],
                         "wellformed_fricative_clusters": [["f","l"], ["f","ɹ"], ["θ","ɹ"], ["ʃ","ɹ"],
                                                           ["θ","w"], ["h","w"], ["f","j"], ["v","j"],
                                                           ["θ","j"], ["z","j"], ["h","j"]],
                         "wellformed_other_clusters": [["m","j"], ["n","j"], ["l","j"]],
                         "wellformed_s_clusters": [["s","p"], ["s","t"], ["s","k"], ["s","m"], ["s","n"],
                                                   ["s","f"], ["s","w"], ["s","l"], ["s","j"], ["s","p","l"],
                                                   ["s","p","ɹ"], ["s","p","j"], ["s","m","j"], ["s","t","ɹ"],
                                                   ["s","t","j"], ["s","k","l"], ["s","k","ɹ"], ["s","k","w"],
                                                   ["s","k","j"]]
                         }
        self.features["wellformed_clusters"] = (self.features["wellformed_plosive_clusters"] +
                                                self.features["wellformed_fricative_clusters"] +
                                                self.features["wellformed_other_clusters"] +
                                                self.features["wellformed_s_clusters"])
        self.features["silence_phone"] = "pau"
        self.features["closure_phone"] = "paucl"
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "ə"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_central"]),
                       "ɜ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_central"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ɑ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_low", "position_back"]),
                       "aɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "aʊ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ð"      : set(["class_consonantal", "consonant", "manner_fricative", "place_dental", "voiced"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "eɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ɪ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ɪə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɒ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_back", "articulation_rounded"]),
                       "ɔɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "əʊ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "ɹ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "θ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_dental"]),
                       "ʊ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "ʊə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ʌ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"]),
                       "ʒ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "ə":"q",     #about
                    "ɜ":"qq",    #bird
                    "a":"a",     #bad
                    "ɑ":"aa",    #bard
                    "aɪ":"ai",   #buy
                    "aʊ":"au",   #cow
                    "b":"b",
                    "tʃ":"ch",   #chin
                    "d":"d",
                    "ð":"dh",    #then
                    "ɛ":"e",     #bed
                    "ɛə":"eq",   #bare
                    "eɪ":"ei",   #bay
                    "f":"f",
                    "g":"g",
                    "h":"h",
                    "ɪ":"i",     #bid
                    "ɪə":"iq",   #beer
                    "i":"ii",    #bead
                    "dʒ":"jh",   #edge
                    "k":"k",
                    "l":"l",
                    "m":"m",
                    "n":"n",
                    "ŋ":"ng",    #sing
                    "ɒ":"o",     #pot
                    "ɔɪ":"oi",   #boy
                    "ɔ":"oo",    #port
                    "əʊ":"ou",   #go
                    "p":"p",
                    "ɹ":"r",     #ray
                    "s":"s",
                    "ʃ":"sh",    #she
                    "t":"t",
                    "θ":"th",    #thin
                    "ʊ":"u",     #put
                    "ʊə":"uq",   #poor
                    "ʌ":"uh",    #bud
                    "u":"uu",    #boot
                    "v":"v",
                    "w":"w",
                    "j":"y",     #yes
                    "z":"z",
                    "ʒ":"zh"     #beige
                    }
       
    def is_plosive(self, phonename):
        return "manner_plosive" in self.phones[phonename]

    def is_voiced(self, phonename):
        return ("voiced" in self.phones[phonename] or
                "vowel" in self.phones[phonename])

    def is_obstruent(self, phonename):
        return ("class_consonantal" in self.phones[phonename] and
                "class_sonorant" not in self.phones[phonename] and
                "class_syllabic" not in self.phones[phonename])

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_glide(self, phonename):
        return "manner_glide" in self.phones[phonename]

    def is_liquid(self, phonename):
        return "manner_liquid" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def is_fricative(self, phonename):
        return "manner_fricative" in self.phones[phonename]

    def is_nasal(self, phonename):
        return "manner_nasal" in self.phones[phonename]

    def sonority_level(self, phonename):
        """ Assigns levels of sonority to phones based on their nature...
        """
        
        if self.is_vowel(phonename):
            if "height_low" in self.phones[phonename]:
                return 9
            if "height_mid" in self.phones[phonename]:
                return 8
            if "height_high" in self.phones[phonename]:
                return 7
        if self.is_liquid(phonename):
            return 6
        if self.is_nasal(phonename):
            return 5
        if self.is_fricative(phonename):
            if self.is_voiced(phonename):
                return 4
            else:
                return 3
        if self.is_plosive(phonename):
            if self.is_voiced(phonename):
                return 2
            else:
                return 1
        return 0


    def _process_cluster(self, cluster, phonelist, match):
        """ Break cluster into syllables according to the rules defined by
            T.A. Hall, "English syllabification as the interaction of
            markedness constraints" in Studia Linguistica, vol. 60, 2006,
            pp. 1-33

            Need to refactor the if statements to make clearer/simpler...
        """
        ###COMMENTS IN THIS FUNCTION ARE OUT OF DATE...

        phonecluster = phonelist[match.start() : match.end()]

        if cluster == "VCV":
            #always split -> V.CV (except disallow /N/ onset):
            if phonecluster[1] == "ŋ":
                return "VC.V"
            else:
                return "V.CV"
        elif cluster == "VGV":
            return "V.GV"

        if cluster == "VCCV":
            CC = phonecluster[1:3]
            #if CC cluster is Tautosyllabic -> V.CCV:
            if ((CC in self.features["wellformed_clusters"] and
                 self.sonority_level(CC[1]) > self.sonority_level(CC[0])) or
                (CC[0] == "s" and
                 self.is_plosive(CC[1]) and
                 not self.is_voiced(CC[1]))):
                return "V.CCV"
            #if CC cluster is Heterosyllabic -> VC.CV:
            if ((self.sonority_level(CC[1]) < self.sonority_level(CC[0])) or
                (self.sonority_level(CC[1]) == self.sonority_level(CC[0])) or
                (CC not in self.features["wellformed_clusters"] and
                 self.sonority_level(CC[1]) > self.sonority_level(CC[0]))):
                return "VC.CV"

        if cluster == "VCCCV":
            CCC = phonecluster[1:4]
            C2C3 = CCC[1:]
            # #if CCC are all obstruents -> VC.CCV:
            # if all([self.is_obstruent(C) for C in CCC]):
            #     return "VC.CCV"
            #if C2C3 are wellformed onsets -> VC.CCV:
            if CCC in self.features["wellformed_clusters"]:
                return "V.CCCV"
            if C2C3 in self.features["wellformed_clusters"]:
                return "VC.CCV"
            else:
                return "VCC.CV"

        if cluster == "VCCCCV":
            if phonecluster[2:5] in self.features["wellformed_clusters"]:
                return "VC.CCCV"
            if phonecluster[3:5] in self.features["wellformed_clusters"]:
                return "VCC.CCV"
            return "VCCC.CV"

        if cluster == "VCGV":
            CG = phonecluster[1:3]
            # if not self.is_plosive(CG[0]):                   #C not a stop
            #     return "VC.GV"
            # else:
            if CG not in self.features["wellformed_clusters"]: #C a stop and CG not wellformed
                return "VC.GV"
            else:
                return "V.CGV"                                 #C a stop and CG wellformed

        if cluster == "VCCGV":
            CCG = phonecluster[1:4]
            # if CCG[0] == "s":
            #     return "V.CCGV"
            # else:
            #     return "VC.CGV"
            if CCG in self.features["wellformed_clusters"]:
                return "V.CCGV"
            else:
                return "VC.CGV"

        if cluster == "VCCCGV":
            if phonecluster[2:5] in self.features["wellformed_clusters"]:
                return "VC.CCGV"
            if phonecluster[3:5] in self.features["wellformed_clusters"]:
                return "VCC.CGV"
            return "VCCC.GV"

        if cluster == "VV":   #not described in the Hall paper...
            return "V.V"


    def syllabify(self, phonelist):
        """ Classes:
               C -> Consonant,
               V -> Short/Long Vowel/Syllabic sonorant/Diphthong
               G -> Glide
        """
        #make a copy (to be edited internally)
        plist = list(phonelist)

        #first construct string representing relevant classes...
        classstr = ""
        for phone in plist:
            if self.is_vowel(phone):
                classstr += "V"
            elif self.is_glide(phone):
                classstr += "G"
            else:
                classstr += "C"
        #Begin Aby's hacks:
        # - Change the last phoneclass under certain conditions..
        try:
            if (self.is_syllabicconsonant(plist[-1]) and
                self.is_obstruent(plist[-2])):
                classstr = classstr[:-1] + "V"
            if (self.is_syllabicconsonant(plist[-1]) and
                self.is_nasal(plist[-2])):
                classstr = classstr[:-1] + "V"
        except IndexError:
            pass
        #End Aby's hacks...

        #find syllable_clusters in order and apply syllabification 
        #process on each...this should be redone... FIXME!!!
        for cluster in self.features["syllable_clusters"]:
            match = re.search(cluster, classstr)
            while match:
                #syllabify cluster
                clustersylstr = self._process_cluster(cluster, plist, match)
                #update classstr...
                start, end = match.span()
                classstr = clustersylstr.join([classstr[:start], classstr[end:]])
                plist = (plist[:match.start() + clustersylstr.index(".")] +
                             [""] + plist[match.start() + clustersylstr.index("."):])
                #next match...
                match = re.search(cluster, classstr)

        sylls = [[]]
        index = 0
        for char in classstr:
            if char != ".":
                sylls[-1].append(phonelist[index])
                index += 1
            else:
                sylls.append([])

        return sylls
        
    def guess_syltonestress(self, word, syllables):
        """ Try to guess stress pattern for an unknown word...
        """
        if len(syllables) == 0:                     # monosyllable always unstressed
            return "0"                              
        elif len(syllables) == 2:                   # bi-syllable guess stress not on schwa
            if "ə" in syllables[0] and "ə" not in syllables[1]:
                return "01"
            else:
                return "10"
        else:
            return "1" + "0" * (len(syllables) - 1) # default stress on first syllable


##############################        
###Helper constants:

#An approximation from Festival's "pos.scm"
PREPOSITIONS = ["of", "for", "in", "on", "that", "with", "by", "at",
                "from", "as", "if", "that", "against", "about",
                "before", "because", "if", "under", "after", "over",
                "into", "while", "without", "through", "new",
                "between", "among", "until", "per", "up", "down",
                "to"]
DETERMINERS = ["the", "a", "an", "no", "some", "this", "that", "each",
               "another", "those", "every", "all", "any", "these",
               "both", "neither", "no", "many"]
MODAL = ["will", "may", "would", "can", "could", "should", "must",
         "ought", "might"]
CONJUNCTIONS = ["and", "but", "or", "plus", "yet", "nor"]
INTERROGATIVE_PRONOUNS = ["who", "what", "where", "how", "when"]
PERSONAL_PRONOUNS = ["her", "his", "their", "its", "our", "their",
                     "mine"]
AUXILIARY_VERBS = ["is", "am", "are", "was", "were", "has", "have",
                   "had", "be"]


###Used directly in Voice implementation:
##############################
SIMPLEMARKUP_MAP = {"^": ("prom", True)}      #word prominence tag
REM_SIMPLEMARKUP_RE = re.compile("[%s]" % re.escape("".join(SIMPLEMARKUP_MAP.keys())))


GPOS = dict([(word, "prep") for word in PREPOSITIONS] +
            [(word, "det") for word in DETERMINERS] +
            [(word, "md") for word in MODAL] +
            [(word, "cc") for word in CONJUNCTIONS] +
            [(word, "wp") for word in INTERROGATIVE_PRONOUNS] + 
            [(word, "pps") for word in PERSONAL_PRONOUNS] +
            [(word, "aux") for word in AUXILIARY_VERBS])


#Only difference between this and the implementation in "default" is
#that num_expanded words are not labelled as "english" lang.
def simple_langclass_words(owner, utt, args=None):
    char_threshold = 3 #if words longer than this occur in "other" pronun resources, then label as such
    for word in utt.get_relation("Word"):
        if word["lang"] is not None: #already set?
            continue
        for lang in [k for k in owner.pronun.keys() if k != "main"]: #other languages according to available resources
            if len(word["name"]) > char_threshold:
                if not (word["name"] in owner.pronun["main"]["pronundict"] or word["name"] in owner.pronun["main"]["pronunaddendum"]):
                    if (word["name"] in owner.pronun[k]["pronundict"] or word["name"] in owner.pronun[k]["pronunaddendum"]):
                        word["lang"] = k
    return utt

class Voice(DefaultVoice):
    pass

Voice.SIMPLEMARKUP_MAP = SIMPLEMARKUP_MAP
Voice.REM_SIMPLEMARKUP_RE = REM_SIMPLEMARKUP_RE
Voice.GPOS = GPOS
Voice.langclass_words = simple_langclass_words

if __name__ == "__main__":
    from ttslab.lang.englishZA import Voice
    v = Voice()
    u = v.synthesize("I ask on 2009-11-12, at 20:41 in my report (A32X05 with a cost of R33.27) 3870 times and more: How does one say good-bye in ^Afrikaans?", "text-to-words")
    print(u)
