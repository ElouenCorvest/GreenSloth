
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

def _driving_force_Cl(Cl_stroma: float, Cl_lumen: float, Dy: float):
    return 0.06 * np.log10(Cl_stroma / Cl_lumen) + Dy

def calc_PsbS_Protonation(pH_lumen: float, pKPsbS: float):
    return 1 / (10 ** (3 * (pH_lumen - pKPsbS)) + 1)

def calc_NPQ(Z, PsbS_H, max_NPQ):
    return 0.4 * max_NPQ * PsbS_H * Z + 0.5 * max_NPQ * PsbS_H + 0.1 * max_NPQ * Z

def calc_phi2(NPQ, QA):
    return 1 / (1 + (1 + NPQ) / (4.88 * QA))

def calc_h(pH):
    return 10 ** (-1 * pH)

def calc_h(pH):
    return 10 ** (-1 * pH)

def calc_pmf(Dy, pH_lumen, pH_stroma):
    return Dy + 0.06 * (pH_stroma - pH_lumen)

def calc_kCBB(PAR):
    return 60 * (PAR / (PAR + 250))

def _delta_pH_inVolts(delta_pH: float):
    return 0.06 * delta_pH


def include_derived_quantities(m: Model):
    
    m.add_derived(
        name="k_CBC",
        fn=calc_kCBB,
        args=['PPFD'],
    )

    m.add_derived(
        name="QA",
        fn=moiety_1,
        args=['QA_red', 'QA_total'],
    )

    m.add_derived(
        name="P700_red",
        fn=moiety_1,
        args=['P700_ox', 'P700_total'],
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
        args=['Cl__stroma', 'Cl__lumen', 'Dy'],
    )

    m.add_derived(
        name="PsbSP",
        fn=calc_PsbS_Protonation,
        args=['pH_lumen', 'pKPsbS'],
    )

    m.add_derived(
        name="NPQ",
        fn=calc_NPQ,
        args=['Zx', 'PsbSP', 'max_NPQ'],
    )

    m.add_derived(
        name="Phi2",
        fn=calc_phi2,
        args=['NPQ', 'QA'],
    )

    m.add_derived(
        name="H_lumen",
        fn=calc_h,
        args=['pH_lumen'],
    )

    m.add_derived(
        name="H_stroma",
        fn=calc_h,
        args=['pH_stroma'],
    )

    m.add_derived(
        name="pmf",
        fn=calc_pmf,
        args=['Dy', 'pH_lumen', 'pH_stroma'],
    )

    m.add_derived(
        name="kCBB",
        fn=calc_kCBB,
        args=['PPFD'],
    )

    m.add_derived(
        name="delta_pH",
        fn=moiety_1,
        args=['pH_lumen', 'pH_stroma'],
    )

    m.add_derived(
        name="delta_pH_inVolts",
        fn=_delta_pH_inVolts,
        args=['delta_pH'],
    )


    return m