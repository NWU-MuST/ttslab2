# -*- coding: utf-8 -*-
"""This file contains specialised implementations for PRASA 2016
   experiments with the pronundict and G2PS in an Afrikaans voice.

   This get imported into afrikaans.py (Voice definition is there).
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

def word_to_phones(word_item, phoneset, pronunaddendum, pronundict, g2ps, syllabify_func, syltonestress_func):
    """Process of lookup in dictionaries, g2p and syllabification and
       determination of syllable stress/tone... we just call it "tone"
    """
    syltones = None #also for "sylstress"
    syllables = None
    ### Use `pronunaddendum` or `pronundict` --> PD?
    if pronunaddendum and pronunaddendum.contains(word_item["name"]):
        pd = pronunaddendum
    else:
        pd = pronundict
    ### Now look for as much info as possible from PD
    if pd.contains(word_item["name"], word_item["pos"]): #with POS?
        syllables = pd.syll_lookup(word_item["name"], word_item["pos"]) #try: might return None
        syltones = pd.tone_lookup(word_item["name"], word_item["pos"])  #try: might return None
        if not syllables:
            phones = pd.pron_lookup(word_item["name"], word_item["pos"])
    elif pd.contains(word_item["name"]):            #without POS?
        syllables = pd.syll_lookup(word_item["name"]) #try: might return None
        syltones = pd.tone_lookup(word_item["name"])  #try: might return None
        if not syllables:
            phones = pd.pron_lookup(word_item["name"])
    else:  #word not in PD
        try:
            syllables = g2ps.predict_word(word_item["name"])
            print("DEMIT: obtained syllables from G2PS model", file=sys.stderr)
        except Exception as e:
            warns = "WARNING: No pronunciation found for '%s'" % word_item["name"]
            print(warns.encode("utf-8"), file=sys.stderr)
            phones = [phoneset.features["silence_phone"]]
            syllables = [phones]
    ### Fill in additional info not obtained from PD or G2PS
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
                                             pronun_resources["g2ps"],
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
