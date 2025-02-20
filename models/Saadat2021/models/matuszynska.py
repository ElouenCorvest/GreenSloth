import numpy as np
from modelbase.ode import Model

from .rate_laws import (
    moiety_1,
    proportional,
    rapid_eq_1_1,
    rapid_eq_2_1,
    rapid_eq_2_2,
    rapid_eq_3_3,
    vPS1,
    michaelis_menten,
)


def keq_PQred(E0_QA, F, E0_PQ, pH_stroma, dG_pH, RT):
    DG1 = -E0_QA * F
    DG2 = -2 * E0_PQ * F
    DG = -2 * DG1 + DG2 + 2 * pH_stroma * dG_pH
    K = np.exp(-DG / RT)
    return K


def Keq_cyc(E0_Fd, F, E0_PQ, pH_stroma, dG_pH, RT):
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_PQ * F
    DG = -2 * DG1 + DG2 + 2 * dG_pH * pH_stroma
    K = np.exp(-DG / RT)
    return K


def Keq_FAFd(E0_FA, F, E0_Fd, RT):
    DG1 = -E0_FA * F
    DG2 = -E0_Fd * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K


def Keq_PCP700(E0_PC, F, E0_P700, RT):
    DG1 = -E0_PC * F
    DG2 = -E0_P700 * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K


def Keq_FNR(E0_Fd, F, E0_NADP, pH_stroma, dG_pH, RT):
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_NADP * F
    DG = -2 * DG1 + DG2 + dG_pH * pH_stroma
    K = np.exp(-DG / RT)
    return K


def Keq_ATP(pH, DeltaG0_ATP, dG_pH, HPR, pH_stroma, Pi_mol, RT):
    DG = DeltaG0_ATP - dG_pH * HPR * (pH_stroma - pH)
    Keq = Pi_mol * np.exp(-DG / RT)
    return Keq


def Keq_cytb6f(pH, F, E0_PQ, E0_PC, pH_stroma, RT, dG_pH):
    DG1 = -2 * F * E0_PQ
    DG2 = -F * E0_PC
    DG = -(DG1 + 2 * dG_pH * pH) + 2 * DG2 + 2 * dG_pH * (pH_stroma - pH)
    Keq = np.exp(-DG / RT)
    return Keq


def calculate_pHstroma(x):
    return -np.log(x * (3.2e-5)) / np.log(10)


def calculate_pHinv(x):
    return 4e3 * 10 ** (-x)


def lhcmoiety(LHC):
    return 1 - LHC


def ps2crosssection(LHC, sigma0_II, sigma0_I):
    """calculates the cross section of PSII"""
    return sigma0_II + (1 - sigma0_II - sigma0_I) * LHC


def quencher(Psbs, Vx, Psbsp, Zx, y0, y1, y2, y3, K_ZSat):
    """co-operative 4-state quenching mechanism"""
    # gamma_0: slow quenching of (Vx - protonation)
    # gamma_1: fast quenching (Vx + protonation)
    # gamma_2: fastest possible quenching (Zx + protonation)
    # gamma_3: slow quenching of Zx present (Zx - protonation)
    ZAnt = Zx / (Zx + K_ZSat)
    return y0 * Vx * Psbs + y1 * Vx * Psbsp + y2 * ZAnt * Psbsp + y3 * ZAnt * Psbs


def ps2states(PQ, PQred, ps2cs, Q, PSII_tot, k2, k_F, k_H, Keq_PQred, k_PQred, pfd, kH0):
    L = ps2cs * pfd
    kH = kH0 + k_H * Q
    k3p = k_PQred * PQ
    k3m = k_PQred * PQred / Keq_PQred

    Bs = []

    if isinstance(kH, float) and isinstance(PQ, np.ndarray):
        kH = np.repeat(kH, len(PQ))

    for L, kH, k3p, k3m in zip(L, kH, k3p, k3m):
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
        Bs.append([B0, B1, B2, B3])
    return np.array(Bs).T


def fluorescence(Q, B0, B2, ps2cs, k2, k_F, k_H, kH0):
    return (ps2cs * k_F * B0) / (k_F + k2 + k_H * Q) + (ps2cs * k_F * B2) / (k_F + k_H * Q)


def calculate_pH(x):
    return -np.log(x * (2.5e-4)) / np.log(10)


def ps1states(PC, PCred, Fd, Fdred, LHC, ps2cs, PSI_tot, k_Fdred, Keq_FAFd, Keq_PCP700, k_PCox, pfd):
    """
    QSSA calculates open state of PSI
    depends on reduction states of plastocyanin and ferredoxin
    C = [PC], F = [Fd] (ox. forms)
    """
    L = (1 - ps2cs) * pfd

    A1 = PSI_tot / (
        1
        + L / (k_Fdred * Fd)
        + (1 + Fdred / (Keq_FAFd * Fd)) * (PC / (Keq_PCP700 * PCred) + L / (k_PCox * PCred))
    )
    return A1


def Pimoiety(
    PGA,
    BPGA,
    GAP,
    DHAP,
    FBP,
    F6P,
    G6P,
    G1P,
    SBP,
    S7P,
    E4P,
    X5P,
    R5P,
    RUBP,
    RU5P,
    ATP,
    P_tot,
):
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
        + ATP
    )


def Nmoiety(Pi, PGA, GAP, DHAP, K_diss_Pext, Pext, K_diss_Pi, K_diss_PGA, K_diss_GAP, K_diss_DHAP):
    """Used several times to calculate the rate of vPGA, vGAP and vDHAP"""
    return 1 + (1 + (K_diss_Pext / Pext)) * ((Pi / K_diss_Pi) + (PGA / K_diss_PGA) + (GAP / K_diss_GAP) + (DHAP / K_diss_DHAP))


def vPS2(B1, k2):
    """reaction rate constant for photochemistry"""
    return 0.5 * k2 * B1


def _oxygen(time, ox, O2_ext, k_NDH, Ton, Toff):
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if ox:
        """by default we assume constant oxygen supply"""
        return O2_ext, k_NDH
    else:
        if time < Ton or time > Toff:
            return O2_ext, 0
        else:
            return 0, k_NDH


def oxygen(time, ox, O2_ext, k_NDH, Ton, Toff):
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if isinstance(time, (int, float)):
        return np.array(_oxygen(time, ox, O2_ext, k_NDH, Ton, Toff))
    else:
        return np.array([_oxygen(t, ox, O2_ext, k_NDH, Ton, Toff) for t in time]).T


def vPTOX(Pred, time, k_PTOX, ox, O2_ext, k_NDH, Ton, Toff):
    """calculates reaction rate of PTOX"""
    return Pred * k_PTOX * oxygen(time, ox, O2_ext, k_NDH, Ton, Toff)[0]


def vNDH(Pox, time, ox, O2_ext, k_NDH, Ton, Toff):
    """
    calculates reaction rate of PQ reduction under absence of oxygen
    can be mediated by NADH reductase NDH
    """
    return oxygen(time, ox, O2_ext, k_NDH, Ton, Toff)[1] * Pox


def vB6f(PC, Pox, Pred, PCred, Keq_B6f, k_Cytb6f):
    """calculates reaction rate of cytb6f"""
    return np.maximum(k_Cytb6f * (Pred * PC ** 2 - (Pox * PCred ** 2) / Keq_B6f), -k_Cytb6f)


def vCyc(Pox, Fdred, k_cyc):
    """
    calculates reaction rate of cyclic electron flow
    considered as practically irreversible
    """
    return k_cyc * ((Fdred ** 2) * Pox)


def vFNR(Fd, Fdred, NADPH, NADP, KM_FNR_F, KM_FNR_N, EFNR, kcat_FNR, Keq_FNR, convf):
    """
    Reaction rate mediated by the Ferredoxin—NADP(+) reductase (FNR)
    Kinetic: convenience kinetics Liebermeister and Klipp, 2006
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [F], [Fdred] in mmol/mol Chl/s
    [NADPH] in mM
    """
    fdred = Fdred / KM_FNR_F
    fdox = Fd / KM_FNR_F
    nadph = (NADPH / convf) / KM_FNR_N  # NADPH requires conversion to mmol/mol of chlorophyll
    nadp = (NADP / convf) / KM_FNR_N  # NADP requires conversion to mmol/mol of chlorophyll
    return (
        EFNR
        * kcat_FNR
        * ((fdred ** 2) * nadp - ((fdox ** 2) * nadph) / Keq_FNR)
        / ((1 + fdred + fdred ** 2) * (1 + nadp) + (1 + fdox + fdox ** 2) * (1 + nadph) - 1)
    )


def vLeak(H, k_Leak, pH_stroma):
    """
    rate of leak of protons through the membrane
    """
    return k_Leak * (H - calculate_pHinv(pH_stroma))


def vSt12(Ant, Pox, k_Stt7, PQ_tot, KM_ST, n_ST):
    """
    reaction rate of state transitions from PSII to PSI
    Ant depending on module used corresponds to non-phosphorylated antennae
    or antennae associated with PSII
    """
    kKin = k_Stt7 * (1 / (1 + ((Pox / PQ_tot) / KM_ST) ** n_ST))
    return kKin * Ant


def vSt21(LHCp, k_Pph1):
    """
    reaction rate of state transitions from PSI to PSII
    """
    return k_Pph1 * LHCp


def vATPsynthase(ATP, ADP, Keq_ATPsynthase, k_ATPsynth, convf):
    """
    Reaction rate of ATP production
    Kinetic: simple mass action with PH dependant equilibrium
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [ATP], [ADP] in mM
    """
    return k_ATPsynth * (ADP / convf - ATP / convf / Keq_ATPsynthase)


def vDeepox(Vx, H, nH, k_DV, K_pHSat):
    """
    activity of xantophyll cycle: de-epoxidation of violaxanthin, modelled by Hill kinetics
    """
    return k_DV * ((H ** nH) / (H ** nH + calculate_pHinv(K_pHSat) ** nH)) * Vx


def vEpox(Zx, k_EZ):
    """
    activity of xantophyll cycle: epoxidation
    """
    return k_EZ * Zx


def vLhcprotonation(Psbs, H, nH, k_prot, K_pHSatLHC):
    """
    activity of PsbS protein protonation: protonation modelled by Hill kinetics
    """
    return k_prot * ((H ** nH) / (H ** nH + calculate_pHinv(K_pHSatLHC) ** nH)) * Psbs


def vLhcdeprotonation(Psbsp, k_deprot):
    """
    activity of PsbS protein protonation: deprotonation
    """
    return k_deprot * Psbsp


def v1(RUBP, PGA, FBP, SBP, P, NADPH, V1, CO2, Km_RuBisCO_RUBP, Ki_RuBisCO_PGA, Ki_RuBisCO_FBP, Ki_RuBisCO_SBP, Ki_RuBisCO_Pi, Ki_RuBisCO_NADPH, Km_RuBisCO_CO2):
    return (V1 * RUBP * CO2) / (
        (RUBP + Km_RuBisCO_RUBP * (1 + (PGA / Ki_RuBisCO_PGA) + (FBP / Ki_RuBisCO_FBP) + (SBP / Ki_RuBisCO_SBP) + (P / Ki_RuBisCO_Pi) + (NADPH / Ki_RuBisCO_NADPH)))
        * (CO2 + Km_RuBisCO_CO2)
    )


def v6(FBP, F6P, P, V6, Km_FBPase, Ki_FBPase_F6P, Ki_FBPase_Pi):
    return (V6 * FBP) / (FBP + Km_FBPase * (1 + (F6P / Ki_FBPase_F6P) + (P / Ki_FBPase_Pi)))


def v9(SBP, Pi, V9, Km_SBPase, Ki_SBPase_Pi):
    return (V9 * SBP) / (SBP + Km_SBPase * (1 + (Pi / Ki_SBPase_Pi)))


def v13(RU5P, ATP, RUBP, PGA, P, ADP, V13, Km_PRKase_RU5P, Ki_PRKase_PGA, Ki_PRKase_RuBP, Ki_PRKase_Pi, Kiunc_PRKase_ADP, Km_PRKase_ATP, Kicom_PRKase_ADP):
    return (V13 * RU5P * ATP) / (
        (RU5P + Km_PRKase_RU5P * (1 + (PGA / Ki_PRKase_PGA) + (RUBP / Ki_PRKase_RuBP) + (P / Ki_PRKase_Pi)))
        * (ATP * (1 + (ADP / Kiunc_PRKase_ADP)) + Km_PRKase_ATP * (1 + (ADP / Kicom_PRKase_ADP)))
    )


def triose_export(S, N, Vx, k):
    return (Vx * S) / (N * k)


def vStarch(G1P, ATP, ADP, P, PGA, F6P, FBP, Vst, Km_Starch_G1P, Ki_Starch_ADP, Km_Starch_ATP, Kact_Starch_PGA, Kact_Starch_F6P, Kact_Starch_FBP):
    """G1P -> Gn-1 ; Starch production"""
    return (Vst * G1P * ATP) / (
        (G1P + Km_Starch_G1P)
        * ((1 + (ADP / Ki_Starch_ADP)) * (ATP + Km_Starch_ATP) + ((Km_Starch_ATP * P) / (Kact_Starch_PGA * PGA + Kact_Starch_F6P * F6P + Kact_Starch_FBP * FBP)))
    )


variables = [
    # "B",  #photosystem II protein concentration
    "PQ",  # oxidised plastoquinone
    "PC",  # oxidised plastocyan
    "Fd",  # oxidised ferrodoxin
    "ATP",  # stromal concentration of ATP
    "NADPH",  # stromal concentration of NADPH
    "H",  # lumenal protons
    "LHC",  # ,  # non-phosphorylated antenna
    "Psbs",  # PsBs
    "Vx",  # vioolaxathin relative concentration
    "PGA",
    "BPGA",
    "GAP",
    "DHAP",
    "FBP",
    "F6P",
    "G6P",
    "G1P",
    "SBP",
    "S7P",
    "E4P",
    "X5P",
    "R5P",
    "RUBP",
    "RU5P",
]


p = {
    "convf": 3.2 * 10e-3,  # converts ATP and NADPH
    "PSII_tot": 2.5,  # [mmol/molChl] total concentration of PSII
    "PSI_tot": 2.5,
    "PQ_tot": 17.5,  # [mmol/molChl]
    "PC_tot": 4.0,  # Bohme1987 but other sources give different values - seems to depend greatly on organism and conditions
    "Fd_tot": 5.0,  # Bohme1987
    "Ctot": 2.5,  # source unclear (Schoettler says 0.4...?, but plausible to assume that complexes (PSII,PSI,b6f) have approx. same abundance)
    "NADP_tot": 0.8,  # estimate from ~ 0.8 mM, Heineke1991
    "AP_tot": 2.55,  # [mmol/molChl] Bionumbers ~2.55mM (=81mmol/molChl) (FIXME: Soma had 50)
    "PsbS_tot": 1.0,  # relative pool of PsbS
    "X_tot": 1.0,  # relative pool of carotenoids (V+A+Z)
    # Mara "ATPasetot": 1., # relative pool of ATPase
    # parameters associated with photosystem II
    "k_H": 5e9,
    "kH0": 5e8,  # base quenching" after calculation with Giovanni
    "k_F": 6.25e8,  # 6.25e7 fluorescence 16ns
    "k1": 5e9,  # excitation of Pheo / charge separation 200ps
    "k1rev": 1e10,
    "k2": 5e9,  # Mara was 5e10 # original 5e9 (charge separation limiting step ~ 200ps) - made this faster for higher Fs fluorescence
    "kdeg": 100,  # rate of PSII damage corresponds to p.k2 / .5e8
    "krep": 5.55e-4,  # rate of repair fo PSII
    # parameters associated with photosystem I
    "k_Stt7": 0.0035,  # [s-1] fitted to the FM dynamics
    "k_Pph1": 0.0013,  # [s-1] fitted to the FM dynamics
    "KM_ST": 0.2,  # Switch point (half-activity of Stt7) for 20% PQ oxidised (80% reduced)
    "n_ST": 2.0,  # Hill coefficient of 4 -> 1/(2.5^4)~1/40 activity at PQox=PQred
    "sigma0_I": 0.37,  # corresponds to PSI - LHCI supercomplex, when chlorophyll decreases more relative fixed antennae
    "sigma0_II": 0.1,  # corresponds to PSII core
    "prob_attach": 1.0,  # probability of antena attaching to PSI
    # ATP and NADPH parameters
    "kActATPase": 0.05,  # on 14.09 increased from 0.01 to saturate between 1-2 min, not 10
    # paramter relating the rate constant of activation of the ATPase in the light
    "kDeactATPase": 0.002,  # paramter relating the deactivation of the ATPase at night
    "k_ATPsynth": 20.0,  # taken from MATLAB
    "kATPcons": 10.0,  # taken from MATLAB
    "ATPcyt": 0.5,  # only relative levels are relevant (normalised to 1) to set equilibrium
    "Pi_mol": 0.01,
    "DeltaG0_ATP": 30.6,  # 30.6kJ/mol / RT
    "HPR": 14.0 / 3.0,  # Vollmar et al. 2009 (after Zhu et al. 2013)
    "kNADPHcons": 15.0,  # taken from MATLAB
    "NADPHcyt": 0.5,  # only relatice levels
    # global conversion factor of PFD to excitation rate
    # "cPFD": 4. # [m^2/mmol PSII]
    # pH and protons
    "pH_stroma": 7.9,
    "k_Leak": 10.0,  # 0.010, # [1/s] leakage rate -- inconsistency with Kathrine
    "b_H": 100.0,  # proton buffer: ratio total / free protons
    # rate constants
    "k_PQred": 250.0,  # [1/(s*(mmol/molChl))]
    "k_Cytb6f": 2.5,  # a rough estimate: transfer PQ->cytf should be ~10ms
    "k_PTOX": 0.01,  # ~ 5 electrons / seconds. This gives a bit more (~20)
    "k_PCox": 2500.0,  # a rough estimate: half life of PC->P700 should be ~0.2ms
    "k_Fdred": 2.5e5,  # a rough estimate: half life of PC->P700 should be ~2micro-s
    "kcat_FNR": 500.0,  # Carrillo2003 (kcat~500 1/s)
    "k_cyc": 1.0,
    "O2_ext": 8.0,  # corresponds to 250 microM cor to 20%
    "k_NDH": 0.002,  # re-introduce e- into PQ pool. Only positive for anaerobic (reducing) condition
    "kNh": 0.05,
    "kNr": 0.004,
    "nH": 5.0,
    "EFNR": 3.0,  # Bohme1987
    "KM_FNR_F": 1.56,  # corresponds to 0.05 mM (Aliverti1990)
    "KM_FNR_N": 0.22,  # corresponds to 0.007 mM (Shin1971 Aliverti2004)
    # quencher fitted parameters
    "gamma_0": 0.1,  # slow quenching of (Vx - protonation)
    "gamma_1": 0.25,  # fast quenching (Vx + protonation)
    "gamma_2": 0.6,  # fastest possible quenching (Zx + protonation)
    "gamma_3": 0.15,  # slow quenching of Zx present (Zx - protonation)
    # non-photochemical quenching PROTONATION
    "k_deprot": 0.0096,
    "k_prot": 0.0096,
    "K_pHSatLHC": 5.8,
    # non-photochemical quenching XANTOPHYLLS
    "k_DV": 0.0024,
    "k_EZ": 0.00024,  # 6.e-4        # converted to [1/s]
    "K_pHSat": 5.8,  # [-] half-saturation pH value for activity de-epoxidase highest activity at ~pH 5.8
    "nh_x": 5.0,  # [-] hill-coefficient for activity of de-epoxidase
    "nh_PsbS": 3.0,  # [-] hill-coefficient for activity of de-epoxidase
    "K_ZSat": 0.12,  # [-] half-saturation constant (relative conc. of Z) for quenching of Z
    # standard redox potentials (at pH=0) in V
    "E0_QA": -0.140,
    "E0_PQ": 0.354,
    "E0_cytf": 0.350,
    "E0_PC": 0.380,
    "E0_P700": 0.480,
    "E0_FA": -0.550,
    "E0_Fd": -0.430,
    "E0_NADP": -0.113,
    # physical constants
    "F": 96.485,  # Faraday constant
    "R": 8.3e-3,  # universal gas constant
    "T": 298.0,  # Temperature in K - for now assumed to be constant at 25 C
    # light
    "pfd": 100.0,
    "Ton": 0.0,
    "Toff": 1800,
    "dT": 120,
    "ox": True,  # 1. means True, switched on
    # CBB cycle associated parameter set according to Pettersson and Pettersson 1988
    "CN": 0.5,
    "CO2": 0.2,
    "P_tot": 15 + 2.05,  # 15.0
    "Ca": 0.5,
    "pHmedium": 7.6,
    "Pext": 0.5,
    # Vmaxes of Calvin cycle enzymes
    "V_maxbase_rubisco": 0.34 * 8,
    "V_maxbase_fbpase": 0.2 * 8,
    "V_maxbase_sbpase": 0.04 * 8,
    "V_maxbase_prkase": 0.9999 * 8,
    "V_maxbase_starch": 0.04 * 8,
    "Vmax_ex": 0.25 * 8,
    # equilibrium constants of calvin cycle enzymes
    "K_PGK1ase": 3.1 * (10.0 ** (-4.0)),
    "K_BPGAdehynase": 1.6 * (10.0 ** 7.0),
    "K_TPIase": 22.0,
    "K_Aldolase_FBP": (7.1),
    "K_TKase_E4P": 0.084,
    "K_Aldolase_SBP": (13.0),
    "K_TKase_R5P": 0.85,
    "K_Rpiase": 0.4,
    "K_RPEase": 0.67,
    "K_PGIase": 2.3,
    "K_PGMase": 0.058,
    # michaelis constants of calvin cycle enzymes
    "Km_RuBisCO_RUBP": 0.02,
    "Km_RuBisCO_CO2": 0.0107,  # millimol laut witzel
    "Km_FBPase": 0.03,
    "Km_SBPase": 0.013,
    "Km_PRKase_RU5P": 0.05,
    "Km_PRKase_ATP": 0.05,
    "Km161": 0.014,
    "Km162": 0.3,
    "Km_Starch_G1P": 0.08,
    "Km_Starch_ATP": 0.08,
    "Kmnadph": 0.19,  # ausgerechneter wert (ideal wert)
    "K_diss_PGA": 0.25,
    "K_diss_GAP": 0.075,
    "K_diss_DHAP": 0.077,
    "K_diss_Pi": 0.63,
    "K_diss_Pext": 0.74,
    "Ki_RuBisCO_PGA": 0.04,
    "Ki_RuBisCO_FBP": 0.04,
    "Ki_RuBisCO_SBP": 0.075,
    "Ki_RuBisCO_Pi": 0.9,
    "Ki_RuBisCO_NADPH": 0.07,
    "Ki_FBPase_F6P": 0.7,
    "Ki_FBPase_Pi": 12.0,
    "Ki_SBPase_Pi": 12.0,
    "Ki_PRKase_PGA": 2.0,
    "Ki_PRKase_RuBP": 0.7,
    "Ki_PRKase_Pi": 4.0,
    "Kiunc_PRKase_ADP": 2.5,
    "Kicom_PRKase_ADP": 0.4,
    "Ki_Starch_ADP": 10.0,
    "Kact_Starch_PGA": 0.1,
    "Kact_Starch_F6P": 0.02,
    "Kact_Starch_FBP": 0.02,
    "k_fast": 10.0 ** 8.0 * 8,
    # CBB speedup factor
    "Km_fcbb": 150.0,
    "Vmax_fcbb": 6.0,
}


def dg_ph(r, t):
    return np.log(10) * r * t


def h_stroma(ph_stroma):
    return 3.2e4 * 10 ** (-ph_stroma)


def h_stroma2(ph_stroma):
    return 1000.0 * 10.0 ** (-ph_stroma)


def protonation(h_stroma):
    return 4e-3 / h_stroma


def get_matusznyska() -> Model():
    m = Model(parameters=p, compounds=variables)

    m.add_derived_parameter("fCBB", michaelis_menten, ["pfd", "Vmax_fcbb", "Km_fcbb"])
    m.add_derived_parameter("V1", proportional, ["V_maxbase_rubisco", "fCBB"])
    m.add_derived_parameter("V6", proportional, ["V_maxbase_fbpase", "fCBB"])
    m.add_derived_parameter("V9", proportional, ["V_maxbase_sbpase", "fCBB"])
    m.add_derived_parameter("V13", proportional, ["V_maxbase_prkase", "fCBB"])
    m.add_derived_parameter("Vst", proportional, ["V_maxbase_starch", "fCBB"])

    m.add_derived_parameter(
        parameter_name="RT",
        function=proportional,
        parameters=["R", "T"],
    )

    m.add_derived_parameter(
        parameter_name="dG_pH",
        function=dg_ph,
        parameters=["R", "T"],
    )

    m.add_derived_parameter(
        parameter_name="Hstroma",
        function=h_stroma,
        parameters=["pH_stroma"],
    )

    m.add_derived_parameter(
        parameter_name="kProtonation",
        function=protonation,
        parameters=["Hstroma"],
    )

    # FIXME: we used two different definitions for H_stroma (!). This one is Nima's
    m.add_derived_parameter(
        parameter_name="H_stroma",
        function=h_stroma2,
        parameters=["pH_stroma"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_PQred",
        function=keq_PQred,
        parameters=["E0_QA", "F", "E0_PQ", "pH_stroma", "dG_pH", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_cyc",
        function=Keq_cyc,
        parameters=["E0_Fd", "F", "E0_PQ", "pH_stroma", "dG_pH", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_FAFd",
        function=Keq_FAFd,
        parameters=["E0_FA", "F", "E0_Fd", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_PCP700",
        function=Keq_PCP700,
        parameters=["E0_PC", "F", "E0_P700", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_FNR",
        function=Keq_FNR,
        parameters=["E0_Fd", "F", "E0_NADP", "pH_stroma", "dG_pH", "RT"],
    )

    m.add_algebraic_module(
        module_name="pq_alm",
        function=moiety_1,
        compounds=["PQ"],
        derived_compounds=["PQred"],
        parameters=["PQ_tot"],
    )

    m.add_algebraic_module(
        module_name="pc_alm",
        function=moiety_1,
        compounds=["PC"],
        derived_compounds=["PCred"],
        parameters=["PC_tot"],
    )

    m.add_algebraic_module(
        module_name="fd_alm",
        function=moiety_1,
        compounds=["Fd"],
        derived_compounds=["Fdred"],
        parameters=["Fd_tot"],
    )

    m.add_algebraic_module(
        module_name="adp_alm",
        function=moiety_1,
        compounds=["ATP"],
        derived_compounds=["ADP"],
        parameters=["AP_tot"],
    )

    m.add_algebraic_module(
        module_name="nadp_alm",
        function=moiety_1,
        compounds=["NADPH"],
        derived_compounds=["NADP"],
        parameters=["NADP_tot"],
    )

    m.add_algebraic_module(
        module_name="lhc_alm",
        function=lhcmoiety,
        compounds=["LHC"],
        derived_compounds=["LHCp"],
    )

    m.add_algebraic_module(
        module_name="xantophylls_alm",
        function=moiety_1,
        compounds=["Vx"],
        derived_compounds=["Zx"],
        parameters=["X_tot"],
    )

    m.add_algebraic_module(
        module_name="psbs_alm",
        function=moiety_1,
        compounds=["Psbs"],
        derived_compounds=["Psbsp"],
        parameters=["PsbS_tot"],
    )

    m.add_algebraic_module(
        module_name="ps2crosssection",
        function=ps2crosssection,
        compounds=["LHC"],
        derived_compounds=["ps2cs"],
        parameters=["sigma0_II", "sigma0_I"],
    )

    m.add_algebraic_module(
        module_name="quencher",
        function=quencher,
        compounds=["Psbs", "Vx", "Psbsp", "Zx"],
        derived_compounds=["Q"],
        parameters=["gamma_0", "gamma_1", "gamma_2", "gamma_3", "K_ZSat"],
    )

    m.add_algebraic_module(
        module_name="ps2states",
        function=ps2states,
        compounds=["PQ", "PQred", "ps2cs", "Q"],
        derived_compounds=["B0", "B1", "B2", "B3"],
        parameters=["PSII_tot", "k2", "k_F", "k_H", "Keq_PQred", "k_PQred", "pfd", "kH0"],
    )

    m.add_algebraic_module(
        module_name="ps1states",
        function=ps1states,
        compounds=["PC", "PCred", "Fd", "Fdred", "LHC", "ps2cs"],
        derived_compounds=["A1"],
        parameters=["PSI_tot", "k_Fdred", "Keq_FAFd", "Keq_PCP700", "k_PCox", "pfd"],
    )

    m.add_algebraic_module(
        module_name="fluorescence",
        function=fluorescence,
        compounds=["Q", "B0", "B2", "ps2cs"],
        derived_compounds=["Fluo"],
        parameters=["k2", "k_F", "k_H", "kH0"],
    )

    m.add_algebraic_module(
        module_name="calculate_pH",
        function=calculate_pH,
        compounds=["H"],
        derived_compounds=["pH"],
    )

    m.add_algebraic_module(
        module_name="pi_alm",
        function=Pimoiety,
        compounds=[
            "PGA",
            "BPGA",
            "GAP",
            "DHAP",
            "FBP",
            "F6P",
            "G6P",
            "G1P",
            "SBP",
            "S7P",
            "E4P",
            "X5P",
            "R5P",
            "RUBP",
            "RU5P",
            "ATP",
        ],
        derived_compounds=["Pi"],
        parameters=["P_tot"],
    )

    m.add_algebraic_module(
        module_name="n_alm",
        function=Nmoiety,
        compounds=["Pi", "PGA", "GAP", "DHAP"],
        derived_compounds=["N"],
        parameters=["K_diss_Pext", "Pext", "K_diss_Pi", "K_diss_PGA", "K_diss_GAP", "K_diss_DHAP"],
    )

    m.add_algebraic_module(
        module_name="Keq_ATPsynthase",
        function=Keq_ATP,
        compounds=["pH"],
        derived_compounds=["Keq_ATPsynthase"],
        parameters=["DeltaG0_ATP", "dG_pH", "HPR", "pH_stroma", "Pi_mol", "RT"],
    )

    m.add_algebraic_module(
        module_name="Keq_B6f",
        function=Keq_cytb6f,
        compounds=["pH"],
        derived_compounds=["Keq_B6f"],
        parameters=["F", "E0_PQ", "E0_PC", "pH_stroma", "RT", "dG_pH"],
    )

    # Rate of electron flow through the photosystems.
    # Calling algebraic modules calculating excited states of each photosystem

    m.add_reaction(
        rate_name="vPS2",
        function=vPS2,
        stoichiometry={"PQ": -1, "H": 2 / m.get_parameter("b_H")},
        modifiers=["B1"],
        dynamic_variables=["B1"],  # doesn't depend on PQ
        parameters=["k2"],
    )
    m.add_reaction(
        rate_name="vPS1",
        function=vPS1,
        stoichiometry={"Fd": -1, "PC": 1},
        modifiers=["A1", "ps2cs"],
        dynamic_variables=["A1", "ps2cs"],  # doesn't depend on Fd
        parameters=["pfd"],
    )

    m.add_reaction(
        rate_name="vPTOX",
        function=vPTOX,
        stoichiometry={"PQ": 1},
        modifiers=["PQred", "time"],
        parameters=["k_PTOX", "ox", "O2_ext", "k_NDH", "Ton", "Toff"],
    )

    m.add_reaction(
        rate_name="vNDH",
        function=vNDH,
        stoichiometry={"PQ": -1},
        modifiers=["time"],
        parameters=["ox", "O2_ext", "k_NDH", "Ton", "Toff"],
    )

    m.add_reaction(
        rate_name="vB6f",
        function=vB6f,
        stoichiometry={"PC": -2, "PQ": 1, "H": 4 / m.get_parameter("b_H")},
        modifiers=["PQred", "PCred", "Keq_B6f"],
        dynamic_variables=["PC", "PQ", "PQred", "PCred", "Keq_B6f"],
        parameters=["k_Cytb6f"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vCyc",
        function=vCyc,
        stoichiometry={"PQ": -1, "Fd": 2},
        modifiers=["Fdred"],
        parameters=["k_cyc"],
    )

    m.add_reaction(
        rate_name="vFNR",
        function=vFNR,
        stoichiometry={"Fd": 2, "NADPH": 1 * m.get_parameter("convf")},
        modifiers=["Fd", "Fdred", "NADPH", "NADP"],
        dynamic_variables=["Fd", "Fdred", "NADPH", "NADP"],
        parameters=["KM_FNR_F", "KM_FNR_N", "EFNR", "kcat_FNR", "Keq_FNR", "convf"],
    )

    m.add_reaction(
        rate_name="vLeak",
        function=vLeak,
        stoichiometry={"H": -1 / m.get_parameter("b_H")},
        parameters=["k_Leak", "pH_stroma"],
    )

    m.add_reaction(
        rate_name="vSt12",
        function=vSt12,
        stoichiometry={"LHC": -1},
        modifiers=["PQ"],
        parameters=["k_Stt7", "PQ_tot", "KM_ST", "n_ST"],
    )

    m.add_reaction(
        rate_name="vSt21",
        function=vSt21,
        stoichiometry={"LHC": 1},
        modifiers=["LHCp"],
        dynamic_variables=["LHCp"],
        parameters=["k_Pph1"],
    )

    m.add_reaction(
        rate_name="vATPsynthase",
        function=vATPsynthase,
        stoichiometry={
            "H": -m.get_parameter("HPR") / m.get_parameter("b_H"),
            "ATP": 1 * m.get_parameter("convf"),
        },
        modifiers=["ADP", "Keq_ATPsynthase"],
        dynamic_variables=["ATP", "ADP", "Keq_ATPsynthase"],
        parameters=[
            "k_ATPsynth",
            "convf",
        ],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vDeepox",
        function=vDeepox,
        stoichiometry={"Vx": -1},
        modifiers=["H"],
        parameters=["nh_x", "k_DV", "K_pHSat"],
    )

    m.add_reaction(
        rate_name="vEpox",
        function=vEpox,
        stoichiometry={"Vx": 1},
        modifiers=["Zx"],
        parameters=["k_EZ"],
    )

    m.add_reaction(
        rate_name="vLhcprotonation",
        function=vLhcprotonation,
        stoichiometry={"Psbs": -1},
        modifiers=["H"],
        parameters=["nh_PsbS", "k_prot", "K_pHSatLHC"],
    )

    m.add_reaction(
        rate_name="vLhcdeprotonation",
        function=vLhcdeprotonation,
        stoichiometry={"Psbs": 1},
        modifiers=["Psbsp"],
        parameters=["k_deprot"],
    )

    ###############################################################################
    # Calvin-Benson-Bassham Cycle Reaction Rates
    ###############################################################################

    m.add_reaction(
        rate_name="vRuBisCO",
        function=v1,
        stoichiometry={"RUBP": -1, "PGA": 2},
        modifiers=["PGA", "FBP", "SBP", "Pi", "NADPH"],
        dynamic_variables=["RUBP", "PGA", "FBP", "SBP", "Pi", "NADPH"],
        parameters=[
            "V1",
            "CO2",
            "Km_RuBisCO_RUBP",
            "Ki_RuBisCO_PGA",
            "Ki_RuBisCO_FBP",
            "Ki_RuBisCO_SBP",
            "Ki_RuBisCO_Pi",
            "Ki_RuBisCO_NADPH",
            "Km_RuBisCO_CO2",
        ],
    )

    m.add_reaction(
        rate_name="vPGA_kinase",
        function=rapid_eq_2_2,
        stoichiometry={"ATP": -1, "PGA": -1, "BPGA": 1},
        modifiers=["ADP"],
        parameters=["k_fast", "K_PGK1ase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vBPGA_dehydrogenase",
        function=rapid_eq_3_3,
        stoichiometry={"BPGA": -1, "NADPH": -1, "GAP": 1},
        modifiers=["Pi", "NADP"],
        parameters=["k_fast", "H_stroma", "K_BPGAdehynase"],
        args=["BPGA", "NADPH", "H_stroma", "GAP", "NADP", "Pi", "k_fast", "K_BPGAdehynase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vTPI",
        function=rapid_eq_1_1,
        stoichiometry={"GAP": -1, "DHAP": 1},
        parameters=["k_fast", "K_TPIase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vAldolase",
        function=rapid_eq_2_1,
        stoichiometry={"GAP": -1, "DHAP": -1, "FBP": 1},
        parameters=["k_fast", "K_Aldolase_FBP"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vFBPase",
        function=v6,
        stoichiometry={"FBP": -1, "F6P": 1},
        modifiers=["Pi"],
        parameters=["V6", "Km_FBPase", "Ki_FBPase_F6P", "Kiunc_PRKase_ADP"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vF6P_Transketolase",
        function=rapid_eq_2_2,
        stoichiometry={"GAP": -1, "F6P": -1, "X5P": 1, "E4P": 1},
        parameters=["k_fast", "K_TKase_E4P"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v8",
        function=rapid_eq_2_1,
        stoichiometry={"DHAP": -1, "E4P": -1, "SBP": 1},
        parameters=["k_fast", "K_Aldolase_SBP"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v9",
        function=v9,
        stoichiometry={"SBP": -1, "S7P": 1},
        modifiers=["Pi"],
        dynamic_variables=["SBP", "Pi"],
        parameters=["V9", "Km_SBPase", "Ki_SBPase_Pi"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v10",
        function=rapid_eq_2_2,
        stoichiometry={"GAP": -1, "S7P": -1, "X5P": 1, "R5P": 1},
        parameters=["k_fast", "K_TKase_R5P"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v11",
        function=rapid_eq_1_1,
        stoichiometry={"R5P": -1, "RU5P": 1},
        parameters=["k_fast", "K_Rpiase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v12",
        function=rapid_eq_1_1,
        stoichiometry={"X5P": -1, "RU5P": 1},
        parameters=["k_fast", "K_RPEase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="v13",
        function=v13,
        stoichiometry={"RU5P": -1, "ATP": -1, "RUBP": 1},
        modifiers=["PGA", "Pi", "ADP"],
        parameters=[
            "V13",
            "Km_PRKase_RU5P",
            "Ki_PRKase_PGA",
            "Ki_PRKase_RuBP",
            "Ki_PRKase_Pi",
            "Kiunc_PRKase_ADP",
            "Km_PRKase_ATP",
            "Kicom_PRKase_ADP",
        ],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vG6P_isomerase",
        function=rapid_eq_1_1,
        stoichiometry={"F6P": -1, "G6P": 1},
        parameters=["k_fast", "K_PGIase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vPhosphoglucomutase",
        function=rapid_eq_1_1,
        stoichiometry={"G6P": -1, "G1P": 1},
        parameters=["k_fast", "K_PGMase"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vpga",
        function=triose_export,
        stoichiometry={"PGA": -1},
        modifiers=["N"],
        parameters=["Vmax_ex", "K_diss_PGA"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vgap",
        function=triose_export,
        stoichiometry={"GAP": -1},
        modifiers=["N"],
        parameters=["Vmax_ex", "K_diss_GAP"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vdhap",
        function=triose_export,
        stoichiometry={"DHAP": -1},
        modifiers=["N"],
        parameters=["Vmax_ex", "K_diss_DHAP"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vStarch",
        function=vStarch,
        stoichiometry={"G1P": -1, "ATP": -1},
        modifiers=["ADP", "Pi", "PGA", "F6P", "FBP"],
        parameters=["Vst", "Km_Starch_G1P", "Ki_Starch_ADP", "Km_Starch_ATP", "Kact_Starch_PGA", "Kact_Starch_F6P", "Kact_Starch_FBP"],
    )
    return m
