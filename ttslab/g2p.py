#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Basic implementation of g2p based on rewrites...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import codecs
import re

class NoRuleFound(Exception):
    pass

class GraphemeNotDefined(Exception):
    pass

class G2P(object):
    """Abstract class just to define the required interface...
    """
    def predict_word(self, word):
        """ Takes a string and returns a list of phonemes...
        """
        raise NotImplementedError

class RewriteRule(object):
    """ Simply keeps rule info together...
    """
    def __init__(self, grapheme, leftcontext, rightcontext, phoneme, ordinal):
        self.grapheme = grapheme
        self.leftcontext = leftcontext
        self.rightcontext = rightcontext
        self.phoneme = phoneme
        self.ordinal = ordinal

    def __str__(self):
        """Print in 'semicolon format'...
        """
        return ";".join([self.grapheme,
                         self.leftcontext,
                         self.rightcontext,
                         self.phoneme,
                         unicode(self.ordinal)]) #Py2

    def match(self, leftcontext, rightcontext):
        """ Returns True if this rule matches the given context...
        """
        #LC matches?
        for c1, c2 in zip(reversed(self.leftcontext), reversed(leftcontext)):
            if not c1 == c2:
                return False
        #RC matches?
        for c1, c2 in zip(self.rightcontext, rightcontext):
            if not c1 == c2:
                return False
        #Both match..
        return True
        

class G2P_Rewrites(G2P):
    """ Class to contain and implement the application of rewrite
        rules to predict pronunciations of isolated words...

        ruleset is a dict of lists where the each list contains all
        RewriteRules associated with a specific grapheme...
        
    """
    WHITESPACE_CHAR = "#"

    def __init__(self):
        self.features = {}
        self.ruleset = {}
        self.gnulls = {}

    def sort_rules(self):
        """ Make sure that all rulelists associated with each grapheme
        are sorted in the correct order for application (i.e. from
        most specific context to least specific context - based on the
        RewriteRule.ordinal)
        """
        for g in self.ruleset:
            self.ruleset[g].sort(key=lambda x: x.ordinal, reverse=True)

    def apply_gnulls(self, word):
        """ Apply gnulls to word if applicable...
        """
        if self.gnulls:
            for gnull in self.gnulls:
                word = re.sub(gnull, self.gnulls[gnull], word)
        return word
    
    def predict_word(self, word):
        """ Predict phone sequence given word...
        """
        phones = []
        #append and prepend whitespace_char
        word = word.join([self.WHITESPACE_CHAR, self.WHITESPACE_CHAR])
        #apply gnulls
        word = self.apply_gnulls(word)
        #find matching rule and thus phoneme for each grapheme..
        for i in list(range(len(word)))[1:-1]: #excluding whitespace..
            lc, g, rc = [word[:i], word[i], word[i+1:]]
            try:
                rulelist = self.ruleset[g]
            except KeyError:
                raise GraphemeNotDefined("Word: " + word + " Grapheme: " + g)

            #no need to do the following if stored in the correct order:
            #rulelist.sort(key=lambda x: x.ordinal, reverse=True)

            for rule in rulelist:
                if rule.match(lc, rc):
                    if rule.phoneme:                 #phoneme can be "" meaning no phone (pnull)
                        phones.append(rule.phoneme)  #only add if not empty string
                    break
            else:
                raise NoRuleFound#(lc + " " + g + " " + rc)
        return phones

class G2P_Rewrites_Semicolon(G2P_Rewrites):
    """Includes methods to load rules from "semicolon format" files...
    """
    def load_simple_mapfile(self, maplocation):
        """ Load phone representation from simple text file...
            e.g:
                 1;p
                 0;0
                 3;bi
            Expecting one-to-one mappings...
        """
        mapping = {}
        with codecs.open(maplocation, "r", encoding="utf-8") as infh:
            for line in infh:
                a, b = line.strip().split(";")
                if a in mapping or b in mapping.values():
                    raise Exception("Mapping is not one-to-one..")
                else:
                    mapping[a] = b
        return mapping

    def load_simple_phonemapfile(self, maplocation):
        self.phonemap = self.load_simple_mapfile(maplocation)

    def load_simple_graphmapfile(self, maplocation):
        self.graphmap = self.load_simple_mapfile(maplocation)

    def load_gnulls(self, gnullslocation, wchar=G2P_Rewrites.WHITESPACE_CHAR):
        """ Load gnulls mappings from simple text file...
            e.g
                uk;u0k
                ne;n0e
                ua;u0a
                u ;u0 
           
            NOTE: Significant whitespace at end of last entry...
        """
        mapping = {}
        with codecs.open(gnullslocation, "r", encoding="utf-8") as infh:
            for line in infh:
                a, b = line.rstrip("\n").split(";")
                a, b = (a.replace(" ", wchar), b.replace(" ", wchar))
                if a in mapping:
                    raise Exception("Keys are not unique...")
                else:
                    mapping[a] = b
        self.gnulls = mapping

    def load_ruleset_semicolon(self, filelocation, wchar=G2P_Rewrites.WHITESPACE_CHAR):
        """ Load rules from semicolon delimited format
            "dictionarymaker format", replacing spaces with 'wchar':
            grapheme, left_context, right_context, phoneme, ordinal, number
            e.g:
                 a;;;a;0;1692
                 a;ntl;;n;1;1
                 b;;;b;0;241
                 c;;;5;0;4
                 d;;;d;0;231
                 e;;;e;0;446
        """
        self.ruleset = {}
        with codecs.open(filelocation, "r", encoding="utf-8") as infh:
            for line in infh:
                g, l, r, p, o, n = line.rstrip("\n").split(";")
                l, r = (l.replace(" ", wchar), r.replace(" ", wchar))
                try:
                    self.ruleset[g].append(RewriteRule(g, l, r, p, int(o)))     # we don't use the last field...
                except KeyError:
                    self.ruleset[g] = []
                    self.ruleset[g].append(RewriteRule(g, l, r, p, int(o)))     # we don't use the last field...
        self.sort_rules()
    
    def map_phones(self):
        """ Apply self.phonemap to all phonemes in self.ruleset
        """
        for grapheme in self.ruleset:
            for rule in self.ruleset[grapheme]:
                rule.phoneme = self.phonemap[rule.phoneme]

    def map_graphs(self):
        """Apply self.graphmap to all graphemes in self.ruleset and
           self.gnulls
        """
        for k, v in self.graphmap.items():
            if k == v: continue
            self.ruleset[v] = self.ruleset[k]
            del self.ruleset[k]
            for g in self.ruleset:
                for r in self.ruleset[g]:
                    r.grapheme = re.sub(k, v, r.grapheme)
                    r.leftcontext = re.sub(k, v, r.leftcontext)
                    r.rightcontext = re.sub(k, v, r.rightcontext)
            if self.gnulls:
                for gk, gv in self.gnulls.items():
                    if (k in gk) or (k in gv):
                        del self.gnulls[gk]
                        gk = re.sub(k, v, gk)
                        gv = re.sub(k, v, gv)
                        self.gnulls.update({gk: gv})

if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rulesfn', metavar='RULESFN', type=str, help="rules file (semicolon format)")
    parser.add_argument('gnullsfn', metavar='GNULLSFN', type=str, help="gnulls file (semicolon format)")
    parser.add_argument('pmapfn', metavar='PMAPFN', type=str, help="phonemap file (semicolon format)")
    parser.add_argument('gmapfn', metavar='GMAPFN', type=str, help="phonemap file (semicolon format)")
    args = parser.parse_args()
    
    rs = G2P_Rewrites_Semicolon()
    rs.load_ruleset_semicolon(args.rulesfn)
    rs.load_gnulls(args.gnullsfn)
    rs.load_simple_phonemapfile(args.pmapfn)
    rs.map_phones()
    rs.load_simple_graphmapfile(args.gmapfn)
    rs.map_graphs()
    
    for line in sys.stdin:
        word = unicode(line, encoding="utf-8").strip()
        print("{}\t{}".format(word, " ".join(rs.predict_word(word))).encode("utf-8"))
