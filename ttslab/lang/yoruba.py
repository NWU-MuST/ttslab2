# -*- coding: utf-8 -*-
""" Initial phoneset implementation for the Yoruba voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
import unicodedata

import ttslab.phoneset
from ttslab.lang.default import remove_control_characters, DefaultVoice
from ttslab.lang.yoruba_orth2tones import word2tones

class Phoneset(ttslab.phoneset.Phoneset):
    """ Developed for PhD studies, based on Yoruba data received from
        Etienne Barnard...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """
    def __init__(self):
        self.features = {"name": "Yoruba Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "paucl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "paucl"  : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       #vowels
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ã"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front", "articulation_nasalized"]),
                       "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front", "articulation_nasalized"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ĩ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front", "articulation_nasalized"]),
                       "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
#                       "õ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded", "articulation_nasalized"]), 
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ɔ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded", "articulation_nasalized"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "ũ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_nasalized"]),
                       #consonants
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "gb"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "kp"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"])
                       }
        self.map = {"pau"    : "pau",
                    "paucl"  : "paucl",
                    "ʔ"      : "paugs",
                    "a"      : "a",
                    "ã"      : "an",
                    "e"      : "e",
                    "ɛ"      : "E",
                    "ɛ̃"      : "En",
                    "i"      : "i",
                    "ĩ"      : "in",
                    "o"      : "o",
#                    "õ"      : "on",
                    "ɔ"      : "O",
                    "ɔ̃"      : "On",
                    "u"      : "u",
                    "ũ"      : "un",
                    "b"      : "b",
                    "d"      : "d",
                    "dʒ"     : "dZ",
                    "f"      : "f",
                    "g"      : "g",
                    "gb"     : "gb",
                    "h"      : "h",
                    "j"      : "j",
                    "k"      : "k",
                    "kp"     : "kp",
                    "l"      : "l",
                    "m"      : "m",
                    "n"      : "n",
                    "r"      : "r",
                    "s"      : "s",
                    "t"      : "t",
                    "ʃ"      : "S",
                    "w"      : "w"
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
            try:
                nphone = phlist[1]
                nnphone = phlist[2]
                #Syllabic consonant followed by C:
                if (self.is_syllabicconsonant(phone) and
                    self.is_consonant(nphone)):
                    #sC.C
                    sylls[-1].append(phlist.pop(0))
                    if phlist: sylls.append([])
                    continue
                ##DEMITASSE: Yoruba doesn't seem to have these:
                ##########
                # #If there is a three phone cluster:
                # if (self.is_vowel(phone) and
                #     not self.is_vowel(nphone) and
                #     not self.is_vowel(nnphone)):
                #     #VC.C
                #     sylls[-1].append(phlist.pop(0))#phone
                #     sylls[-1].append(phlist.pop(0))#nphone
                #     if phlist: sylls.append([])
                #     continue
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

##############################        
###Helper constants:
CONJUNCTIONS = ["ẹyin", "ati", # both,and
                "sibẹ-sibẹ", "sibẹsibẹ", "afi", "ṣugbọn", #but
                "fun", "nitori",#for,because
#                "ni", "to", "ri", #for,because
                "boya", "tabi", "yala", #either/or/nor
                "pẹlu", "jubẹlọ", #yet,although
#                "bi", "o", "ti", "lẹ", "jẹ", "pe", #yet,although
                "lati", "lẹhin", "igbati",  # since
                "titi", #until
                "akoko" #while
                ] #Unicode NFC form
GPOS = dict([(word, "cc") for word in CONJUNCTIONS])

COMBINING_GRAVE = "\u0300"
COMBINING_ACUTE = "\u0301"
COMBINING_UNDOT = "\u0323"
COMBINING_DIACRITICS = [COMBINING_GRAVE, COMBINING_ACUTE, COMBINING_UNDOT]

###Used directly in Voice implementation:
VALID_GRAPHS = "abdeẹfghijklmnoọprsṣtuwy'"

PHRASEBREAK_TOKENS = set(CONJUNCTIONS)

############################## Yoruba voice frontend implementation

def CHAR_NORM(token):
    #character normaliser does NFKD so that we can process all
    #diacritics etc. as separate characters, but all our pronun
    #resources will be lowercased NFC:
    return unicodedata.normalize("NFC", token.lower().replace(COMBINING_ACUTE, "").replace(COMBINING_GRAVE, ""))


############################## UTTERANCE PROCESSORS
def standardise_text(owner, utt, args=None):
    """Various simple tests and transformations to ensure we are working
       with "clean" unicode... For Yoruba we also try to clean out
       dangling combining diacritics.
    """
    punct_transtable = args
    assert type(utt["inputtext"]) is unicode
    text = remove_control_characters(utt["inputtext"])
    text = unicodedata.normalize("NFKD", text) #decompose unicode (with compatibility transform -- also normalises ligatures)
    text = re.sub(u"\\s+([%s])" % COMBINING_DIACRITICS, "\\1", text) #no combining diacritics after whitespace -- fix...
    for c in COMBINING_DIACRITICS:
        text = text.replace("%s%s" % (c, c), c)                #no duplicate diacritics -- fix...
    if punct_transtable:
        text = text.translate(punct_transtable) #normalise some pesky punctuation characters
    utt["text"] = text
    return utt

# Does expansions according to a few standard functions connected to
# the voice, we defer language classification to the "langclass"
# processor, with the exception of applying the meaning of
# simplemarkup.
#
# The Yoruba implementation differs in that it tries to determine
# tones from diacritics during normalisation, this is then carried
# forward as word_item["tone"] and ultimately accepted or overruled
# during pronunciation lookup which operates on NFC without accent
# diacritics..
def normalize_tokens(owner, utt, args=None):
    """Simple "normalization": conversion/expansion of tokens into "words"
       these are not necessarily strict (linguistic) words but defined
       in terms of what is useful for the TTS pronunciation
    """
    word_rel = utt.new_relation("Word")
    for token in utt.get_relation("Token"):
        tokentext = owner.FUNCS["char_norm"](token["name"])
        nfkd_tokentext = None
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
            nfkd_tokentext = token["name"].lower() #original assumed to be NFKD (standardise input does this)
        for wordname in tokentextlist:
            word_item = word_rel.append_item()
            if nfkd_tokentext:
                word_item["tone"] = word2tones(nfkd_tokentext)
            if wordname[0] in owner.SIMPLEMARKUP_MAP:
                word_item[owner.SIMPLEMARKUP_MAP[wordname[0]][0]] = owner.SIMPLEMARKUP_MAP[wordname[0]][1]
                word_item["name"] = wordname[1:]
            else:
                word_item["name"] = wordname
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


############################## 
class Voice(DefaultVoice):
    pass

#const data
Voice.VALID_GRAPHS = VALID_GRAPHS
Voice.PHRASEBREAK_TOKENS = PHRASEBREAK_TOKENS
Voice.GPOS = GPOS
#funcs
Voice.FUNCS["char_norm"] = CHAR_NORM
#uttprocs
Voice.standardise_text = standardise_text
Voice.normalize_tokens = normalize_tokens
Voice.langclass_words = simple_langclass_words

#override previous default tokenizer's:
Voice.tokenize_text.FUNCS = {"char_norm": CHAR_NORM}


if __name__ == "__main__":
    from ttslab.lang.yoruba import Voice
    v = Voice()
    u = v.synthesize("nítorí nípa ìgbàgbọ́ ni àwa ń rìn, kì í ṣe nípa ohun tí a rí.", "text-to-words")
    print(u)

