#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parameters for the photoinhibtion model
"""

import numpy as np

from .utils import pH

pdict = {
    # Pool sizes
    "PSIItot": 2.5,  # PSII reaction centres
    "PQtot": 20,  # PQ + PQH2
    "APtot": 50,  # total adenosine phosphate pool (ATP + ADP)
    "PsbStot": 1,  # LHCII normalized
    "PCtot": 4,
    "PSItot": 2.5,
    "Fdtot": 5,
    "NADPtot": 25,
    "Xtot": 1,  # toal xanthophylls
    "O2ext": 8,  # external oxygen
    "Pi": 0.01,  # internal pool of phosphates
    "bH": 100,
    "HPR": 14.0 / 3.0,
    "pHstroma": 7.8,
    "kleak": 100,
    # Rate constants and key parameters
    "kCytb6f": 2.5,
    "kActATPase": 0.01,
    "kDeactATPase": 0.002,
    "kATPsynthase": 20.0,
    "kATPconsumption": 10,
    "kNADPHconsumption": 20,
    "kPQred": 250.0,
    "kH": 5e9,
    "kF": 6.25e8,
    "kP": 5e9,
    "kT": 9e8,
    # Parameter associated with xanthophyll cycle
    "kDeepoxV": 0.0024,
    "kEpoxZ": 0.00024,
    "KphSatZ": 5.8,
    "nHX": 5.0,
    "Kzsat": 0.12,
    # Parameter associated with PsbS protonation
    "nHL": 3,
    "kDeprot": 0.0096,
    "kProt": 0.0096,
    "KphSatLHC": 5.8,
    # quencher contribution factors
    "gamma0": 0.1,
    "gamma1": 0.25,
    "gamma2": 0.6,
    "gamma3": 0.105,
    "gamma4": 1.01,  # slow quenching
    "slow_quenching": False,
    # Physical constants
    "F": 96.485,
    "R": 8.3e-3,  # J in KJ
    "T": 298,
    # Standard potentials
    "E0QAQAm": -0.140,
    "E0PQPQH2": 0.354,
    "E0PCPCm": 0.380,
    "DG0ATP": 30.6,
    "E0FAFAm": -0.550,
    "E0FdFdm": -0.430,
    "E0P700pP700": 0.480,
    "E0NADPNADPH": -0.113,
    # PFD
    "PFD": 100,
    # PSI
    "kPCox": 2500,
    "kFdred": 2.5e5,
    # FNR
    "EFNR": 3.0,
    "KM_F": 1.56,
    "KM_N": 0.22,
    "kcatFNR": 500.0,
    # cyclic electron flow
    "kPTOX": 0.01,
    "kNDH": 0.004,
    "kcyc": 1,
    # Photoinhibition parameteres
    "kDEG": 0.0000833,  # Pätsikaa 0.3/h
    "kPI0": 300,  # values from Aro Tyystjärvi and Pätsikaa estimated kPI ~= kDEG. Becaue B1 + B3 ~ 1e-7
    "kREP": 0.0000833
    * 100,  # must be faster than kDEG and kPI0 a factor of 100 keeps Udeg near zero
    "beta": 7,
    "Km_PI": 16,
    "mito": 100,
    "activationATP_switch": True,
}


def KeqQAPQ(F, E0QAQAm, E0PQPQH2, pHstroma, RT):
    DG1 = -F * E0QAQAm
    DG2 = -2 * F * E0PQPQH2 + 2 * pHstroma * np.log(10) * RT
    DG0 = -2 * DG1 + DG2
    Keq = np.exp(-DG0 / RT)
    return Keq


def Keqcytb6f(H, F, E0PQPQH2, RT, E0PCPCm, pHstroma):
    DG1 = -2 * F * E0PQPQH2 + 2 * RT * np.log(10) * pH(H)
    DG2 = -F * E0PCPCm
    DG3 = RT * np.log(10) * (pHstroma - pH(H))
    DG = -DG1 + 2 * DG2 + 2 * DG3
    Keq = np.exp(-DG / RT)
    return Keq


def KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi):
    DG = DG0ATP - np.log(10) * (pHstroma - pH(H)) * (14 / 3) * RT
    Keq = Pi * np.exp(-DG / RT)
    return Keq


def Keq_cytb6f(pH, F, E0PQPQH2, E0PCPCm, pHstroma, RT, dG_pH):
    DG1 = -2 * F * E0PQPQH2
    DG2 = -F * E0PCPCm
    DG = -(DG1 + 2 * dG_pH * pH) + 2 * DG2 + 2 * dG_pH * (pHstroma - pH)
    Keq = np.exp(-DG / RT)
    return Keq


def KeqFAFd(E0FAFAm, F, E0FdFdm, RT):
    DG1 = -E0FAFAm * F
    DG2 = -E0FdFdm * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K


def KeqPCP700(E0PCPCm, F, E0P700pP700, RT):
    DG1 = -E0PCPCm * F
    DG2 = -E0P700pP700 * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K


def KeqFNR(E0FdFdm, F, E0NADPNADPH, pHstroma, dG_pH, RT):
    DG1 = -E0FdFdm * F
    DG2 = -2 * E0NADPNADPH * F
    DG = -2 * DG1 + DG2 + dG_pH * pHstroma
    K = np.exp(-DG / RT)
    return K
