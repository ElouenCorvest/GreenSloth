
from mxlpy import Model
from mxlpy.surrogates import qss
import numpy as np
import math
from typing import cast, Iterable
    
from .basic_funcs import (
    moiety_1,
)

def _osc_light(pfd: float, pfd_add: float, f: float, time: float) -> float:
    return pfd + pfd_add * np.cos(2 * np.pi * f * time)

def _sigma_PSII(NPQ_max: float, Q_active: float) -> float:
    return 1 - NPQ_max * Q_active

def _rcii_closed(k1p: float, PQ_ox: float, sigma_PSII: float, light: float, k1m: float, PQ_red: float) -> float:
    top = 1
    bottom = 1 + k1p * PQ_ox / (sigma_PSII * light + k1m * PQ_red)
    return top / bottom

def _rcii_open(k1p: float, PQ_ox: float, sigma_PSII: float, k1m: float, PQ_red: float) -> float:
    return k1p * PQ_ox / ((sigma_PSII + k1m * PQ_red) + k1p * PQ_ox)

def _flourescence(Fluo_0: float, RCII_closed: float, sigma_PSII: float) -> float:
    return (Fluo_0 + RCII_closed) * sigma_PSII

def _npq(npq_max: float, q_active: float):
    return npq_max * q_active /(1 - npq_max * q_active)

def _o2(nPSII: float, k1p: float, RCIIclosed: float, PQ: float, k1m: float, PQ_red: float):
    return (nPSII * ( k1p * RCIIclosed * PQ - k1m * (1 - RCIIclosed) * PQ_red))/4


def include_derived_quantities(m: Model):
    
    m.add_derived(
        name="Q_inactive",
        fn=moiety_1,
        args=['Q_active', 'Q_total'],
    )

    m.add_derived(
        name="PQH_2",
        fn=moiety_1,
        args=['PQ', 'PQ_tot'],
    )

    m.add_derived(
        name="PSI_red",
        fn=moiety_1,
        args=['PSI_ox', 'PSI_total'],
    )

    m.add_derived(
        name="ADP_st",
        fn=moiety_1,
        args=['ATP_st', 'AP_tot'],
    )

    m.add_derived(
        name="osc_light",
        fn=_osc_light,
        args=['PPFD', 'PPFD_add', 'f', 'time'],
    )

    m.add_derived(
        name="sigma_PSII",
        fn=_sigma_PSII,
        args=['NPQ_max', 'Q_active'],
    )

    m.add_derived(
        name="RCII_closed",
        fn=_rcii_closed,
        args=['k1p', 'PQ', 'sigma_PSII', 'osc_light', 'k1m', 'PQH_2'],
    )

    m.add_derived(
        name="RCII_open",
        fn=_rcii_open,
        args=['k1p', 'PQ', 'sigma_PSII', 'k1m', 'PQH_2'],
    )

    m.add_derived(
        name="Fluo",
        fn=_flourescence,
        args=['Fluo_0', 'RCII_closed', 'sigma_PSII'],
    )

    m.add_derived(
        name="NPQ",
        fn=_npq,
        args=['NPQ_max', 'Q_active'],
    )

    m.add_derived(
        name="O2",
        fn=_o2,
        args=['PSI_total', 'k1p', 'RCII_closed', 'PQ', 'k1m', 'PQH_2'],
    )


    return m