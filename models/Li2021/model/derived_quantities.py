
from mxlpy import Model
from mxlpy.surrogates import qss
import numpy as np
import math
from typing import cast, Iterable
    
from .basic_funcs import (
    moiety_1,
)

def calc_kCBB(PAR):
    return 60 * (PAR / (PAR + 250))

def _light_per_L(par: float):
    return 0.84 * par / 0.7

def _driving_force_Cl(Cl_st: float, Cl_lu: float, Dpsi: float):
    return 0.06 * np.log10(Cl_st / Cl_lu) + Dpsi

def calc_PsbS_Protonation(pH_lumen: float, pKa_PsbS: float):
    return 1 / (10 ** (3 * (pH_lumen - pKa_PsbS)) + 1)

def calc_NPQ(Z, PsbS_H, NPQ_max):
    return 0.4 * NPQ_max * PsbS_H * Z + 0.5 * NPQ_max * PsbS_H + 0.1 * NPQ_max * Z

def calc_phi2(NPQ, QA):
    return 1 / (1 + (1 + NPQ) / (4.88 * QA))

def calc_h(pH):
    return 10 ** (-1 * pH)


def calc_pmf(Dpsi, pH_lumen, pH_st):
    return Dpsi + 0.06 * (pH_st - pH_lumen)


def _delta_pH_inVolts(delta_pH: float):
    return 0.06 * delta_pH


def _ql_act(QA: float):
    return QA**3 / (QA**3 + 0.15**3)

def _pH_act(pH_lumen: float):
    return 1 / (10 ** (1 * (pH_lumen - 6.0)) + 1)

def include_derived_quantities(m: Model):


    m.add_derived(
        name="QA",
        fn=moiety_1,
        args=['QA_red', 'QA_total'],
    )

    m.add_derived(
        name="Y0",
        fn=moiety_1,
        args=['Y2', 'P700_total'],
    )

    m.add_derived(
        name="PQ",
        fn=moiety_1,
        args=['PQH_2', 'PQ_tot'],
    )

    m.add_derived(
        name="PC_red",
        fn=moiety_1,
        args=['PC_ox', 'PC_tot'],
    )

    m.add_derived(
        name="Fd_ox",
        fn=moiety_1,
        args=['Fd_red', 'Fd_tot'],
    )

    m.add_derived(
        name="NADP_st",
        fn=moiety_1,
        args=['NADPH_st', 'NADP_tot'],
    )

    m.add_derived(
        name="Vx",
        fn=moiety_1,
        args=['Zx', 'Carotenoids_tot'],
    )

    m.add_derived(
        name="light_per_L",
        fn=_light_per_L,
        args=['PPFD'],
    )

    m.add_derived(
        name="driving_force_Cl",
        fn=_driving_force_Cl,
        args=['Cl_st', 'Cl_lu', 'Dpsi'],
    )

    m.add_derived(
        name="PsbSP",
        fn=calc_PsbS_Protonation,
        args=['pH_lumen', 'pKa_PsbS'],
    )

    m.add_derived(
        name="NPQ",
        fn=calc_NPQ,
        args=['Zx', 'PsbSP', 'NPQ_max'],
    )

    m.add_derived(
        name="PhiPSII",
        fn=calc_phi2,
        args=['NPQ', 'QA'],
    )

    m.add_derived(
        name="H_lumen",
        fn=calc_h,
        args=['pH_lumen'],
    )

    m.add_derived(
        name="H_st",
        fn=calc_h,
        args=['pH_st'],
    )

    m.add_derived(
        name="pmf",
        fn=calc_pmf,
        args=['Dpsi', 'pH_lumen', 'pH_st'],
    )

    m.add_derived(
        name="kCBB",
        fn=calc_kCBB,
        args=['PPFD'],
    )

    m.add_derived(
        name="delta_pH",
        fn=moiety_1,
        args=['pH_lumen', 'pH_st'],
    )

    m.add_derived(
        name="delta_pH_inVolts",
        fn=_delta_pH_inVolts,
        args=['delta_pH'],
    )
    
    m.add_derived(
        name="qL_act",
        fn=_ql_act,
        args=["QA"],
    )
    
    m.add_derived(
        name="pH_act",
        fn=_pH_act,
        args=["pH_lumen"],
    )

    return m