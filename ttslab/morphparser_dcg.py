#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Loads a simplified form of Definite Clause Grammar (each rule only
   either maps to terminals or nonterminals and no overlap between
   terminal and nonterminal symbols -- see for example `zul.dvn.dcg`)
   and creates OpenFST grammars to parse and classify words.
"""
from __future__ import unicode_literals, print_function, division

import os, sys
import re
from collections import defaultdict
import tempfile

import morphparser
import pywrapfst as ot

RULE_RE = re.compile("(?P<head>\w+)\s*\-\-\>\s*(?P<body>.+?)\.")
EPS = "_"

def load_simpledcg(dcg):
    terminals = defaultdict(list)
    nonterminals = defaultdict(list)
    for rule in dcg.splitlines():
        m = RULE_RE.search(rule)
        head, body = m.group("head"), m.group("body")
        if "[" in body:
            syms = list(body.strip("[]"))
            terminals[head].append(syms)
        else:
            syms = re.sub("\s+", "", body).split(",")
            nonterminals[head].append(syms)
    return {"terminals": dict(terminals), "nonterminals": dict(nonterminals)}


def make_symmaps(dcg, graphs, othersyms):
    syms = set(graphs)
    syms.update([e for e in othersyms if e != EPS])
    for k in ["terminals", "nonterminals"]:
        for kk, v in dcg[k].iteritems():
            syms.add(kk)
            for seq in v:
                syms.update(seq)
    itos = dict(zip(range(1, len(syms)+1), sorted(syms)))
    itos[0] = EPS
    stoi = dict((v, k) for k, v in itos.iteritems())
    return itos, stoi


def get_undefsyms(dcg, stoi):
    """Determine which symbols are undefined"""
    defined = set(list(dcg["nonterminals"]) + list(dcg["terminals"]))
    targets = set()
    for k, v in dcg["nonterminals"].iteritems():
        for vv in v:
            targets.update(vv)
    return list(targets.difference(defined))


def make_kleeneplus(s, graphs, stoi):
    """one-or-more-graphs"""
    fst = ot.Fst()
    start = fst.add_state()
    end = fst.add_state()
    fst.set_start(start)
    fst.set_final(end, ot.Weight.One(fst.weight_type()))
    for g in graphs:
        fst.add_arc(start, ot.Arc(stoi[g], stoi[s], ot.Weight.One(fst.weight_type()), end))
        fst.add_arc(end, ot.Arc(stoi[g], 0, ot.Weight.One(fst.weight_type()), end))
    return fst

def replace_arc(rootfst, subfst, sym, label="input"):
    sstart = subfst.start()
    smap = {}
    for rs in rootfst.states():
        arcs = [(a.ilabel, a.olabel, a.weight, a.nextstate) for a in rootfst.arcs(rs)]
        if label == "input":
            arcs_other = [a for a in arcs if a[0] != sym]
            arcs_replace = [a for a in arcs if a[0] == sym]
        else:
            arcs_other = [a for a in arcs if a[1] != sym]
            arcs_replace = [a for a in arcs if a[1] == sym]
        rootfst.delete_arcs(rs)
        for ra in arcs_other:
            rootfst.add_arc(rs, ot.Arc(*ra))
        for ra in arcs_replace:
            todo = [sstart]
            done = set()
            s = rootfst.add_state()
            rootfst.add_arc(rs, ot.Arc(0, 0, ot.Weight.One(rootfst.weight_type()), s))
            smap[sstart] = s
            while todo:
                ss = todo.pop(0)
                done.add(ss)
                if subfst.final(ss) != ot.Weight.Zero(rootfst.weight_type()):
                    rootfst.add_arc(smap[ss], ot.Arc(0, 0, ot.Weight.One(rootfst.weight_type()), ra[-1]))
                for sa in subfst.arcs(ss):
                    ns = sa.nextstate
                    if ns not in smap:
                        s = rootfst.add_state()
                        smap[ns] = s
                    if ns not in todo and ns not in done:
                        todo.append(ns)
                    rootfst.add_arc(smap[ss], ot.Arc(sa.ilabel, sa.olabel, sa.weight, smap[ns]))


def make_termfst(s, paths, stoi):
    fst = ot.Fst()
    prestart = fst.add_state()
    fst.set_start(prestart)
    start = fst.add_state()
    fst.add_arc(prestart, ot.Arc(0, stoi[s], ot.Weight.One(fst.weight_type()), start))
    for path in paths:
        a = start
        for g in path:
            b = fst.add_state()
            fst.add_arc(a, ot.Arc(stoi[g], 0, ot.Weight.One(fst.weight_type()), b))
            a = b
        fst.set_final(b, ot.Weight.One(fst.weight_type()))
    fst2 = ot.determinize(fst)
    fst2.minimize()
    return fst2


def make_termfsts(dcg, graphs, stoi):
    """Make fsts mapping terminals to nonterminal symbols"""
    undefsyms = get_undefsyms(dcg, stoi)
    print("UNDEFSYMS:", undefsyms, file=sys.stderr)
    fsts = {}
    for s in undefsyms:
        fsts[s] = make_kleeneplus(s, graphs, stoi)
        save_dot(fsts[s], stoi, "tmp/"+s+".dot")
    for s in dcg["terminals"]:
        fsts[s] = make_termfst(s, dcg["terminals"][s], stoi)        
        save_dot(fsts[s], stoi, "tmp/"+s+".dot")
    return fsts


def make_fst(s, dcg, stoi):
    fstcoll = {}
    fst = ot.Fst()
    prestart = fst.add_state()
    fst.set_start(prestart)
    start = fst.add_state()
    fst.add_arc(prestart, ot.Arc(0, stoi[s], ot.Weight.One(fst.weight_type()), start))
    for path in dcg[s]:
        a = start
        for ss in path:
            b = fst.add_state()
            if ss in dcg and ss not in fstcoll:
                fstcoll[ss] = make_fst(ss, dcg, stoi)
            fst.add_arc(a, ot.Arc(stoi[ss], 0, ot.Weight.One(fst.weight_type()), b))
            a = b
        fst.set_final(b, ot.Weight.One(fst.weight_type()))
    #print(s, "fstcoll", fstcoll.keys(), file=sys.stderr)
    for sym in fstcoll:
        replace_arc(fst, fstcoll[sym], stoi[sym])
    return fst

def save_dot(fst, stoi=None, fn="_fst.dot"):
    if stoi is not None:
        st = ot.SymbolTable()
        for k, v in stoi.iteritems():
            st.add_symbol(k.encode("utf-8"), v)
            fst.set_input_symbols(st)
            fst.set_output_symbols(st)
    fst.draw(fn)
    

def make_input(chars, stoi):
    fst = ot.Fst()
    s0 = fst.add_state()
    fst.set_start(s0)
    cs = s0
    for c in chars:
        ns = fst.add_state()
        fst.add_arc(cs, ot.Arc(stoi[c], stoi[c], ot.Weight.One(fst.weight_type()), ns))
        cs = ns
    fst.set_final(cs, ot.Weight.One(fst.weight_type()))
    return fst


class Morphparse_DCG(morphparser.Morphparse):
    def __init__(self, dcg, descr):
        othersyms = set()
        for pos in descr["renamesyms"]:
            othersyms.update([e[1] for e in descr["renamesyms"][pos]])
        self.itos, self.stoi = make_symmaps(dcg, descr["graphs"], othersyms)
        #print(self.stoi, file=sys.stderr)
        fsts = make_termfsts(dcg, descr["graphs"], self.stoi)
        dcgall = dcg["nonterminals"]
        dcgall.update(dcg["terminals"])
        self.fsts = {}
        for pos in descr["pos"]:
            #print("POS:", pos, file=sys.stderr)
            self.fsts[pos] = make_fst(pos, dcgall, self.stoi)
            for sym in set(fsts).difference(dcgall): #also do open-class symbols
                replace_arc(self.fsts[pos], fsts[sym], self.stoi[sym])
            if pos in descr["renamesyms"]:
                self.fsts[pos].relabel_pairs(opairs=map(lambda x: (self.stoi[x[0]], self.stoi[x[1]]), descr["renamesyms"][pos]))
            self.fsts[pos].rmepsilon()
            save_dot(self.fsts[pos], self.stoi, pos+".dot")
            # try:
            #     self.fsts[pos] = ot.determinize(self.fsts[pos])
            # except ot.FstOpError:
            #     pass
        
    def __getstate__(self):
        fsts = {}
        for pos in self.fsts:
            try:
                fd, path = tempfile.mkstemp()
                self.fsts[pos].write(path)
                with open(path, "rb") as infh:
                    serialisedfst = infh.read()
            finally:
                os.close(fd)
                os.remove(path)
            fsts[pos] = serialisedfst
        return {"fsts": fsts,
                "itos": self.itos,
                "stoi": self.stoi}

    def __setstate__(self, d):
        self.fsts = {}
        for pos in d["fsts"]:
            try:
                fd, path = tempfile.mkstemp()
                with open(path, "wb") as outfh:
                    outfh.write(d["fsts"][pos])
                fst = ot.Fst.read(path)
            finally:
                os.close(fd)
                os.remove(path)
            self.fsts[pos] = fst
        self.itos = d["itos"]
        self.stoi = d["stoi"]

    def parse_word(self, word, pos=None):
        if pos:
            posl = [pos]
        else:
            posl = list(self.fsts.keys())
        parses = set()
        for pos in posl:
            #print("parse_word(): trying POS:", pos, file=sys.stderr)
            ifst = make_input(word, self.stoi)
            ofst = ot.compose(ifst, self.fsts[pos])
            ofstnstates = len(list(ofst.states()))
            if not ofstnstates:
                #print("parse_word(): no parse for POS:", pos, file=sys.stderr)
                continue
            #print("parse_word(): parse successful for POS:", pos, file=sys.stderr)
            save_dot(ofst, self.stoi, "output.dot")
            paths = []
            dfs_walk(ofst, self.itos, ofst.start(), None, [], paths)
            for path in paths:
                #print(" ".join([e[1] for e in path if e[1]]).encode("utf-8"))
                parses.add(path2parse(path))
        parses = list(sorted(parses))
        return parses
        
def path2parse(path):
    parse = []
    for i, o in path:
        if o != EPS:
            parse.append("<{}>".format(o))
        if i != EPS:
            parse.append(i)
    return "".join(parse)
    
def dfs_walk(fst, itos, state, labels, path, fullpaths):
    path = path[:]
    if labels:
        path.append(labels)
    if fst.final(state) != ot.Weight.Zero(fst.weight_type()): #nextstate is final?
        fullpaths.append(path)
    for arc in fst.arcs(state):
        labs = (itos[arc.ilabel], itos[arc.olabel])
        dfs_walk(fst, itos, arc.nextstate, labs, path, fullpaths)
    
if __name__ == "__main__":
    import sys, codecs, argparse, pickle, json
    import morphparser_dcg
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dcgfn', metavar='DCGFN', type=str, help="input DCG filename")
    parser.add_argument('descrfn', metavar='DESCRFN', type=str, help="JSON file containing a description of how to interpret the DCG file (e.g. graphemes and POS categories etc.)")    
    parser.add_argument('--dumpmodel', dest='dumpmodel', action='store_true', help="Just dump the parser model (pickle)")
    args = parser.parse_args()
    
    with codecs.open(args.dcgfn, encoding="utf-8") as infh:
        dcg = load_simpledcg(infh.read())
    with codecs.open(args.descrfn, encoding="utf-8") as infh:
        descr = json.load(infh)

    morphparse = morphparser_dcg.Morphparse_DCG(dcg, descr)

    if args.dumpmodel:
        print(pickle.dumps(morphparse))
    else:
        print("WARNING: Model not dumped, use --dumpmodel", file=sys.stderr)
