
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

def neg_point_one_val(x: float):
    return -0.1 * x

def neg_point_two_val(x: float):
    return -0.2 * x

def neg_thrice(x: float):
    return x * -3

def neg_2_div(x: float, y: float):
    return -2 * x / y

def ATP_stoi(x: float, y: float, z: float):
    return x * y / z

def _vPSII_recomb(Dpsi, QAm, pH_lumen, k_recomb):  # checked
    delta_delta_g_recomb = Dpsi + 0.06 * (7.0 - pH_lumen)
    return k_recomb * QAm * 10 ** (delta_delta_g_recomb / 0.06)

def _vPSII_ChSep(PPFD, PhiPSII):  # checked
    return PPFD * PhiPSII

def _v_PSII(QAm, PQ, k_QA):
    return QAm * PQ * k_QA # checked

def _v_PQ(PQH2, QA, k_QA, Keq_QA):
    return PQH2 * QA * k_QA / Keq_QA # checked

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
):  # checked
    pHmod = 1 - (1 / (10 ** (pH_lumen - pKa_reg) + 1))
    b6f_deprot = pHmod * c_b6f

    Em_PC = Em_PC_pH7
    Em_PQH2 = Em_PQH2_pH7 - 0.06 * (pH_lumen - 7.0)

    Keq_b6f = 10 ** ((Em_PC - Em_PQH2 - pmf) / 0.06)
    k_b6f = b6f_deprot * Vmax_b6f

    k_b6f_reverse = k_b6f / Keq_b6f
    f_PQH2 = PQH2 / ( PQH2 + PQ) 
    f_PQ = 1 - f_PQH2
    return f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse

def _PSI_ChSep(Fd_ox, P700_red, PSI_antenna_size, PPFD): #checked
    return P700_red * PPFD * PSI_antenna_size * Fd_ox

def _v_PSI_PCoxid(PC_red, P700_ox, k_PCtoP700): #checked
    return PC_red * k_PCtoP700 * P700_ox

def _v_FNR(Fd_red, NADP_pool, k_FdtoNADP): #checked
    return k_FdtoNADP * NADP_pool * Fd_red

def vATPsynthase(Vmax_ATPsynth, ATP_synthase_driving_force): #checked
    return Vmax_ATPsynth*ATP_synthase_driving_force 

def _v_KEA3(K_lu, H_lumen, H_st, K_stroma, k_KEA3): #checked
    return k_KEA3 * (H_lumen * K_stroma - H_st * K_lu) 

def _v_VKC(K_lu, Dpsi, K_stroma, P_K): #checked
    K_deltaG = -0.06 * np.log10(K_stroma / K_lu) + Dpsi
    return P_K * K_deltaG * (K_lu + K_stroma) / 2

def _v_Epox(Z, k_EZ): #checked
    return Z * k_EZ

def _v_VDE(V, pH_lumen, nh_VDE, pKa_VDE, Vmax_VDE): #checked
    pHmod=1-(1 - (1 / (10 ** (nh_VDE*(pH_lumen - pKa_VDE)) + 1)))
    return V * Vmax_VDE * pHmod

def vCBB(NADPH, kCBB): #checked
    return kCBB * NADPH

def include_rates(m: Model):
    
    m.add_reaction(
        name="vPSII_recomb",
        fn=_vPSII_recomb,
        args=['Dpsi', 'QA_red', 'pH_lumen', 'k_recomb'],
        stoichiometry={"singO2": Derived(fn=mul, args=['phi_triplet', 'phi_1O2'], unit=None), #checked
                       "QA_red": -1, #checked
                       "pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'b_H'], unit=None), #checked
                       "Dpsi": Derived(fn=neg, args=['volt_per_charge'], unit=None), }
    )
    m.add_reaction( 
        name="vPSII_ChSep", #checked
        fn=_vPSII_ChSep,
        args=['PPFD', 'PhiPSII'],
        stoichiometry={"QA_red": 1, 
                       "pH_lumen": Derived(fn=neg_div, args=['lumen_protons_per_turnover', 'b_H'], unit=None), 
                       "Dpsi": Derived(fn=value, args=['volt_per_charge'], unit=None), }
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
        stoichiometry={"PQH_2": -0.5, 
                       "PC_ox": -1, 
                       "pH_lumen": Derived(fn=neg_2_div, args=['lumen_protons_per_turnover', 'b_H'], unit=None), 
                       "Dpsi": Derived(fn=value, args=['volt_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="PSI_ChSep",
        fn=_PSI_ChSep,
        args=['Fd_ox', 'P700_red', 'PSI_antenna_size', 'PPFD'],
        stoichiometry={"P700_ox": 1, "Fd_red": 1, "Dpsi": Derived(fn=value, args=['volt_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_PSI_PCoxid",
        fn=_v_PSI_PCoxid,
        args=['PC_red', 'P700_ox', 'k_PCtoP700'],
        stoichiometry={"P700_ox": -1, "PC_ox": 1, }
    )

    m.add_reaction(
        name="v_FNR",
        fn=_v_FNR,
        args=['Fd_red', 'NADP_st', 'k_FdtoNADP'],
        stoichiometry={"Fd_red": -1, "NADPH_st": 0.5, "LEF": 1}
    )

    m.add_reaction(
        name="vATPsynthase",
        fn= vATPsynthase,
        args=['Vmax_ATPsynth','ATP_synthase_driving_force'],
        stoichiometry={"ATP_made": 1, 
                       "pH_lumen": Derived(fn=ATP_stoi, args=['lumen_protons_per_turnover', 'n', 'b_H'], unit=None), 
                       }
    )

    m.add_reaction(
        name="v_CBB",
        fn= vCBB,
        args=['NADPH_st', 'k_CBB'],
        stoichiometry={"NADPH_st": -1}
    )

    m.add_reaction(
        name="v_KEA3",
        fn=_v_KEA3,
        args=['K_lu', 'H_lumen', 'H_stroma', 'K_st', 'k_KEA3'],
        stoichiometry={"K_lu": Derived(fn=value, args=['lumen_protons_per_turnover'], unit=None), 
                       "pH_lumen": Derived(fn=div, args=['lumen_protons_per_turnover', 'b_H'], unit=None), 
                       "Dpsi": Derived(fn=neg, args=['volt_per_charge'], unit=None), }
    )
    m.add_reaction(
        name="v_VKC",
        fn=_v_VKC,
        args=['K_lu', 'Dpsi', 'K_st', 'P_K'],
        stoichiometry={"K_lu": Derived(fn=neg, args=['lumen_protons_per_turnover'], unit=None), 
                       "Dpsi": Derived(fn=neg, args=['volt_per_charge'], unit=None), }
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