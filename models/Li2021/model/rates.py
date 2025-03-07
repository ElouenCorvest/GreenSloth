from modelbase2 import Model, Derived
import numpy as np
from .basic_funcs import (
    value,
    value1_divided_value2,
    neg_value,
    neg_value1_divided_value2,
    neg_two_times_value,
    fourteenthirds_value1_divided_value2,
    times_neg_fourteen_thirds,
    neg_two_value1_divided_value2,
    two_times_value,
)


def vb6f(k_b6f, K_b6f, PQ, PQH_2, PC_ox, PC_red):  # correct
    k_b6f_reverse = k_b6f / K_b6f
    f_PQH2 = PQH_2 / (
        PQH_2 + PQ
    )  # want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ = 1 - f_PQH2
    v_b6f = f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse
    return v_b6f


def vNDH1(K_NDH1, k_NDH1, Fd_red, Fd_ox, PQ, PQH_2):  # correct
    kNDH1_rev = k_NDH1 / K_NDH1
    vNDH1 = k_NDH1 * Fd_red * PQ - kNDH1_rev * Fd_ox * PQH_2
    return vNDH1


def vPGR(Vmax_PGR, Fd_red, PQ, PQH_2):  # correct
    vPGR = Vmax_PGR * (Fd_red**4 / (Fd_red**4 + 0.1**4)) * PQ / (PQ + PQH_2)
    return vPGR


def vVDE(Vmax_VDE, pKa_VDE, nh_VDE, k_EZ, pH_lu, Vx, Zx):  # correct
    pHmod = 1 / (10 ** (nh_VDE * (pH_lu - pKa_VDE)) + 1)
    vVDE = Vx * Vmax_VDE * pHmod - Zx * k_EZ
    return vVDE


def vATPsynthase(PMF, ppPSII, Prot_ATPsynth, H_lu, k_Leak):  # correct
    if isinstance(ppPSII, np.ndarray):
        ppPSII = ppPSII[0]
        if ppPSII > 0:
            vATPsynthase = Prot_ATPsynth + PMF * k_Leak * H_lu
        else:
            vATPsynthase = PMF * k_Leak * H_lu
    else:
        if ppPSII > 0:
            vATPsynthase = Prot_ATPsynth + PMF * k_Leak * H_lu
        else:
            vATPsynthase = PMF * k_Leak * H_lu

    return vATPsynthase


def vVCCN1(Cl_df, Cl_lu, Cl_st, k_VCCN1):  # correct
    relative_VCCN1 = 332 * (Cl_df**3) + 30.8 * (Cl_df**2) + 3.6 * Cl_df
    vVCCN1 = k_VCCN1 * relative_VCCN1 * (Cl_st + Cl_lu) / 2
    return vVCCN1


def vClCe(Cl_df, PMF, Cl_lu, Cl_st, H_lu, H_st, k_ClCe):  # correct
    vClCe = k_ClCe * (Cl_df * 2 + PMF) * (Cl_st + Cl_lu) * (H_lu + H_st) / 4
    return vClCe


def vKEA3(k_KEA3, QA_red, pH_lu, H_lu, H_st, K_lu, K_st):  # correct
    qL = 1 - QA_red
    qL_act = qL**3 / (qL**3 + 0.15**3)
    pH_act = 1 / (10 ** (1 * (pH_lu - 6.0)) + 1)
    reg_KEA3 = qL_act * pH_act
    vKEA3 = k_KEA3 * (H_lu * K_st - H_st * K_lu) * reg_KEA3
    return vKEA3


def vVoltageK_channel(P_K, Dpsi, K_lu, K_st):  # correct
    dG_voltageK = -0.06 * np.log10(K_st / K_lu) + Dpsi
    vVoltageK_channel = P_K * dG_voltageK * (K_lu + K_st) / 2
    return vVoltageK_channel


def vPSII(PQH_2, QA_ox, PQ, QA_red, k_QA, K_QA):  # correct
    vPSII = QA_red * PQ * k_QA - PQH_2 * QA_ox * (k_QA / K_QA)
    return vPSII


def vPSI_charge_separation(Y0, ppPSII, sigma0_I, Fd_ox):  # correct
    PSI_charge_separation = Y0 * ppPSII * sigma0_I * Fd_ox
    return PSI_charge_separation


def vPSI_PC_oxidation(PC_red, k_PCtoP700, Y2):
    vPSI = PC_red * k_PCtoP700 * Y2
    return vPSI


def vFNR(NADP_st, Fd_red, k_FdtoNADP):  # correct
    vFNR = k_FdtoNADP * NADP_st * Fd_red
    return vFNR


def vCBB_consumption(k_CBB, NADPH_st, NADP_st, time):  # correct
    vCBB_consumption = (
        k_CBB
        * (1 - np.exp(-time / 600))
        * (np.log(NADPH_st / NADP_st) - np.log(1.25))
        / (np.log(3.5 / 1.25))
    )
    return vCBB_consumption


def vMehler(Fd_red, Fd_ox):  # correct
    vMehler = 4 * 0.000265 * Fd_red / (Fd_red + Fd_ox)
    return vMehler


def include_rates(m: Model):
    m.add_reaction(
        name="vB6f",
        fn=vb6f,
        args=["k_b6f", "K_b6f", "PQ", "PQH_2", "PC_ox", "PC_red"],
        stoichiometry={
            "PC_red": 1,
            "PC_ox": -1,
            "PQH_2": -0.5,
            "PQ": 0.5,
            "pH_lu": Derived(neg_two_value1_divided_value2, args=["ipt_lu", "b_H"]),
            "Dpsi": Derived(value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vNDH1",
        fn=vNDH1,
        args=["K_NDH1", "k_NDH1", "Fd_red", "Fd_ox", "PQ", "PQH_2"],
        stoichiometry={
            "Fd_red": -1,
            "Fd_ox": 1,
            "PQ": -0.5,
            "PQH_2": 0.5,
            "pH_lu": Derived(neg_two_value1_divided_value2, args=["ipt_lu", "b_H"]),
            "Dpsi": Derived(two_times_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vPGR",
        fn=vPGR,
        args=["Vmax_PGR", "Fd_red", "PQ", "PQH_2"],
        stoichiometry={"Fd_red": -1, "Fd_ox": 1, "PQ": -0.5, "PQH_2": 0.5},
    )

    m.add_reaction(
        name="vVDE",
        fn=vVDE,
        args=["Vmax_VDE", "pKa_VDE", "nh_VDE", "k_EZ", "pH_lu", "Vx", "Zx"],
        stoichiometry={"Vx": -1, "Zx": 1},
    )

    m.add_reaction(
        name="vATPsynthase",
        fn=vATPsynthase,
        args=["PMF", "ppPSII", "Prot_ATPsynth", "H_lu", "k_Leak"],
        stoichiometry={
            "pH_lu": Derived(
                fourteenthirds_value1_divided_value2, args=["ipt_lu", "b_H"]
            ),
            "Dpsi": Derived(times_neg_fourteen_thirds, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vVCCN1",
        fn=vVCCN1,
        args=["Cl_df", "Cl_lu", "Cl_st", "k_VCCN1"],
        stoichiometry={
            "Cl_lu": Derived(value, args=["ipt_lu"]),
            "Cl_st": Derived(neg_value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vClCe",
        fn=vClCe,
        args=[
            "Cl_df",
            "PMF",
            "Cl_lu",
            "Cl_st",
            "H_lu",
            "H_st",
            "k_ClCe",
        ],
        stoichiometry={
            "pH_lu": Derived(value1_divided_value2, args=["ipt_lu", "b_H"]),
            "Cl_lu": Derived(neg_two_times_value, args=["ipt_lu"]),
            "Cl_st": Derived(neg_two_times_value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vKEA3",
        fn=vKEA3,
        args=["k_KEA3", "QA_red", "pH_lu", "H_lu", "H_st", "K_lu", "K_st"],
        stoichiometry={
            "K_lu": Derived(value, args=["ipt_lu"]),
            "K_st": Derived(neg_value, args=["ipt_st"]),
            "pH_lu": Derived(value1_divided_value2, args=["ipt_lu", "b_H"]),
        },
    )

    m.add_reaction(
        name="vVoltageK_channel",
        fn=vVoltageK_channel,
        args=["P_K", "Dpsi", "K_lu", "K_st"],
        stoichiometry={
            "K_lu": Derived(neg_value, args=["ipt_lu"]),
            "K_st": Derived(value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vPSII_charge_separation",
        fn=value,
        args=["ChSep_PSII"],
        stoichiometry={
            "QA_red": 1,
            "QA_ox": -1,
            "Dpsi": Derived(value, args=["vpc"]),
            "pH_lu": Derived(neg_value1_divided_value2, args=["ipt_lu", "b_H"]),
        },
    )

    m.add_reaction(
        name="vRecomb_PSII",
        fn=value,
        args=["PSII_recomb"],
        stoichiometry={
            "QA_red": -1,
            "QA_ox": 1,
            "Dpsi": Derived(neg_value, args=["vpc"]),
            "pH_lu": Derived(value1_divided_value2, args=["ipt_lu", "b_H"]),
        },
    )

    m.add_reaction(
        name="vPSII",
        fn=vPSII,
        args=["PQH_2", "QA_ox", "PQ", "QA_red", "k_QA", "K_QA"],
        stoichiometry={"QA_red": -1, "QA_ox": 1, "PQH_2": 0.5, "PQ": -0.5},
    )

    m.add_reaction(
        name="vPSI_charge_separation",
        fn=vPSI_charge_separation,
        args=["Y0", "ppPSII", "sigma0_I", "Fd_ox"],
        stoichiometry={
            "Y2": 1,
            "Y0": -1,
            "Fd_red": 1,
            "Fd_ox": -1,
            "Dpsi": Derived(value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vPSI_PC_oxidation",
        fn=vPSI_PC_oxidation,
        args=["PC_red", "k_PCtoP700", "Y2"],
        stoichiometry={"PC_ox": 1, "PC_red": -1, "Y2": -1, "Y0": 1},
    )

    m.add_reaction(
        name="vFNR",
        fn=vFNR,
        args=["NADP_st", "Fd_red", "k_FdtoNADP"],
        stoichiometry={"NADPH_st": 0.5, "NADP_st": -0.5, "Fd_ox": 1, "Fd_red": -1},
    )

    m.add_reaction(
        name="vCBB_consumption",
        fn=vCBB_consumption,
        args=["k_CBB", "NADPH_st", "NADP_st", "time"],
        stoichiometry={"NADPH_st": -0.5, "NADP_st": 0.5},
    )

    m.add_reaction(
        name="vMehler",
        fn=vMehler,
        args=["Fd_red", "Fd_ox"],
        stoichiometry={"Fd_red": -1, "Fd_ox": 1},
    )

    return m
