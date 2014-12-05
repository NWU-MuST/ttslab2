#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Number expansion for the Afrikaans language...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"


patterns1 = {0: ["nul"],
             1: ["een"],
             2: ["twee"],
             3: ["drie"],
             4: ["vier"],
             5: ["vyf"],
             6: ["ses"],
             7: ["sewe"],
             8: ["agt"],
             9: ["nege"],
             10: ["tien"],
             11: ["elf"],
             12: ["twaalf"],
             13: ["dertien"],
             14: ["veertien"],
             15: ["vyftien"],
             16: ["sestien"],
             17: ["sewentien"],
             18: ["agtien"],
             19: ["negentien"],
             20: ["twintig", "%(mod)s en twintig"],
             30: ["dertig", "%(mod)s en dertig"],
             40: ["veertig", "%(mod)s en veertig"],
             50: ["vyftig", "%(mod)s en vyftig"],
             60: ["sestig", "%(mod)s en sestig"],
             70: ["sewentig", "%(mod)s en sewentig"],
             80: ["tagtig", "%(mod)s en tagtig"],
             90: ["negentig", "%(mod)s en negentig"],
             100: ["%(div)s honderd", "%(div)s honderd %(mod)s"],
             1000: ["%(div)s duisend", "%(div)s duisend %(mod)s"],
             1000000: ["%(div)s miljoen", "%(div)s miljoen %(mod)s"],
             1000000000: ["%(div)s miljard", "%(div)s miljard %(mod)s"],
             1000000000000: ["%(div)s biljoen", "%(div)s biljoen %(mod)s"],
             1000000000000000: ["%(div)s biljard", "%(div)s biljard %(mod)s"],
             1000000000000000000: ["%(div)s triljoen", "%(div)s triljoen %(mod)s"]
            }

def expand(n):
    patterns = patterns1
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
            modt = expand(m)
            t = patterns[pn][1]
        else:
            t = patterns[pn][0]
        divt = expand(d)
        return t % {"div": divt, "mod": modt}

if __name__ == "__main__":
    import os, sys
    print(expand(int(sys.argv[1])))
