# -*- coding: utf-8 -*-
"""This file contains specialised implementations the "New" NTTS
   project voice implementations.

   This gets imported into zulu.py (Voice definition is there).
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys, re

PARSE_RE = re.compile("^(.*?){(.*?)}(.*?)$")

OFFSETS = set("aeiounm") #to fix splitting of orthography to be syllable-friendly

#Does expansions according to a few standard functions connected to
#the voice, we defer language classification to the "langclass"
#processor, with the exception of applying the meaning of
#simplemarkup.
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
            gposlist = ["c"] * len(tokentextlist)
        elif token["class"] == "date":
            tokentextlist = owner.FUNCS["date_to_words"](tokentext, owner.FUNCS["num_expand"])
            gposlist = ["c"] * len(tokentextlist)
        elif token["class"] == "time":
            tokentextlist = owner.FUNCS["time_to_words"](tokentext, owner.FUNCS["num_expand"], owner.FUNCS["letters_to_words"])
            gposlist = ["c"] * len(tokentextlist)
        elif token["class"] == "currency":
            tokentextlist = owner.FUNCS["curr_to_words"](owner.NORM_CURR_RE.match(tokentext), owner.FUNCS["num_expand"]).split()
            gposlist = ["c"] * len(tokentextlist)
        elif token["class"] == "float":
            tokentextlist = owner.FUNCS["float_to_words"](tokentext, owner.FUNCS["num_expand"])
            gposlist = ["c"] * len(tokentextlist)
        elif token["class"] == "integer":
            tokentextlist = owner.FUNCS["num_expand"](int(tokentext)).split()
            gposlist = ["c"] * len(tokentextlist)
        else:
            if "|" in tokentext:
                tokentextlist = [tokentext]
                gposlist = ["c"]
            else: #Assume that all the above refers to "foreign lang"
                #Here: split all Zulu words using morph "stemmer" (or dict) and mark "content/function" distinction immediately
                try:
                    parse = owner.morphdict[tokentext]
                except KeyError:
                    parse = owner.morphparser.parse_word_simple(tokentext)[0]
                if not "{" in parse:
                    tokentextlist = [tokentext]
                    gposlist = ["nc"]
                else:
                    #print(parse)
                    tokentextlist = []
                    gposlist = []
                    d = {0: "nc", 1: "c", 2: "nc"}
                    p = list(PARSE_RE.search(parse).groups())
                    for i in range(2):
                        while p[i]:
                            if p[i][-1] not in OFFSETS and p[i+1]:
                                p[i+1] = p[i][-1] + p[i+1]
                                p[i] = p[i][:-1]
                            else:
                                break
                    for i, t in enumerate(p):
                        if t:
                            tokentextlist.append(t)
                            gposlist.append(d[i])
        for wordname, gpos in zip(tokentextlist, gposlist):
            word_item = word_rel.append_item()
            word_item["gpos"] = gpos
            if wordname[0] in owner.SIMPLEMARKUP_MAP:
                word_item[owner.SIMPLEMARKUP_MAP[wordname[0]][0]] = owner.SIMPLEMARKUP_MAP[wordname[0]][1]
                word_item["name"] = wordname[1:]
            else:
                word_item["name"] = wordname
            token.add_daughter(word_item)
    return utt
