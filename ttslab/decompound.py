#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Recursive splitting of words for decompounding , splitting
   algorithm is original, FST code from examples here:
   http://nbviewer.ipython.org/url/nlpa.iupr.com/resources/nlpa-openfst.ipynb
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys
import codecs
import itertools

import openfst

class Decompounder(object):
    def decompound(self, word):
        raise NotImplementedError

    def __call__(self, word):
        return self.decompound(word)


def show_fst(fst, fstsymtable):
    import pydot, pylab
    graph = pydot.Dot(rankdir="LR")
    isyms = fst.InputSymbols()
    if not isyms: isyms = fstsymtable
    osyms = fst.OutputSymbols()
    if not osyms: osyms = fstsymtable
    for s in range(fst.NumStates()):
        if s==fst.Start():
            n = pydot.Node("%d"%s,shape="box")
            graph.add_node(n)
        if fst.IsFinal(s):
            l = '"'
            l += "%d"%s # node id
            if fst.Final(s).Value()!=0.0: # optional non-zero accept cost
                l += "/%s"%fst.Final(s).Value()
            l += '"'
            n = pydot.Node("%d"%s,label=l,penwidth="3")
            graph.add_node(n)
        for t in range(fst.NumArcs(s)):
            a = fst.GetArc(s,t)
            l = '"'
            l += '%s'%isyms.Find(a.ilabel)
            if a.olabel!=a.ilabel: l += ":%s"%osyms.Find(a.olabel)
            v = a.weight.Value()
            if v!=0.0: l += "/%s"%v
            l += '"'
            n = a.nextstate
            e = pydot.Edge("%d"%s,"%d"%n,label=l)
            graph.add_edge(e)
    graph.write_png("/tmp/_test.png")
    pylab.gca().set_xticks([]); pylab.gca().set_yticks([])
    pylab.clf()
    pylab.imshow(pylab.imread("/tmp/_test.png"))
    pylab.show()

def label_seq(fst, symtablel, which=1, full=0):
    result = []
    total = 0
    state = fst.Start()
    while not fst.IsFinal(state):
        assert fst.NumArcs(state) == 1
        a = fst.GetArc(state, 0)
        if which == 0:
            l = a.ilabel
        else:
            l = a.olabel
        result.append(l)
        total += a.weight.Value()
        state = a.nextstate
    result = [symtablel[i] for i in result]
    if full:
        return result, total
    else:
        return result

class Tree():
    """ Very simple, used to capture recursive structure...
        Modified from:
           http://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree-in-python
    """
    def __init__(self, value):
      self.nodes = []
      self.value = value

    def insert(self, value):
        self.nodes.append(Tree(value))
        return self.nodes[-1]

    def nleafnodes(self):
        count = 0
        if not self.nodes:
            count += 1
        else:
            for n in self.nodes:
                count += n.nleafnodes()
        return count

    def getsyms(self):
        syms = set()
        syms.add(self.value)
        for n in self.nodes:
            syms.update(n.getsyms())
        return syms

    def makelattice(self, fst, startstate, symtable, cost):
        length = self.nleafnodes()
        fst.AddArc(startstate, symtable[self.value], symtable[self.value], cost(self.value), startstate+length)
        offset = 0
        for n in self.nodes:
            n.makelattice(fst, startstate+offset, symtable, cost)
            offset += n.nleafnodes()

    def __str__(self):
        l = []
        for node in self.nodes:
            l.extend(str(node).splitlines())
        lines = [str(self.value)] + ["\t" + line for line in l]
        return "\n".join(lines)

def test_tree():
    my_tree = Tree("BobTonySteven")
    my_tree.insert("Bob")
    my_tree.insert("Tony")
    my_tree.insert("Steven")


class SimpleCompoundSplitter(Decompounder):
    def __init__(self, wordlist):
        self.words = set(wordlist)
        
    def _to_split_or_not(self, splitcand):
        if len(splitcand) == 2: #split proposed?
            if splitcand[0] in self.words or splitcand[1] in self.words:
                w = splitcand
            else:
                w = ["".join(splitcand)]
        else:
            w = splitcand
        return w
        
    def _split(self, word, rootnode):
        center = len(word) / 2.0
        scores = []
        for i in range(len(word)):
            w1, w2 = word[:i], word[i:]
            matches = int(w1 in self.words) + int(w2 in self.words)
            if matches:
                #print(w1, w2, [i, matches, abs(i - center)])
                scores.append([i, matches, abs(i - center)])
        if not scores: #early stop if no good candidates
            return [word]
        scores.sort(key=lambda x:x[2])
        scores.sort(key=lambda x:x[1], reverse=True)
        bestidx = scores[0][0]
        if bestidx == 0:
            return [word]
        else:
            #print("trying:", word[:bestidx], word[bestidx:])
            left = rootnode.insert(word[:bestidx])
            self._split(word[:bestidx], left)
            #print(cand1, len(cand1))
            right = rootnode.insert(word[bestidx:])
            self._split(word[bestidx:], right)

    def wordcost(self, word):
        if word in self.words:
            return -1.0
        return 1.0

    def decompound(self, word):
        tree = Tree(word)
        self._split(word, tree)
        #print(tree)
        nleafnodes = tree.nleafnodes()
        #print("Number of leaf nodes:", nleafnodes)
        symtablel = sorted(tree.getsyms())
        symtable = dict([(s, i) for i, s in enumerate(symtablel)])
        #print("Symbols:")
        #print(symtable)
        fst = openfst.StdVectorFst()
        [fst.AddState() for i in range(nleafnodes + 1)]
        fst.SetFinal(nleafnodes, 0.0)
        fst.SetStart(0)
        tree.makelattice(fst, 0, symtable, self.wordcost)
        #display for debugging
        # fstsymtable = openfst.SymbolTable(b"default")
        # for i, sym in enumerate(symtablel):
        #     fstsymtable.AddSymbol(sym.encode("utf-8"), i)
        # show_fst(fst, fstsymtable)
        best = openfst.StdVectorFst()
        openfst.ShortestPath(fst, best, 1)
        wordseq = label_seq(best, symtablel)
        return wordseq
        

def test(wordlistfn, compword):
    with codecs.open(wordlistfn, encoding="utf-8") as infh:
        wordlist = infh.read().split()
    csplitter = SimpleCompoundSplitter(wordlist)
    splitform = csplitter.decompound(compword)
    return splitform
    
if __name__ == "__main__":
    print(test(sys.argv[1], sys.argv[2]))
    #test_tree()
