
from mxlpy import Model, Derived
import numpy as np
from typing import cast
    
from .basic_funcs import (
    neg_div,
    mul,
    value,
    twice,
    div,
    neg,
)

def _v_PSII_recombination(Dy, QAm, pH_lumen, k_recomb):  # correct
    delta_delta_g_recomb = Dy + 0.06 * (7.0 - pH_lumen)
    return k_recomb * QAm * 10 ** (delta_delta_g_recomb / 0.06)

def _v_PSII_charge_separations(antenna_size, light_per_L, Phi2):  # correct
    return antenna_size * light_per_L * Phi2

def _v_PQ_reduction_QA(QAm, PQ, kQA):
    return QAm * PQ * kQA

def _v_PQH2_oxidation_QA(PQH2, QA, kQA, Keq_QA_PQ):
    return PQH2 * QA * kQA / Keq_QA_PQ

def _v_b6f(
    pH_lumen,
    PQH2,
    PQ,
    PC_ox,
    PC_red,
    pKreg,
    b6f_content,
    Em7_PC,
    Em7_PQH2,
    pmf,
    max_b6f,
):  # correct
    pHmod = 1 - (1 / (10 ** (pH_lumen - pKreg) + 1))
    b6f_deprot = pHmod * b6f_content

    Em_PC = Em7_PC
    Em_PQH2 = Em7_PQH2 - 0.06 * (pH_lumen - 7.0)

    Keq_b6f = 10 ** ((Em_PC - Em_PQH2 - pmf) / 0.06)
    k_b6f = b6f_deprot * max_b6f

    k_b6f_reverse = k_b6f / Keq_b6f
    f_PQH2 = PQH2 / (
        PQH2 + PQ
    )  # want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ = 1 - f_PQH2
    return f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse

def neg_2_div(x: float, y: float):
    return -2 * x / y

def _v_NDH(Fd_red, PQ, Fd_ox, PQH2, pH_stroma, Em7_PQH2, Em_Fd, k_NDH, pmf):
    Em_PQH2 = Em7_PQH2 - 0.06 * (pH_stroma - 7.0)
    deltaEm = Em_PQH2 - Em_Fd
    Keq_NDH = 10 ** ((deltaEm - pmf * 2) / 0.06)
    k_NDH_reverse = k_NDH / Keq_NDH
    return k_NDH * Fd_red * PQ - k_NDH_reverse * Fd_ox * PQH2

def _v_PGR(Fd_red, PQ, PQH2, PGR_vmax):
    return PGR_vmax * (Fd_red**4 / (Fd_red**4 + 0.1**4)) * PQ / (PQ + PQH2)

def _v_PSI_charge_separation(Fd_ox, P700_red, PSI_antenna_size, light_per_L):
    return P700_red * light_per_L * PSI_antenna_size * Fd_ox

def _v_PC_oxidation_P700(PC_red, P700_ox, k_PC_to_P700):
    return PC_red * k_PC_to_P700 * P700_ox

def _v_LEF(Fd_red, NADP_pool, k_Fd_to_NADP):
    return k_Fd_to_NADP * NADP_pool * Fd_red

def _v_Mehler(Fd_red, Fd_ox):
    return 4 * 0.000265 * Fd_red / (Fd_red + Fd_ox)

def _v_CBB_NADPH(NADPH_pool, NADP_pool, t, k_CBC):
    # print(f"{NADPH_pool=}, {NADP_pool=}, {t=}, {k_CBC=}")
    return (
        k_CBC
        * (1.0 - np.exp(-t / 600))
        * (np.log(NADPH_pool / NADP_pool) - np.log(1.25))
        / (np.log(3.5 / 1.25))
    )

def _v_KEA(QAm, pH_lumen, K_lumen, H_lumen, H_stroma, K_stroma, k_KEA):
    qL = 1 - QAm
    qL_act = qL**3 / (qL**3 + 0.15**3)
    pH_act = 1 / (10 ** (1 * (pH_lumen - 6.0)) + 1)
    f_KEA_act = qL_act * pH_act
    return k_KEA * (H_lumen * K_stroma - H_stroma * K_lumen) * f_KEA_act

def _v_K_channel(K_lumen, Dy, K_stroma, perm_K):
    K_deltaG = -0.06 * np.log10(K_stroma / K_lumen) + Dy
    return perm_K * K_deltaG * (K_lumen + K_stroma) / 2

def _v_VCCN1(Cl_lumen, Cl_stroma, driving_force_Cl, k_VCCN1):
    relative_Cl_flux = (
        332 * (driving_force_Cl**3)
        + 30.8 * (driving_force_Cl**2)
        + 3.6 * driving_force_Cl
    )
    return k_VCCN1 * relative_Cl_flux * (Cl_stroma + Cl_lumen) / 2

def neg_point_one_val(x: float):
    return -0.1 * x

def _v_CLCE(Cl_lumen, Cl_stroma, H_lumen, H_stroma, driving_force_Cl, pmf, k_CLCE):
    return (
        k_CLCE
        * (driving_force_Cl * 2 + pmf)
        * (Cl_stroma + Cl_lumen)
        * (H_lumen + H_stroma)
        / 4
    )

def neg_point_two_val(x: float):
    return -0.2 * x

def neg_thrice(x: float):
    return x * -3

def _v_leak(H_lumen, pmf, k_leak):
    return pmf * k_leak * H_lumen

def _v_pmf_protons_activity(t, pmf, n, ATP_synthase_max_turnover, light_per_L):
    x = t / 165
    actvt = 0.2 + 0.8 * (x**4 / (x**4 + 1))
    v_proton_active = 1 - (
        1 / (10 ** ((pmf - 0.132) * 1.5 / 0.06) + 1)
    )  # reduced ATP synthase
    v_proton_inert = 1 - (
        1 / (10 ** ((pmf - 0.204) * 1.5 / 0.06) + 1)
    )  # oxidized ATP synthase

    v_active = actvt * v_proton_active * n * ATP_synthase_max_turnover
    v_inert = (1 - actvt) * v_proton_inert * n * ATP_synthase_max_turnover

    v_proton_ATP = v_active + v_inert

    if light_per_L > 0:
        return v_proton_ATP
    else:
        return 0

def _v_ZE(Z, kZE):
    return Z * kZE

def _v_VDE(V, pH_lumen, VDE_Hill, pKvde, VDE_max_turnover_number):
    pHmod = 1 / (10 ** (VDE_Hill * (pH_lumen - pKvde)) + 1)
    return V * VDE_max_turnover_number * pHmod


def include_rates(m: Model):
    
    m.add_reaction(
        name="v_PSII_recombination",
        fn=_v_PSII_recombination,
        args=['Dy', 'QA_red', 'pH_lumen', 'k_recomb'],
        stoichiometry={"singletO2": Derived(fn=mul, args=['triplet_yield', 'triplet_to_singletO2_yield'], unit=None), "QA_red": -1, "pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=neg, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_PSII_charge_separations",
        fn=_v_PSII_charge_separations,
        args=['PSII_antenna_size', 'light_per_L', 'Phi2'],
        stoichiometry={"QA_red": 1, "pH_lumen": Derived(fn=neg_div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=value, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_PQ_reduction_QA",
        fn=_v_PQ_reduction_QA,
        args=['QA_red', 'PQ', 'kQA'],
        stoichiometry={"QA_red": -1, "PQH_2": 0.5, }
    )
    m.add_reaction(
        name="v_PQH2_oxidation_QA",
        fn=_v_PQH2_oxidation_QA,
        args=['PQH_2', 'QA', 'kQA', 'Keq_QA_PQ'],
        stoichiometry={"QA_red": 1, "PQH_2": -0.5, }
    )
    m.add_reaction(
        name="v_b6f",
        fn=_v_b6f,
        args=['pH_lumen', 'PQH_2', 'PQ', 'PC_ox', 'PC_red', 'pKreg', 'b6f_content', 'Em7_PC', 'Em7_PQH2', 'pmf', 'max_b6f'],
        stoichiometry={"PQH_2": -0.5, "PC_ox": -1, "pH_lumen": Derived(fn=neg_2_div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=value, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_NDH",
        fn=_v_NDH,
        args=['Fd_red', 'PQ', 'Fd_ox', 'PQH_2', 'pH_stroma', 'Em7_PQH2', 'Em_Fd', 'k_NDH', 'pmf'],
        stoichiometry={"PQH_2": 0.5, "Fd_red": -1, "pH_lumen": Derived(fn=neg_2_div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=twice, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_PGR",
        fn=_v_PGR,
        args=['Fd_red', 'PQ', 'PQH_2', 'PGR_vmax'],
        stoichiometry={"PQH_2": 0.5, "Fd_red": -1, }
    )
    m.add_reaction(
        name="v_PSI_charge_separation",
        fn=_v_PSI_charge_separation,
        args=['Fd_ox', 'P700_red', 'PSI_antenna_size', 'light_per_L'],
        stoichiometry={"P700_ox": 1, "Fd_red": 1, "Dy": Derived(fn=value, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_PC_oxidation_P700",
        fn=_v_PC_oxidation_P700,
        args=['PC_red', 'P700_ox', 'k_PC_to_P700'],
        stoichiometry={"P700_ox": -1, "PC_ox": 1, }
    )
    m.add_reaction(
        name="v_LEF",
        fn=_v_LEF,
        args=['Fd_red', 'NADP_st', 'k_Fd_to_NADP'],
        stoichiometry={"Fd_red": -1, "NADPH_st": 0.5, }
    )
    m.add_reaction(
        name="v_Mehler",
        fn=_v_Mehler,
        args=['Fd_red', 'Fd_ox'],
        stoichiometry={"Fd_red": -1, }
    )
    m.add_reaction(
        name="v_CBB_NADPH",
        fn=_v_CBB_NADPH,
        args=['NADPH_st', 'NADP_st', 'time', 'k_CBC'],
        stoichiometry={"NADPH_st": -1, }
    )
    m.add_reaction(
        name="v_KEA",
        fn=_v_KEA,
        args=['QA_red', 'pH_lumen', 'K_lumen', 'H_lumen', 'H_stroma', 'K__stroma', 'k_KEA'],
        stoichiometry={"K_lumen": Derived(fn=value, args=['lumen_protons_per_turnover'], unit=None), "pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), }
    )
    m.add_reaction(
        name="v_K_channel",
        fn=_v_K_channel,
        args=['K_lumen', 'Dy', 'K__stroma', 'perm_K'],
        stoichiometry={"K_lumen": Derived(fn=neg, args=['lumen_protons_per_turnover'], unit=None), "Dy": Derived(fn=neg, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_VCCN1",
        fn=_v_VCCN1,
        args=['Cl_lumen', 'Cl_stroma', 'driving_force_Cl', 'k_VCCN1'],
        stoichiometry={"Cl_lumen": Derived(fn=value, args=['lumen_protons_per_turnover'], unit=None), "Cl_stroma": Derived(fn=neg_point_one_val, args=['lumen_protons_per_turnover'], unit=None), "Dy": Derived(fn=neg, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_CLCE",
        fn=_v_CLCE,
        args=['Cl_lumen', 'Cl_stroma', 'H_lumen', 'H_stroma', 'driving_force_Cl', 'pmf', 'k_CLCE'],
        stoichiometry={"Cl_lumen": Derived(fn=twice, args=['lumen_protons_per_turnover'], unit=None), "Cl_stroma": Derived(fn=neg_point_two_val, args=['lumen_protons_per_turnover'], unit=None), "pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=neg_thrice, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_leak",
        fn=_v_leak,
        args=['H_lumen', 'pmf', 'k_leak'],
        stoichiometry={"pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=neg, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_pmf_protons_activity",
        fn=_v_pmf_protons_activity,
        args=['time', 'pmf', 'n', 'ATP_synthase_max_turnover', 'light_per_L'],
        stoichiometry={"pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'buffering_capacity'], unit=None), "Dy": Derived(fn=neg, args=['Volts_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_ZE",
        fn=_v_ZE,
        args=['Zx', 'kZE'],
        stoichiometry={"Zx": -1, }
    )
    m.add_reaction(
        name="v_Deepox",
        fn=_v_VDE,
        args=['Vx', 'pH_lumen', 'VDE_Hill', 'pKvde', 'VDE_max_turnover_number'],
        stoichiometry={"Zx": 1, }
    )

    return m