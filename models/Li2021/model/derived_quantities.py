from modelbase2 import Model
import numpy as np
from .basic_funcs import *  # noqa: F403


def pH_to_proton(pH):
    return 10 ** (-1 * pH)


def Light_per_L(PAR):
    return 0.84 * (PAR / 0.7)


def pmf(Dpsi, pH_lu, pHstroma):  # correct
    pmf = Dpsi + 0.06 * (pHstroma - pH_lu)
    return pmf


def PsbS_protonation(pKPsbS, pH_lu):  # correct
    PsbS_H = 1 / (10 ** (3 * (pH_lu - pKPsbS)) + 1)
    return PsbS_H


def NPQ(max_NPQ, PsbS_protonation, Zx):  # correct
    NPQ = (
        0.4 * max_NPQ * PsbS_protonation * Zx
        + 0.5 * max_NPQ * PsbS_protonation
        + 0.1 * max_NPQ * Zx
    )
    return NPQ


def Keq_b6f(Em7_PC, Em7_PQH2, pH_lu, pmf):  # correct
    Em_PC = Em7_PC
    Em_PQH2 = Em7_PQH2 - 0.06 * (pH_lu - 7.0)
    Keq_b6f = 10 ** ((Em_PC - Em_PQH2 - pmf) / 0.06)
    return Keq_b6f


def pmf_activity(ATP_st, ADP, Pi, dG0ATP, F, HPR):  # correct
    dGATP = dG0ATP + 2.44 * np.log(ATP_st / (ADP * Pi))  # in kJ/mol
    pmf_activity = dGATP / (F * HPR)
    return pmf_activity


def kb6f(max_b6f, b6f_content, pKreg, pH_lu):  # correct
    # pHmod is the fraction of b6f complex that is deprotonated
    pHmod = 1 - (1 / (10 ** (pH_lu - pKreg) + 1))
    b6f_deprot = pHmod * b6f_content
    k_b6f = b6f_deprot * max_b6f
    return k_b6f


def Keq_NDH1(pHstroma, pmf, Em7_PQH2, Em_Fd):  # correct
    Em_PQH2 = Em7_PQH2 - 0.06 * (pHstroma - 7.0)
    deltaEm = Em_PQH2 - Em_Fd
    Keq_NDH1 = 10 ** ((deltaEm - pmf * 2) / 0.06)
    return Keq_NDH1


def ATPsynthase_activity(time):
    x = time / 165
    actvity = 0.2 + 0.8 * (x**4 / (x**4 + 1))
    return actvity


def protons_to_ATPsynthase(pmf, ATPsynthase_activity, max_ATPsynthase, HPR):
    v_proton_active = 1 - (
        1 / (10 ** ((pmf - 0.132) * 1.5 / 0.06) + 1)
    )  # reduced ATP synthase
    v_proton_inert = 1 - (
        1 / (10 ** ((pmf - 0.204) * 1.5 / 0.06) + 1)
    )  # oxidized ATP synthase
    v_active = ATPsynthase_activity * v_proton_active * HPR * max_ATPsynthase
    v_inert = (1 - ATPsynthase_activity) * v_proton_inert * HPR * max_ATPsynthase
    protons_to_ATPsynthase = v_active + v_inert
    return protons_to_ATPsynthase


def PhiPSII(QA_ox, NPQ):  # quantum yield of photosystem II #correct
    PhiPSII = 1 / (1 + (1 + NPQ) / (4.88 * QA_ox))
    return PhiPSII


def PSII_charge_separation(PSII_antenna_size, PhiPSII, light_per_L):
    PSII_charge_separation = PSII_antenna_size * light_per_L * PhiPSII
    return PSII_charge_separation


def dG_PSII_recomb(pH_lu, Dpsi):  # correct
    dG_PSII_recomb = Dpsi + 0.06 * (7.0 - pH_lu)
    return dG_PSII_recomb


def Recomb_PSII(dG_PSII_recomb, kRecomb, QA_red):  # correct
    Recomb_PSII = kRecomb * QA_red * 10 ** (dG_PSII_recomb / 0.06)
    return Recomb_PSII


def singletO2(Recomb_PSII, triplet_yield, triplet_to_singletO2_yield):  # correct
    singletO2 = Recomb_PSII * triplet_yield * triplet_to_singletO2_yield
    return singletO2


def Cl_driving_force(Dpsi, Cl_lu, Cl_st):  # correct
    Cl_driving_force = 0.06 * np.log10(Cl_st / Cl_lu) + Dpsi
    return Cl_driving_force


def relative_VCCN1(
    Cl_driving_force,
):  # empirical equation was obtained from Herdean et al. 2016 DOI: 10.1038/ncomms11654
    relative_VCCN1 = (
        332 * (Cl_driving_force**3)
        + 30.8 * (Cl_driving_force**2)
        + 3.6 * Cl_driving_force
    )
    return relative_VCCN1


def reg_KEA3(pH_lu, QA_red):  # correct
    qL = 1 - QA_red
    qL_act = qL**3 / (qL**3 + 0.15**3)
    pH_act = 1 / (10 ** (1 * (pH_lu - 6.0)) + 1)
    reg_KEA3 = qL_act * pH_act
    return reg_KEA3


def dG_voltageK(Dpsi, K_lu, K_st):  # correct
    dG_voltageK = -0.06 * np.log10(K_st / K_lu) + Dpsi
    return dG_voltageK


def include_derived_quantities(m: Model):
    m.add_derived(name="Hlumen", fn=pH_to_proton, args=["pH_lu"])

    m.add_derived(name="Hstroma", fn=pH_to_proton, args=["pHstroma"])

    m.add_derived(name="Light_per_L", fn=Light_per_L, args=["light_per_L"])

    m.add_derived(name="pmf", fn=pmf, args=["Dpsi", "pH_lu", "pHstroma"])

    m.add_derived(
        name="PsbS_protonation", fn=PsbS_protonation, args=["pKPsbS", "pH_lu"]
    )

    m.add_derived(name="NPQ", fn=NPQ, args=["max_NPQ", "PsbS_protonation", "Zx"])

    m.add_derived(
        name="Keq_b6f", fn=Keq_b6f, args=["Em7_PC", "Em7_PQH2", "pH_lu", "pmf"]
    )

    m.add_derived(
        name="pmf_activity",
        fn=pmf_activity,
        args=["ATP_st", "ADP", "Pi", "dG0ATP", "F", "HPR"],
    )

    m.add_derived(
        name="kb6f", fn=kb6f, args=["max_b6f", "b6f_content", "pKreg", "pH_lu"]
    )

    m.add_derived(
        name="Keq_NDH1", fn=Keq_NDH1, args=["pHstroma", "pmf", "Em7_PQH2", "Em_Fd"]
    )

    m.add_derived(name="ATPsynthase_activity", fn=ATPsynthase_activity, args=["time"])

    m.add_derived(
        name="protons_to_ATPsynthase",
        fn=protons_to_ATPsynthase,
        args=["pmf", "ATPsynthase_activity", "max_ATPsynthase", "HPR"],
    )

    m.add_derived(name="PhiPSII", fn=PhiPSII, args=["QA_ox", "NPQ"])

    m.add_derived(
        name="PSII_charge_separation",
        fn=PSII_charge_separation,
        args=["PSII_antenna_size", "PhiPSII", "Light_per_L"],
    )

    m.add_derived(name="dG_PSII_recomb", fn=dG_PSII_recomb, args=["pH_lu", "Dpsi"])

    m.add_derived(
        name="Recomb_PSII", fn=Recomb_PSII, args=["dG_PSII_recomb", "kRecomb", "QA_red"]
    )

    m.add_derived(
        name="singlet_O2",
        fn=singletO2,
        args=["Recomb_PSII", "triplet_yield", "triplet_to_singletO2_yield"],
    )

    m.add_derived(
        name="Cl_driving_force", fn=Cl_driving_force, args=["Dpsi", "Cl_lu", "Cl_st"]
    )

    m.add_derived(name="relative_VCCN1", fn=relative_VCCN1, args=["Cl_driving_force"])

    m.add_derived(name="reg_KEA3", fn=reg_KEA3, args=["pH_lu", "QA_red"])

    m.add_derived(name="dG_voltageK", fn=dG_voltageK, args=["Dpsi", "K_lu", "K_st"])

    return m
