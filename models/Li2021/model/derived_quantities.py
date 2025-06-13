import numpy as np
from mxlpy import Model


def pH_to_proton(pH):
    return 10 ** (-1 * pH)


def ppPSII(PAR):
    return 0.84 * (PAR / 0.7)


def PMF(Dpsi, pH_lu, pH_st):  # correct
    PMF = Dpsi + 0.06 * (pH_st - pH_lu)
    return PMF


def PsbSP(pKa_PsbS, pH_lu):  # correct
    PsbS_H = 1 / (10 ** (3 * (pH_lu - pKa_PsbS)) + 1)
    return PsbS_H


def NPQ(NPQ_max, PsbSP, Zx):  # correct
    NPQ = 0.4 * NPQ_max * PsbSP * Zx + 0.5 * NPQ_max * PsbSP + 0.1 * NPQ_max * Zx
    return NPQ


def K_b6f(Em_PC_pH7, Em_PQH2_pH7, pH_lu, PMF):  # correct
    Em_PC = Em_PC_pH7
    Em_PQH2 = Em_PQH2_pH7 - 0.06 * (pH_lu - 7.0)
    K_b6f = 10 ** ((Em_PC - Em_PQH2 - PMF) / 0.06)
    return K_b6f


# def pmf_activity(ATP_st, ADP, Pi_st, DeltaG0_ATP, F, HPR):  # correct
#     dGATP = DeltaG0_ATP + 2.44 * np.log(ATP_st / (ADP * Pi_st))  # in kJ/mol
#     pmf_activity = dGATP / (F * HPR)
#     return pmf_activity


def k_b6f(Vmax_b6f, c_b6f, pKa_reg, pH_lu):  # correct
    # pHmod is the fraction of b6f complex that is deprotonated
    pHmod = 1 - (1 / (10 ** (pH_lu - pKa_reg) + 1))
    b6f_deprot = pHmod * c_b6f
    k_b6f = b6f_deprot * Vmax_b6f
    return k_b6f


def K_NDH1(pH_st, PMF, Em_PQH2_pH7, Em_Fd):  # correct
    Em_PQH2 = Em_PQH2_pH7 - 0.06 * (pH_st - 7.0)
    deltaEm = Em_PQH2 - Em_Fd
    K_NDH1 = 10 ** ((deltaEm - PMF * 2) / 0.06)
    return K_NDH1


def Act_ATPsynth(time):
    x = time / 165
    actvity = 0.2 + 0.8 * (x**4 / (x**4 + 1))
    return actvity


def Prot_ATPsynth(PMF, Act_ATPsynth, Vmax_ATPsynth, HPR):
    v_proton_active = 1 - (
        1 / (10 ** ((PMF - 0.132) * 1.5 / 0.06) + 1)
    )  # reduced ATP synthase
    v_proton_inert = 1 - (
        1 / (10 ** ((PMF - 0.204) * 1.5 / 0.06) + 1)
    )  # oxidized ATP synthase
    v_active = Act_ATPsynth * v_proton_active * HPR * Vmax_ATPsynth
    v_inert = (1 - Act_ATPsynth) * v_proton_inert * HPR * Vmax_ATPsynth
    Prot_ATPsynth = v_active + v_inert
    return Prot_ATPsynth


def PhiPSII(QA_ox, NPQ):  # quantum yield of photosystem II #correct
    PhiPSII = 1 / (1 + (1 + NPQ) / (4.88 * QA_ox))
    return PhiPSII


def PSII_ChSep(sigma0_II, PhiPSII, ppPSII):
    PSII_ChSep = sigma0_II * ppPSII * PhiPSII
    return PSII_ChSep


def PSII_recomb(k_recomb, QA_red, Dpsi, pH_lu):  # correct
    dG_PSII_recomb = Dpsi + 0.06 * (7.0 - pH_lu)
    PSII_recomb = k_recomb * QA_red * 10 ** (dG_PSII_recomb / 0.06)
    return PSII_recomb


def singlet_O2(PSII_recomb, phi_triplet, phi_1O2):  # correct
    singlet_O2 = PSII_recomb * phi_triplet * phi_1O2
    return singlet_O2


def Cl_df(Dpsi, Cl_lu, Cl_st):  # correct
    Cl_df = 0.06 * np.log10(Cl_st / Cl_lu) + Dpsi
    return Cl_df


def include_derived_quantities(m: Model):
    m.add_derived(name="H_lu", fn=pH_to_proton, args=["pH_lu"])

    m.add_derived(name="H_st", fn=pH_to_proton, args=["pH_st"])

    m.add_derived(name="ppPSII", fn=ppPSII, args=["PAR"])

    m.add_derived(name="PMF", fn=PMF, args=["Dpsi", "pH_lu", "pH_st"])

    m.add_derived(name="PsbSP", fn=PsbSP, args=["pKa_PsbS", "pH_lu"])

    m.add_derived(name="NPQ", fn=NPQ, args=["NPQ_max", "PsbSP", "Zx"])

    m.add_derived(
        name="K_b6f", fn=K_b6f, args=["Em_PC_pH7", "Em_PQH2_pH7", "pH_lu", "PMF"]
    )

    # m.add_derived(
    #     name="pmf_activity",
    #     fn=pmf_activity,
    #     args=["ATP_st", "ADP", "Pi_st", "DeltaG0_ATP", "F", "HPR"],
    # )

    m.add_derived(
        name="k_b6f", fn=k_b6f, args=["Vmax_b6f", "c_b6f", "pKa_reg", "pH_lu"]
    )

    m.add_derived(
        name="K_NDH1", fn=K_NDH1, args=["pH_st", "PMF", "Em_PQH2_pH7", "Em_Fd"]
    )

    m.add_derived(name="Act_ATPsynth", fn=Act_ATPsynth, args=["time"])

    m.add_derived(
        name="Prot_ATPsynth",
        fn=Prot_ATPsynth,
        args=["PMF", "Act_ATPsynth", "Vmax_ATPsynth", "HPR"],
    )

    m.add_derived(name="PhiPSII", fn=PhiPSII, args=["QA_ox", "NPQ"])

    m.add_derived(
        name="PSII_ChSep",
        fn=PSII_ChSep,
        args=["sigma0_II", "PhiPSII", "ppPSII"],
    )

    m.add_derived(
        name="PSII_recomb",
        fn=PSII_recomb,
        args=["k_recomb", "QA_red", "Dpsi", "pH_lu"],
    )

    m.add_derived(
        name="singO2",
        fn=singlet_O2,
        args=["PSII_recomb", "phi_triplet", "phi_1O2"],
    )

    m.add_derived(name="Cl_df", fn=Cl_df, args=["Dpsi", "Cl_lu", "Cl_st"])

    return m
