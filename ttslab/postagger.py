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

from postagger_perceptron import AveragedPerceptron


class PerceptronTagger(object):
    '''Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.

    See more implementation details here:
        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

    :param load: Load the pickled model upon instantiation.
    '''

    START = ['-START-', '-START2-']
    END = ['-END-', '-END2-']

    def __init__(self):
        self.model = AveragedPerceptron()
        self.tagdict = {}
        self.classes = set()

    def __setstate__(self, state):
        self.model = AveragedPerceptron()
        self.model.weights, self.tagdict, self.classes = state
        self.model.classes = self.classes

    def __getstate__(self):
        return (self.model.weights, self.tagdict, self.classes)

    def tag(self, sentence, tagsonly=True):
        """ Tags a tokenized sentence, i.e. a list of words (strings).
        """
        prev, prev2 = self.START
        tokens = []
        context = self.START + [self._normalize(w) for w in sentence] + self.END
        for i, word in enumerate(sentence):
            tag = self.tagdict.get(word)
            if not tag:
                features = self._get_features(i, word, context, prev, prev2)
                tag = self.model.predict(features)
            if tagsonly:
                tokens.append(tag)
            else:
                tokens.append((word, tag))
            prev2 = prev
            prev = tag
        return tokens

    def train(self, sentences, n_iter=10, seed=7):
        '''Train a model from sentences, and save it at ``save_loc``. ``n_iter``
        controls the number of Perceptron training iterations.

        :param sentences: A list of (words, tags) tuples.
        :param save_loc: If not ``None``, saves a pickled model in this location.
        :param n_iter: Number of training iterations.
        '''
        random.seed(seed)
        self._make_tagdict(sentences)
        self.model.classes = self.classes
        for iter_ in range(n_iter):
            c = 0
            n = 0
            for words, tags in sentences:
                prev, prev2 = self.START
                context = self.START + [self._normalize(w) for w in words] \
                                                                    + self.END
                for i, word in enumerate(words):
                    guess = self.tagdict.get(word)
                    if not guess:
                        feats = self._get_features(i, word, context, prev, prev2)
                        guess = self.model.predict(feats)
                        self.model.update(tags[i], guess, feats)
                    prev2 = prev
                    prev = guess
                    c += guess == tags[i]
                    n += 1
            random.shuffle(sentences)
            print("Iter {0}: {1}/{2}={3}".format(iter_, c, n, _pc(c, n)), file=sys.stderr)
        self.model.average_weights()

    def _normalize(self, word):
        '''Normalization used in pre-processing.

        - All words are lower cased
        - Digits in the range 1800-2100 are represented as !YEAR;
        - Other digits are represented as !DIGITS

        :rtype: str
        '''
        if '-' in word and word[0] != '-':
            return '!HYPHEN'
        elif word.isdigit() and len(word) == 4:
            return '!YEAR'
        elif word[0].isdigit():
            return '!DIGITS'
        else:
            return word.lower()

    def _get_features(self, i, word, context, prev, prev2):
        '''Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        '''
        sufflen = 3
        def add(name, *args):
            features[' '.join((name,) + tuple(args))] += 1

        i += len(self.START)
        features = defaultdict(int)
        # It's useful to have a constant feature, which acts sort of like a prior
        add('bias')
        add('i suffix', word[-sufflen:])
        add('i pref1', word[0])
        add('i-1 tag', prev)
        add('i-2 tag', prev2)
        add('i tag+i-2 tag', prev, prev2)
        add('i word', context[i])
        add('i-1 tag+i word', prev, context[i])
        add('i-1 word', context[i-1])
        add('i-1 suffix', context[i-1][-sufflen:])
        add('i-2 word', context[i-2])
        add('i+1 word', context[i+1])
        add('i+1 suffix', context[i+1][-sufflen:])
        add('i+2 word', context[i+2])
        return features

    def _make_tagdict(self, sentences):
        '''Make a tag dictionary for single-tag words.'''
        counts = defaultdict(lambda: defaultdict(int))
        for words, tags in sentences:
            for word, tag in zip(words, tags):
                counts[word][tag] += 1
                self.classes.add(tag)
        freq_thresh = 20
        ambiguity_thresh = 0.97
        for word, tag_freqs in counts.items():
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            # Don't add rare words to the tag dictionary
            # Only add quite unambiguous words
            if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                self.tagdict[word] = tag

def _pc(n, d):
    return (float(n) / d) * 100


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
        taggertags = [e[1] for e in tagged_sentence]
        for ref, result in zip(reftags, taggertags):
            if ref == result:
                correct += 1
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
        print("Correct(%): %s" % correct/total*100.0)
