# -*- coding: utf-8 -*-
"""Functions to create HTS labels for synthesis...  We override some
   of the "standard" sets of features here to exclude phrase and
   utterance context (only up to the word level)
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from ttslab.synthesizers.hts_labels import NONE_STRING, float_to_htk_int, htk_int_to_float, nonestring, zero

def p(segitem, phonemap):
    def map_or_not(p):
        try:
            return phonemap[p]
        except KeyError:
            if p is not None:
                print("hts_labels*.py: WARNING: phone name not mapped: '{}'".format(p).encode("utf-8"), file=sys.stderr)
        return p

    def in_word_to_feat_or_none(p, feat, w):
        if p is not None:
            pword = p.traverse("R:SylStructure.parent.parent")
            if pword is w:
                return p[feat]
        return None

    worditem = segitem.traverse("R:SylStructure.parent.parent")

    if worditem is None:
        p1 = segitem.traverse("p.p.F:name")
        p2 = segitem.traverse("p.F:name")
        #here we allow for symbols to be overridden based on "hts_symbol":
        if "hts_symbol" in segitem:
            p3 = segitem["hts_symbol"]
        else:
            p3 = segitem["name"]
        p4 = segitem.traverse("n.F:name")
        p5 = segitem.traverse("n.n.F:name")
    else:
        p1 = in_word_to_feat_or_none(segitem.traverse("p.p"), "name", worditem)
        p2 = in_word_to_feat_or_none(segitem.traverse("p"), "name", worditem)
        #here we allow for symbols to be overridden based on "hts_symbol":
        if "hts_symbol" in segitem:
            p3 = segitem["hts_symbol"]
        else:
            p3 = segitem["name"]
        p4 = in_word_to_feat_or_none(segitem.traverse("n"), "name", worditem)
        p5 = in_word_to_feat_or_none(segitem.traverse("n.n"), "name", worditem)
    p6 = segitem.segpos_insyl_f()
    p7 = segitem.segpos_insyl_b()

    return "%s^%s-%s+%s=%s@%s_%s" % (tuple(map(nonestring, map(map_or_not, (p1, p2, p3, p4, p5)))) + (p6, p7))


def a(segitem):

    #SylStructure relation will give phone context answers strictly in
    #word context:
    a1 = segitem.traverse("R:SylStructure.parent.p.F:tone")
    a2 = segitem.traverse("R:SylStructure.parent.p.F:accent")
    a3 = segitem.traverse("R:SylStructure.parent.p.M:num_daughters()")
    
    return "A:%s_%s_%s" % (tuple(map(nonestring, (a1, a2))) + tuple(map(zero, (a3,))))


def b(segitem, phones, phonemap):
    
    b1 = segitem.traverse("R:SylStructure.parent.F:tone")
    b2 = segitem.traverse("R:SylStructure.parent.F:accent")
    b3 = segitem.traverse("R:SylStructure.parent.M:num_daughters()")
    b4 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_f()")
    b5 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_b()")
    b6 = segitem.traverse("R:NoRelation")#
    b7 = segitem.traverse("R:NoRelation")#
    b8 = segitem.traverse("R:NoRelation")#
    b9 = segitem.traverse("R:NoRelation")#
    b10 = segitem.traverse("R:NoRelation")#
    b11 = segitem.traverse("R:NoRelation")#
    b12 = segitem.traverse("R:SylStructure.parent.M:syldistprev_inword('tone', '1')")
    b13 = segitem.traverse("R:SylStructure.parent.M:syldistnext_inword('tone', '1')")
    b14 = segitem.traverse("R:SylStructure.parent.M:syldistprev_inword('accent', '1')")
    b15 = segitem.traverse("R:SylStructure.parent.M:syldistnext_inword('accent', '1')")

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
    
    return "B:%s-%s-%s@%s-%s&%s-%s#%s-%s$%s-%s!%s-%s;%s-%s|%s" % (tuple(map(zero, (b1, b2, b3, b4,
                                                                                   b5, b6, b7, b8,
                                                                                   b9, b10, b11, b12,
                                                                                   b13, b14, b15))) + 
                                                                  tuple(map(nonestring, (b16, ))))


def c(segitem):

    #SylStructure relation will give phone context answers strictly in
    #word context:
    c1 = segitem.traverse("R:SylStructure.parent.n.F:tone")
    c2 = segitem.traverse("R:SylStructure.parent.n.F:accent")
    c3 = segitem.traverse("R:SylStructure.parent.n.M:num_daughters()")
    
    return "C:%s+%s+%s" % tuple(map(zero, (c1, c2, c3)))

    

def d(segitem):

    d1 = segitem.traverse("R:NoRelation")
    if d1 is None: d1 = NONE_STRING
    d2 = segitem.traverse("R:NoRelation")
    if d2 is None: d2 = 0
    
    return "D:%s_%s" % (d1, d2)


def e(segitem):

    e1 = segitem.traverse("R:SylStructure.parent.parent.F:gpos")
    if e1 is None: e1 = NONE_STRING
    e2 = segitem.traverse("R:SylStructure.parent.parent.M:num_daughters()")
    e3 = segitem.traverse("R:NoRelation")
    e4 = segitem.traverse("R:NoRelation")
    e5 = segitem.traverse("R:NoRelation")
    e6 = segitem.traverse("R:NoRelation")
    e7 = segitem.traverse("R:NoRelation")
    e8 = segitem.traverse("R:NoRelation")
    
    return "E:%s+%s@%s+%s&%s+%s#%s+%s" % tuple(map(zero, (e1, e2, e3, e4, e5, e6, e7, e8)))


def f(segitem):

    f1 = segitem.traverse("R:NoRelation")
    if f1 is None: f1 = NONE_STRING
    f2 = segitem.traverse("R:NoRelation")
    if f2 is None: f2 = 0
    
    return "F:%s_%s" % (f1, f2)


def g(segitem):

    g1 = segitem.traverse("R:NoRelation")
    g2 = segitem.traverse("R:NoRelation")

    return "G:%s_%s" % tuple(map(zero, (g1, g2)))


def h(segitem):

    h1 = segitem.traverse("R:NoRelation")
    h2 = segitem.traverse("R:NoRelation")
    h3 = segitem.traverse("R:NoRelation")
    h4 = segitem.traverse("R:NoRelation")
    h5 = segitem.traverse("R:NoRelation")
    if h5 is None: h5 = NONE_STRING

    return "H:%s=%s@%s=%s|%s" % tuple(map(zero, (h1, h2, h3, h4, h5)))


def i(segitem):

    i1 = segitem.traverse("R:NoRelation")
    i2 = segitem.traverse("R:NoRelation")

    return "I:%s_%s" % tuple(map(zero, (i1, i2)))


def j(segitem):
    
    utt = segitem.relation.utterance
    
    j1 = 0
    j2 = 0
    j3 = 0

    return "J:%s+%s-%s" % (j1, j2, j3)
