# -*- coding: utf-8 -*-
"""This file contains language-specific implementation for an
   Afrikaans voice.

   The idea is that this file contains derived Voice and Phoneset
   implementations. This package ttslab/lang may then also contain
   speaker specific implementations e.g. "afrikaans_SPEAKER.py"
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
import unicodedata

#not in standard library:
import dateutil.parser

from ttslab.lang.afrikaans_numexp import expand as NUM_EXPAND
import ttslab.phoneset
from ttslab.lang.default import DefaultVoice


class Phoneset(ttslab.phoneset.Phoneset):
    """ The clusters and syllabification are ripped from the English
        implementation and should be revisited...
    """
    def __init__(self):
        #syllable_clusters are processed in order, thus a list, not a set...
        self.features = {"name": "Lwazi Afrikaans Phoneset",
                         "syllable_clusters": ["VCV", "VCCV", "VCCCV", "VCCCCV",
                                                "VCGV", "VCCGV", "VCCCGV", "VV"],
                         "wellformed_plosive_clusters": [["p","l"], ["b","l"], ["k","l"], ["g","l"], ["p","r"],
                                                         ["b","r"], ["t","r"], ["d","r"], ["k","r"], ["g","r"],
                                                         ["t","w"], ["d","w"], ["g","w"], ["k","w"]],
                         "wellformed_fricative_clusters": [["f","l"], ["f","r"], ["f","j"], ["ʃ","j"]],
                         "wellformed_other_clusters": [["m","j"], ["n","j"]],
                         "wellformed_s_clusters": [["s","p"], ["s","t"], ["s","k"], ["s","m"], ["s","n"],
                                                   ["s","f"], ["s","w"], ["s","l"], ["s","p","l"],
                                                   ["s","p","r"], ["s","t","r"], ["s","k","l"],
                                                   ["s","k","r"], ["s","k","w"]]
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
                       "əi"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_back"]),
                       "ai"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "œ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front", "articulation_rounded"]),
                       "əu"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "œy"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ɔi"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "ʒ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar", "voiced"]),
                       "æ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ɑː"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_low", "position_back"]),
                       "ɑːi"    : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "iə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_front"]),
                       "øː"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_front", "articulation_rounded"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "iu"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "uə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_back", "articulation_rounded"]),
                       "uəi"    : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "ui"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "x"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar"]),
                       "y"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "paucl":"paucl",
                    "ʔ":"paugs",
                    "ə":"q",       #sin
                    "əi":"qi",     #wyn
                    "a":"a",       #man
                    "ai":"ai",     #katjie
                    "ɛ":"E",       #ken
                    "œ":"qoeq",    #mus
                    "əu":"qu",     #bou
                    "œy":"qoeqy",  #huis
                    "ŋ":"N",       #sing
                    "ɔ":"O",       #son
                    "ɔi":"Oi",     #potjie
                    "ʃ":"S",       #chef
                    "ʒ":"Z",       #mirage
                    "æ":"qaeq",    #ek
                    "ɑː":"AA",     #aan
                    "ɑːi":"AAi",   #saai
                    "b":"b",
                    "d":"d",
                    "iə":"iq",     #seer
                    "øː":"qooq",   #seun
                    "f":"f",
                    "g":"g",
                    "ɦ":"hq",
                    "i":"i",       #sien
                    "iu":"iu",     #meeu
                    "j":"j",
                    "k":"k",
                    "l":"l",
                    "m":"m",
                    "n":"n",
                    "uə":"uq",     #room
                    "uəi":"uqi",   #rooi
                    "p":"p",
                    "r":"r",
                    "s":"s",
                    "t":"t",
                    "tʃ":"tS",     #tjek
                    "u":"u",       #boek
                    "ui":"ui",     #boei
                    "v":"v",       #wens
                    "w":"w",       #twee
                    "x":"x",       #gee
                    "y":"y",       #muur
                    "z":"z"
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
            
            Implementation for English... needs to be revisited...
        """
        phonecluster = phonelist[match.start() : match.end()]

        if cluster == "VCV":
            #always split -> V.CV:
            return "V.CV"

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
            #if CCC are all obstruents -> VC.CCV:
            if all([self.is_obstruent(C) for C in CCC]):
                return "VC.CCV"
            #if C2C3 are wellformed onsets -> VC.CCV:
            if C2C3 in self.features["wellformed_clusters"]:
                return "VC.CCV"
            else:
                return "VCC.CV"

        if cluster == "VCCCCV":
            #always split -> VC.CCCV:
            return "VC.CCCV"

        if cluster == "VCGV":
            CG = phonecluster[1:3]
            if not self.is_plosive(CG[0]):                         #C not a stop
                return "VC.GV"
            else:
                if CG not in self.features["wellformed_clusters"]: #C a stop and CG not wellformed
                    return "VC.GV"
                else:
                    return "V.CGV"                                 #C a stop and CG wellformed

        if cluster == "VCCGV":
            CCG = phonecluster[1:4]
            if CCG[0] == "s":
                return "V.CCGV"
            else:
                return "VC.CGV"

        if cluster == "VCCCGV":
            return "VC.CCGV"

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
        if len(syllables) == 1:                     # monosyllable always stressed
            return "1"                              
        return "0" * len(syllables)                 #implement a "default" soon -- this used for the current experiments


##############################        
###Helper constants:
PREPOSITIONS = ["in", "van", "vir", "op", "daardie", "met",
                "by", "vanaf", "as", "teen", "voor", "onder",
                "na", "oor", "terwyl", "sonder", "dat", "deur",
                "tussen", "per", "af", "langs", "hierdie", "naas"]
DETERMINERS = ["die", "n", "'n", "_n", "geen", "nie", "elke", "nog", "al",
               "enige", "beide", "baie"]
MODAL = ["sal", "wil", "mag", "sou", "wou", "moet", "wees"]
CONJUNCTIONS = ["en", "maar", "omdat", "want", "of"]
INTERROGATIVE_PRONOUNS = ["wie", "wat", "watter", "waar", "hoe", "wanneer", "hoekom"]
PERSONAL_PRONOUNS = ["hy", "haar", "sy", "hulle", "hul", "ons", "syne", "myne", "hare"]
AUXILIARY_VERBS = ["is", "het"]
DEMIT = ["dan", "toe", "nadat", "aan", "voordat", "jy", "u",
         "was", "gewees", "geword", "word", "om", "te", "uit",
         "tydens", "waarin", "se"] #DEMITASSE

###Used directly in Voice implementation:
VALID_GRAPHS = set("abcdefghijklmnopqrstuvwxyz'àèìòùäëïöüâêîôû") #specify only lowercase NFC -- used for pronunciation/language determination

GPOS = dict([(word, "prep") for word in PREPOSITIONS] +
            [(word, "det") for word in DETERMINERS] +
            [(word, "md") for word in MODAL] +
            [(word, "cc") for word in CONJUNCTIONS] +
            [(word, "wp") for word in INTERROGATIVE_PRONOUNS] + 
            [(word, "pps") for word in PERSONAL_PRONOUNS] +
            [(word, "aux") for word in AUXILIARY_VERBS] +
            [(word, "demit") for word in DEMIT])

PHRASEBREAK_TOKENS = set() #set(CONJUNCTIONS)


############################## Afrikaans voice frontend implementation
COMBINING_ACUTE = "\u0301"
def CHAR_NORM(token):
    #text standardiser does NFKD so that we can process all diacritics
    #etc. as separate characters, but all our pronun resources will be
    #lowercased NFC:
    return unicodedata.normalize("NFC", token.lower().replace(COMBINING_ACUTE, ""))

def FLOAT_TO_WORDS(f, num_expand):
    w = []
    for c in f:
        if c == ".":
            w.append("punt")
        else:
            w.append(num_expand(int(c)))
    return w

def CURR_TO_WORDS(m, num_expand):
    template = {"r": "%(curr)s rand %(cents)s",
                "$": "%(curr)s dollar %(cents)s",
                "£": "%(curr)s pond %(cents)s",
                "€": "%(curr)s euro %(cents)s",
                "¥": "%(curr)s jen %(cents)s",
                "a$": "%(curr)s australiese dollar %(cents)s",
                "nz$": "%(curr)s nieu seelandse dollar %(cents)s"}
    groups = m.groups()
    denom = groups[0]
    d = {"curr": num_expand(int(groups[1]))}
    if groups[2]:
        i = int(groups[2][1:])
        if i:
            d["cents"] = "en %s sent" % num_expand(i)
        else:
            d["cents"] = ""
    else:
        d["cents"] = ""
    return template[denom] % d

def DATE_TO_WORDS(tokentext, num_expand):
    months = {1: "januarie",
              2: "februarie",
              3: "maart",
              4: "april",
              5: "mei",
              6: "junie",
              7: "julie",
              8: "augustus",
              9: "september",
              10: "oktober",
              11: "november",
              12: "desember"}
    datetime = dateutil.parser.parse(tokentext, dayfirst=True)
    if datetime.year >= 2000 and datetime.year < 2010:
        year = num_expand(datetime.year)
    else:
        year = " ".join([num_expand(int(str(datetime.year)[:2])), num_expand(int(str(datetime.year)[2:]))])
    month = months[datetime.month]
    day = num_expand(datetime.day)
    return " ".join([day, month, year]).split()

def TIME_TO_WORDS(tokentext, num_expand, letters_to_words):
    datetime = dateutil.parser.parse(tokentext)
    if datetime.hour == 12 and datetime.minute == 0:
        noon = "middag"
    elif datetime.hour == 0 and datetime.minute == 0:
        noon = "middernag"
    elif datetime.hour >= 12:
        noon = "namiddag"
    else:
        noon = "voormiddag"
    if datetime.minute == 0:
        hour = (datetime.hour) % 12
        if hour == 0:
            hour = 12        
        time = "%(hour)s uur %(noon)s" % {"hour": num_expand(hour), "noon": noon}
    elif datetime.minute == 30:
        hour = (datetime.hour + 1) % 12
        if hour == 0:
            hour = 12                
        time = "half %(hour)s %(noon)s" % {"hour": num_expand(hour), "noon": noon}
    elif datetime.minute > 30:
        hour = (datetime.hour + 1) % 12
        if hour == 0:
            hour = 12
        time = "%(mins)s minute voor %(hour)s %(noon)s" % {"mins": num_expand(60 - datetime.minute),
                                                           "hour": num_expand(hour),
                                                           "noon": noon}
    else:
        hour = datetime.hour % 12
        if hour == 0:
            hour = 12
        time = "%(mins)s minute oor %(hour)s %(noon)s" % {"mins": num_expand(datetime.minute),
                                                          "hour": num_expand(hour),
                                                          "noon": noon}
    return time.split()

def normalize_tokens(owner, utt, args=None):
    """Simple "normalization": conversion/expansion of tokens into "words"
       these are not necessarily strict (linguistic) words but defined
       in terms of what is useful for the TTS pronunciation
    """
    word_rel = utt.new_relation("Word")
    for token in utt.get_relation("Token"):
        if COMBINING_ACUTE in token["name"]:
            prominence = True
        else:
            prominence = False
        tokentext = owner.FUNCS["char_norm"](token["name"]) #this now removes acute accents
        if token["class"] == "letters":
            tokentextlist = owner.FUNCS["letters_to_words"](tokentext)
        elif token["class"] == "date":
            tokentextlist = owner.FUNCS["date_to_words"](tokentext, owner.FUNCS["num_expand"])
        elif token["class"] == "time":
            tokentextlist = owner.FUNCS["time_to_words"](tokentext, owner.FUNCS["num_expand"], owner.FUNCS["letters_to_words"])
        elif token["class"] == "currency":
            tokentextlist = owner.FUNCS["curr_to_words"](owner.NORM_CURR_RE.match(tokentext), owner.FUNCS["num_expand"]).split()
        elif token["class"] == "float":
            tokentextlist = owner.FUNCS["float_to_words"](tokentext, owner.FUNCS["num_expand"])
        elif token["class"] == "integer":
            tokentextlist = owner.FUNCS["num_expand"](int(tokentext)).split()
        else:
            tokentextlist = [tokentext]
        for wordname in tokentextlist:
            word_item = word_rel.append_item()
            if wordname[0] in owner.SIMPLEMARKUP_MAP:
                word_item[owner.SIMPLEMARKUP_MAP[wordname[0]][0]] = owner.SIMPLEMARKUP_MAP[wordname[0]][1]
                word_item["name"] = wordname[1:]
            else:
                word_item["name"] = wordname
            if prominence:
                word_item["prom"] = True
            token.add_daughter(word_item)
    return utt

def simple_langclass_words(owner, utt, args=None):
    """Use simple heuristics to determine the word item's language.
    """
    char_threshold = 10 #if words longer than this occur in other pronun resources, then label as such --- a value of 10 here: it is virtually/practically disabled
    for word in utt.get_relation("Word"):
        parent_token = word.get_item_in_relation("Token").parent_item
        if word["lang"] is not None: #already set?
            continue
        if parent_token["class"] in ["currency", "float", "integer", "date", "time"]:
            continue
        for lang in [k for k in owner.pronun.keys() if k != "main"]: #other languages according to available resources
            if len(word["name"]) > char_threshold:
                if not (word["name"] in owner.pronun["main"]["pronundict"] or word["name"] in owner.pronun["main"]["pronunaddendum"]):
                    if (word["name"] in owner.pronun[k]["pronundict"] or word["name"] in owner.pronun[k]["pronunaddendum"]):
                        word["lang"] = k
    return utt


class Voice(DefaultVoice):
    pass 

#const data
Voice.VALID_GRAPHS = VALID_GRAPHS
Voice.GPOS = GPOS
Voice.PHRASEBREAK_TOKENS = PHRASEBREAK_TOKENS
#funcs
Voice.FUNCS["num_expand"] = NUM_EXPAND
Voice.FUNCS["char_norm"] = CHAR_NORM
Voice.FUNCS["float_to_words"] = FLOAT_TO_WORDS
Voice.FUNCS["curr_to_words"] = CURR_TO_WORDS
Voice.FUNCS["date_to_words"] = DATE_TO_WORDS
Voice.FUNCS["time_to_words"] = TIME_TO_WORDS
#uttprocs
Voice.normalize_tokens = normalize_tokens
Voice.langclass_words = simple_langclass_words

if __name__ == "__main__":
    from ttslab.lang.afrikaans import Voice
    v = Voice()
    u = v.synthesize("Ek vra op 2009-11-12, om 20:41 in my verslag (A32X05 met `n koste van R33.27) 3870 keer en verder: Hoe sê mens |good-|bye in Afrikááns?", "text-to-words")
    print(u)
