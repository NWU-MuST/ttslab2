# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...

    DEMITASSE: I have renamed the "syllable stress" feature to "tone"
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab
import ttslab.hrg as hrg
ttslab.extend(hrg.Item, "ttslab.funcs.ifuncs_hts")

NONE_STRING = "xxx"


def float_to_htk_int(string):
    """ Converts a string representing a floating point number to an
        integer (time in 100ns units)...
    """
    try:
        return int(round(float(string)*10000000))
    except:
        print(string)
        raise

def htk_int_to_float(string):
    """ Converts a string representing an integer (time in 100ns units)
        to floating point value (time in seconds)...
    """
    return float(string) / 10000000.0

def nonestring(s):
    if s is None:
        return NONE_STRING
    return s

def zero(s):
    if s is None:
        return 0
    return s

def p(segitem, phonemap):
    
    segitem = segitem.get_item_in_relation("Segment")

    try:
        p1 = phonemap[segitem.traverse("p.p.F:name")]
    except KeyError:
        p1 = None
    try:
        p2 = phonemap[segitem.traverse("p.F:name")]
    except KeyError:
        p2 = None
    #here we allow for symbols to be overridden based on "hts_symbol":
    if "hts_symbol" in segitem:
        p3 = segitem["hts_symbol"]
    else:
        p3 = phonemap[segitem["name"]]
    try:
        p4 = phonemap[segitem.traverse("n.F:name")]
    except KeyError:
        p4 = None
    try:
        p5 = phonemap[segitem.traverse("n.n.F:name")]
    except KeyError:
        p5 = None
    p6 = segitem.segpos_insyl_f()
    p7 = segitem.segpos_insyl_b()

    return "%s^%s-%s+%s=%s@%s_%s" % tuple(map(nonestring, (p1, p2, p3, p4, p5, p6, p7)))


def a(segitem):

    a1 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:tone")
    a2 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:accent")
    a3 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.M:num_daughters()")
    
    return "A:%s_%s_%s" % tuple(map(zero, (a1, a2, a3)))


def b(segitem, phones, phonemap):
    
    b1 = segitem.traverse("R:SylStructure.parent.F:tone")
    b2 = segitem.traverse("R:SylStructure.parent.F:accent")
    b3 = segitem.traverse("R:SylStructure.parent.M:num_daughters()")
    b4 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_f()")
    b5 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_b()")
    b6 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_f()")
    b7 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_b()")
    b8 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('tone', '1')")
    b9 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('tone', '1')")
    b10 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('accent', '1')")
    b11 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('accent', '1')")
    b12 = segitem.traverse("R:SylStructure.parent.M:syldistprev('tone', '1')")
    b13 = segitem.traverse("R:SylStructure.parent.M:syldistnext('tone', '1')")
    b14 = segitem.traverse("R:SylStructure.parent.M:syldistprev('accent', '1')")
    b15 = segitem.traverse("R:SylStructure.parent.M:syldistnext('accent', '1')")

    vowelname = None
    if segitem is not None:
        vowelnames = [ph for ph in phones if "vowel" in phones[ph]]
        sylphones = segitem.traverse("R:SylStructure.parent.M:get_daughters()")
        if sylphones is None:
            pass
        else:
            for phname in [ph["name"] for ph in sylphones]:
                if phname in vowelnames:
                    vowelname = phonemap[phname]
                    break
    b16 = vowelname
    
    return "B:%s-%s-%s@%s-%s&%s-%s#%s-%s$%s-%s!%s-%s;%s-%s|%s" % tuple(map(zero, (b1, b2, b3, b4,
                                                                                  b5, b6, b7, b8,
                                                                                  b9, b10, b11, b12,
                                                                                  b13, b14, b15, b16)))


def c(segitem):

    c1 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:tone")
    c2 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:accent")
    c3 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.M:num_daughters()")
    
    return "C:%s+%s+%s" % tuple(map(zero, (c1, c2, c3)))

    

def d(segitem):

    d1 = segitem.traverse("R:SylStructure.parent.parent.p.F:gpos")
    if d1 is None: d1 = NONE_STRING
    d2 = segitem.traverse("R:SylStructure.parent.parent.p.M:num_daughters()")
    if d2 is None: d2 = 0
    
    return "D:%s_%s" % (d1, d2)


def e(segitem):

    e1 = segitem.traverse("R:SylStructure.parent.parent.F:gpos")
    if e1 is None: e1 = NONE_STRING
    e2 = segitem.traverse("R:SylStructure.parent.parent.M:num_daughters()")
    e3 = segitem.traverse("R:SylStructure.parent.parent.M:wordpos_inphrase_f()")
    e4 = segitem.traverse("R:SylStructure.parent.parent.M:wordpos_inphrase_b()")
    e5 = segitem.traverse("R:SylStructure.parent.parent.M:numwordsbeforeword_inphrase('gpos', 'c')")
    e6 = segitem.traverse("R:SylStructure.parent.parent.M:numwordssafterword_inphrase('gpos', 'c')")
    e7 = segitem.traverse("R:SylStructure.parent.parent.M:worddistprev('gpos', 'c')")
    e8 = segitem.traverse("R:SylStructure.parent.parent.M:worddistnext('gpos', 'c')")
    
    return "E:%s+%s@%s+%s&%s+%s#%s+%s" % tuple(map(zero, (e1, e2, e3, e4, e5, e6, e7, e8)))


def f(segitem):

    f1 = segitem.traverse("R:SylStructure.parent.parent.n.F:gpos")
    if f1 is None: f1 = NONE_STRING
    f2 = segitem.traverse("R:SylStructure.parent.parent.n.M:num_daughters()")
    if f2 is None: f2 = 0
    
    return "F:%s_%s" % (f1, f2)


def g(segitem):

    g1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.p.M:numsyls_inphrase()")
    g2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.p.M:num_daughters()")

    return "G:%s_%s" % tuple(map(zero, (g1, g2)))


def h(segitem):

    h1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:numsyls_inphrase()")
    h2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:num_daughters()")
    h3 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:phrasepos_inutt_f()")
    h4 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:phrasepos_inutt_b()")
    h5 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.F:tobi")
    if h5 is None: h5 = NONE_STRING

    return "H:%s=%s@%s=%s|%s" % tuple(map(zero, (h1, h2, h3, h4, h5)))


def i(segitem):

    i1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.n.M:numsyls_inphrase()")
    i2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.n.M:num_daughters()")

    return "I:%s_%s" % tuple(map(zero, (i1, i2)))


def j(segitem):
    
    utt = segitem.relation.utterance
    
    j1 = len(utt.get_relation("Syllable"))
    j2 = len(utt.get_relation("Word"))
    j3 = len(utt.get_relation("Phrase"))

    return "J:%s+%s-%s" % (j1, j2, j3)
