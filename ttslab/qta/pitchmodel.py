# -*- coding: utf-8 -*-
"""This is PitchModel implementation modelling and synthesising pitch
   on a per-syllable basis using Quantitative Target Approximation
   (qTA) [1]. Our implementation here is based on (independent)
   regression models for the _height_ and _slope_ of linear targets,
   with a synthesis algorithm that heuristically determines the
   strength of articulation (_lambda_) as was described in [2].

   [1] S. Prom-On, Y. Xu, and B. Thipakorn, "Modeling tone and
    intonation in Mandarin and English as a process of target
    approximation," The Journal of the Acoustical Society of America,
    vol.  125, pp. 405-424, 2009.

   [2] D.R. van Niekerk and E. Barnard, "A target approximation
    intonation model for Yorùbá TTS," in Proceedings of the 15th
    Annual Conference of the International Speech Communication
    Association (Interspeech), pp 36-40, Singapore, September 2014.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import numpy as np

import ttslab
import ttslab.pitchmodel
import ttslab.qta

import ttslab.hrg as hrg
ttslab.extend(hrg.Item, "ttslab.ifuncs.synthcontext")

NONE_STRING = "xxx"

class PitchModel(ttslab.pitchmodel.PitchModel):
    """ Pitch values are in semitones relative to 1 Hz.
    """
    def __init__(self, strengthmax, featencoder, heightmodelfn=None, slopemodelfn=None):
        self.strengthmax = strengthmax
        self.featencoder = featencoder
        if heightmodelfn:
            self.heightmodel = ttslab.fromfile(heightmodelfn)
        if slopemodelfn:
            self.slopemodel = ttslab.fromfile(slopemodelfn)

    def _encodefeat(self, featidx, val):
        if featidx in self.featencoder:
            if val in self.featencoder[featidx]:
                return self.featencoder[featidx][val]
            else:
                return self.featencoder[featidx][NONE_STRING]
        else:
            return [int(val)]
            
    def feats(self, voice, utt, args):
        """Refer to featdescr.txt
        """
        def phmap(ph):
            try:
                return voice.phonemap[ph]
            except KeyError:
                return None
        vowels = [ph for ph, phfeats in voice.phones.iteritems() if "vowel" in phfeats]
        sylfeats = []
        j1 = len(utt.get_relation("Syllable"))
        j2 = len(utt.get_relation("Word"))
        j3 = len(utt.get_relation("Phrase"))
        for syl in utt.gr("Syllable"):
            p1, p2, p3 = onset, nucleus, coda = map(phmap, syl.sylsegsstructure(vowels)) or None
            nextsyl = syl.next_item
            prevsyl = syl.prev_item
            if nextsyl:
                p4 = phmap(nextsyl.sylsegsstructure(vowels)[1])
            else:
                p4 = NONE_STRING
            if prevsyl:
                p5 = phmap(prevsyl.sylsegsstructure(vowels)[1])
            else:
                p5 = NONE_STRING
            a1 = syl.traverse("p.F:tone") or 0
            a2 = syl.traverse("p.F:accent") or 0
            b1 = syl["tone"] or 0
            b2 = syl["accent"] or 0
            c1 = syl.traverse("n.F:tone") or 0
            c2 = syl.traverse("n.F:accent") or 0
            #there is no b3
            b4 = syl.traverse("R:SylStructure.M:sylpos_inword_f()") or 0
            b5 = syl.traverse("R:SylStructure.M:sylpos_inword_b()") or 0
            b6 = syl.traverse("R:SylStructure.M:sylpos_inphrase_f()") or 0
            b7 = syl.traverse("R:SylStructure.M:sylpos_inphrase_b()") or 0
            b8 = syl.traverse("R:SylStructure.M:numsylsbeforesyl_inphrase('tone', '1')") or 0
            b9 = syl.traverse("R:SylStructure.M:numsylsaftersyl_inphrase('tone', '1')") or 0
            b10 = syl.traverse("R:SylStructure.M:numsylsbeforesyl_inphrase('accent', '1')") or 0
            b11 = syl.traverse("R:SylStructure.M:numsylsaftersyl_inphrase('accent', '1')") or 0
            b12 = syl.traverse("R:SylStructure.M:syldistprev('tone', '1')") or 0
            b13 = syl.traverse("R:SylStructure.M:syldistnext('tone', '1')") or 0
            b14 = syl.traverse("R:SylStructure.M:syldistprev('accent', '1')") or 0
            b15 = syl.traverse("R:SylStructure.M:syldistnext('accent', '1')") or 0
            d1 = syl.traverse("R:SylStructure.parent.p.F:gpos") or NONE_STRING
            d2 = syl.traverse("R:SylStructure.parent.p.M:num_daughters()") or 0
            e1 = syl.traverse("R:SylStructure.parent.F:gpos") or NONE_STRING
            e2 = syl.traverse("R:SylStructure.parent.M:num_daughters()") or 0
            e3 = syl.traverse("R:SylStructure.parent.M:wordpos_inphrase_f()") or 0
            e4 = syl.traverse("R:SylStructure.parent.M:wordpos_inphrase_b()") or 0
            e5 = syl.traverse("R:SylStructure.parent.M:numwordsbeforeword_inphrase('gpos', 'c')") or 0
            e6 = syl.traverse("R:SylStructure.parent.M:numwordssafterword_inphrase('gpos', 'c')") or 0
            e7 = syl.traverse("R:SylStructure.parent.M:worddistprev('gpos', 'c')") or 0
            e8 = syl.traverse("R:SylStructure.parent.M:worddistnext('gpos', 'c')") or 0
            f1 = syl.traverse("R:SylStructure.parent.n.F:gpos") or NONE_STRING
            f2 = syl.traverse("R:SylStructure.parent.n.M:num_daughters()") or 0
            g1 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.p.M:numsyls_inphrase()") or 0
            g2 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.p.M:num_daughters()") or 0
            h1 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.M:numsyls_inphrase()") or 0
            h2 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.M:num_daughters()") or 0
            h3 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.M:phrasepos_inutt_f()") or 0
            h4 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.M:phrasepos_inutt_b()") or 0
            h5 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.F:tobi") or NONE_STRING
            i1 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.n.M:numsyls_inphrase()") or 0
            i2 = syl.traverse("R:SylStructure.parent.R:Phrase.parent.n.M:num_daughters()") or 0
            sylfeat = []
            for i, val in enumerate([p1, p2, p3, p4, p5,
                                     a1, a2,
                                     b1, b2, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15,
                                     c1, c2,
                                     d1, d2,
                                     e1, e2, e3, e4, e5 ,e6, e7, e8,
                                     f1, f2,
                                     g1, g2,
                                     h1, h2, h3, h4, h5,
                                     i1, i2,
                                     j1, j2, j3]):
                sylfeat.extend(self._encodefeat(i, val))
            sylfeats.append(sylfeat)
            utt["sylpitchfeats"] = sylfeats
        return utt

    def synth(self, voice, utt, args):
        sylfeats = np.array(utt["sylpitchfeats"])
        heights = self.heightmodel.predict(sylfeats)
        slopes = self.slopemodel.predict(sylfeats)
        #put these into the utt in standard places:
        for syl, height, slope in zip(utt.gr("Syllable"), heights, slopes):
            syl["qta_endheight"] = height
            syl["qta_slope"] = slope
            syl["qta_lambd"] = self.strengthmax
        #pick up parameters from utt:
        # -- qta_startpitch for each phrase (inserted by main synthesiser -- HTS)
        # -- qta_endheight, qta_slope and qta_lambd for each syl
        # -- start and end for each syl (inserted by main synthesiser -- HTS)
        f0track = ttslab.qta.qta_synth_utt(utt, synthfunc=ttslab.qta.synth) #synth2 is the strength limiting algorithm [2]
        utt["f0track"] = f0track
        return utt
