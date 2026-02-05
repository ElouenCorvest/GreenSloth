
from mxlpy import Model, Derived
import numpy as np
from typing import cast
    
from .basic_funcs import (
    mass_action_1s,
)

def _v_PSII_O2(stoic_PSII: float, sigma_PSII: float, light: float, RCII_closed: float) -> float:
    return stoic_PSII * sigma_PSII * light * (1 - RCII_closed)

def x_div_yz(x: float, y: float, z: float) -> float:
    return x / (y * z)

def _v_PSI(stoic_PSI: float, sigma_PSI: float, light: float, PSI_ox: float, L_PSI: float) -> float:
    return stoic_PSI * sigma_PSI * L_PSI * light / (L_PSI + light) * (stoic_PSI - PSI_ox)

def _v_PSII_PQ(k1p: float, RCII_closed: float, PQ_ox: float, k1m: float, RCII_open: float, PQ_red: float) -> float:
    return k1p * RCII_closed * PQ_ox - (k1m * RCII_open * PQ_red)

def _v_PQH2_PSI(k2p: float, PQ_red: float, PSI_ox: float, k2m: float, PQ_ox: float, PSI_red: float) -> float:
    return k2p * PQ_red * PSI_ox - k2m * PQ_ox * PSI_red

def _v3(k3: float, h_lumen: float, Q_active: float, K_NPQ: float, n: float) -> float:
    return k3 * (1 - Q_active) / (1 + (K_NPQ / h_lumen)**n)

def _v_ATPsynth(k5: float, ADP: float, ATP: float, H_stroma: float, H_lumen: float, cEqP: float) -> float:
    return k5 * (ADP - ATP * (H_stroma / H_lumen)**(14/3) / cEqP)

def proton_generation(V_stroma: float, V_lumen: float, bH: float) -> float:
    return -14/3 * V_stroma / V_lumen * bH

def _v_Leak(k7: float, H_lumen: float, H_stroma: float) -> float:
    return k7 * (H_lumen - H_stroma)


def include_rates(m: Model):
    
    m.add_reaction(
        name="v_PSII_O2",
        fn=_v_PSII_O2,
        args=['stoic_PSII', 'sigma_PSII', 'osc_light', 'RCII_closed'],
        stoichiometry={"H_lumen": Derived(fn=x_div_yz, args=['bH', 'V_lumen', 'N_A'], unit=None), }
    )
    m.add_reaction(
        name="v_PSI",
        fn=_v_PSI,
        args=['stoic_PSI', 'sigma_PSI_0', 'osc_light', 'PSI_ox', 'L_PSI'],
        stoichiometry={"PSI_ox": 1, }
    )
    m.add_reaction(
        name="v_PSII_PQ",
        fn=_v_PSII_PQ,
        args=['k1p', 'RCII_closed', 'PQ', 'k1m', 'RCII_open', 'PQH_2'],
        stoichiometry={"PQ": -0.5, }
    )
    m.add_reaction(
        name="v_PQH2_PSI",
        fn=_v_PQH2_PSI,
        args=['k2p', 'PQH_2', 'PSI_ox', 'k2m', 'PQ', 'PSI_red'],
        stoichiometry={"PQ": 0.5, "PSI_ox": -1, "H_lumen": Derived(fn=x_div_yz, args=['bH', 'V_lumen', 'N_A'], unit=None), }
    )
    m.add_reaction(
        name="v3",
        fn=_v3,
        args=['k3', 'H_lumen', 'Q_active', 'keq_NPQ', 'n_NPQ'],
        stoichiometry={"Q_active": 1, }
    )
    m.add_reaction(
        name="v4",
        fn=mass_action_1s,
        args=['Q_active', 'k4'],
        stoichiometry={"Q_active": -1, }
    )
    m.add_reaction(
        name="v_ATPsynth",
        fn=_v_ATPsynth,
        args=['k5', 'ADP_st', 'ATP_st', 'H_stroma', 'H_lumen', 'cEqP'],
        stoichiometry={"ATP_st": 1, "H_lumen": Derived(fn=proton_generation, args=['V_stroma', 'V_lumen', 'bH'], unit=None), }
    )
    m.add_reaction(
        name="v_ATPcons",
        fn=mass_action_1s,
        args=['ATP_st', 'k6'],
        stoichiometry={"ATP_st": -1, }
    )
    m.add_reaction(
        name="v_Leak",
        fn=_v_Leak,
        args=['k7', 'H_lumen', 'H_stroma'],
        stoichiometry={"H_lumen": -1, }
    )
    m.add_reaction(
        name="v_PQ",
        fn=mass_action_1s,
        args=['PQH_2', 'k_X'],
        stoichiometry={"PQ": 1, }
    )

    return m