from __future__ import annotations

import numpy as np


def calculate_pHinv(x: float) -> float:
    return 4e3 * 10 ** (-x)


def proportional(x: float, y: float) -> float:
    return x * y


def dG_pH(r: float, t: float) -> float:
    return np.log(10) * r * t  # type: ignore


def Hstroma(pHstroma: float) -> float:
    return 3.2e4 * 10 ** (-pHstroma)


def kProtonation(Hstroma: float) -> float:
    return 4e-3 / Hstroma


def light(pfd: float) -> float:
    """
    :return: light intensity at certain point of time.
    Typical PAM light function
    """
    return pfd


def keq_PQred(
    E0_QA: float,
    F: float,
    E0_PQ: float,
    pHstroma: float,
    dG_pH: float,
    RT: float,
) -> float:
    DG1 = -E0_QA * F
    DG2 = -2 * E0_PQ * F
    DG = -2 * DG1 + DG2 + 2 * pHstroma * dG_pH
    K = np.exp(-DG / RT)
    return K  # type: ignore


def Keq_cyc(
    E0_Fd: float,
    F: float,
    E0_PQ: float,
    pHstroma: float,
    dG_pH: float,
    RT: float,
) -> float:
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_PQ * F
    DG = -2 * DG1 + DG2 + 2 * dG_pH * pHstroma
    K = np.exp(-DG / RT)
    return K  # type: ignore


def Keq_FAFd(
    E0_FA: float,
    F: float,
    E0_Fd: float,
    RT: float,
) -> float:
    DG1 = -E0_FA * F
    DG2 = -E0_Fd * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K  # type: ignore


def Keq_PCP700(
    E0_PC: float,
    F: float,
    E0_P700: float,
    RT: float,
) -> float:
    DG1 = -E0_PC * F
    DG2 = -E0_P700 * F
    DG = -DG1 + DG2
    K = np.exp(-DG / RT)
    return K  # type: ignore


def Keq_FNR(
    E0_Fd: float,
    F: float,
    E0_NADP: float,
    pHstroma: float,
    dG_pH: float,
    RT: float,
) -> float:
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_NADP * F
    DG = -2 * DG1 + DG2 + dG_pH * pHstroma
    K = np.exp(-DG / RT)
    return K  # type: ignore


def Keq_ATP(
    pH: float,
    DeltaG0_ATP: float,
    dG_pH: float,
    HPR: float,
    pHstroma: float,
    Pi_mol: float,
    RT: float,
) -> float:
    DG = DeltaG0_ATP - dG_pH * HPR * (pHstroma - pH)
    Keq = Pi_mol * np.exp(-DG / RT)
    return Keq  # type: ignore


def Keq_cytb6f(
    pH: float,
    F: float,
    E0_PQ: float,
    E0_PC: float,
    pHstroma: float,
    RT: float,
    dG_pH: float,
) -> float:
    DG1 = -2 * F * E0_PQ
    DG2 = -F * E0_PC
    DG = -(DG1 + 2 * dG_pH * pH) + 2 * DG2 + 2 * dG_pH * (pHstroma - pH)
    Keq = np.exp(-DG / RT)
    return Keq  # type: ignore


def pqmoiety(PQ: float, pqtot: float) -> float:
    return pqtot - PQ


def pcmoiety(PC: float, pctot: float) -> float:
    return pctot - PC


def fdmoiety(Fd: float, fdtot: float) -> float:
    return fdtot - Fd


def adpmoiety(ATP: float, atptot: float) -> float:
    return atptot - ATP


def nadpmoiety(NADPH: float, nadptot: float) -> float:
    return nadptot - NADPH


def lhcmoiety(LHC: float) -> float:
    return 1 - LHC


def ps2crosssection(
    LHC: float,
    staticAntII: float,
    staticAntI: float,
) -> float:
    """calculates the cross section of PSII"""
    cs = staticAntII + (1 - staticAntII - staticAntI) * LHC
    return cs


def ps2states(
    PQ: float,
    PQred: float,
    ps2cs: float,
    PSIItot: float,
    k2: float,
    kF: float,
    _kH: float,
    kH0: float,
    Keq_PQred: float,
    kPQred: float,
    pfd: float,
) -> tuple[float, float, float, float]:
    L = ps2cs * light(pfd)
    kH = kH0
    k3p = kPQred * PQ
    k3m = kPQred * PQred / Keq_PQred

    Bs = []

    if isinstance(kH, float) and isinstance(PQ, np.ndarray):
        kH = np.repeat(kH, len(PQ))

    for L, kH, k3p, k3m in zip(L, kH, k3p, k3m):  # type: ignore
        M = np.array(
            [
                [-L - k3m, kH + kF, k3p, 0],
                [L, -(kH + kF + k2), 0, 0],
                [0, 0, L, -(kH + kF)],
                [1, 1, 1, 1],
            ]
        )
        A = np.array([0, 0, 0, PSIItot])
        B0, B1, B2, B3 = np.linalg.solve(M, A)
        Bs.append([B0, B1, B2, B3])
    return np.array(Bs).T  # type: ignore


def ps1states(
    PC: float,
    PCred: float,
    Fd: float,
    Fdred: float,
    LHC: float,
    ps2cs: float,
    PSItot: float,
    kFdred: float,
    Keq_FAFd: float,
    Keq_PCP700: float,
    kPCox: float,
    pfd: float,
) -> float:
    """
    QSSA calculates open state of PSI
    depends on reduction states of plastocyanin and ferredoxin
    C = [PC], F = [Fd] (ox. forms)
    accepts: light, y as an array of arrays
    returns: array of PSI open
    """
    L = (1 - ps2cs) * light(pfd)

    A1 = PSItot / (
        1
        + L / (kFdred * Fd)
        + (1 + Fdred / (Keq_FAFd * Fd))
        * (PC / (Keq_PCP700 * PCred) + L / (kPCox * PCred))
    )
    return A1


def fluorescence(
    B0: float,
    B2: float,
    ps2cs: float,
    k2: float,
    kF: float,
    kH: float,
    kH0: float,
) -> float:
    fluo = (ps2cs * kF * B0) / (kF + kH0 + k2 + kH) + (ps2cs * kF * B2) / (kF + kH0 + kH)
    return fluo


def calculate_pH(x: float) -> float:
    return -np.log(x * (2.5e-4)) / np.log(10)  # type: ignore


def vPS2(
    B1: float,
    k2: float,
) -> float:
    """reaction rate constant for photochemistry"""
    v = 0.5 * k2 * B1
    return v


def vPS1(
    A: float,
    ps2cs: float,
    pfd: float,
) -> float:
    """reaction rate constant for open PSI"""
    L = (1 - ps2cs) * light(pfd)
    v = L * A
    return v


###############################################################################
# Other reaction rates
###############################################################################
def _oxygen(
    time: float,
    ox: float,
    O2ext: float,
    kNDH: float,
    Ton: float,
    Toff: float,
) -> tuple[float, float]:
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if ox:
        """by default we assume constant oxygen supply"""
        return O2ext, kNDH
    else:
        if time < Ton or time > Toff:
            return O2ext, 0
        else:
            return 0, kNDH


##############################################################################
def oxygen(
    time: float,
    ox: float,
    O2ext: float,
    kNDH: float,
    Ton: float,
    Toff: float,
) -> list[float]:
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if isinstance(time, (int, float)):
        return np.array(_oxygen(time, ox, O2ext, kNDH, Ton, Toff))  # type: ignore
    else:
        return np.array([_oxygen(t, ox, O2ext, kNDH, Ton, Toff) for t in time]).T  # type: ignore


def vPTOX(
    Pred: float,
    time: float,
    kPTOX: float,
    ox: float,
    O2ext: float,
    kNDH: float,
    Ton: float,
    Toff: float,
) -> float:
    """calculates reaction rate of PTOX"""
    v = Pred * kPTOX * oxygen(time, ox, O2ext, kNDH, Ton, Toff)[0]
    return v  # type: ignore


def vNDH(
    Pox: float,
    time: float,
    ox: float,
    O2ext: float,
    kNDH: float,
    Ton: float,
    Toff: float,
) -> float:
    """
    calculates reaction rate of PQ reduction under absence of oxygen
    can be mediated by NADH reductase NDH
    """
    v = oxygen(time, ox, O2ext, kNDH, Ton, Toff)[1] * Pox
    return v


def vB6f(
    PC: float,
    Pox: float,
    H: float,
    Pred: float,
    PCred: float,
    pH: float,
    kCytb6f: float,
    F: float,
    E0_PQ: float,
    E0_PC: float,
    pHstroma: float,
    RT: float,
    dG_pH: float,
) -> float:
    """calculates reaction rate of cytb6f"""
    Keq = Keq_cytb6f(pH, F, E0_PQ, E0_PC, pHstroma, RT, dG_pH)
    v = np.maximum(kCytb6f * (Pred * PC**2 - (Pox * PCred**2) / Keq), -kCytb6f)
    return v  # type: ignore


def vCyc(
    Pox: float,
    Fdred: float,
    kcyc: float,
) -> float:
    """
    calculates reaction rate of cyclic electron flow
    considered as practically irreversible
    """
    v = kcyc * ((Fdred**2) * Pox)
    return v


def vFNR(
    Fd: float,
    Fdred: float,
    NADPH: float,
    NADP: float,
    KM_FNR_F: float,
    KM_FNR_N: float,
    EFNR: float,
    kcatFNR: float,
    Keq_FNR: float,
) -> float:
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
    nadph = (NADPH) / KM_FNR_N  # NADPH requires conversion to mmol/mol of chlorophyll
    nadp = (NADP) / KM_FNR_N  # NADP requires conversion to mmol/mol of chlorophyll
    v = (
        EFNR
        * kcatFNR
        * ((fdred**2) * nadp - ((fdox**2) * nadph) / Keq_FNR)
        / (
            (1 + fdred + fdred**2) * (1 + nadp)
            + (1 + fdox + fdox**2) * (1 + nadph)
            - 1
        )
    )
    return v


def vLeak(
    H: float,
    kLeak: float,
    pHstroma: float,
) -> float:
    """
    rate of leak of protons through the membrane
    """
    v = kLeak * (H - calculate_pHinv(pHstroma))
    return v


def vSt12(
    Ant: float,
    Pox: float,
    kStt7: float,
    PQtot: float,
    KM_ST: float,
    n_ST: float,
) -> float:
    """
    reaction rate of state transitions from PSII to PSI
    Ant depending on module used corresponds to non-phosphorylated antennae
    or antennae associated with PSII
    """
    kKin: float = kStt7 * (1.0 / (1.0 + ((Pox / PQtot) / KM_ST) ** n_ST))
    return kKin * Ant


def vSt21(
    LHCp: float,
    kPph1: float,
) -> float:
    """
    reaction rate of state transitions from PSI to PSII
    """
    return kPph1 * LHCp


def vATPsynthase(
    ATP: float,
    ADP: float,
    pH: float,
    kATPsynth: float,
    DeltaG0_ATP: float,
    dG_pH: float,
    HPR: float,
    pHstroma: float,
    Pi_mol: float,
    RT: float,
) -> float:
    """
    Reaction rate of ATP production
    Kinetic: simple mass action with PH dependant equilibrium
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [ATP], [ADP] in mM
    """
    v = kATPsynth * (
        ADP - ATP / Keq_ATP(pH, DeltaG0_ATP, dG_pH, HPR, pHstroma, Pi_mol, RT)
    )  # * E
    return v


def vATPconsumption(
    A: float,
    kATPcons: float,
) -> float:
    return kATPcons * A


def vNADPHconsumption(
    N: float,
    kNADPHcons: float,
) -> float:
    return kNADPHcons * N
