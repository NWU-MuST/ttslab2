# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from ttslab.synthesizers.hts_labels import *

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
