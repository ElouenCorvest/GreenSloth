#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rates for the photoinhibtion model
"""

import numpy as np
from scipy.optimize import fsolve

from .parameters import Keq_cytb6f, KeqATPsyn
from .utils import pHinv

#############################################################################################################
# Modules
#############################################################################################################


def ps2states(P, Uact, Q, light, PQtot, kPQred, KeqQAPQ, kH, kF, kP):
    Bs = []
    Pox = PQtot - P
    b0 = light + kPQred * P / KeqQAPQ
    b1 = kH * Q + kF
    b2 = kH * Q + kF + kP

    for Pox, Uact, b0, b1, b2 in zip(Pox, Uact, b0, b1, b2):
        A = np.array(
            [
                [-b0, b1, kPQred * Pox, 0],  # B0
                [light, -b2, 0, 0],  # B1
                [0, 0, light, -b1],  # B3
                [1, 1, 1, 1],
            ]
        )

        b = np.array([0, 0, 0, Uact])
        B0, B1, B2, B3 = np.linalg.solve(A, b)
        Bs.append([B0, B1, B2, B3])
    return np.array(Bs).T


def ps2statesET(
    P, Uact, Udeg, Uinh, Q, light, PQtot, kT, kP, kF, kH, kPQred, KeqQAPQ, beta
):
    Bs = []
    Pox = PQtot - P
    kPQ = kPQred
    kPQr = kPQred / KeqQAPQ

    def system(x0, light, Q, P, Pox, kT, kP, kF, kH, kPQ, kPQr, Uact, Uinh, Udeg, beta):
        B0, B1, B2, B3, Uip, Uin, Udp, Udn = x0

        dB0dt = (kH * Q + kF) * B1 + kPQ * B2 * Pox - (light + kPQr * P) * B0
        dB1dt = light * B0 - (kH * Q + kP + kF) * B1
        dB2dt = (
            (kH * Q + kF) * B3
            + kP * B1
            + kPQr * B0 * P
            - (kPQ * Pox + light) * B2
            + kT * (Uin + Udn) * B3
        )
        total = Uact - (B0 + B1 + B2 + B3)

        dUipdt = light * Uin - (kH * Q * beta + kF) * Uip + kT * B3 * Uin
        total_Ui = Uinh - (Uip + Uin)

        dUdpdt = light * Udn - (kH * Q * beta + kF) * Udp + kT * B3 * Udn
        total_Ud = Udeg - (Udp + Udn)

        return [dB0dt, dB1dt, dB2dt, total, dUipdt, total_Ui, dUdpdt, total_Ud]

    for P, Pox, Uact, Udeg, Uinh, Q in zip(P, Pox, Uact, Udeg, Uinh, Q):
        B0, B1, B2, B3, Uip, Uin, Udp, Udn = fsolve(
            system,
            [Uact, 0, 0, 0, 0, Uinh, 0, Udeg],
            args=(light, Q, P, Pox, kT, kP, kF, kH, kPQ, kPQr, Uact, Uinh, Udeg, beta),
        )
        Bs.append([B0, B1, B2, B3, Uip, Uin, Udp, Udn])
    return np.array(Bs).T


def ps1states(PCred, Fdred, PCox, Fdox, PSItot, kFdred, KeqFAFd, KeqPCP700, kPCox, PFD):
    light = PFD

    A1 = PSItot / (
        1
        + light / (kFdred * Fdox)
        + (1 + Fdred / (KeqFAFd * Fdox))
        * (PCox / (KeqPCP700 * PCred) + light / (kPCox * PCred))
    )
    return A1


def pqmoiety(P, PQtot):
    return PQtot - P


def atpmoiety(A, APtot):
    return APtot - A


def psbsmoiety(Pr, PsbStot):
    return PsbStot - Pr


def xcycmoiety(V, Xtot):
    return Xtot - V


def pcmoiety(PC, PCtot):
    return PCtot - PC


def fdmoiety(Fd, Fdtot):
    return Fdtot - Fd


def Nmoiety(NADPH, NADPtot):
    return NADPtot - NADPH


def Quencher(
    Pr,
    V,
    Uact,
    Xtot,
    PsbStot,
    Kzsat,
    gamma0,
    gamma1,
    gamma2,
    gamma3,
    gamma4,
    slow_quenching,
):
    Z = Xtot - V
    P = PsbStot - Pr
    Zs = Z / (Z + Kzsat)

    Q = (
        gamma0 * (1 - Zs) * Pr
        + gamma1 * (1 - Zs) * P
        + gamma2 * Zs * P
        + gamma3 * Zs * Pr
        + slow_quenching * gamma4 * (1 - Uact / 2.5)
    )
    return Q


def FInh(B0, B2, Uinh, Udeg, Q, kF, kH, kP, beta):
    F = (
        kF / (kF + kH * Q + kP) * B0
        + kF / (kF + kH * Q) * B2
        + kF / (kF + beta * kH * Q) * (Uinh + Udeg)
    )
    return F


def FInh2(B0, B2, Uinh, Udeg, Q, kF, kH, kP, kT, beta):
    F = (
        kF / (kF + kH * Q + kP) * B0
        + kF / (kF + kH * Q + kT * (Uinh + Udeg)) * B2
        + kF / (kF + kH * Q * beta) * (Uinh + Udeg)
    )
    return F


#############################################################################################################
# Rate equations
#############################################################################################################


def vPSII(B1, kP):
    v = kP * 0.5 * B1
    return v


def vB6f(PCox, PC, P, Pox, pH, kCytb6f, F, E0PQPQH2, E0PCPCm, pHstroma, RT, dG_pH):
    Keq = Keq_cytb6f(pH, F, E0PQPQH2, E0PCPCm, pHstroma, RT, dG_pH)
    v = np.maximum(
        kCytb6f * (P * PCox**2 - (Pox * PC**2) / Keq), -kCytb6f
    )  # maybe change
    return v


def vATPsynthase(
    A, H, E, kATPsynthase, DG0ATP, pHstroma, RT, Pi, APtot, activationATP_switch
):
    v = kATPsynthase * (APtot - A - A / KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi))
    if activationATP_switch:
        return v * E
    else:
        return v


def vLeak(H, kleak, pHstroma):
    v = kleak * (H - pHinv(pHstroma))
    return v


def vATPcons(A, kATPconsumption):
    v = kATPconsumption * A
    return v


def vVDE(V, H, nHX, KphSatZ, kDeepoxV):
    a = H**nHX / (H**nHX + pHinv(KphSatZ) ** nHX)
    v = kDeepoxV * a * V
    return v


def vZEP(V, kEpoxZ, Xtot):
    v = kEpoxZ * (Xtot - V)
    return v


def vPsbSProt(Pr, H, nHL, KphSatLHC, kProt):
    a = H**nHL / (H**nHL + pHinv(KphSatLHC) ** nHL)
    v = kProt * a * Pr
    return v


def vPsbSDeProt(Pnr, kDeprot):
    v = kDeprot * Pnr
    return v


def vFNR(Fd, Fdm, NADPH, NADP, KM_F, KM_N, EFNR, kcatFNR, KeqFNR):
    fdred = Fdm / KM_F
    fdox = Fd / KM_F
    nadph = (NADPH) / KM_N
    nadp = (NADP) / KM_N
    v = (
        EFNR
        * kcatFNR
        * ((fdred**2) * nadp - ((fdox**2) * nadph) / KeqFNR)
        / (
            (1 + fdred + fdred**2) * (1 + nadp)
            + (1 + fdox + fdox**2) * (1 + nadph)
            - 1
        )
    )
    return v


def vPTOX(P, kPTOX, O2ext):
    v = kPTOX * O2ext * P
    return v


def vCyc(Pox, Fd, kcyc):
    v = kcyc * ((Fd**2) * Pox)
    return v


def vATPactivity(E, light, kActATPase, kDeactATPase):
    switch = light >= 1
    v = kActATPase * switch * (1 - E) - kDeactATPase * (1 - switch) * E
    return v


def vNADPHconsumption(NADPH, kNADPHconsumption):
    v = kNADPHconsumption * NADPH
    return v


def vPhotInh(B1, B3, kPI0):
    v = (B1 + B3) * kPI0  # Uact rausnehmen, KpIO ma 2.5
    return v


def vPhotInh2(Uinh, kDEG, A, Km_PI):
    v = kDEG * Uinh * A / (A + Km_PI)
    return v


def vPhotInh3(Udeg, kREP, A, Km_PI):
    v = kREP * Udeg * A / (A + Km_PI)
    return v


def mito(PFD, mito):
    switch = 10**2 / (PFD**2 + 10**2)
    v = mito * switch
    return v


def vPSI(Y0A, PFD):
    v = Y0A * PFD
    return v
