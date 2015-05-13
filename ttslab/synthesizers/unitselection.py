# -*- coding: utf-8 -*-
"""Contains a basic RELP-based unit-selection synthesizer
   implementation similar to the "MultiSyn" implementation in
   Festival:

   R. A. J. Clark, K. Richmond, and S. King, "Multisyn: Open-domain
   unit selection for the Festival speech synthesis system," Speech
   Communication, vol. 49, no. 4, pp. 317–330, 2007.

   ---------
   Need ways of documenting and ensuring requirements for
   processors...

   TODO:
      - Modularize and clean up handling of certain parms such as
        samplerate, samplewidth etc.
      - Clean up implementation: Initially the Viterbi used joincost
        and targetcost methods, however after optimisation, joinscore
        calculation was integrated into selectunits method.
      - Rewrite code to use only numpy arrays cleanly...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import copy
from collections import OrderedDict

import numpy as np
from scipy.spatial.distance import cdist

import ttslab
from ttslab.waveform import Waveform

import ttslab.synthesizer
from ttslab.synthesizers.relp import synth_filter

SAMPLERATE = 16000
WINDOWFACTOR = 1
#using the hamming window: np.hamming

def window_residual(lpctrack, residual):
    """ creates frames of windowed residual around lpc center
        times
        DEMITASSE: Review for possible off by one errors
    """
    residual = residual.flatten()
    prevtime = 0.0
    residuals = []
    for i in range(len(lpctrack)):
        # if i == len(lpctrack) - 1: #last coef:
        #     nexttime = len(residual) / SAMPLERATE
        # else:
        #     nexttime = lpctrack.times[i+1]

        halfperiod = lpctrack.times[i] - prevtime
        centersample = int(round(lpctrack.times[i] * SAMPLERATE))
        firsttime = lpctrack.times[i] - (halfperiod * WINDOWFACTOR)
        firstsample = int(round(firsttime * SAMPLERATE))
        lastsample = centersample + (centersample - firstsample) #could overflow

        res = residual[firstsample:lastsample+1]
        res = np.hamming(len(res)) * res
        residuals.append(res)
        prevtime = lpctrack.times[i]

    return residuals


class Synthesizer(ttslab.synthesizer.Synthesizer):
    """ Implementation with halfphone units... 
    """
    def __init__(self, unitcataloguefile=None):
        if unitcataloguefile:
            self._load_unitcatalogue(unitcataloguefile)

    def _load_unitcatalogue(self, unitcataloguefile):
        self.unitcatalogue = ttslab.fromfile(unitcataloguefile)


    def feats(self, voice, utt, args):
        """ Create target units for synthesis.. (halfphones)
        """
        unit_rel = utt.new_relation("Unit")
        seglist = utt.get_relation("Segment").as_list()
        for i, seg in enumerate(seglist):
            #determine relevant unit features...
            num_syls_in_word = self._countsyls(seg)
            position_in_syl = self._getsylposition(seg)
            position_in_word = self._getwordposition(seg)
            position_in_phrase = self._getphraseposition(seg)
            context_nextsegment = seg.traverse("n.F:name") #can be None
            context_prevsegment = seg.traverse("p.F:name") #can be None

            # #don't do unnecessary "pau" joins at start of utterance:
            if not (i == 0 and seg["name"] == "pau"):
                lunit_item = unit_rel.append_item()
                lunit_item["name"] = "left-" + seg["name"]
                seg.add_daughter(lunit_item)
                lunit_item["num_syls"] = num_syls_in_word
                lunit_item["position_in_syl"] = position_in_syl
                lunit_item["position_in_word"] = position_in_word
                lunit_item["position_in_phrase"] = position_in_phrase
                lunit_item["context_nextsegment"] = context_nextsegment
                lunit_item["context_prevsegment"] = context_prevsegment

            # #don't do unnecessary "pau" joins at end of utterance:
            if not (i == len(seglist) - 1 and seg["name"] == "pau"):
                runit_item = unit_rel.append_item()
                runit_item["name"] = "right-" + seg["name"]
                seg.add_daughter(runit_item)
                runit_item["num_syls"] = num_syls_in_word
                runit_item["position_in_syl"] = position_in_syl
                runit_item["position_in_word"] = position_in_word
                runit_item["position_in_phrase"] = position_in_phrase
                runit_item["context_nextsegment"] = context_nextsegment
                runit_item["context_prevsegment"] = context_prevsegment
        return utt

    
    def synth(self, voice, utt, args):
        utt = self._selectunits(utt, args)
        utt = self._concatunits(utt, args)
        return utt

    #################### Lower level synth methods...
    def _selectunits(self, utt, args):
        """ Does a Viterbi search given the target Utterance and
            unitcatalogue, using the joinscore and targetscore
            functions defined... Update: joinscore calculation
            integrated here...
        """

        unit_rel = utt.get_relation("Unit")

        prunescoredelta = 0.01
        prunenumcands = 100
        trellis = []
        unit_item = unit_rel.head_item
        #t = 0:
        trellis.append([{"candidate": cand, "prevcandidate": None, "total_score": 0.0}
                        for cand in self.unitcatalogue[unit_item["name"]]])
        unit_item = unit_item.next_item
        #viterbi
        while unit_item is not None:
            # #feedback:
            # stime = time.time()
            # print(unit_item["name"],
            #       len(trellis[-1]), "x", len(self.unitcatalogue[unit_item["name"]]),
            #       "comparisons")
            #calc joinscores:
            a = np.array([c["left-joincoef"] for c in self.unitcatalogue[unit_item["name"]]])
            b = np.array([c["candidate"]["right-joincoef"] for c in trellis[-1]])
            distmatrix = cdist(a, b, "euclidean")
            scorematrix = 6 / (distmatrix + 6)
            #calc targetscores, combine with joinscores and save in trellis
            currentnode = []
            targetscores_i = np.array([self._targetscore(unit_item, nextcandidate) for
                                       nextcandidate in self.unitcatalogue[unit_item["name"]]])
            prevtotalscores_j = np.array([prevcandidate["total_score"] for prevcandidate in trellis[-1]])
            for i in range(len(self.unitcatalogue[unit_item["name"]])):
                scorematrix[i,:] += prevtotalscores_j
            for j in range(len(trellis[-1])):
                scorematrix[:,j] += targetscores_i
            for i, nextcandidate in enumerate(self.unitcatalogue[unit_item["name"]]):
                currentnode.append({"candidate": nextcandidate,
                                    "prevcandidate": np.argmax(scorematrix[i,:]),
                                    "total_score": np.max(scorematrix[i,:])})
            #candidate pruning:
            ##based on score delta:
            currbestcand = currentnode[np.array([n["total_score"] for n in currentnode]).argmax()]
            currentnode = [n for n in currentnode if
                           n["total_score"] > currbestcand["total_score"] - \
                               (prunescoredelta * currbestcand["total_score"])]
            ##based on numcands:
            if len(currentnode) > prunenumcands:
                currentnode.sort(key=lambda x: x["total_score"], reverse=True)
                currentnode = currentnode[:prunenumcands]
            # print("added %s candidates" % len(currentnode))
            trellis.append(currentnode)
            unit_item = unit_item.next_item
            # print("done in", time.time() - stime, "seconds...")

            # nodes = []
            # for nextcandidate in self.unitcatalogue[unit_item["name"]]:
            #     targetscore = self._targetscore(unit_item, nextcandidate)
            #     total_scores = []
            #     for prevcandidate in trellis[-1]:
            #         total_scores.append(prevcandidate["total_score"] +
            #                             targetscore * self._joinscore(prevcandidate["candidate"], nextcandidate))
            #     nodes.append({"candidate": nextcandidate,
            #                   "prevcandidate": np.argmax(total_scores),
            #                   "total_score": np.max(total_scores)})
            # trellis.append(nodes)
            # unit_item = unit_item.next_item
            # print("done in", time.time() - stime, "seconds...")

        #traceback
        bestpath = []
        bestindex = np.argmax([node["total_score"] for node in trellis[-1]])
        #print(bestindex)
        for t in reversed(trellis):
            bestnode = t[bestindex]
            #print(bestnode["total_score"], bestnode["prevcandidate"])
            bestpath.append(bestnode)
            bestindex = bestnode["prevcandidate"]
        bestpath = list(reversed(bestpath))
        
        #add best candidates to utt
        index = 0
        unit_item = unit_rel.head_item
        while unit_item is not None:
            unit_item["selected_unit"] = bestpath[index]
            index += 1
            unit_item = unit_item.next_item
            
        ### DEMITASSE: this block needs to live somewhere else, this
        ### method needs to be independent of unit type...
        # #put (approximate) endtimes in segs:
        # starttime = 0.0
        # for seg in utt.gr("Segment"):
        #     seg["end"] = starttime + sum([unit["selected_unit"]["candidate"]["dur"] for unit in seg.get_daughters()])
        #     starttime = seg["end"]

        return utt

    
    def _concatunits(self, utt, args):
        """ Concatenates units and produces waveform via residual
            excited LPC synthesis filter...
        """
        
        unit_rel = utt.get_relation("Unit")
        #concat:
        unit_item = unit_rel.head_item
        lpctrack = copy.deepcopy(unit_item["selected_unit"]["candidate"]["lpc-coefs"])
        residuals = window_residual(unit_item["selected_unit"]["candidate"]["lpc-coefs"],
                                    unit_item["selected_unit"]["candidate"]["residuals"])
        unit_item = unit_item.next_item
        while unit_item is not None:
            temptrack = unit_item["selected_unit"]["candidate"]["lpc-coefs"]
            #append lpccoefs to lpctrack:
            lpctrack.times = np.concatenate((lpctrack.times, (temptrack.times + lpctrack.times[-1])))
            lpctrack.values = np.concatenate((lpctrack.values, temptrack.values))
            #append windowed residuals:
            residuals.extend(window_residual(temptrack,
                                             unit_item["selected_unit"]["candidate"]["residuals"]))
            unit_item = unit_item.next_item
        
        #overlap add residual:
        lastsample = int(round(lpctrack.times[-1] * SAMPLERATE)) + int(round(len(residuals[-1]) / 2))
        residual = np.zeros(lastsample + 1)

        for i, time in enumerate(lpctrack.times):
            centersample = int(round(time * SAMPLERATE))
            firstsample = centersample - int(len(residuals[i]) / 2)
            residual[firstsample:firstsample+len(residuals[i])] += np.array(residuals[i])

        #synth filter:
        samples = synth_filter(lpctrack.times, lpctrack.values, residual.astype(np.float), SAMPLERATE)

        #save in utterance:
        w = Waveform()
        w.samplerate = SAMPLERATE
        w.samples = samples.astype("int16") #16bit samples
        w.channels = 1
        utt["waveform"] = w
        return utt


    #################### "Feature functions" -- for HTS this is in hts_label.py...
    def _countsyls(self, segitem):
        """ Determine the number of syllables of the Word to which
            this Segment belongs...
        """
        seg_in_sylstructure = segitem.get_item_in_relation("SylStructure")
        if not seg_in_sylstructure:
            return None
        else:
            counter = 0
            syl_item = seg_in_sylstructure.parent_item.parent_item.first_daughter
            while syl_item is not None:
                counter += 1
                syl_item = syl_item.next_item
            return counter
        
    def _getsylposition(self, segitem):
        """ Determine the position of a Segment in its parent
            Syllable..
        """
        seg_in_sylstructure = segitem.get_item_in_relation("SylStructure")
        if not seg_in_sylstructure:
            return None
        elif seg_in_sylstructure.next_item and seg_in_sylstructure.prev_item:
            return "medial"
        elif seg_in_sylstructure.next_item and not seg_in_sylstructure.prev_item:
            return "initial"
        elif not seg_in_sylstructure.next_item and seg_in_sylstructure.prev_item:
            return "final"
    
    def _getwordposition(self, segitem):
        """ Determine the position of the Segment's parent Syllable in
            the Word to which they belong..
        """
        seg_in_sylstructure = segitem.get_item_in_relation("SylStructure")
        if not seg_in_sylstructure:
            return None
        else:
            syl_item = seg_in_sylstructure.parent_item
            if syl_item.next_item and syl_item.prev_item:
                return "medial"
            elif syl_item.next_item and not syl_item.prev_item:
                return "initial"
            elif not syl_item.next_item and syl_item.prev_item:
                return "final"

    def _getphraseposition(self, segitem):
        """ Determine the position of the Segment's Word in the Phrase
            to which they belong..
        """
        seg_in_sylstructure = segitem.get_item_in_relation("SylStructure")
        if not seg_in_sylstructure:
            return None
        else:
            word_item = seg_in_sylstructure.parent_item.parent_item
            if word_item.next_item and word_item.prev_item:
                return "medial"
            elif word_item.next_item and not word_item.prev_item:
                return "initial"
            elif not word_item.next_item and word_item.prev_item:
                return "final"
        
    def _targetscore(self, targetunit, candidateunit):
        """ Calculates a (crude) value representing a level of match
            between target and candidate units, based on linguistic
            questions... value range: [0.0, 1.0]
        """
        score = 0.0
        tsylls = targetunit["num_syls"]
        csylls = candidateunit["num_syls"]
        try:
            if csylls >= tsylls:
                score += tsylls / csylls
            else:
                score += csylls / tsylls
        except TypeError: #must be None..
            score += 1.0
        if targetunit["position_in_syl"] == candidateunit["position_in_syl"]:
            score += 1.0
        if targetunit["position_in_word"] == candidateunit["position_in_word"]:
            score += 1.0
        if targetunit["position_in_phrase"] == candidateunit["position_in_phrase"]:
            score += 1.0
        if targetunit["context_nextsegment"] == candidateunit["context_nextsegment"]:
            score += 1.0
        if targetunit["context_prevsegment"] == candidateunit["context_prevsegment"]:
            score += 1.0
        return score / 6.0

    # def _joinscore(self, unit1, unit2):
    #     """ Calculates a value representing a level of match between
    #         two consecutive candidate units based on acoustic
    #         similarity.. value range: (0.0, 1.0]
    #     """
        
    #     fa = unit1["right-joincoef"]
    #     fb = unit2["left-joincoef"]

    #     #fa and fb need to be numpy arrays...
    #     euclidian_distance = math.sqrt(((fa - fb)**2).sum())

    #     #6 is a scaling factor...
    #     return 6 / (6 + euclidian_distance)
