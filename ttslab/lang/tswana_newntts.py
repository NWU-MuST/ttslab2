# -*- coding: utf-8 -*-
"""This file contains specialised implementations the "New" NTTS
   project voice implementations.

   This gets imported into tswana.py (Voice definition is there).
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys
import re
import unicodedata

from ttslab.lang.default import remove_control_characters

FOREIGN_RE = re.compile("(\|.+?)(?:[\\s]|$)", re.UNICODE)
DIAC_MACRON = "\u0304" #used here to explicitly specify lack of DIAC_CIRCUM
DIAC_CIRCUM = "\u0302"
DIACS = set([DIAC_MACRON, DIAC_CIRCUM])

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
    ### APPLY SETSWANA DIACRITISER:
    ### This currently strips any existing diacritics before starting -- may want to leave in place in future?
    intext = text #save for simple hack below to restore input diacritic patterns on token level
    text = unicodedata.normalize("NFC", text)
    text = owner.diacritiser(text)
    ### HACK: Restore input diacritic patterns (ifon token level
    toks = []
    toksa = intext.split()
    toksb = text.split()
    assert len(toksa) == len(toksb)
    for a, b in zip(toksa, toksb):
        #'a' is still in NFD
        if set(a).intersection(DIACS):
            toks.append(unicodedata.normalize("NFC", a.replace(DIAC_MACRON, "")))
        else:
            toks.append(b)
    text = " ".join(toks)
    ### HACK: Revert possible diacritics for foreign-lang marked-up tokens:
    text = FOREIGN_RE.sub(lambda x: x.group().replace("ê", "e").replace("ô", "o").replace("Ê", "E").replace("Ô", "O"), text)
    utt["text"] = text
    return utt

def simple_postag_words(owner, utt, args=None):
    d = {"CONT": "c", "FUNC": "nc"}
    words = [w["name"].replace("ê", "e").replace("ô", "o") for w in utt.get_relation("Word")]
    tags = owner.postag.tag(words)
    for w, t in zip(utt.get_relation("Word"), tags):
        if w["lang"] is not None and w["lang"] == "englishZA":
            w["gpos"] = "c"
        else:
            w["gpos"] = d[t]
    return utt
