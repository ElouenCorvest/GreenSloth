import numpy as np
from modelbase2 import Model

from . import basic_funcs as bf


def pH(H):
    return -np.log10(H * 2.5e-4)


def pHinv(pH):
    return 3.2e4 * 10**-pH


def K_QAPQ(F, E0_QA, E0_PQ, pH_st, R, T):
    RT = R * T
    DG1 = -F * E0_QA
    DG2 = -2 * F * E0_PQ + 2 * pH_st * np.log(10) * RT
    DG0 = -2 * DG1 + DG2
    Keq = np.exp(-DG0 / RT)
    return Keq


def K_cytb6f(pH_lu, F, E0_PQ, R, T, E0_PC, pH_st):
    """Equilibriu constant of Cytochrome b6f"""
    RT = R * T
    DG1 = -2 * F * E0_PQ + 2 * RT * np.log(10) * pH_lu
    DG2 = -F * E0_PC
    DG3 = RT * np.log(10) * (pH_st - pH_lu)
    DG = -DG1 + 2 * DG2 + 2 * DG3
    Keq = np.exp(-DG / RT)
    return Keq


def K_ATPsynth(pH_lu, DG_ATP, pH_st, R, T, Pi):
    """Equilibrium constant of ATP synthase. For more
    information see Matuszynska et al 2016 or Ebenhöh et al. 2011,2014
    """
    RT = R * T
    DG = DG_ATP - np.log(10) * (pH_st - pH_lu) * (14 / 3) * RT
    Keq = Pi * np.exp(-DG / RT)
    return Keq


def Quencher(psbS, Zx, PsbSP, K_ZSat, gamma_0, gamma_1, gamma_2, gamma_3):
    """Quencher mechanism

    accepts:
    psbS: fraction of non-protonated PsbS protein
    Vx: fraction of Violaxanthin
    """
    Zs = Zx / (Zx + K_ZSat)

    Q = (
        gamma_0 * (1 - Zs) * psbS
        + gamma_1 * (1 - Zs) * PsbSP
        + gamma_2 * Zs * PsbSP
        + gamma_3 * Zs * psbS
    )
    return Q


def PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot):
    # light = np.ones(len(P)) * light
    b0 = pfd + k_PQH2 * PQH_2 / K_QAPQ
    b1 = k_H * Q + k_F
    b2 = k_H * Q + k_F + k_P

    if any(
        [not isinstance(i, np.ndarray) for i in [b0, b1, k_PQH2, PQ, pfd, b2, PSII_tot]]
    ):
        M = np.array(
            [
                [-b0, b1, k_PQH2 * PQ, 0],  # B0
                [pfd, -b2, 0, 0],  # B1
                [0, 0, pfd, -b1],  # B3
                [1, 1, 1, 1],
            ]
        )

        A = np.array([0, 0, 0, PSII_tot])
        B0, B1, B2, B3 = np.linalg.solve(M, A)
        return B0, B1, B2, B3

    B0 = []
    B1 = []
    B2 = []
    B3 = []

    for b0, b1, k_PQH2, PQ, pfd, b2, PSII_tot in zip(
        b0, b1, k_PQH2, PQ, pfd, b2, PSII_tot, strict=False
    ):
        M = np.array(
            [
                [-b0, b1, k_PQH2 * PQ, 0],  # B0
                [pfd, -b2, 0, 0],  # B1
                [0, 0, pfd, -b1],  # B3
                [1, 1, 1, 1],
            ]
        )

        A = np.array([0, 0, 0, PSII_tot])
        B0_, B1_, B2_, B3_ = np.linalg.solve(M, A)
        B0.append(B0_)
        B1.append(B1_)
        B2.append(B2_)
        B3.append(B3_)

    return np.array(B0), np.array(B1), np.array(B2), np.array(B3)


def B0_PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot):
    B0, B1, B2, B3 = PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot)
    return B0


def B1_PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot):
    B0, B1, B2, B3 = PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot)
    return B1


def B2_PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot):
    B0, B1, B2, B3 = PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot)
    return B2


def B3_PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot):
    B0, B1, B2, B3 = PSII(PQ, PQH_2, Q, pfd, k_PQH2, K_QAPQ, k_H, k_F, k_P, PSII_tot)
    return B3


def Fluorescence(Q, B0, B2, k_H, k_F, k_P):
    """Fluorescence function"""
    Fluo = k_F / (k_H * Q + k_F + k_P) * B0 + k_F / (k_H * Q + k_F) * B2
    return Fluo


def include_derived_quantities(m: Model):
    m.add_derived(name="pH_lu", fn=pH, args=["H_lu"])

    m.add_derived(name="H_st", fn=pHinv, args=["pH_st"])

    m.add_derived(name="K_pHSat_inv", fn=pHinv, args=["K_pHSat"])

    m.add_derived(name="K_pHSatLHC_inv", fn=pHinv, args=["K_pHSatLHC"])

    m.add_derived(
        name="K_QAPQ", fn=K_QAPQ, args=["F", "E0_QA", "E0_PQ", "pH_st", "R", "T"]
    )

    m.add_derived(
        name="K_cytb6f",
        fn=K_cytb6f,
        args=["pH_lu", "F", "E0_PQ", "R", "T", "E0_PC", "pH_st"],
    )

    m.add_derived(
        name="K_ATPsynth",
        fn=K_ATPsynth,
        args=["pH_lu", "DG_ATP", "pH_st", "R", "T", "Pi"],
    )

    m.add_derived(name="PQ", fn=bf.continous_subtraction, args=["PQ_tot", "PQH_2"])

    m.add_derived(name="ADP_st", fn=bf.continous_subtraction, args=["AP_tot", "ATP_st"])

    m.add_derived(name="PsbSP", fn=bf.continous_subtraction, args=["PsbS_tot", "psbS"])

    m.add_derived(name="Zx", fn=bf.continous_subtraction, args=["X_tot", "Vx"])

    m.add_derived(
        name="Q",
        fn=Quencher,
        args=[
            "psbS",
            "Zx",
            "PsbSP",
            "K_ZSat",
            "gamma_0",
            "gamma_1",
            "gamma_2",
            "gamma_3",
        ],
    )

    m.add_derived(
        name="B0",
        fn=B0_PSII,
        args=[
            "PQ",
            "PQH_2",
            "Q",
            "pfd",
            "k_PQH2",
            "K_QAPQ",
            "k_H",
            "k_F",
            "k_P",
            "PSII_tot",
        ],
    )

    m.add_derived(
        name="B1",
        fn=B1_PSII,
        args=[
            "PQ",
            "PQH_2",
            "Q",
            "pfd",
            "k_PQH2",
            "K_QAPQ",
            "k_H",
            "k_F",
            "k_P",
            "PSII_tot",
        ],
    )

    m.add_derived(
        name="B2",
        fn=B2_PSII,
        args=[
            "PQ",
            "PQH_2",
            "Q",
            "pfd",
            "k_PQH2",
            "K_QAPQ",
            "k_H",
            "k_F",
            "k_P",
            "PSII_tot",
        ],
    )

    m.add_derived(
        name="B3",
        fn=B3_PSII,
        args=[
            "PQ",
            "PQH_2",
            "Q",
            "pfd",
            "k_PQH2",
            "K_QAPQ",
            "k_H",
            "k_F",
            "k_P",
            "PSII_tot",
        ],
    )

    m.add_derived(
        name="Fluo", fn=Fluorescence, args=["Q", "B0", "B2", "k_H", "k_F", "k_P"]
    )

    return m
