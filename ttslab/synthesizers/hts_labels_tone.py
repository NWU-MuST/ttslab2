# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from ttslab.synthesizers.hts_labels import *

def a(segitem):

    a1 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:stress")
    a2 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:accent")
    a3 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.M:num_daughters()")
    
    return "A:%s_%s_%s" % tuple(map(zero, (a1, a2, a3)))


def b(segitem, phones, phonemap):
    
    b1 = segitem.traverse("R:SylStructure.parent.F:stress")
    b2 = segitem.traverse("R:SylStructure.parent.F:accent")
    b3 = segitem.traverse("R:SylStructure.parent.M:num_daughters()")
    b4 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_f()")
    b5 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_b()")
    b6 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_f()")
    b7 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_b()")
    b8 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('stress', '1')")
    b9 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('stress', '1')")
    b10 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('accent', '1')")
    b11 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('accent', '1')")
    b12 = segitem.traverse("R:SylStructure.parent.M:syldistprev('stress', '1')")
    b13 = segitem.traverse("R:SylStructure.parent.M:syldistnext('stress', '1')")
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

    c1 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:stress")
    c2 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:accent")
    c3 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.M:num_daughters()")
    
    return "C:%s+%s+%s" % tuple(map(zero, (c1, c2, c3)))


def k(segitem):
    k0 = segitem.traverse("R:SylStructure.parent.F:tone")
    if k0 is None:
        k0 = NONE_STRING
    return "K:%s" % k0

def l(segitem):
    l0 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.F:tone")
    if l0 is None:
        l0 = NONE_STRING
    return "L:%s" % l0

def m(segitem):
    m0 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.p.F:tone")
    if m0 is None:
        m0 = NONE_STRING
    return "M:%s" % m0

def n(segitem):
    n0 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.F:tone")
    if n0 is None:
        n0 = NONE_STRING
    return "N:%s" % n0
