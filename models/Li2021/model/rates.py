
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

def _vPSII_recomb(Dpsi, QAm, pH_lumen, k_recomb):  # correct
    delta_delta_g_recomb = Dpsi + 0.06 * (7.0 - pH_lumen)
    return k_recomb * QAm * 10 ** (delta_delta_g_recomb / 0.06)

def _vPSII_ChSep(antenna_size, light_per_L, PhiPSII):  # correct
    return antenna_size * light_per_L * PhiPSII

def _v_PSII(QAm, PQ, k_QA):
    return QAm * PQ * k_QA

def _v_PQ(PQH2, QA, k_QA, Keq_QA):
    return PQH2 * QA * k_QA / Keq_QA

def _v_b6f(
    pH_lumen,
    PQH2,
    PQ,
    PC_ox,
    PC_red,
    pKa_reg,
    c_b6f,
    Em_PC_pH7,
    Em_PQH2_pH7,
    pmf,
    Vmax_b6f,
):  # correct
    pHmod = 1 - (1 / (10 ** (pH_lumen - pKa_reg) + 1))
    b6f_deprot = pHmod * c_b6f

    Em_PC = Em_PC_pH7
    Em_PQH2 = Em_PQH2_pH7 - 0.06 * (pH_lumen - 7.0)

    Keq_b6f = 10 ** ((Em_PC - Em_PQH2 - pmf) / 0.06)
    k_b6f = b6f_deprot * Vmax_b6f

    k_b6f_reverse = k_b6f / Keq_b6f
    f_PQH2 = PQH2 / (
        PQH2 + PQ
    )  # want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ = 1 - f_PQH2
    return f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse

def neg_2_div(x: float, y: float):
    return -2 * x / y

def _v_NDH(Fd_red, PQ, Fd_ox, PQH2, pH_st, Em_PQH2_pH7, Em_Fd, k_NDH1, pmf):
    Em_PQH2 = Em_PQH2_pH7 - 0.06 * (pH_st - 7.0)
    deltaEm = Em_PQH2 - Em_Fd
    Keq_NDH = 10 ** ((deltaEm - pmf * 2) / 0.06)
    k_NDH_reverse = k_NDH1 / Keq_NDH
    return k_NDH1 * Fd_red * PQ - k_NDH_reverse * Fd_ox * PQH2

def _v_PGR(Fd_red, PQ, PQH2, Vmax_PGR):
    return Vmax_PGR * (Fd_red**4 / (Fd_red**4 + 0.1**4)) * PQ / (PQ + PQH2)

def _PSI_ChSep(Fd_ox, Y0, sigma0_I, light_per_L):
    return Y0 * light_per_L * sigma0_I * Fd_ox

def _v_PSI_PCoxid(PC_red, Y2, k_PCtoP700):
    return PC_red * k_PCtoP700 * Y2

def _v_FNR(Fd_red, NADP_pool, k_FdtoNADP):
    return k_FdtoNADP * NADP_pool * Fd_red

def _v_Mehler(Fd_red, Fd_ox):
    return 4 * 0.000265 * Fd_red / (Fd_red + Fd_ox)

def _v_CBB(NADPH_pool, NADP_pool, t, kCBB):
    return (
        kCBB
        * (1.0 - np.exp(-t / 600))
        * (np.log(NADPH_pool / NADP_pool) - np.log(1.25))
        / (np.log(3.5 / 1.25))
    )

def _v_KEA3(qL_act, pH_act, K_lu, H_lumen, H_st, K_stroma, k_KEA3):
    f_KEA_act = qL_act * pH_act
    return k_KEA3 * (H_lumen * K_stroma - H_st * K_lu) * f_KEA_act

def _v_VKC(K_lu, Dpsi, K_stroma, P_K):
    K_deltaG = -0.06 * np.log10(K_stroma / K_lu) + Dpsi
    return P_K * K_deltaG * (K_lu + K_stroma) / 2

def _v_VCCN1(Cl_lu, Cl_st, driving_force_Cl, k_VCCN1):
    relative_Cl_flux = (
        332 * (driving_force_Cl**3)
        + 30.8 * (driving_force_Cl**2)
        + 3.6 * driving_force_Cl
    )
    return k_VCCN1 * relative_Cl_flux * (Cl_st + Cl_lu) / 2

def neg_point_one_val(x: float):
    return -0.1 * x

def _v_ClCe(Cl_lu, Cl_st, H_lumen, H_st, driving_force_Cl, pmf, k_ClCe):
    return (
        k_ClCe
        * (driving_force_Cl * 2 + pmf)
        * (Cl_st + Cl_lu)
        * (H_lumen + H_st)
        / 4
    )

def neg_point_two_val(x: float):
    return -0.2 * x

def neg_thrice(x: float):
    return x * -3

def _v_Leak(H_lumen, pmf, k_leak):
    return pmf * k_leak * H_lumen

def _v_pmf_protons_activity(t, pmf, HPR, Vmax_ATPsynth, light_per_L):
    x = t / 165
    actvt = 0.2 + 0.8 * (x**4 / (x**4 + 1))
    v_proton_active = 1 - (
        1 / (10 ** ((pmf - 0.132) * 1.5 / 0.06) + 1)
    )  # reduced ATP synthase
    v_proton_inert = 1 - (
        1 / (10 ** ((pmf - 0.204) * 1.5 / 0.06) + 1)
    )  # oxidized ATP synthase

    v_active = actvt * v_proton_active * HPR * Vmax_ATPsynth
    v_inert = (1 - actvt) * v_proton_inert * HPR * Vmax_ATPsynth

    v_proton_ATP = v_active + v_inert

    if light_per_L > 0:
        return v_proton_ATP
    else:
        return 0

def _v_Epox(Z, k_EZ):
    return Z * k_EZ

def _v_VDE(V, pH_lumen, nh_VDE, pKa_VDE, Vmax_VDE):
    pHmod = 1 / (10 ** (nh_VDE * (pH_lumen - pKa_VDE)) + 1)
    return V * Vmax_VDE * pHmod


def include_rates(m: Model):
    
    m.add_reaction(
        name="vPSII_recomb",
        fn=_vPSII_recomb,
        args=['Dpsi', 'QA_red', 'pH_lumen', 'k_recomb'],
        stoichiometry={"singO2": Derived(fn=mul, args=['phi_triplet', 'phi_1O2'], unit=None), "QA_red": -1, "pH_lumen": Derived(fn=div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=neg, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="vPSII_ChSep",
        fn=_vPSII_ChSep,
        args=['sigma0_II', 'light_per_L', 'PhiPSII'],
        stoichiometry={"QA_red": 1, "pH_lumen": Derived(fn=neg_div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=value, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_PSII",
        fn=_v_PSII,
        args=['QA_red', 'PQ', 'k_QA'],
        stoichiometry={"QA_red": -1, "PQH_2": 0.5, }
    )
    m.add_reaction(
        name="v_PQ",
        fn=_v_PQ,
        args=['PQH_2', 'QA', 'k_QA', 'Keq_QA'],
        stoichiometry={"QA_red": 1, "PQH_2": -0.5, }
    )
    m.add_reaction(
        name="v_b6f",
        fn=_v_b6f,
        args=['pH_lumen', 'PQH_2', 'PQ', 'PC_ox', 'PC_red', 'pKa_reg', 'c_b6f', 'Em_PC_pH7', 'Em_PQH2_pH7', 'pmf', 'Vmax_b6f'],
        stoichiometry={"PQH_2": -0.5, "PC_ox": -1, "pH_lumen": Derived(fn=neg_2_div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=value, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_NDH",
        fn=_v_NDH,
        args=['Fd_red', 'PQ', 'Fd_ox', 'PQH_2', 'pH_st', 'Em_PQH2_pH7', 'Em_Fd', 'k_NDH1', 'pmf'],
        stoichiometry={"PQH_2": 0.5, "Fd_red": -1, "pH_lumen": Derived(fn=neg_2_div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=twice, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_PGR",
        fn=_v_PGR,
        args=['Fd_red', 'PQ', 'PQH_2', 'Vmax_PGR'],
        stoichiometry={"PQH_2": 0.5, "Fd_red": -1, }
    )
    m.add_reaction(
        name="PSI_ChSep",
        fn=_PSI_ChSep,
        args=['Fd_ox', 'Y0', 'sigma0_I', 'light_per_L'],
        stoichiometry={"Y2": 1, "Fd_red": 1, "Dpsi": Derived(fn=value, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_PSI_PCoxid",
        fn=_v_PSI_PCoxid,
        args=['PC_red', 'Y2', 'k_PCtoP700'],
        stoichiometry={"Y2": -1, "PC_ox": 1, }
    )
    m.add_reaction(
        name="v_FNR",
        fn=_v_FNR,
        args=['Fd_red', 'NADP_st', 'k_FdtoNADP'],
        stoichiometry={"Fd_red": -1, "NADPH_st": 0.5, }
    )
    m.add_reaction(
        name="v_Mehler",
        fn=_v_Mehler,
        args=['Fd_red', 'Fd_ox'],
        stoichiometry={"Fd_red": -1, }
    )
    m.add_reaction(
        name="v_CBB",
        fn=_v_CBB,
        args=['NADPH_st', 'NADP_st', 'time', 'kCBB'],
        stoichiometry={"NADPH_st": -1, }
    )
    m.add_reaction(
        name="v_KEA3",
        fn=_v_KEA3,
        args=["qL_act", 'pH_act', 'K_lu', 'H_lumen', 'H_st', 'K_st', 'k_KEA3'],
        stoichiometry={"K_lu": Derived(fn=value, args=['ipt_lu'], unit=None), "pH_lumen": Derived(fn=div, args=['ipt_lu', 'b_H'], unit=None), }
    )
    m.add_reaction(
        name="v_VKC",
        fn=_v_VKC,
        args=['K_lu', 'Dpsi', 'K_st', 'P_K'],
        stoichiometry={"K_lu": Derived(fn=neg, args=['ipt_lu'], unit=None), "Dpsi": Derived(fn=neg, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_VCCN1",
        fn=_v_VCCN1,
        args=['Cl_lu', 'Cl_st', 'driving_force_Cl', 'k_VCCN1'],
        stoichiometry={"Cl_lu": Derived(fn=value, args=['ipt_lu'], unit=None), "Cl_st": Derived(fn=neg_point_one_val, args=['ipt_lu'], unit=None), "Dpsi": Derived(fn=neg, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_ClCe",
        fn=_v_ClCe,
        args=['Cl_lu', 'Cl_st', 'H_lumen', 'H_st', 'driving_force_Cl', 'pmf', 'k_ClCe'],
        stoichiometry={"Cl_lu": Derived(fn=twice, args=['ipt_lu'], unit=None), "Cl_st": Derived(fn=neg_point_two_val, args=['ipt_lu'], unit=None), "pH_lumen": Derived(fn=div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=neg_thrice, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_Leak",
        fn=_v_Leak,
        args=['H_lumen', 'pmf', 'k_leak'],
        stoichiometry={"pH_lumen": Derived(fn=div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=neg, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_pmf_protons_activity",
        fn=_v_pmf_protons_activity,
        args=['time', 'pmf', "HPR", 'Vmax_ATPsynth', 'light_per_L'],
        stoichiometry={"pH_lumen": Derived(fn=div, args=['ipt_lu', 'b_H'], unit=None), "Dpsi": Derived(fn=neg, args=['vpc'], unit=None), }
    )
    m.add_reaction(
        name="v_Epox",
        fn=_v_Epox,
        args=['Zx', 'k_EZ'],
        stoichiometry={"Zx": -1, }
    )
    m.add_reaction(
        name="v_Deepox",
        fn=_v_VDE,
        args=['Vx', 'pH_lumen', 'nh_VDE', 'pKa_VDE', 'Vmax_VDE'],
        stoichiometry={"Zx": 1, }
    )

    return m