#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
"""Copyright 2013 Matthew Honnibal

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import codecs
import random
from collections import defaultdict
import pickle

from ttslab.postagger_perceptron import PerceptronTagger


def load_csv(text, sep="\t"):
    sentences = [[[], []]]    
    for line in text.splitlines():
        if line.strip() == "":
            sentences.append([[], []])
            continue
        word, tag = line.split(sep)
        sentences[-1][0].append(word)
        sentences[-1][1].append(tag)
    if sentences[-1] == []:
        sentences.pop(-1)
    return sentences

def train_fromfn(trainfn):
    sentences = load_csv(codecs.open(trainfn, encoding="utf-8").read())
    print(len(sentences), file=sys.stderr)
    tagger = PerceptronTagger()
    tagger.train(sentences)
    return tagger

def test(testsents, tagger):
    total = 0
    correct = 0
    for sentence in testsents:
        reftags = sentence[1]
        total += len(reftags)
        tagged_sentence = tagger.tag(sentence[0]) #words only
        #taggertags = [e[1] for e in tagged_sentence]
        #from pprint import pprint
        #pprint(zip(reftags, tagged_sentence))
        for ref, result in zip(reftags, tagged_sentence):
            if ref == result:
                correct += 1
    print(correct, total)
    return correct, total

def test_fromfn(testfn, modelfn):
    sentences = load_csv(codecs.open(testfn, encoding="utf-8").read())
    print(len(sentences), file=sys.stderr)
    with open(modelfn, "rb") as infh:
        tagger = pickle.load(infh)
    return test(sentences, tagger)

if __name__ == "__main__":
    if sys.argv[1] == "train":
        with open(sys.argv[3], "wb") as outfh:
            tagger = train_fromfn(sys.argv[2])
            pickle.dump(tagger, outfh, protocol=2)
    elif sys.argv[1] == "test":
        correct, total = test_fromfn(sys.argv[2], sys.argv[3])
        print("Correct (perc.): %s" % (correct/total*100.0))
