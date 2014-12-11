#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Default text processing stuff. The DefaultVoice implementation
   serves as a template to illustrate the intended use of utterance
   processors etc. and structures/interfaces assumed by a number of
   tools and code in TTSLab.

   The idea is that each language's text-processing frontend can take
   the generic fields and implementations from here and _compose_ its
   own implementation from the Voice class, or just inherit from
   DefaultVoice if so desired.

   There should no longer be Voice interface differences because of
   the backend used.

   The new DefaultVoice implementation draws on experience from
   processing Yoruba and real word text, important steps added:

    -- Text standardisation (unicode encoding and punctuation).

    -- Separating orthographic aspects involved in phoneme prediction
       and original forms which may contain diacritics indicating
       other information (such as tone).

    -- Handle code switching!

    -- Parsing lightweight markup for language and prosodic cues.

    -- Incorporate character normalisation, number expansion, and
       token splitting in modular fashion.

    -- Compound splitting may be implemented as an UttProcessor
       operating on traditional "Word" relation, moving it and
       creating a new "Word" relation.
"""

from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys
import re
import unicodedata

#not in standard library:
import dateutil.parser

from ttslab.voice import Voice
from ttslab.g2p import NoRuleFound, GraphemeNotDefined
from ttslab.uttprocessor import UttProcessor

from ttslab.lang.english_numexp import expand as NUM_EXPAND

############################## THESE SHOULD ALL BE ATTACHED TO THE VOICE CLASS TO BE USED
VALID_GRAPHS = set("abcdefghijklmnopqrstuvwxyz'") #specify only lowercase NFC -- used for pronunciation/language determination
VALID_PUNCTS = set('".,:;!?(){}[]-')
PHRASEBREAK_PUNCTS = set("!?.,:;)")
PHRASEBREAK_TOKENS = set()
#translation table for non-standard punct characters
inchars = "–”“’‘`"
outchars = "-\"\"'''"
PUNCT_TRANSTABLE = dict((ord(inchar), ord(outchar)) for inchar, outchar in zip(inchars, outchars))
####
GPOS = {} #this will have to be defined per language (see afrikaans.py
          #implementation), at this point it only seems sensible for
          #the primary language.
####
SIMPLEMARKUP_MAP = {"|": ("lang", "englishZA"), #word language tag
                    "^": ("prom", True)}      #word prominence tag
REM_SIMPLEMARKUP_RE = re.compile("[%s]" % re.escape("".join(SIMPLEMARKUP_MAP.keys())))
####
TOKENPREP_DATE_RE = re.compile(r"(^|[^0-9\-/]+\s*)\b([0-9]+)\s*[-/]+\s*([0-9]+)\s*[-/]+\s*([0-9]+)\b(\s*[^0-9\-/]+|$)")
TOKENPREP_TIME_RE = re.compile(r"\b([0-9]+)\s*([h:])\s*([0-9]{2})(\s*am|\s*pm)?\b", re.IGNORECASE)
TOKENPREP_CURR_RE = re.compile(r"\b(A\$|NZ\$|\$|R|£|¥|€)\s+([0-9]+|[0-9]+\.[0-9]{2})\b", re.IGNORECASE)
####
TOKENCLASS_DATE_RE = re.compile(r"^[0-9]+\s*[-/]+\s*[0-9]+\s*[-/]+\s*[0-9]+$")
TOKENCLASS_TIME_RE = re.compile(r"(^[0-9]+[h:][0-9]{2})(|am|pm)$", re.IGNORECASE)
TOKENCLASS_CURR_RE = re.compile(r"^(A\$|NZ\$|\$|R|£|¥|€)([0-9]+|[0-9]+\.[0-9]{2})$", re.IGNORECASE)
TOKENCLASS_FLOAT_RE = re.compile(r"^[0-9]+\.[0-9]+$")
####
NORM_CURR_RE = re.compile(r"^(A\$|NZ\$|\$|R|£|¥|€)([0-9]+)(\.[0-9]{2})?$", re.IGNORECASE)

#Will overwrite for Yoruba, remove tone-bearing diacritics... also for
#Afrikaans remove acute accent diacritic
def CHAR_NORM(token):
    #text standardiser does NFKD so that we can process all diacritics
    #etc. as separate characters, but all our pronun resources will be
    #lowercased NFC:
    return unicodedata.normalize("NFC", token.lower())

def FLOAT_TO_WORDS(f, num_expand):
    w = []
    for c in f:
        if c == ".":
            w.append("point")
        else:
            w.append(num_expand(int(c)))
    return w

def CURR_TO_WORDS(m, num_expand):
    template = {"r": "%(curr)s rand %(cents)s",
                "$": "%(curr)s dollar %(cents)s",
                "£": "%(curr)s pound %(cents)s",
                "€": "%(curr)s euro %(cents)s",
                "¥": "%(curr)s yen %(cents)s",
                "a$": "%(curr)s australian dollar %(cents)s",
                "nz$": "%(curr)s new zealand dollar %(cents)s"}
    groups = m.groups()
    denom = groups[0]
    d = {"curr": num_expand(int(groups[1]))}
    if groups[2]:
        i = int(groups[2][1:])
        if i:
            d["cents"] = "%s cents" % num_expand(i)
        else:
            d["cents"] = ""
    else:
        d["cents"] = ""
    return template[denom] % d

def LETTERS_TO_WORDS(tokentext):
    l = []
    for i, c in enumerate(tokentext):
        l.append("char_" + "_".join(unicodedata.name(c).lower().split()))
        # if i < len(tokentext) - 1:
        #     l.append("char_pause")
    return l

def DATE_TO_WORDS(tokentext, num_expand):
    months = {1: "january",
              2: "february",
              3: "march",
              4: "april",
              5: "may",
              6: "june",
              7: "july",
              8: "august",
              9: "september",
              10: "october",
              11: "november",
              12: "december"}
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
        noon = "noon"
    elif datetime.hour == 0 and datetime.minute == 0:
        noon = "midnight"
    elif datetime.hour >= 12:
        noon = " ".join(letters_to_words("pm"))
    else:
        noon = " ".join(letters_to_words("am"))
    if datetime.minute == 0:
        hour = (datetime.hour) % 12
        if hour == 0:
            hour = 12        
        time = "%(hour)s o'clock %(noon)s" % {"hour": num_expand(hour), "noon": noon}
    elif datetime.minute == 30:
        hour = (datetime.hour) % 12
        if hour == 0:
            hour = 12                
        time = "half past %(hour)s %(noon)s" % {"hour": num_expand(hour), "noon": noon}
    elif datetime.minute > 30:
        hour = (datetime.hour + 1) % 12
        if hour == 0:
            hour = 12
        time = "%(mins)s minutes to %(hour)s %(noon)s" % {"mins": num_expand(60 - datetime.minute),
                                                          "hour": num_expand(hour),
                                                          "noon": noon}
    else:
        hour = datetime.hour % 12
        if hour == 0:
            hour = 12
        time = "%(mins)s minutes past %(hour)s %(noon)s" % {"mins": num_expand(datetime.minute),
                                                            "hour": num_expand(hour),
                                                            "noon": noon}
    return time.split()

##############################

def remove_control_characters(s):
    return "".join(c for c in s if unicodedata.category(c)[0] != "C")

############################## UTTERANCE PROCESSORS
def standardise_text(owner, utt, args=None):
    """Various simple tests and transformations to ensure we are working
       with "clean" unicode...
    """
    punct_transtable = args
    assert type(utt["inputtext"]) is unicode
    text = remove_control_characters(utt["inputtext"])
    text = unicodedata.normalize("NFKD", text) #decompose unicode (with compatibility transform -- also normalises ligatures)
    if punct_transtable:
        text = text.translate(punct_transtable) #normalise some pesky punctuation characters
    utt["text"] = text
    return utt


def whitespace_tokenize_text(owner, utt, args):
    """ Simplest whitespace-based tokenizer...
    """
    valid_puncts, remmarkup_re, simplemarkup_map = args
    #First try to detect some whitespace separated tokens and fix
    #(remove extraneous whitespace) with regexes
    text = owner._prep_text(utt["text"])
    #split tokens and punctuation
    rawtokens = text.split()
    token_rel = utt.new_relation("Token")
    for rawtoken in rawtokens:
        if ((rawtoken[0] in valid_puncts) or
            (rawtoken[-1] in valid_puncts)):
            prepunct = []
            postpunct = []
            while (rawtoken and
                   (rawtoken[0] in valid_puncts or
                    rawtoken[-1] in valid_puncts)):
                if rawtoken[0] in valid_puncts:
                    prepunct.insert(0, rawtoken[0])
                    rawtoken = rawtoken[1:]
                if rawtoken and rawtoken[-1] in valid_puncts:
                    postpunct.insert(0, rawtoken[-1])
                    rawtoken = rawtoken[:-1]
        else:
            prepunct = None
            postpunct = None
        #if anything left, add to token_rel (means tokens consisting only of punctuation will be overlooked):
        if rawtoken:
            tokenclass = owner._classify_token(rawtoken, remmarkup_re)                  #check if class already recognisable
            if tokenclass in ["default"]:                                               #if not, split further
                tokens = owner._split_token(rawtoken, simplemarkup_map.keys())
            else:
                tokens = [rawtoken]
            for i, token in enumerate(tokens):
                item = token_rel.append_item()
                item["name"] = token
                item["class"] = owner._classify_token(token, remmarkup_re)              #classify final found token
                if i == 0 and prepunct:
                    item["prepunc"] = prepunct
                if i == (len(tokens) - 1) and postpunct:
                    item["postpunc"] = postpunct
    return utt


class DefaultTokenizer(UttProcessor):
    """Simple tokenizer based on whitespace splitting...

       Searches for know regexes before splitting to avoid separating
       some related tokens and applies regexes for simple known
       patterns to classify tokens into a few simple types...
    """

    def _prep_text(self, text):
        text = self.TOKENPREP_DATE_RE.sub("\\1\\2-\\3-\\4\\5", text)
        text = self.TOKENPREP_TIME_RE.sub(lambda m: "".join([e.strip() for e in m.groups() if e]), text) #python3 re simplifies this
        text = self.TOKENPREP_CURR_RE.sub("\\1\\2", text)
        return text

    #In Nguni languages we will also split on token-internal capitals...
    def _split_token(self, token, simplemarkupchars):
        """Function that may be defined to further split (default) tokens that
           have not been handled as other classes... For this simple
           implementation, we split on dashes and any token-internal
           markup characters...
        """
        splitchars = "-" + "".join(simplemarkupchars)
        temp = token
        temp = re.sub(r"(.)([%s])(.)" % re.escape(splitchars), "\\1 \\2\\3", temp, flags=re.UNICODE)
        temp = temp.replace("-", "")
        return temp.split()

    def _classify_token(self, token, remmarkup):
        """Rule-based token class assignment...
           Classes are: DATE, TIME, FLOAT, INTEGER, CURRENCY, LETTERS,
           DEFAULT
        """
        text = remmarkup.sub("", token) #temporarily ignore markup characters
        #Assign token class by matching regular expression:
        if self.TOKENCLASS_DATE_RE.match(text):
            tokenclass = "date"
        elif self.TOKENCLASS_TIME_RE.match(text):
            tokenclass = "time"
        elif self.TOKENCLASS_CURR_RE.match(text):
            tokenclass = "currency"
        elif self.TOKENCLASS_FLOAT_RE.match(text):
            tokenclass = "float"
        elif text.isdigit():
            tokenclass = "integer"
        elif len(text) > 1 and text.isupper():
            tokenclass = "letters"
        else:
            tokenclass = "default"
        return tokenclass

    def process(self, voice, utt, args=None):
        utt = self.tokenize_text(utt, args=(voice.VALID_PUNCTS, voice.REM_SIMPLEMARKUP_RE, voice.SIMPLEMARKUP_MAP))
        return utt

DefaultTokenizer.TOKENPREP_DATE_RE = TOKENPREP_DATE_RE
DefaultTokenizer.TOKENPREP_TIME_RE = TOKENPREP_TIME_RE
DefaultTokenizer.TOKENPREP_CURR_RE = TOKENPREP_CURR_RE
DefaultTokenizer.TOKENCLASS_DATE_RE = TOKENCLASS_DATE_RE
DefaultTokenizer.TOKENCLASS_TIME_RE = TOKENCLASS_TIME_RE
DefaultTokenizer.TOKENCLASS_CURR_RE = TOKENCLASS_CURR_RE
DefaultTokenizer.TOKENCLASS_FLOAT_RE = TOKENCLASS_FLOAT_RE
DefaultTokenizer.tokenize_text = whitespace_tokenize_text


#Does expansions according to a few standard functions connected to
#the voice, we defer language classification to the "langclass"
#processor, with the exception of applying the meaning of
#simplemarkup. Will overwrite for Afrikaans, handling acute accent to
#set prominence...
def normalize_tokens(owner, utt, args=None):
    """Simple "normalization": conversion/expansion of tokens into "words"
       these are not necessarily strict (linguistic) words but defined
       in terms of what is useful for the TTS pronunciation
    """
    word_rel = utt.new_relation("Word")
    for token in utt.get_relation("Token"):
        tokentext = owner.FUNCS["char_norm"](token["name"])
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
            token.add_daughter(word_item)
    return utt


def simple_gpostag_words(owner, utt, args=None):
    """Simple function to label words based on their "guessed
       part-of-speech" (idea from the Festival System). In this
       simplest implementation, we simply use it to try and
       distinguish "content words" and "grammatical words".
    """
    for word_item in utt.get_relation("Word"):
        if word_item["name"] in owner.GPOS:
            word_item["gpos"] = "nc"
        else:
            word_item["gpos"] = "c"
    return utt

def simple_langclass_words(owner, utt, args=None):
    """Use simple heuristics to determine the word item's language. For
       the default voice we assume all number expansion and unknowns
       are English.
    """
    char_threshold = 4 #if words longer than this occur in other pronun resources, then label as such
    for word in utt.get_relation("Word"):
        parent_token = word.get_item_in_relation("Token").parent_item
        if word["lang"] is not None: #already set?
            continue
        if parent_token["class"] in ["currency", "float", "integer", "date", "time"]:
            word["lang"] = "englishZA"
            continue
        if not set(word["name"]).issubset(owner.VALID_GRAPHS): #valid orthography?
            word["lang"] = "englishZA"
            continue
        for lang in [k for k in owner.pronun.keys() if k != "main"]: #other languages according to available resources
            if len(word["name"]) > char_threshold:
                if not (word["name"] in owner.pronun["main"]["pronundict"] or word["name"] in owner.pronun["main"]["pronunaddendum"]):
                    if (word["name"] in owner.pronun[k]["pronundict"] or word["name"] in owner.pronun[k]["pronunaddendum"]):
                        word["lang"] = k
    return utt

def word_to_phones(word_item, phoneset, pronunaddendum, pronundict, g2p, syllabify_func, syltonestress_func):
    """Process of lookup in dictionaries, g2p and syllabification and
       determination of syllable stress/tone... we just call it "tone"
    """
    syltones = None #also for "sylstress"
    syllables = None
    if pronunaddendum and pronunaddendum.contains(word_item["name"]):
        phones = pronunaddendum.pron_lookup(word_item["name"]) #DEMITASSE: assumed simple for now...
    else:
        if pronundict.contains(word_item["name"], word_item["pos"]): #with POS?
            syllables = pronundict.syll_lookup(word_item["name"], word_item["pos"]) #try: might return None
            syltones = pronundict.tone_lookup(word_item["name"], word_item["pos"])  #try: might return None
            if not syllables:
                phones = pronundict.pron_lookup(word_item["name"], word_item["pos"])
        elif pronundict.contains(word_item["name"]):            #without POS?
            syllables = pronundict.syll_lookup(word_item["name"]) #try: might return None
            syltones = pronundict.tone_lookup(word_item["name"])  #try: might return None
            if not syllables:
                phones = pronundict.pron_lookup(word_item["name"])
        else:  #word not in pronundict
            try:
                phones = g2p.predict_word(word_item["name"])
            except (GraphemeNotDefined, NoRuleFound):
                warns = "WARNING: No pronunciation found for '%s'" % word_item["name"]
                print(warns.encode("utf-8"), file=sys.stderr)
                phones = [phoneset.features["silence_phone"]]
    if not syllables:
        syllables = syllabify_func(phones)
    if not syltones:
        if "tone" in word_item and len(word_item["tone"]) == len(syllables):
            syltones = word_item["tone"]
        else:
            syltones = syltonestress_func(word_item, syllables)
    word_item["tone"] = syltones #save finally agreed upon tone also in word item (will overwrite previous -- determined from orth -- if relevant)
    return syllables, syltones

def phonetize_words(owner, utt, args=None):
    syl_rel = utt.new_relation("Syllable")
    sylstruct_rel = utt.new_relation("SylStructure")
    seg_rel = utt.new_relation("Segment")
    for word_item in utt.get_relation("Word"):
        #determine pronun resources for this word
        if word_item["lang"]:
            pronun_resources = owner.pronun[word_item["lang"]]
        else:
            pronun_resources = owner.pronun["main"]
        #determine syllabify and tone/stress back-off funcs
        syllabify_func = pronun_resources["phoneset"].syllabify
        if "guess_syltonestress" in owner.FUNCS:
            syltonestress_func = owner.FUNCS["guess_syltonestress"]
        else:
            syltonestress_func = pronun_resources["phoneset"].guess_syltonestress
        #convert
        syllables, syltones = word_to_phones(word_item,
                                             pronun_resources["phoneset"],
                                             pronun_resources["pronunaddendum"],
                                             pronun_resources["pronundict"],
                                             pronun_resources["g2p"],
                                             syllabify_func,
                                             syltonestress_func)
        #rename phones:
        if word_item["lang"] and word_item["lang"] != "main":
            for syl in syllables:
                for i in range(len(syl)):
                    syl[i] = "_".join([word_item["lang"], syl[i]])
        #add new items to new relations:
        word_item_in_sylstruct = sylstruct_rel.append_item(word_item)
        for syl, syltone in zip(syllables, syltones):
            syl_item = syl_rel.append_item()
            syl_item["name"] = "syl"
            syl_item["tone"] = syltone
            syl_item_in_sylstruct = word_item_in_sylstruct.add_daughter(syl_item)
            for phone in syl:
                seg_item = seg_rel.append_item()
                seg_item["name"] = phone
                seg_item_in_sylstruct = syl_item_in_sylstruct.add_daughter(seg_item)
    return utt

def phrasify_words(owner, utt, args=None):
    """Determine phrase breaks between words (breathgroups) based on
       punctuation...
    """
    word_rel = utt.get_relation("Word")
    pb_punct = owner.PHRASEBREAK_PUNCTS
    pb_toks = owner.PHRASEBREAK_TOKENS
    phrase_rel = utt.new_relation("Phrase")
    phrase_item = phrase_rel.append_item()
    phrase_item["name"] = "BB"
    for word_item in word_rel:
        phrase_item.add_daughter(word_item)
        token_item = word_item.get_item_in_relation("Token").parent_item
        if word_item.get_item_in_relation("Token") is token_item.last_daughter:
            if "postpunc" in token_item:
                postpunk = token_item["postpunc"] #postpunk! :-)
                if word_item is not word_rel.tail_item and pb_punct.intersection(postpunk):
                    phrase_item = phrase_rel.append_item()
                    phrase_item["name"] = "BB"
                    continue
            if token_item.next_item and token_item.next_item["name"].lower() in pb_toks:
                phrase_item = phrase_rel.append_item()
                phrase_item["name"] = "BB"
                continue
    return utt

def phrasify_segments(owner, utt, args):
    """ Insert pauses in the segment sequence where phrase breaks occur...
    """
    silphone = args
    seg_rel = utt.get_relation("Segment")
    #add pause at start of utterance...
    first_seg = seg_rel.head_item
    pause_item = first_seg.prepend_item()
    pause_item["name"] = silphone

    #add pauses at end of each phrase..
    phr_rel = utt.get_relation("Phrase")
    for phr_item in phr_rel:
        try:
            last_seg = phr_item.last_daughter.get_item_in_relation("SylStructure").last_daughter.last_daughter.get_item_in_relation("Segment")
            pause_item = last_seg.append_item()
            pause_item["name"] = silphone
        except AttributeError:
            print("WARNING: Could not find last segment in phrase...")
            #raise ttslab.SynthesisError("Could not find last segment in phrase...")
    return utt


############################## DefaultVoice implementation
class DefaultVoice(Voice):
    def __init__(self, pronun=None, wavesynth=None):
        Voice.__init__(self)
        #required resources for pronunciation prediction, first key
        #specifies language
        if pronun:
            self.pronun = pronun
            self._make_combined_phonesmaps()
        else:
            self.pronun = {"main": {"phoneset": None,
                                    "g2p": None,
                                    "pronundict": {},
                                    "pronunaddendum": {}},
                           "englishZA": {"phoneset": None,
                                         "g2p": None,
                                         "pronundict": {},
                                         "pronunaddendum": {}}}
            self.phones = None   #a dict: keys (phones) --> values (sets of phone features)
            self.phonemap = None #a dict: keys (phones) --> values (ASCII/HTK/HTS/etc. friendly representations)
        if wavesynth:
            self.wavesynth = wavesynth
        else:
            self.wavesynth = None #Waveform synthesizer utterance processor

    def _make_combined_phonesmaps(self):
        """Call this after assembling pronunciation resources...
        """
        self.phonemap = self.pronun["main"]["phoneset"].map.copy()
        self.phones = self.pronun["main"]["phoneset"].phones.copy()
        for lang in self.pronun:
            if lang != "main":
                self.phonemap.update([(lang + "_" + k, (lang + v).replace("_", "")) for k, v in self.pronun[lang]["phoneset"].map.iteritems()])
                self.phones.update([(lang + "_" + k, v) for k, v in self.pronun[lang]["phoneset"].phones.iteritems()])
                try:
                    assert len(self.phones) == len(self.phonemap)
                except AssertionError:
                    for p in self.phones:
                        if not p in self.phonemap:
                            print("%s not in phonemap" % p, file=sys.stderr)
                    for p in self.phonemap:
                        if not p in self.phones:
                            print("%s not in phones" % p, file=sys.stderr)
                    raise

    def process(self, utt, args):
        processname, synthparms = args
        if not processname in ["text-to-words", "text-to-segments", "text-to-feats", "text-to-wave"]:
            raise Exception("Process not defined in voice: %s", processname)
        if processname in ["text-to-words", "text-to-segments", "text-to-feats", "text-to-wave"]:
            utt = self.standardize_text(utt, args=self.PUNCT_TRANSTABLE)
            utt = self.tokenize_text(utt)
            utt = self.normalize_tokens(utt) #also handles simple markup..
            utt = self.gpostag_words(utt)
            utt = self.langclass_words(utt)
            if hasattr(self, 'decompound_words'):
                utt = self.decompound_words(utt)
            utt = self.phrasify_words(utt)
        if processname in ["text-to-segments", "text-to-feats", "text-to-wave"]:
            utt = self.phonetize_words(utt)
            utt = self.phrasify_segments(utt, args=self.pronun["main"]["phoneset"].features["silence_phone"])
        if processname in ["text-to-feats", "text-to-wave"]:
            utt = self.wavesynth(utt, ("feats", synthparms))
        if processname in ["text-to-wave"]:
            utt = self.wavesynth(utt, ("synth", synthparms))
        return utt

#const data
DefaultVoice.VALID_GRAPHS = VALID_GRAPHS
DefaultVoice.VALID_PUNCTS = VALID_PUNCTS
DefaultVoice.PUNCT_TRANSTABLE = PUNCT_TRANSTABLE
DefaultVoice.SIMPLEMARKUP_MAP = SIMPLEMARKUP_MAP
DefaultVoice.REM_SIMPLEMARKUP_RE = REM_SIMPLEMARKUP_RE
DefaultVoice.NORM_CURR_RE = NORM_CURR_RE
DefaultVoice.PHRASEBREAK_PUNCTS = PHRASEBREAK_PUNCTS
DefaultVoice.PHRASEBREAK_TOKENS = PHRASEBREAK_TOKENS
DefaultVoice.GPOS = GPOS
#funcs
DefaultVoice.FUNCS = {"num_expand": NUM_EXPAND,
                      "char_norm": CHAR_NORM,
                      "float_to_words": FLOAT_TO_WORDS,
                      "curr_to_words": CURR_TO_WORDS,
                      "letters_to_words": LETTERS_TO_WORDS,
                      "date_to_words": DATE_TO_WORDS,
                      "time_to_words": TIME_TO_WORDS}

#uttprocs
DefaultVoice.standardize_text = standardise_text
DefaultVoice.tokenize_text = DefaultTokenizer()
DefaultVoice.normalize_tokens = normalize_tokens
DefaultVoice.gpostag_words = simple_gpostag_words
DefaultVoice.langclass_words = simple_langclass_words
DefaultVoice.phonetize_words = phonetize_words
DefaultVoice.phrasify_words = phrasify_words
DefaultVoice.phrasify_segments = phrasify_segments


if __name__ == "__main__":
    from ttslab.lang.default import DefaultVoice
    v = DefaultVoice()
    u = v.synthesize("Ek vra op 2009-11-12, om 20:41 in my verslag (A32X05 met `n koste van R33.27) 3870 keer en verder: Hoe sê mens |good-|bye in ^Afrikaans?", "text-to-words")
    print(u.gr("Word"))
