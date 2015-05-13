# -*- coding: utf-8 -*-
""" Straightforward adaptation of unitselection synthesizer
    to use word units...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab.synthesizers.unitselection

class Synthesizer(ttslab.synthesizers.unitselection.Synthesizer):        

    def feats(self, voice, utt, processname):
        """ Create target units for synthesis.. (words)
        """
        unit_rel = utt.new_relation("Unit")
        wordseq = utt.gr("Word").as_list()
        for i, word in enumerate(wordseq):
            context_nextword = word.traverse("n.F:name") #can be None
            context_prevword = word.traverse("p.F:name") #can be None
            
            unit_item = unit_rel.append_item()
            unit_item["name"] = word["name"]
            unit_item["context_prevword"] = context_prevword
            unit_item["context_nextword"] = context_nextword
        return utt

    #################### Lower lower level methods...
        
    def _targetscore(self, targetunit, candidateunit):
        """ Calculates a (crude) value representing a level of match
            between target and candidate units, based on linguistic
            questions... value range: [0.0, 1.0]
        """
        score = 0.0
        if targetunit["context_prevword"] == candidateunit["context_prevword"]:
            score += 0.5
        if targetunit["context_nextword"] == candidateunit["context_nextword"]:
            score += 0.5
        return score
