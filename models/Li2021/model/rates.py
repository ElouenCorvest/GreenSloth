from modelbase2 import Model, Derived
import numpy as np
from .basic_funcs import *

def vb6f(kb6f, Keq_b6f, PQ, PQH_2, PC_ox, PC_red):  #correct
    k_b6f_reverse = kb6f / Keq_b6f
    f_PQH2=PQH_2/(PQH_2+PQ) #want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ=1-f_PQH2
    v_b6f=f_PQH2*PC_ox*kb6f - f_PQ*PC_red*k_b6f_reverse
    return(v_b6f)

def vNDH1(Keq_NDH1, k_NDH1, Fd_red, Fd_ox, PQ, PQH_2): #correct
    kNDH1_rev = k_NDH1/Keq_NDH1
    vNDH1 = k_NDH1 * Fd_red * PQ - kNDH1_rev  * Fd_ox * PQH_2
    return vNDH1

def vPGR(PGR_vmax, Fd_red, PQ, PQH_2): #correct
    vPGR = PGR_vmax * (Fd_red**4/(Fd_red**4+0.1**4))*PQ/(PQ+PQH_2)
    return vPGR

def vVDE(VDE_max, pKvde, VDE_Hill, kZE, pH_lu, Vx, Zx): #correct
    pHmod= 1 / (10 ** (VDE_Hill*(pH_lu - pKvde)) + 1)
    vVDE = Vx * VDE_max * pHmod - Zx *kZE
    return vVDE

def vATPsynthase(pmf, light_per_L, protons_to_ATPsynthase, Hlumen, kLeak): #correct

    if isinstance(light_per_L, np.ndarray):
        light_per_L = light_per_L[0]
        if light_per_L > 0:
            vATPsynthase = protons_to_ATPsynthase + pmf*kLeak*Hlumen
        else:
            vATPsynthase = pmf*kLeak*Hlumen
    else:
        if light_per_L > 0:
            vATPsynthase = protons_to_ATPsynthase + pmf*kLeak*Hlumen
        else:
            vATPsynthase = pmf*kLeak*Hlumen

    return vATPsynthase

def vVCCN1(relative_VCCN1, Cl_lu, Cl_stroma, k_VCCN1): #correct
    vVCCN1 = k_VCCN1 * relative_VCCN1 * (Cl_stroma + Cl_lu)/2
    return vVCCN1

def vClCe(Cl_driving_force, pmf, Cl_lu, Cl_stroma, Hlumen, Hstroma, kClCe): #correct
    vClCe = kClCe*(Cl_driving_force*2+pmf)*(Cl_stroma + Cl_lu)*(Hlumen+Hstroma)/4
    return vClCe

def vKEA3(k_KEA3, reg_KEA3, Hlumen, Hstroma, K_lu, K_st): #correct
    vKEA3 = k_KEA3 * (Hlumen*K_st - Hstroma*K_lu) * reg_KEA3
    return vKEA3

def vVoltageK_channel(perm_K, dG_voltageK, K_lu, K_st): #correct
    vVoltageK_channel = perm_K * dG_voltageK*(K_lu+K_st)/2
    return vVoltageK_channel

def vPSII_charge_separation(PSII_antenna_size, PhiPSII, light_per_L): #correct
    PSII_charge_separation = PSII_antenna_size * light_per_L * PhiPSII
    return PSII_charge_separation

def vRecomb_PSII(dG_PSII_recomb, kRecomb, QAm): #correct
    Recomb_PSII = kRecomb * QAm * 10**(dG_PSII_recomb/0.06)
    return Recomb_PSII

def vPSII(PQH_2, QA_ox, PQ, QAm, kQA, Keq_QA_PQ): #correct
    vPSII = QAm * PQ * kQA - PQH_2 * QA_ox * (kQA / Keq_QA_PQ)
    return vPSII

def vPSI_charge_separation(Y0, light_per_L, PSI_antenna_size, Fd_ox): #correct
    PSI_charge_separation = Y0 * light_per_L * PSI_antenna_size * Fd_ox
    return PSI_charge_separation

def vPSI_PC_oxidation(PC_red, k_PC_to_P700, Y2):
    vPSI= PC_red * k_PC_to_P700 * Y2
    return vPSI

def vFNR(NADP_st, Fd_red, k_Fd_to_NADP): #correct
    vFNR = k_Fd_to_NADP*NADP_st*Fd_red
    return vFNR

def vCBB_consumption(kCBB, NADPH_st, NADP_st, time): #correct
    vCBB_consumption = kCBB * (1 - np.exp(-time/600))*(np.log(NADPH_st/NADP_st)-np.log(1.25))/(np.log(3.5/1.25))
    return vCBB_consumption

def vMehler(Fd_red, Fd_ox): #correct
    vMehler = 4*0.000265*Fd_red/(Fd_red+Fd_ox)
    return vMehler

def include_rates(
    m: Model
):

    m.add_reaction(
        name='vB6f',
        fn=vb6f,
        args=["kb6f", "Keq_b6f", "PQ", "PQH_2", "PC_ox", "PC_red"],
        stoichiometry={"PC_red": 1, "PC_ox":-1, "PQH_2":-0.5, "PQ":0.5, "pH_lu": Derived(neg_two_value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity']), "Dpsi": Derived(value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vNDH1',
        fn=vNDH1,
        args=["Keq_NDH1", "k_NDH1", "Fd_red", "Fd_ox", "PQ", "PQH_2"],
        stoichiometry={"Fd_red":-1, "Fd_ox":1, "PQ":-0.5, "PQH_2":0.5, "pH_lu":Derived(neg_two_value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity']), "Dpsi": Derived(two_times_value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vPGR',
        fn=vPGR,
        args=["PGR_vmax", "Fd_red", "PQ", "PQH_2"],
        stoichiometry={"Fd_red":-1, "Fd_ox":1, "PQ":-0.5, "PQH_2":0.5}
    )

    m.add_reaction(
        name='vVDE',
        fn=vVDE,
        args=["VDE_max", "pKvde", "VDE_Hill", "kZE", "pH_lu", "Vx", "Zx"],
        stoichiometry={"Vx": -1, "Zx": 1}
    )

    m.add_reaction(
        name='vATPsynthase',
        fn=vATPsynthase,
        args=["pmf", "Light_per_L","protons_to_ATPsynthase", "Hlumen", "kLeak"],
        stoichiometry={"pH_lu": Derived(fourteenthirds_value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity']), "Dpsi": Derived(times_neg_fourteen_thirds, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vVCCN1',
        fn=vVCCN1,
        args=["relative_VCCN1", "Cl_lu","Cl_stroma", "kVCCN1"],
        stoichiometry={"Cl_lu": Derived(value, args=['lumen_ions_per_turnover']), "Cl_stroma": Derived(neg_value, args=['stroma_ions_per_turnover']), "Dpsi": Derived(neg_value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vClCe',
        fn=vClCe,
        args=["Cl_driving_force", "pmf", "Cl_lu", "Cl_stroma", "Hlumen", "Hstroma", "kClCe"],
        stoichiometry={"pH_lu": Derived(value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity']), "Cl_lu": Derived(two_times_value, args=['lumen_ions_per_turnover']), "Cl_stroma": Derived(neg_two_times_value, args=['stroma_ions_per_turnover']), "Dpsi": Derived(neg_value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vKEA3',
        fn=vKEA3,
        args=["k_KEA3", "reg_KEA3", "Hlumen", "Hstroma", "K_lu", "K_st"],
        stoichiometry={"K_lu": Derived(value, args=['lumen_ions_per_turnover']), "K_st": Derived(neg_value, args=['stroma_ions_per_turnover']), "pH_lu": Derived(value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity'])}
    )

    m.add_reaction(
        name='vVoltageK_channel',
        fn=vVoltageK_channel,
        args=["perm_K", "dG_voltageK", "K_lu", "K_st"],
        stoichiometry={"K_lu": Derived(neg_value, args=['lumen_ions_per_turnover']), "K_st": Derived(value, args=['stroma_ions_per_turnover']), "Dpsi": Derived(neg_value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vPSII_charge_separation',
        fn=vPSII_charge_separation,
        args=["PSII_antenna_size", "PhiPSII", "Light_per_L"],
        stoichiometry={"QAm":1, "QA_ox":-1, "Dpsi": Derived(value, args=['volts_per_charge']),"pH_lu": Derived(neg_value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity'])}
    )

    m.add_reaction(
        name='vRecomb_PSII',
        fn=vRecomb_PSII,
        args=["dG_PSII_recomb", "kRecomb", "QAm"],
        stoichiometry={"QAm":-1, "QA_ox":1, "Dpsi": Derived(neg_value, args=['volts_per_charge']), "pH_lu": Derived(value1_divided_value2, args=['lumen_ions_per_turnover', 'buffering_capacity'])}
    )

    m.add_reaction(
        name='vPSII',
        fn=vPSII,
        args=["PQH_2", "QA_ox", "PQ", "QAm", "kQA", "Keq_QA_PQ"],
        stoichiometry={"QAm":-1, "QA_ox":1, "PQH_2":0.5, "PQ":-0.5}
    )

    m.add_reaction(
        name='vPSI_charge_separation',
        fn=vPSI_charge_separation,
        args=["Y0", "Light_per_L", "PSI_antenna_size", "Fd_ox"],
        stoichiometry={"Y2":1, "Y0":-1, "Fd_red":1, "Fd_ox":-1, "Dpsi": Derived(value, args=['volts_per_charge'])}
    )

    m.add_reaction(
        name='vPSI_PC_oxidation',
        fn=vPSI_PC_oxidation,
        args=["PC_red", "k_PC_to_P700", "Y2"],
        stoichiometry={"PC_ox":1, "PC_red":-1, "Y2":-1, "Y0":1}
    )

    m.add_reaction(
        name='vFNR',
        fn=vFNR,
        args=["NADP_st", "Fd_red", "k_Fd_to_NADP"],
        stoichiometry={"NADPH_st":0.5, "NADP_st":-0.5, "Fd_ox":1, "Fd_red":-1}
    )

    m.add_reaction(
        name='vCBB_consumption',
        fn=vCBB_consumption,
        args=["kCBB", "NADPH_st", "NADP_st", "time"],
        stoichiometry={"NADPH_st":-0.5, "NADP_st":0.5}
    )

    m.add_reaction(
        name='vMehler',
        fn=vMehler,
        args=["Fd_red", "Fd_ox"],
        stoichiometry={"Fd_red":-1, "Fd_ox":1}
    )

    return m
