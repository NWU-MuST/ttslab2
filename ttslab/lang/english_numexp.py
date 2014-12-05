#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Number expansion for the English language...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"


patterns1 = {0: ["zero"],
             1: ["one"],
             2: ["two"],
             3: ["three"],
             4: ["four"],
             5: ["five"],
             6: ["six"],
             7: ["seven"],
             8: ["eight"],
             9: ["nine"],
             10: ["ten"],
             11: ["eleven"],
             12: ["twelve"],
             13: ["thirteen"],
             14: ["fourteen"],
             15: ["fifteen"],
             16: ["sixteen"],
             17: ["seventeen"],
             18: ["eighteen"],
             19: ["nineteen"],
             20: ["twenty", "twenty %(mod)s"],
             30: ["thirty", "thirty %(mod)s"],
             40: ["forty", "forty %(mod)s"],
             50: ["fifty", "fifty %(mod)s"],
             60: ["sixty", "sixty %(mod)s"],
             70: ["seventy", "seventy %(mod)s"],
             80: ["eighty", "eighty %(mod)s"],
             90: ["ninety", "ninety %(mod)s"],
             100: ["%(div)s hundred", "%(div)s hundred and %(mod)s"],
             1000: ["%(div)s thousand", "%(div)s thousand %(mod)s"],
             1000000: ["%(div)s million", "%(div)s million %(mod)s"],
             1000000000: ["%(div)s billion", "%(div)s billion %(mod)s"],             
             1000000000000: ["%(div)s trillion", "%(div)s trillion %(mod)s"]
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
