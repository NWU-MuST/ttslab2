#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implementation of "Quantitative Target Approximation":

    S. Prom-On, Y. Xu, and B. Thipakorn, "Modeling tone and intonation
    in Mandarin and English as a process of target approximation," The
    Journal of the Acoustical Society of America, vol.  125,
    pp. 405–424, 2009.

    Specifically: 

      - The critically-damped synthesis of a syllable contour from
        initial conditions and underlying linear target function is
        implemented in qta_sylcontour.sylcontour
      - 

    This is like qta2.py but here we and set the starting velocity to
    zero if a pause is present before the syllable. If a syllable has
    no valid F0 values, we use linear interpolation.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys
import math
import time
import cPickle as pickle

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

import ttslab
from ttslab.trackfile import Track
ttslab.extend(Track, "ttslab.trackfile.funcs.tfuncs_praat")
from ttslab.hrg import Utterance
ttslab.extend(Utterance, "ttslab.ufuncs.analysis")

from qta_sylcontour import sylcontour
# def sylcontour(t, m, b, p0, dp0, ddp0, l):
#     xt = np.polyval([m, b], t)
#     # pl.plot(t, xt, linestyle="dashed", color="red")
#     c1 = p0 - b
#     c2 = dp0 + c1 * l - m
#     c3 = (ddp0 + 2 * c2 * l - c1 * l ** 2) / 2.0
#     pt = xt + (c1 + c2*t + c3*t**2) * np.exp(-l * t)
#     return pt

STARTLAB = "start"
ENDLAB = "end"
QTAPREFIX = "qta"

DEF_F0MIN = 60.0  #Hz
DEF_F0MAX = 350.0 #Hz
DEF_PITCHRANGE = [12.0 * np.log2(DEF_F0MIN),
                  12.0 * np.log2(DEF_F0MAX)]  #semitones relative to
#1Hz, equiv to: 50.0 - 250.0 Hz quantization of the pitch range for
#analysis-by-synthesis search, approximate resolution 1/4 st:
DEF_PITCHSTEPS = int((DEF_PITCHRANGE[1] - DEF_PITCHRANGE[0]) / 0.25)

# This defines the granularity and search ranges for the
# analysis-by-synthesis process for the three parameters: pitch, slope
# and lambda (strength of articulation). We also allow for defining
# these parameters seperately for different contexts (see Yoruba
# example below). These contexts are retrieved by querying the
# "qtaparmclass" feature of the syllable item.

DEF_QTASPECS = {"pitch": DEF_PITCHRANGE + [DEF_PITCHSTEPS],
                "slope": [-60.0, 60.0, 31],
                "lambd": [40.0, 80.0, 17],
                "xcept": {}
                }

#### FOR QUICK DEBUGGING USE THIS:
# DEF_QTASPECS = {"pitch": DEF_PITCHRANGE + [31],
#                 "slope": [0.0, 0.0, 1],
#                 "lambd": [40.0, 80.0, 9],
#                 "xcept": {}
#                 }

#### Example for parameter extraction in Yoruba (see Interspeech paper 2014)
# DEF_QTASPECS_FULL = {"pitch": DEF_PITCHRANGE + [DEF_PITCHSTEPS],
#                      "slope": [0.0, 0.0, 1],
#                      "lambd": [40.0, 120.0, 17],
#                      "xcept": {"H": {"pitch": DEF_PITCHRANGE + [DEF_PITCHSTEPS],
#                                      "slope": [0.0, 60.0, 16],
#                                      "lambd": [40.0, 120.0, 17]},
#                                "L": {"pitch": DEF_PITCHRANGE + [DEF_PITCHSTEPS],
#                                      "slope": [-60.0, 0.0, 16],
#                                      "lambd": [40.0, 120.0, 17]}}
#                      }


def get_intercept(t, val, slope):
    """Get intercept for linear function given value at time and slope
    """
    #y = mx + c
    c = val - slope * t
    return c

#This function should ideally be used to extract parms for syllable
#sequences *within a breath group* or similar relevant context...
def get_synthparms(syls, f0, startpitch, qtaspecs):
    syls = [syl.gir("Syllable") for syl in syls]

    endheights = np.linspace(qtaspecs["pitch"][0],
                             qtaspecs["pitch"][1],
                             qtaspecs["pitch"][2])
    slopes = np.linspace(qtaspecs["slope"][0],
                         qtaspecs["slope"][1],
                         qtaspecs["slope"][2])
    lambds = np.linspace(qtaspecs["lambd"][0],
                         qtaspecs["lambd"][1],
                         qtaspecs["lambd"][2])
    xcepts = qtaspecs["xcept"]

    times = []
    contiguous = []
    for i, syl in enumerate(syls):
        times.append([syl[STARTLAB], syl[ENDLAB]])
        if i == 0:
            contiguous.append(False)
        else:
            if times[-2][1] != times[-1][0]:
                contiguous.append(False)
            else:
                contiguous.append(True)

    synthparms = []
    sylmses = []
    for i, iscont, tbounds, syl in zip(range(len(syls)), contiguous, times, syls):
        #set initial conditions
        if i == 0:
            p0 = startpitch
            dp0 = 0.0
            ddp0 = 0.0
        if not iscont: #if not contiguous, we reset the pitch dynamics but keep "p0"
            dp0 = 0.0
            ddp0 = 0.0
        #special context parameter ranges:
        sylcontext = syl["qtaparmclass"] #can be None
        if sylcontext in xcepts:
            xparms = xcepts[sylcontext]
            l_endheights = np.linspace(xparms["pitch"][0], xparms["pitch"][1], xparms["pitch"][2])
            l_slopes = np.linspace(xparms["slope"][0], xparms["slope"][1], xparms["slope"][2])
            l_lambds = np.linspace(xparms["lambd"][0], xparms["lambd"][1], xparms["lambd"][2])
        else:            
            l_endheights = endheights
            l_slopes = slopes
            l_lambds = lambds
        #get f0 contour for this syllable, interpolate if completely
        #unvoiced (this should theoretically not be possible but may
        #occur because of extraction and/or alignment errors):
        f0syl = f0.slice(f0.index_at(tbounds[0]), f0.index_at(tbounds[1]))
        try:
            assert len(f0syl.values.ravel().nonzero()[0]) > 0
        except AssertionError:
            f0syl = f0.newtrack_from_linearinterp(f0.times[f0.index_at(tbounds[0]):f0.index_at(tbounds[1])], ignore_zeros=True)
        #search over parameters to minimise MSE
        parms = np.zeros((len(l_endheights) * len(l_slopes) * len(l_lambds), 3))
        mses = np.zeros(len(l_endheights) * len(l_slopes) * len(l_lambds))
        i = 0
        syl_t = f0syl.times - f0syl.times[0]
        for endheight in l_endheights:
            for slope in l_slopes:
                for l in l_lambds:
                    parms[i][0] = endheight
                    parms[i][1] = slope
                    parms[i][2] = l
                    #syltarget = mx + c
                    syltarget_m = slope
                    syltarget_c = get_intercept(syl_t[-1], endheight, slope)
                    a = sylcontour(syl_t, syltarget_m, syltarget_c, p0, dp0, ddp0, l)
                    nonzeroindices = f0syl.values.ravel().nonzero()
                    mses[i] = np.mean((f0syl.values.ravel()[nonzeroindices] - a[nonzeroindices]) ** 2)
                    i += 1
        #process the best parms:
        bestparms = parms[np.argmin(mses)]
        syltarget_m = bestparms[1]
        syltarget_c = get_intercept(syl_t[-1], bestparms[0], bestparms[1])
        a = sylcontour(syl_t, syltarget_m, syltarget_c, p0, dp0, ddp0, bestparms[2])
        synthparms.append([tbounds[0], tbounds[1], bestparms[0], bestparms[1], bestparms[2]])
        sylmses.append(np.min(mses))
        #calculate initial conditions for next syllable
        spline = InterpolatedUnivariateSpline(syl_t, a)
        p0, dp0, ddp0, unused = spline.derivatives(syl_t[-1])
    return synthparms, sylmses

def synth(startpitch, synthparms, numpoints=100, plot=False):
    times = np.zeros(len(synthparms) * numpoints)
    contour = np.zeros(len(synthparms) * numpoints)
    for i, synthparm in enumerate(synthparms):
        if i == 0:
            p0 = startpitch
            dp0 = 0.0
            ddp0 = 0.0
        if synthparm[0] != synthparms[i-1][1]: #not contiguous (e.g. a pause is present)
            dp0 = 0.0
            ddp0 = 0.0
        if any([e is None for e in synthparm]): #no parameters available for this syllable, skip...
            dp0 = 0.0
            ddp0 = 0.0
            continue
        utt_t = np.linspace(synthparm[0], synthparm[1], numpoints, endpoint=False)
        times[i*numpoints:i*numpoints+numpoints] = utt_t
        syl_t = utt_t - synthparm[0] #start at 0.0
        #y = mx + c
        syltarget_m = synthparm[3]
        syltarget_c = get_intercept(syl_t[-1], synthparm[2], synthparm[3])
        scontour = sylcontour(syl_t, syltarget_m, syltarget_c, p0, dp0, ddp0, synthparm[4])
        if plot:
            pl.plot(syl_t + synthparm[0], np.polyval(coefs, syl_t), linestyle="dashed", color="red")
            pl.plot(syl_t + synthparm[0], scontour, color="green")
        spline = InterpolatedUnivariateSpline(syl_t, scontour)
        contour[i*numpoints:i*numpoints+numpoints] = scontour
        p0, dp0, ddp0, temp = spline.derivatives(syl_t[-1])
    synthtrack = Track()
    synthtrack.times = times[contour.nonzero()].copy()
    synthtrack.values = contour[contour.nonzero()].reshape((-1, 1)).copy()
    return synthtrack

def synth2(startpitch, synthparms, numpoints=100, plot=False, minlambd=10.0, dlambd=5.0):
    """ Limit the strength of articulation to avoid acceleration in
        opposite direction of endheight target...
    """
    times = np.zeros(len(synthparms) * numpoints)
    contour = np.zeros(len(synthparms) * numpoints)
    for i, synthparm in enumerate(synthparms):
        if i == 0:
            p0 = startpitch
            dp0 = 0.0
            ddp0 = 0.0
        if synthparm[0] != synthparms[i-1][1]: #not contiguous (e.g. a pause is present)
            dp0 = 0.0
            ddp0 = 0.0
        if any([e is None for e in synthparm]): #no parameters available for this syllable, skip...
            dp0 = 0.0
            ddp0 = 0.0
            continue
        utt_t = np.linspace(synthparm[0], synthparm[1], numpoints, endpoint=False)
        times[i*numpoints:i*numpoints+numpoints] = utt_t
        syl_t = utt_t - synthparm[0] #start at 0.0
        #y = mx + c
        syltarget_m = synthparm[3]
        syltarget_c = get_intercept(syl_t[-1], synthparm[2], synthparm[3])
        while True: #resynthesise with lower strength until constraint met
            scontour = sylcontour(syl_t, syltarget_m, syltarget_c, p0, dp0, ddp0, synthparm[4])
            spline = InterpolatedUnivariateSpline(syl_t, scontour)
            #check acceleration
            if synthparm[4] <= minlambd:
                break
            accels = spline(syl_t, 2)
            if synthparm[2] > p0:
                if np.all(accels > 0.0):
                    break
            elif synthparm[2] < p0:
                if np.all(accels < 0.0):
                    break
            else:
                break
            synthparm[4] -= dlambd
            if synthparm[4] < minlambd:
                synthparm[4] = minlambd
        if plot:
            pl.plot(syl_t + synthparm[0], np.polyval(coefs, syl_t), linestyle="dashed", color="red")
            pl.plot(syl_t + synthparm[0], scontour, color="green")
        contour[i*numpoints:i*numpoints+numpoints] = scontour
        p0, dp0, ddp0, temp = spline.derivatives(syl_t[-1])
    synthtrack = Track()
    synthtrack.times = times[contour.nonzero()].copy()
    synthtrack.values = contour[contour.nonzero()].reshape((-1, 1)).copy()
    return synthtrack


def qta_annotate_utt(utt, f0, qtaspecs=DEF_QTASPECS):
    utt[QTAPREFIX + "_specs"] = qtaspecs
    for phr in utt.gr("Phrase"):
        syls = []
        for word in phr.get_daughters():
            syls.extend(word.gir("SylStructure").get_daughters())
        #startpitch defined as the mean of the first quarter of nonzero
        #values of the first syllable:
        f0syl0 = f0.slice(f0.index_at(syls[0][STARTLAB]), f0.index_at(syls[0][ENDLAB]))
        f0nonzerovals = f0syl0.values.flatten()[f0syl0.values.flatten().nonzero()]
        if len(f0nonzerovals) >= 4:
            startpitch = np.mean(f0nonzerovals[:len(f0nonzerovals)//4])
        elif len(f0nonzerovals) != 0:
            startpitch = f0nonzerovals[0]
        else:
            startpitch = DEF_PITCHRANGE[0]
        phr[QTAPREFIX + "_startpitch"] = startpitch
        ####
        qtaparms, sylmses = get_synthparms(syls, f0, startpitch, qtaspecs)
        phr[QTAPREFIX + "_sylmses"] = sylmses
        for qtap, syl in zip(qtaparms, syls):
            syl[QTAPREFIX + "_endheight"] = qtap[2]
            syl[QTAPREFIX + "_slope"] = qtap[3]
            syl[QTAPREFIX + "_lambd"] = qtap[4]
    return utt


def qta_synth_utt(utt, synthfunc=synth):
    times = np.array([])
    values = np.array([])
    for phr in utt.gr("Phrase"):
        synthparms = []
        for word in phr.get_daughters():
            for syl in word.gir("SylStructure").get_daughters():
                synthparms.append([syl[STARTLAB], syl[ENDLAB], syl[QTAPREFIX + "_endheight"], syl[QTAPREFIX + "_slope"], syl[QTAPREFIX + "_lambd"]])
        phrf0track = synthfunc(phr[QTAPREFIX + "_startpitch"], synthparms)
        times = np.concatenate((times, phrf0track.times))
        values = np.concatenate((values, phrf0track.values.flatten()))
    f0track = Track()
    f0track.times = times
    f0track.values = values.reshape((-1, 1))
    return f0track


def plotstuff(utt, f0track, qtaf0track, ymin=DEF_PITCHRANGE[0]-5.0, ymax=DEF_PITCHRANGE[1]+5.0, title=None):
    def sylpron(syl):
        syl = syl.gir("SylStructure")
        return "[" + "".join([seg["name"] for seg in syl.get_daughters()]) + "]"
    import pylab as pl
    pl.plot(f0track.times, f0track.values)
    pl.plot(qtaf0track.times, qtaf0track.values)
    syls = utt.gr("Syllable").as_list()
    pl.xticks([syl[ENDLAB] for syl in syls], [syl["tone"] + ":" + sylpron(syl) for syl in syls])
    for syl in syls:
        t = np.linspace(syl[STARTLAB], syl[ENDLAB], 100, endpoint=False)
        try:
            syltarget_m = syl[QTAPREFIX + "_slope"]
            syltarget_c = get_intercept(t[-1], syl[QTAPREFIX + "_endheight"], syl[QTAPREFIX + "_slope"])
            coefs = (syltarget_m, syltarget_c)
            pl.plot(t, np.polyval(coefs, t), linestyle="dashed", color="red")
        except TypeError: #if no qta parameters exist
            pass
    pl.axis([None, None, ymin, ymax])
    pl.ylabel("Pitch (semitones)")
    pl.xlabel("Time (syllables)")
    pl.grid()
    pl.title(title or utt["file_id"])
    pl.show()

def utt_plot(utt, f0, qtaspecs=DEF_QTASPECS, annotate=True):
    if annotate:
        t0 = time.time()
        utt = qta_annotate_utt(utt, f0, qtaspecs)
        #report processing time
        print("qta annotate took: %s seconds" % (time.time() - t0))
        #report mean sylrmse
        uttsylmses = []
        for phr in utt.gr("Phrase"):
            uttsylmses.extend(phr["qta_sylmses"])
        print("Mean syl rmses: %s" % np.mean(map(math.sqrt, [e for e in uttsylmses if e is not None])))
        #print(utt.gr("Syllable"))
    qtaf0 = qta_synth_utt(utt)
    plotstuff(utt, f0, qtaf0)

def main(utt, f0, qtaspecs=DEF_QTASPECS):
    utt = qta_annotate_utt(utt, f0, qtaspecs)
    print(pickle.dumps(utt, protocol=2))


if __name__ == "__main__":
    utt = ttslab.fromfile(sys.argv[1])
    f0 = ttslab.fromfile(sys.argv[2])

    utt.fill_startendtimes()
    main_test(utt, f0)
    #main(utt, f0)
