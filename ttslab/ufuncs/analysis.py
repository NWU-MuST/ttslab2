# -*- coding: utf-8 -*-
"""Implements functions used to analyse utterances
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"


def fill_startendtimes(utt):
    """ Use 'end' time feature in segments to fill info for other
        items in other common relations..
    """
    #segments (are contiguous in time)...
    currtime = 0.0
    for seg_item in utt.get_relation("Segment"):
        seg_item["start"] = currtime
        currtime = seg_item["end"]

    for syl_item in utt.get_relation("Syllable"):
        syl_item["start"] = syl_item.get_item_in_relation("SylStructure").first_daughter["start"]
        syl_item["end"] = syl_item.get_item_in_relation("SylStructure").last_daughter["end"]

    for word_item in utt.get_relation("Word"):
        word_item["start"] = word_item.get_item_in_relation("SylStructure").first_daughter["start"]
        word_item["end"] = word_item.get_item_in_relation("SylStructure").last_daughter["end"]

    for phrase_item in utt.get_relation("Phrase"):
        phrase_item["start"] = phrase_item.first_daughter["start"]
        phrase_item["end"] = phrase_item.last_daughter["end"]
