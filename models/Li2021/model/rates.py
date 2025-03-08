from modelbase2 import Model, Derived
import numpy as np
from greensloth_utils.basicfuncs import (
    value,
    value1_divided_value2,
    neg_value,
    neg_value1_divided_value2,
    neg_two_value,
    fourteenthirds_value1_divided_value2,
    neg_fourteen_thirds_value,
    neg_two_value1_divided_value2,
    two_value,
)


def vb6f(k_b6f, K_b6f, PQ, PQH_2, PC_ox, PC_red):  # correct
    k_b6f_reverse = k_b6f / K_b6f
    f_PQH2 = PQH_2 / (
        PQH_2 + PQ
    )  # want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ = 1 - f_PQH2
    v_b6f = f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse
    return v_b6f


def v_NDH(K_NDH1, k_NDH1, Fd_red, Fd_ox, PQ, PQH_2):  # correct
    kNDH1_rev = k_NDH1 / K_NDH1
    v_NDH = k_NDH1 * Fd_red * PQ - kNDH1_rev * Fd_ox * PQH_2
    return v_NDH


def v_PGR(Vmax_PGR, Fd_red, PQ, PQH_2):  # correct
    v_PGR = Vmax_PGR * (Fd_red**4 / (Fd_red**4 + 0.1**4)) * PQ / (PQ + PQH_2)
    return v_PGR


def v_Deepox(Vmax_VDE, pKa_VDE, nh_VDE, k_EZ, pH_lu, Vx, Zx):  # correct
    pHmod = 1 / (10 ** (nh_VDE * (pH_lu - pKa_VDE)) + 1)
    v_Deepox = Vx * Vmax_VDE * pHmod - Zx * k_EZ
    return v_Deepox


def v_ATPsynth(PMF, ppPSII, Prot_ATPsynth, H_lu, k_Leak):  # correct
    if isinstance(ppPSII, np.ndarray):
        ppPSII = ppPSII[0]
        if ppPSII > 0:
            v_ATPsynth = Prot_ATPsynth + PMF * k_Leak * H_lu
        else:
            v_ATPsynth = PMF * k_Leak * H_lu
    else:
        if ppPSII > 0:
            v_ATPsynth = Prot_ATPsynth + PMF * k_Leak * H_lu
        else:
            v_ATPsynth = PMF * k_Leak * H_lu

    return v_ATPsynth


def v_VCCN1(Cl_df, Cl_lu, Cl_st, k_VCCN1):  # correct
    relative_VCCN1 = 332 * (Cl_df**3) + 30.8 * (Cl_df**2) + 3.6 * Cl_df
    v_VCCN1 = k_VCCN1 * relative_VCCN1 * (Cl_st + Cl_lu) / 2
    return v_VCCN1


def v_ClCe(Cl_df, PMF, Cl_lu, Cl_st, H_lu, H_st, k_ClCe):  # correct
    v_ClCe = k_ClCe * (Cl_df * 2 + PMF) * (Cl_st + Cl_lu) * (H_lu + H_st) / 4
    return v_ClCe


def v_KEA3(k_KEA3, QA_red, pH_lu, H_lu, H_st, K_lu, K_st):  # correct
    qL = 1 - QA_red
    qL_act = qL**3 / (qL**3 + 0.15**3)
    pH_act = 1 / (10 ** (1 * (pH_lu - 6.0)) + 1)
    reg_KEA3 = qL_act * pH_act
    v_KEA3 = k_KEA3 * (H_lu * K_st - H_st * K_lu) * reg_KEA3
    return v_KEA3


def v_VKC(P_K, Dpsi, K_lu, K_st):  # correct
    dG_voltageK = -0.06 * np.log10(K_st / K_lu) + Dpsi
    v_VKC = P_K * dG_voltageK * (K_lu + K_st) / 2
    return v_VKC


def v_PSII(PQH_2, QA_ox, PQ, QA_red, k_QA, K_QA):  # correct
    v_PSII = QA_red * PQ * k_QA - PQH_2 * QA_ox * (k_QA / K_QA)
    return v_PSII


def PSI_ChSep(Y0, ppPSII, sigma0_I, Fd_ox):  # correct
    PSI_charge_separation = Y0 * ppPSII * sigma0_I * Fd_ox
    return PSI_charge_separation


def v_PSI_PCoxid(PC_red, k_PCtoP700, Y2):
    vPSI = PC_red * k_PCtoP700 * Y2
    return vPSI


def v_FNR(NADP_st, Fd_red, k_FdtoNADP):  # correct
    v_FNR = k_FdtoNADP * NADP_st * Fd_red
    return v_FNR


def v_CBB(k_CBB, NADPH_st, NADP_st, time):  # correct
    v_CBB = (
        k_CBB
        * (1 - np.exp(-time / 600))
        * (np.log(NADPH_st / NADP_st) - np.log(1.25))
        / (np.log(3.5 / 1.25))
    )
    return v_CBB


def v_Mehler(Fd_red, Fd_ox):  # correct
    v_Mehler = 4 * 0.000265 * Fd_red / (Fd_red + Fd_ox)
    return v_Mehler


def include_rates(m: Model):
    m.add_reaction(
        name="v_b6f",
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
        name="v_NDH",
        fn=v_NDH,
        args=["K_NDH1", "k_NDH1", "Fd_red", "Fd_ox", "PQ", "PQH_2"],
        stoichiometry={
            "Fd_red": -1,
            "Fd_ox": 1,
            "PQ": -0.5,
            "PQH_2": 0.5,
            "pH_lu": Derived(neg_two_value1_divided_value2, args=["ipt_lu", "b_H"]),
            "Dpsi": Derived(two_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="v_PGR",
        fn=v_PGR,
        args=["Vmax_PGR", "Fd_red", "PQ", "PQH_2"],
        stoichiometry={"Fd_red": -1, "Fd_ox": 1, "PQ": -0.5, "PQH_2": 0.5},
    )

    m.add_reaction(
        name="v_Deepox",
        fn=v_Deepox,
        args=["Vmax_VDE", "pKa_VDE", "nh_VDE", "k_EZ", "pH_lu", "Vx", "Zx"],
        stoichiometry={"Vx": -1, "Zx": 1},
    )

    m.add_reaction(
        name="v_ATPsynth",
        fn=v_ATPsynth,
        args=["PMF", "ppPSII", "Prot_ATPsynth", "H_lu", "k_Leak"],
        stoichiometry={
            "pH_lu": Derived(
                fourteenthirds_value1_divided_value2, args=["ipt_lu", "b_H"]
            ),
            "Dpsi": Derived(neg_fourteen_thirds_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="v_VCCN1",
        fn=v_VCCN1,
        args=["Cl_df", "Cl_lu", "Cl_st", "k_VCCN1"],
        stoichiometry={
            "Cl_lu": Derived(value, args=["ipt_lu"]),
            "Cl_st": Derived(neg_value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="v_ClCe",
        fn=v_ClCe,
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
            "Cl_lu": Derived(two_value, args=["ipt_lu"]),
            "Cl_st": Derived(neg_two_value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="v_KEA3",
        fn=v_KEA3,
        args=["k_KEA3", "QA_red", "pH_lu", "H_lu", "H_st", "K_lu", "K_st"],
        stoichiometry={
            "K_lu": Derived(value, args=["ipt_lu"]),
            "K_st": Derived(neg_value, args=["ipt_st"]),
            "pH_lu": Derived(value1_divided_value2, args=["ipt_lu", "b_H"]),
        },
    )

    m.add_reaction(
        name="v_VKC",
        fn=v_VKC,
        args=["P_K", "Dpsi", "K_lu", "K_st"],
        stoichiometry={
            "K_lu": Derived(neg_value, args=["ipt_lu"]),
            "K_st": Derived(value, args=["ipt_st"]),
            "Dpsi": Derived(neg_value, args=["vpc"]),
        },
    )

    m.add_reaction(
        name="vPSII_ChSep",
        fn=value,
        args=["PSII_ChSep"],
        stoichiometry={
            "QA_red": 1,
            "QA_ox": -1,
            "Dpsi": Derived(value, args=["vpc"]),
            "pH_lu": Derived(neg_value1_divided_value2, args=["ipt_lu", "b_H"]),
        },
    )

    m.add_reaction(
        name="vPSII_recomb",
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
        name="v_PSII",
        fn=v_PSII,
        args=["PQH_2", "QA_ox", "PQ", "QA_red", "k_QA", "K_QA"],
        stoichiometry={"QA_red": -1, "QA_ox": 1, "PQH_2": 0.5, "PQ": -0.5},
    )

    m.add_reaction(
        name="PSI_ChSep",
        fn=PSI_ChSep,
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
        name="v_PSI_PCoxid",
        fn=v_PSI_PCoxid,
        args=["PC_red", "k_PCtoP700", "Y2"],
        stoichiometry={"PC_ox": 1, "PC_red": -1, "Y2": -1, "Y0": 1},
    )

    m.add_reaction(
        name="v_FNR",
        fn=v_FNR,
        args=["NADP_st", "Fd_red", "k_FdtoNADP"],
        stoichiometry={"NADPH_st": 0.5, "NADP_st": -0.5, "Fd_ox": 1, "Fd_red": -1},
    )

    m.add_reaction(
        name="v_CBB",
        fn=v_CBB,
        args=["k_CBB", "NADPH_st", "NADP_st", "time"],
        stoichiometry={"NADPH_st": -0.5, "NADP_st": 0.5},
    )

    m.add_reaction(
        name="v_Mehler",
        fn=v_Mehler,
        args=["Fd_red", "Fd_ox"],
        stoichiometry={"Fd_red": -1, "Fd_ox": 1},
    )

    return m
