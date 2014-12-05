#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Number expansion for the Bomu language...
    Should work correctly for numbers < 2 000 000 000
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"
__copyright__ = "Copyright 2012, The EU VOICES project"
__licence__ = "MIT"
__status__ = "Prototype"

import re

patterns1 = {0: ["woo"],
             1: ["de'ele"],
             2: ["gnun"],
             3: ["tin"],
             4: ["na"],
             5: ["honu"],
             6: ["hozin"],
             7: ["hognun"],
             8: ["hotin"],
             9: ["annawe"],
             10: ["buwe"],
             11: ["buwe-dee"],
             12: ["buwe-gnun"],
             13: ["buwe-tin"],
             14: ["buwe-na"],
             15: ["buwe-honu"],
             16: ["buwe-hozin"],
             17: ["buwe-hognun"],
             18: ["buwe-hotin"],
             19: ["buwe-annawe"],
             20: ["buweme", "buweme ma %(mod)s"],
             30: ["buya-buwe", "buya-buwe ma %(mod)s"],
             40: ["buya-gnun", "buya-gnun ma %(mod)s"],
             50: ["buya-gnun ma buwe", "buya-gnun ma buwe ma %(mod)s"],
             60: ["buya-tin", "buya-tin ma %(mod)s"],
             70: ["buya-tin ma buwe", "buya-tin ma buwe ma %(mod)s"],
             80: ["buya-na", "buya-na ma %(mod)s"],
             90: ["buya-na ma buwe", "buya-na ma buwe ma %(mod)s"],
             100: ["mumuwennu", "mumuwennu ma %(mod)s"],
             120: ["buya-hozin", "buya-hozin ma %(mod)s"],
             140: ["buya-hognun", "buya-hognun ma %(mod)s"],
             160: ["buya-hotin", "buya-hotin ma %(mod)s"],
             180: ["buya-annawe", "buya-annawe ma %(mod)s"]
            }

patterns2 = {100: ["mumuwen-%(div)s", "mumuwen-%(div)s ma %(mod)s"]}

patterns3 = {1000: ["sere-%(div)s", "sere-%(div)s ma %(mod)s"],
             1000000: ["miliyo de'ele", "miliyo de'ele ma %(mod)s"]}

patterns4 = {1000000: ["miliyola be-%(div)s", "miliyola be-%(div)s ma %(mod)s"],
             1000000000: ["miliyari", "miliyari ma %(mod)s"]}

def _expand(n):
    if n < 200:
        patterns = patterns1
    elif n < 2000:
        patterns = patterns2
    elif n < 2000000:
        patterns = patterns3
    elif n < 2000000000:
        patterns = patterns4
    else:
        raise Exception("Number out of range: [0, 2 000 000 000)")
    if n <= 1:
        return patterns[n][0]
    for pn in reversed(sorted(patterns)):
        modt = ""
        divt = ""
        d = n // pn
        if d == 0:
            continue
        m = n % pn
        if m > 0:
            modt = _expand(m)
            t = patterns[pn][1]
        else:
            t = patterns[pn][0]
        divt = expand(d)
        return t % {"div": divt, "mod": modt}

            
def expand(n):
    text = _expand(n)
    for t in ["gnun", "tin", "na", "honu", "hozin", "hognun", "hotin", "annawe"]:
        text = re.sub("ma %s" % t, "ma be-%s" % t, text)
        text = re.sub("^%s" % t, "be-%s" % t, text)
    return text

if __name__ == "__main__":
    import os, sys
    print(expand(int(sys.argv[1])))
