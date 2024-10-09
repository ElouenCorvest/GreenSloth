#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilities 
"""
from copy import deepcopy
from typing import Union

# %%
import numpy as np
from modelbase.ode import Simulator
from modelbase.ode.models.model import Model


def pH(H):
    return -np.log10(H * 2.5e-4)


def pHinv(pH):
    return 4e3 * 10**-pH


def changingLight(
    model: Model,
    y0d: dict,
    lights: Union[np.ndarray, list],
    interval: Union[np.ndarray, list],
    exact_time: bool = False,
    exact_dt: int = 100,
):
    s = Simulator(deepcopy(model))
    s.initialise(y0d)
    dt = 0
    for i in range(len(interval)):
        if exact_time:
            dt_new = dt + interval[i]
            t = np.linspace(dt, float(dt_new), exact_dt)
            dt = dt_new
            s.simulate(
                time_points=t,
                **{"rtol": 1e-16, "atol": 1e-10, "maxnef": 20, "maxncf": 10}
            )
        else:
            s.update_parameter("PFD", lights[i])
            dt += interval[i]
            s.simulate(dt, **{"rtol": 1e-16, "atol": 1e-10, "maxnef": 20, "maxncf": 10})
    return s


def get_NPQ(
    F: Union[np.ndarray, list],
    t: Union[np.ndarray, list],
    lights: Union[np.ndarray, list],
    maxlight: int = 5000,
):
    z = (
        []
    )  # container for lists. Each list contains the positions of fluorescence values for one peak
    o = []  # container for position of Fo'
    cnt = 0
    while cnt < len(lights):
        if lights[cnt] == maxlight:
            h = (
                []
            )  # temporary container for all F==maxlight. For each peak it is renewed
            while cnt != len(lights) and lights[cnt] == maxlight:
                h.append(cnt)
                cnt += 1
            z.append(h)
            o.append(h[0] - 1)  # value directly at the bottom of peak is Fo
        else:
            cnt += 1
    peaks = [
        i[np.argmax(F[i])] for i in z
    ]  # Fm is the maximal value for each peak sequence
    Fm = F[peaks]
    tm = t[peaks]
    Fo = F[o]
    to = t[o]
    NPQ = (Fm[0] - Fm) / Fm
    PhiPSII = (Fm - Fo) / Fm  # see Baker2000
    return Fm, NPQ, tm, Fo, to, PhiPSII


def get_NPQ2(
    F: Union[np.ndarray, list],
    t: Union[np.ndarray, list],
    Ua: Union[np.ndarray, list],
    Q: Union[np.ndarray, list],
    lights: Union[np.ndarray, list],
    maxlight: int = 5000,
):
    z = (
        []
    )  # container for lists. Each list contains the positions of fluorescence values for one peak
    o = []  # container for position of Fo'
    cnt = 0
    while cnt < len(lights):
        if lights[cnt] == maxlight:
            h = (
                []
            )  # temporary container for all F==maxlight. For each peak it is renewed
            while cnt != len(lights) and lights[cnt] == maxlight:
                h.append(cnt)
                cnt += 1
            z.append(h)
            o.append(h[0] - 1)  # value directly at the bottom of peak is Fo
        else:
            cnt += 1
    peaks = [
        i[np.argmax(F[i])] for i in z
    ]  # Fm is the maximal value for each peak sequence
    Fm = F[peaks]
    tm = t[peaks]
    Uam = Ua[o]
    Qm = Q[o]
    Fo = F[o]
    to = t[o]
    NPQ = (Fm[0] - Fm) / Fm
    PhiPSII = (Fm - Fo) / Fm  # see Baker2000
    return Fm, NPQ, tm, Fo, to, PhiPSII, Uam, Qm


def FvFm_experiment(
    model: Model,
    y0d: dict,
    timestep: int = 60,
    tm_out: bool = True,
    SPint: int = 5000,
    HLint: int = 800,
    DARK: int = 0,
):
    Fo_lst = []
    Fm_lst = []
    FvFm_lst = []
    total_tm = []
    PAM1_lst = []
    Ua_lst = []
    abs_time = []
    # for i in [0, 0.5, 1, 3, 5, 6,]:
    for i in np.linspace(0, 20, 30):
        print(i)
        if i == 0:
            tprot = np.array([20 * 60, 0.8])
            ProtPFDs = np.array([DARK, SPint])
            PAM1 = changingLight(model, y0d, ProtPFDs, tprot)
            L = PAM1.get_variable("L")
            F = PAM1.get_variable("Fluo")
            t = PAM1.get_time()
            Ua = PAM1.get_variable("Uact")
            Q = PAM1.get_variable("Q")
            Fm, NPQ, tm, Fo, to, PhiPSII, Uam, Qm = get_NPQ2(
                F, t, Ua, Q, L, maxlight=SPint
            )
            FvFm = (Fm - Fo) / Fm
            FvFm_lst.append(FvFm)
            Fo_lst.append(Fo)
            Fm_lst.append(Fm)
            total_tm.append(tm)
            PAM1_lst.append(PAM1)
            Ua_lst.append(Uam)
            abs_time.append(i)
        else:
            tprot = np.array([20 * 60, i * 60 * timestep, 20 * 60, 0.8])
            ProtPFDs = np.array([DARK, HLint, DARK, SPint])
            PAM1 = changingLight(model, y0d, ProtPFDs, tprot)
            L = PAM1.get_variable("L")
            F = PAM1.get_variable("Fluo")
            t = PAM1.get_time()
            Ua = PAM1.get_variable("Uact")
            Q = PAM1.get_variable("Q")
            Fm, NPQ, tm, Fo, to, PhiPSII, Uam, Qm = get_NPQ2(
                F, t, Ua, Q, L, maxlight=SPint
            )
            FvFm = (Fm - Fo) / Fm
            FvFm_lst.append(FvFm)
            Fm_lst.append(Fm)
            Fo_lst.append(Fo)
            total_tm.append(tm)
            PAM1_lst.append(PAM1)
            Ua_lst.append(Uam)
            abs_time.append(i)
    if tm_out is True:
        return FvFm_lst, Fm_lst, Fo_lst, np.array(total_tm), PAM1_lst, Ua_lst, abs_time
    else:
        return FvFm_lst


def FvFm_experiment2(
    model: Model,
    y0d: dict,
    timestep: int = 60,
    tm_out: bool = True,
    SPint: int = 5000,
    HLint: int = 800,
    DARK: int = 0,
    PAM_out: bool = False,
    exact_time: bool = False,
):
    Fo_lst = []
    Fm_lst = []
    FvFm_lst = []
    total_tm = []
    absolute_tm = []  # time as given in the function
    PAM1_lst = []

    if exact_time:
        timespace = np.arange(0, 6.1, 0.1)
    else:
        timespace = np.linspace(0, 6, 50)
    for i in timespace:
        print(i)
        if i == 0:
            tprot = np.array([20 * 60, 0.8])
            ProtPFDs = np.array([DARK, SPint])
            PAM1 = changingLight(model, y0d, ProtPFDs, tprot)
            L = PAM1.get_variable("L")
            F = PAM1.get_variable("Fluo")
            t = PAM1.get_time()
            Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(F, t, L, maxlight=SPint)
            FvFm = (Fm - Fo) / Fm
            FvFm_lst.append(FvFm)
            Fo_lst.append(Fo)
            Fm_lst.append(Fm)
            total_tm.append(tm)
            absolute_tm.append(i)
            PAM1_lst.append(PAM1)
        else:
            tprot = np.array([20 * 60, i * 60 * timestep, 20 * 60, 0.8])
            ProtPFDs = np.array([DARK, HLint, DARK, SPint])
            PAM1 = changingLight(model, y0d, ProtPFDs, tprot)
            L = PAM1.get_variable("L")
            F = PAM1.get_variable("Fluo")
            t = PAM1.get_time()
            Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(F, t, L, maxlight=SPint)
            FvFm = (Fm - Fo) / Fm
            FvFm_lst.append(FvFm)
            Fm_lst.append(Fm)
            Fo_lst.append(Fo)
            total_tm.append(tm)
            absolute_tm.append(i)
            PAM1_lst.append(PAM1)
    if tm_out is True:
        if PAM_out is True:
            return (
                FvFm_lst,
                Fm_lst,
                Fo_lst,
                np.array(total_tm),
                np.array(absolute_tm),
                PAM1_lst,
            )
        else:
            return FvFm_lst, Fm_lst, Fo_lst, np.array(total_tm), np.array(absolute_tm)
    else:
        return FvFm_lst
