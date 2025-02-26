from modelbase2 import Model
import numpy as np
import numpy.typing as npt
from .basic_funcs import continous_subtraction, proportional

def H_st(pH_stroma: float) -> float:
    """Calculate stromal H concentration from stromal pH

    Args:
        pH_stroma (float): Stromal pH

    Returns:
        float: Stromal H concentration
    """
    return 3.2e4 * 10 ** (-pH_stroma)

def Keq_nernst_S1_P1(SE0: float, PE0: float, R: float, T: float, F: float) -> float:
    """Calculation of equilibrium constant of reaction: S -> P.

    Args:
        SE0 (float): Standard electrode potential of Substrate
        PE0 (float): Standard electrode potential of Product
        R (float): Universal gas constant
        T (float): Temperature in Kelvin
        F (float): Farraday Constant

    Returns:
        float: Equilibrium constant
    """
    SDG = -SE0 * F
    PDG = -PE0 * F
    DG = (PDG) - (SDG)
    return np.exp(DG / (R * T))

def Keq_nernst_S2_P2_PpHstroma1(SE0: float, PE0: float, pH_stroma: float, R: float, T: float, F: float) -> float:
    """Calculation of equilibrium constant of reaction: 2S -> 2P + 1pH_stroma.

    Args:
        SE0 (float): Standard electrode potential of Substrate
        PE0 (float): Standard electrode potential of Product
        pH_stroma (float): pH Value of stroma
        R (float): Universal gas constant
        T (float): Temperature in Kelvin
        F (float): Farraday Constant

    Returns:
        float: Equilibrium constant
    """
    SDG = -SE0 * F
    PDG = -PE0 * F
    DG = (2 * PDG + pH_stroma * np.log(10) * R * T) - (2 * SDG)
    return np.exp(DG / (R * T))

def Keq_nernst_S2_P2_PpHstroma2(SE0: float, PE0: float, pH_stroma: float, R: float, T: float, F: float) -> float:
    """Calculation of equilibrium constant of reaction: 2S -> 2P + 2pH_stroma.

    Args:
        SE0 (float): Standard electrode potential of Substrate
        PE0 (float): Standard electrode potential of Product
        pH_stroma (float): pH Value of stroma
        R (float): Universal gas constant
        T (float): Temperature in Kelvin
        F (float): Farraday Constant

    Returns:
        float: Equilibrium constant
    """
    SDG = -SE0 * F
    PDG = -PE0 * F
    DG = (2 * PDG + 2 * pH_stroma * np.log(10) * R * T) - (2 * SDG)
    return np.exp(DG / (R * T))

def Keq_nernst_S1_SpHlumen2_P2_PpHstroma2(SE0: float, PE0: float, pH_stroma: float, pH_lu: float, R: float, T: float, F: float) -> float:
    """Calculation of equilibrium constant of reaction: 2S -> 2P + 2pH_stroma.

    Args:
        SE0 (float): Standard electrode potential of Substrate
        PE0 (float): Standard electrode potential of Product
        pH_stroma (float): pH Value of stroma
        R (float): Universal gas constant
        T (float): Temperature in Kelvin
        F (float): Farraday Constant

    Returns:
        float: Equilibrium constant
    """
    SDG = -SE0 * F
    PDG = -PE0 * F
    DG = (2 * PDG + 2 * (pH_stroma - pH_lu) * np.log(10) * R * T) - (2 * SDG + 2 * np.log(10) * R * T * pH_lu)
    return np.exp(DG / (R * T))

def psIIcross(LHC: float, sigma0_I: float, sigma0_II: float) -> float:
    """Calculates the crosssection of PSII

    Args:
        LHC (float): Non-phosphorylated fraction of light harvesting complexes
        sigma0_I (float): Relative cross section of PSI-LHCl supercomplex
        sigma0_II (float): Relative cross section of PSII

    Returns:
        float: Cross section of PSII
    """
    return sigma0_II + (1 - sigma0_II - sigma0_I) * LHC

def Quencher(psbS: float, Vx: float, PsbSP: float, Zx: float, gamma_0: float, gamma_1: float, gamma_2: float, gamma_3: float, K_ZSat: float) -> float:
    """Calculates co-operative 4-state quenching mechanism

    Args:
        psbS (float): Concentration of psbS protein
        Vx (float): Violaxanthin
        PsbSP (float): Concentration of protonated psbS protein
        Zx (float): Zeaxanthin concentration
        gamma_0 (float): Fitted quencher factor corresponding to base quenching not associated with protonation or zeaxanthin
        gamma_1 (float): Fitted quencher factor corresponding to fast quenching due to protonation
        gamma_2 (float): Fitted quencher factor corresponding to fastest possible quenching
        gamma_3 (float): Fitted quencher factor corresponding to slow quenching of Zx present despite lack of protonation
        K_ZSat (float): Half-saturation constant (relative conc. of Zx) for quenching

    Returns:
        float: Quencher
    """
    ZAnt = Zx / (Zx + K_ZSat)
    return gamma_0 * Vx * psbS + gamma_1 * Vx * PsbSP + gamma_2 * ZAnt * PsbSP + gamma_3 * ZAnt * psbS

def psIIstates(PQ: float, PQH_2: float, Q: float, psIIcross: float, k_H: float, kH0: float, pfd: float, k_PQred: float, K_QAPQ: float, k_F: float, k2: float, PSII_tot: float) -> npt.NDArray:
    L = psIIcross * pfd
    kH = kH0 + k_H * Q
    k3p = k_PQred * PQ
    k3m = k_PQred * PQH_2 / K_QAPQ

    Bs = []

    if isinstance(kH, float) and isinstance(PQ, np.ndarray):
        kH = np.repeat(kH, len(PQ))

    # if isinstance(L, float):
    #     L = tuple([L])

    # if isinstance(kH, float):
    #     kH = tuple([kH])

    # if isinstance(k3p, float):
    #     k3p = tuple([k3p])

    # if isinstance(k3m, float):
    #     k3m = tuple([k3m])

    #for L, kH, k3p, k3m in zip(L, kH, k3p, k3m):
    M = np.array(
        [
            [-L - k3m, kH + k_F, k3p, 0],
            [L, -(kH + k_F + k2), 0, 0],
            [0, 0, L, -(kH + k_F)],
            [1, 1, 1, 1],
        ]
    )
    A = np.array([0, 0, 0, PSII_tot])
    B0, B1, B2, B3 = np.linalg.solve(M, A)
    # Bs.append([B0, B1, B2, B3])
    # print(Bs)
    return B0, B1, B2, B3

def B0_psIIstates(PQ: float, PQH_2: float, Q: float, psIIcross: float, k_H: float, kH0: float, pfd: float, k_PQred: float, K_QAPQ: float, k_F: float, k2: float, PSII_tot: float) -> float:
    B0, B1, B2, B3 = psIIstates(PQ, PQH_2, Q, psIIcross, k_H, kH0, pfd, k_PQred, K_QAPQ, k_F, k2, PSII_tot)
    return B0

def B1_psIIstates(PQ: float, PQH_2: float, Q: float, psIIcross: float, k_H: float, kH0: float, pfd: float, k_PQred: float, K_QAPQ: float, k_F: float, k2: float, PSII_tot: float) -> float:
    B0, B1, B2, B3 = psIIstates(PQ, PQH_2, Q, psIIcross, k_H, kH0, pfd, k_PQred, K_QAPQ, k_F, k2, PSII_tot)
    return B1

def B2_psIIstates(PQ: float, PQH_2: float, Q: float, psIIcross: float, k_H: float, kH0: float, pfd: float, k_PQred: float, K_QAPQ: float, k_F: float, k2: float, PSII_tot: float) -> float:
    B0, B1, B2, B3 = psIIstates(PQ, PQH_2, Q, psIIcross, k_H, kH0, pfd, k_PQred, K_QAPQ, k_F, k2, PSII_tot)
    return B2

def B3_psIIstates(PQ: float, PQH_2: float, Q: float, psIIcross: float, k_H: float, kH0: float, pfd: float, k_PQred: float, K_QAPQ: float, k_F: float, k2: float, PSII_tot: float) -> float:
    B0, B1, B2, B3 = psIIstates(PQ, PQH_2, Q, psIIcross, k_H, kH0, pfd, k_PQred, K_QAPQ, k_F, k2, PSII_tot)
    return B3

def psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext):
    """
    QSSA calculates open state of PSI
    depends on reduction states of plastocyanin and ferredoxin
    C = [PC_ox], F = [Fd_ox] (ox. forms)
    """
    kLI = (1 - psIIcross) * pfd

    y0 = (
        K_PCP700
        * K_FAFd
        * PC_red
        * PSI_tot
        * k_PCox
        * (Fd_ox * k_Fd_red + O2_ext * k_Mehler)
        / (
            Fd_ox * K_PCP700 * K_FAFd * PC_red * k_Fd_red * k_PCox
            + Fd_ox * K_FAFd * k_Fd_red * (K_PCP700 * kLI + PC_ox * k_PCox)
            + Fd_red * k_Fd_red * (K_PCP700 * kLI + PC_ox * k_PCox)
            + K_PCP700 * K_FAFd * O2_ext * PC_red * k_Mehler * k_PCox
            + K_PCP700 * K_FAFd * PC_red * kLI * k_PCox
            + K_FAFd * O2_ext * k_Mehler * (K_PCP700 * kLI + PC_ox * k_PCox)
        )
    )

    y1 = (
        PSI_tot
        * (Fd_red * k_Fd_red * (K_PCP700 * kLI + PC_ox * k_PCox) + K_PCP700 * K_FAFd * PC_red * kLI * k_PCox)
        / (
            Fd_ox * K_PCP700 * K_FAFd * PC_red * k_Fd_red * k_PCox
            + Fd_ox * K_FAFd * k_Fd_red * (K_PCP700 * kLI + PC_ox * k_PCox)
            + Fd_red * k_Fd_red * (K_PCP700 * kLI + PC_ox * k_PCox)
            + K_PCP700 * K_FAFd * O2_ext * PC_red * k_Mehler * k_PCox
            + K_PCP700 * K_FAFd * PC_red * kLI * k_PCox
            + K_FAFd * O2_ext * k_Mehler * (K_PCP700 * kLI + PC_ox * k_PCox)
        )
    )
    y2 = PSI_tot - y0 - y1

    return y0, y1, y2

def Y0_psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext):
    y0, y1, y2 = psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext)
    return y0

def Y1_psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext):
    y0, y1, y2 = psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext)
    return y1

def Y2_psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext):
    y0, y1, y2 = psIstates(PC_ox, PC_red, Fd_ox, Fd_red, psIIcross, PSI_tot, k_Fd_red, K_FAFd, K_PCP700, k_PCox, pfd, k_Mehler, O2_ext)
    return y2

def Flou(Q, B0, B2, psIIcross, k2, k_F, k_H):
    return (psIIcross * k_F * B0) / (k_F + k2 + k_H * Q) + (psIIcross * k_F * B2) / (k_F + k_H * Q)

def pH_lu(H_lu):
    return -np.log(H_lu * (2.5e-4)) / np.log(10)

def Pi_st(PGA, BPGA, GAP, DHAP, FBP, F6P, G6P, G1P, SBP, S7P, E4P, X5P, R5P, RUBP, RU5P, ATP_st, P_tot):
    return P_tot - (
        PGA
        + 2 * BPGA
        + GAP
        + DHAP
        + 2 * FBP
        + F6P
        + G6P
        + G1P
        + 2 * SBP
        + S7P
        + E4P
        + X5P
        + R5P
        + 2 * RUBP
        + RU5P
        + ATP_st
    )

def IF_3Pfunc(Pi_st, PGA, GAP, DHAP, K_diss_Pext, Pext, K_diss_Pi, K_diss_PGA, K_diss_GAP, K_diss_DHAP):
    """Used several times to calculate the rate of vPGA, vGAP and vDHAP"""
    return 1 + (1 + (K_diss_Pext / Pext)) * ((Pi_st / K_diss_Pi) + (PGA / K_diss_PGA) + (GAP / K_diss_GAP) + (DHAP / K_diss_DHAP))

def K_ATPsynth(Pi_st, pH_stroma, pH_lu, DeltaG0_ATP, HPR, R, T):
    DG = DeltaG0_ATP - (np.log(10) * R * T) * HPR * (pH_stroma - pH_lu)
    return Pi_st * np.exp(-DG / (R * T))

def GSH(Glutathion_total, GSSG):
    return Glutathion_total - 2 * GSSG

def LHCp(LHC):
    return 1 - LHC

def include_derived_quantities(
    m: Model
):
    # ------------------------------------
    # Matuszynska Module
    # ------------------------------------

    m.add_derived(
        name='H_st',
        fn=H_st,
        args=['pH_stroma']
    )

    m.add_derived(
        name='K_QAPQ',
        fn=Keq_nernst_S2_P2_PpHstroma2,
        args=['E0_QA', 'E0_PQ', 'pH_stroma', 'R', 'T', 'F']
    )

    m.add_derived(
        name='K_FAFd',
        fn=Keq_nernst_S1_P1,
        args=['E0_FA', 'E0_Fd', 'R', 'T', 'F']
    )

    m.add_derived(
        name='K_PCP700',
        fn=Keq_nernst_S1_P1,
        args=['E0_PC', 'E0_P700', 'R', 'T', 'F']
    )

    m.add_derived(
        name='K_FNR',
        fn=Keq_nernst_S2_P2_PpHstroma1,
        args=['E0_PC', 'E0_P700', 'pH_stroma', 'R', 'T', 'F']
    )

    m.add_derived(
        name='PQH_2',
        fn=continous_subtraction,
        args=['PQ_tot', 'PQ']
    )

    m.add_derived(
        name='PC_red',
        fn=continous_subtraction,
        args=['PC_tot', 'PC_ox']
    )

    m.add_derived(
        name='Fd_red',
        fn=continous_subtraction,
        args=['Fd_tot', 'Fd_ox']
    )

    m.add_derived(
        name='ADP_st',
        fn=continous_subtraction,
        args=['AP_tot', 'ATP_st']
    )

    m.add_derived(
        name='NADP_st',
        fn=continous_subtraction,
        args=['NADP_tot', 'NADPH_st']
    )

    m.add_derived(
        name='LHCp',
        fn=LHCp,
        args=['LHC']
    )

    m.add_derived(
        name='Zx',
        fn=continous_subtraction,
        args=['X_tot', 'Vx']
    )

    m.add_derived(
        name='PsbSP',
        fn=continous_subtraction,
        args=['PsbS_tot', 'psbS']
    )

    m.add_derived(
        name='psIIcross',
        fn=psIIcross,
        args=['LHC', 'sigma0_I', 'sigma0_II']
    )

    m.add_derived(
        name='Q',
        fn=Quencher,
        args=['psbS', 'Vx', 'PsbSP', 'Zx', 'gamma_0', 'gamma_1', 'gamma_2', 'gamma_3', 'K_ZSat']
    )

    m.add_derived(
        name='B0',
        fn=B0_psIIstates,
        args=['PQ', 'PQH_2', 'Q', 'psIIcross', 'k_H', 'kH0', 'pfd', 'k_PQred', 'K_QAPQ', 'k_F', 'k2', 'PSII_tot']
    )

    m.add_derived(
        name='B1',
        fn=B1_psIIstates,
        args=['PQ', 'PQH_2', 'Q', 'psIIcross', 'k_H', 'kH0', 'pfd', 'k_PQred', 'K_QAPQ', 'k_F', 'k2', 'PSII_tot']
    )

    m.add_derived(
        name='B2',
        fn=B2_psIIstates,
        args=['PQ', 'PQH_2', 'Q', 'psIIcross', 'k_H', 'kH0', 'pfd', 'k_PQred', 'K_QAPQ', 'k_F', 'k2', 'PSII_tot']
    )

    m.add_derived(
        name='B3',
        fn=B3_psIIstates,
        args=['PQ', 'PQH_2', 'Q', 'psIIcross', 'k_H', 'kH0', 'pfd', 'k_PQred', 'K_QAPQ', 'k_F', 'k2', 'PSII_tot']
    )

    m.add_derived(
        name='Flou',
        fn=Flou,
        args=['Q', 'B0', 'B2', 'psIIcross', 'k2', 'k_F', 'k_H']
    )

    m.add_derived(
        name='pH_lu',
        fn=pH_lu,
        args=['H_lu']
    )

    m.add_derived(
        name='Pi_st',
        fn=Pi_st,
        args=['PGA', 'BPGA', 'GAP', 'DHAP', 'FBP', 'F6P', 'G6P', 'G1P', 'SBP', 'S7P', 'E4P', 'X5P', 'R5P', 'RUBP', 'RU5P', 'ATP_st', 'P_tot']
    )

    m.add_derived(
        name='IF_3P',
        fn=IF_3Pfunc,
        args=['Pi_st', 'PGA', 'GAP', 'DHAP', 'K_diss_Pext', 'Pext', 'K_diss_Pi', 'K_diss_PGA', 'K_diss_GAP', 'K_diss_DHAP']
    )

    m.add_derived(
        name='K_ATPsynth',
        fn=K_ATPsynth,
        args=['Pi_st', 'pH_stroma', 'pH_lu', 'DeltaG0_ATP', 'HPR', 'R', 'T']
    )

    m.add_derived(
        name='K_cytb6f',
        fn=Keq_nernst_S1_SpHlumen2_P2_PpHstroma2,
        args=['E0_PQ', 'E0_PC', 'pH_stroma', 'pH_lu', 'R', 'T', 'F']
    )

    # --------------------------------------
    # Thioredoxin Module
    # --------------------------------------

    m.add_derived(
        name='TRX_red',
        fn=continous_subtraction,
        args=['thioredoxin_tot', 'TRX_ox']
    )

    m.add_derived(
        name='E_CBB_active',
        fn=continous_subtraction,
        args=['e_cbb_tot', 'E_CBB_inactive']
    )

    for name in ['rubisco', 'fbpase', 'sbpase', 'prkase', 'starch']:
        m.add_derived(
            name=f'Vmax_{name}',
            fn=proportional,
            args=['E_CBB_active', f'V_maxbase_{name}']
        )

    # ----------------------------------
    # Mehler Module
    # ----------------------------------

    m.add_derived(
        name='ASC',
        fn=continous_subtraction,
        args=['Ascorbate_total', 'MDA', 'DHA']
    )

    m.add_derived(
        name='GSH',
        fn=GSH,
        args=['Glutathion_total', 'GSSG']
    )

    m.add_derived(
        name='Y0',
        fn=Y0_psIstates,
        args=['PC_ox', 'PC_red', 'Fd_ox', 'Fd_red', 'psIIcross', 'PSI_tot', 'k_Fdred', 'K_FAFd', 'K_PCP700', 'k_PCox', 'pfd', 'k_Mehler', 'O2_ext']
    )

    m.add_derived(
        name='Y1',
        fn=Y1_psIstates,
        args=['PC_ox', 'PC_red', 'Fd_ox', 'Fd_red', 'psIIcross', 'PSI_tot', 'k_Fdred', 'K_FAFd', 'K_PCP700', 'k_PCox', 'pfd', 'k_Mehler', 'O2_ext']
    )

    m.add_derived(
        name='Y2',
        fn=Y2_psIstates,
        args=['PC_ox', 'PC_red', 'Fd_ox', 'Fd_red', 'psIIcross', 'PSI_tot', 'k_Fdred', 'K_FAFd', 'K_PCP700', 'k_PCox', 'pfd', 'k_Mehler', 'O2_ext']
    )

    # ------------------------------------
    # Consumption Module
    # ------------------------------------

    return m
