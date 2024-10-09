#!/usr/bin/env python

# >> changed: added full spectrum light description of Fuente2021 (temporarily from local drive) <<
import matplotlib.pyplot as plt
import modelbase
import numpy as np
from modelbase.ode import LabelModel, LinearLabelModel, Model, Simulator, mca
from modelbase.ode import ratefunctions as rf
from modelbase.ode import ratelaws as rl
from sympy import Matrix, Tuple, lambdify, linsolve, symbols

import functions_light_absorption as lip
import parameters

# CHANGE LOG
# 000            | original model by elena
# 001 26.11.2021 | removed vCell reaction, parameter k_Cell
#                | added reaction vO2out; parameters kO2out, O2ext
# 002 29.11.2021 | modified stoichiometries of Keq_vb6f, Keq_PQred,
#                | Keq_vSDH, Keq_vbd, Keq_vaa, Keq_vFlv, Keq_vNDH
#     30.11.2021 | modified stoichiometries of Keq_vFQ, Keq_FNR, Keq_vNQ
#                | corrected standerd electrode potentials E0_O2/H2O, E0_NADP, E0_succinate/fumarate
#                | preliminary corrections for k_krebs and k_SDH to account for miscalculations
# 003 02.12.2021 | recalculated all parameter values
# 005 07.12.2021 | removed protons from reversible kinetics, added protons to irreversible kinetics
#                | increased E0_PQ according to other source
# 006 15.12.2021 | added reaction vCCM and parameters kCCM, CO2ext, fCin
#                | changed vPass dependency from pH to proton concentration
# 007 15.12.2021 | modified proton stoichiometries of vPS2, vb6f, vSDH, vbd,
#                | vNDH, vFQ, vNADPHconsumption
#     16.12.2021 | increased bHo
# 008 16.12.2021 | changed concentration parameters NADP_tot, c_AP_tot
#                | changed kinetic parameters k_NDH, k_SDH, k_O2, k_FQ, k_NQ, k_krebs
# 009 17.12.2021 | changed kinetic parameters k_FN, k_O2
#     21.12.2021 | corrected the stoichiometric protons of cyclicsuccinate
# 010 22.12.2021 | added the algebraic module for PS2 fluorescence estimation from Ebenhöh2014
#     14.01.2022 | changed kinetic parameters k_O2, k_ox1, k_aa, k_krebs
# 011 16.01.2022 | defined the incoming light as different colors (changed parameter pfd) and the photosystems
#                | as differentially excited by them (affects functions light, ps2states, ps1states, vPS1, fluorescence)
#                | added state transitions through the compound PSIIq and the function PSIIquench
#                | added parameters kHst, kQuench, kUnquench, excite_ps2, excite_ps1
#     23.01.2022 | removed exponents from compounds in vb6f, vaa, vFlv, vFQ, vFNR
#                | changed kinetic parameters k_aa, k_O2, k_FQ, k_FN according to the new exponents
#                | changed rate cyclic succinate and kinetic parameter k_krebs to not include Ho
#     24.01.2022 | changed kinetic parameters k_ox1, k_aa to adapt them to dark Ho concentrations instead of light
# 012 28.01.2022 | changed light conversion parameters excite_ps1 and excite_ps2 with a source
#                | changed the volume fraction of thylakoids from new source and the depending parameters cf_lumen, cf_cytoplasm, k_ox1, k_O2, k_aa
#                | changed bHo to reflect the new volume ratio
#     07.02.2022 | changed reaction vNQ to oxidise Fd_red instead of Q_red (affects Keq_NQ, vNQ, parameter k_NQ)
#     10.02.2022 | used a different source for PHOTOACTIVE plastoquinone concentrations (affects c_Q_tot, c_Q_red, c_Q_ox and all dependencies)
#                | normalised the rates k_SDH, k_ox1, k_NQ, k_NDH, k_FQ to dark plastoquinone redox states
#                | changed the source for kinetic parameter k_Q
#     13.02.2022 | changed the kinetic parameter k_FN after correcting its calculation
# 013 18.02.2022 | added compounds NAD and NADH with conserved total NADtot
#                | replaced NADPH usage of NDH2 with NADH (affects k_NDH, Keq_vNDH and vNDH, added E0_NADH)
#     20.02.2022 | replaced reaction cyclicSuccinate with lumped reaction vRespiration approximating glycolysis and TCA cycle (affects kRespiration and vRespiration)
#     23.02.2022 | changed the stoichiometry of respiration, taking into account the different respiratory pathways
#                | corrected cs_ps1 and cs_ps2 for wrong source plot annotation
#     01.03.2022 | changed kinetic constants kQuench and kUnquench to visually fitted values
# 014 08.04.2022 | changed the stoichiometry and rate of respiration
#                | adjusted k_ox1, k_O2, k_aa to an adapted intracellular dark pH
#     10.04.2022 | removed "changed" comments prior to change 014
#                | changed the kinetics vFQ, vNQ, vNDH, and vb6f to irreversible mass action
#                | corrected the reversible kinetics of FNR and SDH to be thermodynamically plausible (redefined vFNR and vSDH, added dG0_FNR, dG_FNR, dG0_SDH, and dG_SDH)
#                | replaced k_FN with k_FN_fwd and k_FN_rev
#                | removed all Keqs since they are now unused
#     14.04.2022 | removed factor 0.5 multiplied to the light function in ps1states, vPS1, and ps2states
#                | corrected normalisation of excite_ps1
#     26.04.2022 | added the consumption reactions for ATP and NADH and Fd-dependent (de)activation reaction for Flv
#                | removed Keq_vFlv
# 015 29.04.2022 | removed older change notes
#                | adjusted excite_ps1 and excite_ps2 for an assumed, higher fraction of excitation transferred from PBS to PS2
#     04.05.2022 | corrected respiration Ho stoichiometry
# 016 07.07.2022 | edited values of k_Q, kQuench, and kUnquench to be the temporary values
# 017 02.08.2022 | moved consuming reactions to module_consuming_reactions
#     01.11.2022 | added full spectrum light description (temporarily from local drive)
#     02.11.2022 | changed full spectrum light description implementation to submodule
#                | added parameter pigment_content and derived parameter ps_ratio, changed definition of parameter pfd
#     03.11.2022 | added derived parameter complex_abs and replaced "light" function with algebraic module ps_normabsorption
#                | adapted functions ps2rates, ps1states, and vPS1
#     04.11.2022 | added parameter PBS_free
#     07.11.2022 | replaced function ps1states to account for fluorescence excitation quenching, added parameter k_F1
#                | added measuring light light intensity and parameter fluo_influence for fluorescence calculation
#     08.11.2022 | added remaining PSI states and renamed them to Y0, Y1, Y2
#     11.11.2022 | replaced ps2states with sympy generated algebraic solution
#     14.11.2022 | modified the ps_ratio to take into account PS2 dimers and PS1 trimers
#     06.03.2023 | switched parameters to import from parameters.py
#                | removed FQ reaction because of missing proof of existence


# Define general functions
def calculate_v(S, P, dG, dG0, kfwd, krev, RT):
    """Calculate the reversible mass-action kinetic rate
    Uses a decomposition into kinetic and thermodynamic effects.

    Args:
        S (float): Product of the substrate concentrations
        P (float): Product of the product concentrations
        dG (float): Gibbs free energy of the reaction
        dG0 (float): Standard Gibbs free energy of the reaction
        kfwd (float): Kinetic constant of the forward reaction
        krev (float): Kinetic constant of the reverse reaction
        RT (float): Physical parameter of gas constant and temperature

    Returns:
        float: kinetic rate under the given concentrations
    """
    # Calculate the forward reaction rate
    vfwd = kfwd * S * (1 - np.exp(dG))

    # If any delta G is positive, also calculate the reverse rate
    dG_pos = dG > 0
    if np.any(dG_pos):
        Keq = np.exp(-dG0 / RT)
        vrev = krev / Keq * P * (np.exp(-dG) - 1)

        # Replace those rates with a positive delta G with the one calculated with the reverse formula
        vfwd[dG_pos] = vrev[dG_pos]

    return vfwd


# Define all other functions

# Add the parameter dG_pH which is used in the calculation of equilibrium constants when protons take part
def dG_pH(R, T):
    return np.log(10) * R * T


# Add the ratio of photosystems (PS1:PS2) which is used in light handling >> changed: took into account PS2 dimers and PS1 trimers <<
def ps_ratio(PSItot, PSIItot):
    return (PSItot * 3) / (PSIItot * 2)

# Add the calculation of light absorption by the complexes >> changed: added, updated pigment association to new calculation <<
def complex_absorption(pfd, ps_ratio, pigment_content):
    absorption = lip.get_pigment_absorption(pigment_content)
    association = lip.get_pigment_association(
        ps_ratio,
        beta_carotene_method="stoichiometric",
        pigments=pigment_content,
        verbose=False,
    )

    M_chl = 893.509  # [g mol^-1] molar mass of chlorophyll a (C55H72MgN4O5)

    return (
        lip.get_complex_absorption(pfd, absorption, association) * M_chl
    )  # [µmol(Photons) mmol(Chl)^-1 s^-1]


# Define the functions used for calculation of pH/molar proton concentrations
def calculate_molarHlumen(H, cf_lumen):
    """
    Calculate the molar concentration of protons in the thylakoid lumen from the chlorophyll-normalised concentration. Uses a conversion factor dependent on the volume of the thylakoid lumen.
    """
    return H * cf_lumen  # (2.9e-5)


def calculate_molarHcytoplasm(H, cf_cytoplasm):
    """
    Calculate the molar concentration of protons in the cytoplasm from the chlorophyll-normalised concentration. Uses a conversion factor dependent on the volume of the cytoplasm.
    """
    return H * cf_cytoplasm  # (4.8e-6)


def calculate_pH(H_mol):
    return -np.log(H_mol) / np.log(10)


def deltapH(lumen, cytoplasm):
    d = cytoplasm - lumen
    return d


# Add the calculation of normalised absorption by the photosystems >> changed: added to replace "light" function <<
# Includes PBS association
def ps_normabsorption(time, PBS_PS1, PBS_PS2, complex_abs, PSItot, PSIItot, lcf):
    light_ps1 = (complex_abs["ps1"] + complex_abs["pbs"] * PBS_PS1) / PSItot
    light_ps2 = (complex_abs["ps2"] + complex_abs["pbs"] * PBS_PS2) / PSIItot

    if isinstance(light_ps2, float) and isinstance(time, np.ndarray):
        light_ps1 = np.repeat(light_ps1, len(time))
        light_ps2 = np.repeat(light_ps2, len(time))

    return light_ps1 * lcf, light_ps2 * lcf # Get float values


def ps_normabsorption_tot(light_ps1, light_ps2, light_ps1_ML, light_ps2_ML):
    return [light_ps1 + light_ps1_ML, light_ps2 + light_ps2_ML]


# Add compounds which sum with a tracked compound to a common total
def derived(part, total):
    return total - part


def PBS_free(PBS_PS1, PBS_PS2):
    return 1 - PBS_PS1 - PBS_PS2


def PSIIquench(PSII, PSIIq, Q_red, Q_ox, kQuench, kUnquench):
    return PSII * kQuench * Q_red - PSIIq * kUnquench * Q_ox


# Add reaction: Photosystem 2
def Keq_PQred(pHcytoplasm, E0_QA, F, E0_PQ, dG_pH, RT):
    DG1 = -E0_QA * F
    DG2 = -2 * E0_PQ * F + 2 * dG_pH * pHcytoplasm
    DG = -2 * DG1 + DG2
    K = np.exp(-DG / RT)
    return K


# Add the algebraic solution of ps2 as a parameter to the model and adapt the ps2states function
def _ps2states_alg_generator(reduced_size=False):
    B0, B1, B2, B3, L, k3m, k3p, kH, kF, k2, PSIItot = symbols(
        "B0 B1 B2 B3 L k3m k3p kH kF k2 PSIItot"
    )

    M = Matrix(
        (
            [
                [-L - k3m, kH + kF, k3p, 0, 0],
                [L, -(kH + kF + k2), 0, 0, 0],
                [0, 0, L, -(kH + kF), 0],
                [1, 1, 1, 1, PSIItot],
            ]
        )
    )

    sol = linsolve(M, (B0, B1, B2, B3)).args[0]
    if reduced_size:
        # If size should be reduced, only return B1 and B3
        sol = Tuple(sol[1], sol[3])
    return lambdify([L, k3m, k3p, kH, kF, k2, PSIItot], sol, "numpy", cse=True)


def _ps2states_alg_all(L, k3m, k3p, kH, kF, k2, PSIItot):
    # Output of the above _ps2states_alg_generator function with option reduced_size=False
    # If the PS2 system is redefined, apply the changes in _ps2states_alg_generator
    # and redefine this _ps2states_alg function with the result in
    # help(_ps2states_alg_generator()) under "Source code"
    # Outputs : B0, B1, B2, B3
    x0 = k2 * k3p
    x1 = kF * x0
    x2 = kH * x0
    x3 = kF**2
    x4 = k3p * x3
    x5 = kH**2
    x6 = k3p * x5
    x7 = 2 * kF * kH
    x8 = k3p * x7
    x9 = L * k2
    x10 = k3m * x9
    x11 = kF * x9
    x12 = kH * x9
    x13 = L * k3m
    x14 = kF * x13
    x15 = kH * x13
    x16 = L * k3p
    x17 = kF * x16
    x18 = kH * x16
    x19 = k2 * k3m
    x20 = kF * x19
    x21 = kH * x19
    x22 = L**2 * k2
    x23 = k3m * x3
    x24 = k3m * x5
    x25 = k3m * x7
    x26 = (
        x1
        + x10
        + x11
        + x12
        + x14
        + x15
        + x17
        + x18
        + x2
        + x20
        + x21
        + x22
        + x23
        + x24
        + x25
        + x4
        + x6
        + x8
    ) ** (-1.0)
    return (
        x26
        * (PSIItot * x1 + PSIItot * x2 + PSIItot * x4 + PSIItot * x6 + PSIItot * x8),
        x26 * (PSIItot * x17 + PSIItot * x18),
        x26
        * (
            PSIItot * x11
            + PSIItot * x12
            + PSIItot * x20
            + PSIItot * x21
            + PSIItot * x23
            + PSIItot * x24
            + PSIItot * x25
        ),
        x26 * (PSIItot * x10 + PSIItot * x14 + PSIItot * x15 + PSIItot * x22),
    )


def _ps2states_alg_reduced(L, k3m, k3p, kH, kF, k2, PSIItot):
    # Output of the above _ps2states_alg_generator function with option reduced_size=False
    # If the PS2 system is redefined, apply the changes in _ps2states_alg_generator
    # and redefine this _ps2states_alg function with the result in
    # help(_ps2states_alg_generator()) under "Source code"
    # Outputs : B1, B3
    x0 = L * k3p
    x1 = kF * x0
    x2 = kH * x0
    x3 = L * k2
    x4 = k3m * x3
    x5 = L * k3m
    x6 = kF * x5
    x7 = kH * x5
    x8 = k2 * k3m
    x9 = k2 * k3p
    x10 = L**2 * k2
    x11 = kF**2
    x12 = kH**2
    x13 = 2 * kF * kH
    x14 = (
        k3m * x11
        + k3m * x12
        + k3m * x13
        + k3p * x11
        + k3p * x12
        + k3p * x13
        + kF * x3
        + kF * x8
        + kF * x9
        + kH * x3
        + kH * x8
        + kH * x9
        + x1
        + x10
        + x2
        + x4
        + x6
        + x7
    ) ** (-1.0)
    return (
        x14 * (PSIItot * x1 + PSIItot * x2),
        x14 * (PSIItot * x10 + PSIItot * x4 + PSIItot * x6 + PSIItot * x7),
    )


def ps2states(
    PSIIq,
    PQ,
    PQred,
    Keq_PQred,
    light_ps2,
    PSIItot,
    k2,
    kF,
    kH0,
    kHst,
    kPQred,
    _ps2states_alg,
):
    # Calculate some rates
    kH = kH0 + kHst * (PSIIq / PSIItot)
    k3p = kPQred * PQ
    k3m = kPQred * PQred / Keq_PQred

    # Pack parameters and potential variables as dicts and insert them
    var_dict = {"L": light_ps2, "k3m": k3m, "k3p": k3p, "kH": kH}
    param_dict = {"kF": kF, "k2": k2, "PSIItot": PSIItot}

    return np.array(_ps2states_alg(**var_dict, **param_dict))


def vPS2(B1, k2):
    """reaction rate constant for photochemistry"""
    v = (
        0.5 * k2 * B1
    )  # k2 is scaled to single electron extraction (B1 -> B2) and has to be scaled by 0.5 for 2-electron PS2 reaction
    return v


# Add reaction: Succinate dehydrogenase
def Keq_vSDH(pHcytoplasm, E0_PQ, F, E0_succinate_fumarate, RT, dG_pH):
    DG1 = -2 * E0_PQ * F + 2 * dG_pH * pHcytoplasm
    DG2 = -2 * E0_succinate_fumarate * F + 2 * dG_pH * pHcytoplasm
    DG = DG1 - DG2
    K = np.exp(-DG / RT)
    return K


def vSDH(q, succinate, fumarate, pqred, Ksdh, ksdh):
    """electron flow via SDH"""
    return ksdh * (q * succinate - (pqred * fumarate) / (Ksdh))


# Add reaction: respiration
# An approximation of glycolysis and the tricarboxylic acid cycle
def vRespiration(PGA, fumarate, ADP, NAD, NADP, kRespiration, KMPGA):
    """approximation of respiration resulting in the consumption of 3PGA with generation of ATP, NADPH, NADH, and succinate (from fumarate)"""
    return (
        kRespiration * fumarate * ADP * NAD * NADP * rf.michaelis_menten(PGA, 1, KMPGA)
    )


def vbd(o2, qred, ho, kox1):  # q, Kbd,   water ignored
    """electron flow from Q to O2 via terminal oxidase"""
    return kox1 * qred * o2 * ho  # - q/Kbd)


# Add reaction: Cytochrome b6f complex
def vb6f(pc, ho, qred, kq):
    """electron flow from Q to PC (Q oxidized)"""
    return kq * qred * pc * ho


# Add reaction: aa3-type terminal oxidase
def vaa(pcred, o2, ho, kaa):  # pc, hi, Kaa
    """electron flow via aa3 Cox"""
    return kaa * pcred * o2 * ho


# Add reaction: Photosystem 1
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


# PS1 state supplemental functions
def calc_a(Fd_red, Keq_FAFd, k_L1, kFdred, **kwargs):
    return (kFdred / Keq_FAFd) * Fd_red - k_L1


def calc_b(Fd_ox, k_L1, k_F1, kFdred, **kwargs):
    return kFdred * Fd_ox + k_F1 + k_L1


def calc_c(PC_ox, Keq_PCP700, k_L1, kPCox, **kwargs):
    return (kPCox / Keq_PCP700) * PC_ox + k_L1


def calc_d(a, b, PC_red, k_F1, kPCox, **kwargs):
    return k_F1 * a / b + kPCox * PC_red


def calc_f(a, b, d, **kwargs):
    return (1 + a / b) / d


def calc_Y0(b, c, f, PSItot, k_L1, k_F1, **kwargs):
    return (PSItot * (1 - (k_L1 / b) * (1 - k_F1 * f))) / (1 + c * f)


def calc_Y2(Y0, b, c, d, PSItot, k_L1, k_F1, **kwargs):
    return (Y0 * c - (k_F1 * k_L1 * PSItot) / b) / d


def calc_Y1(Y2, a, b, PSItot, k_L1, **kwargs):
    return Y2 * a / b + (k_L1 * PSItot) / b


# Internal PS1 states >> changed: rpleaced with new function accounting for fluorescence excitation quenching <<
def ps1states(
    Fd_ox,
    Fd_red,
    PC_ox,
    PC_red,
    light_ps1,
    Keq_PCP700,
    Keq_FAFd,
    PSItot,
    k_F1,
    kPCox,
    kFdred,
):
    k_L1 = light_ps1

    a = calc_a(Fd_red, Keq_FAFd, k_L1, kFdred)
    b = calc_b(Fd_ox, k_L1, k_F1, kFdred)
    c = calc_c(PC_ox, Keq_PCP700, k_L1, kPCox)
    d = calc_d(a, b, PC_red, k_F1, kPCox)
    f = calc_f(a, b, d)

    Y0 = calc_Y0(b, c, f, PSItot, k_L1, k_F1)
    Y2 = calc_Y2(Y0, b, c, d, PSItot, k_L1, k_F1)
    Y1 = calc_Y1(Y2, a, b, PSItot, k_L1)

    return Y0, Y1, Y2


def vPS1(
    Y0, Y1, light_ps1, k_F1
):  # >> changed: replaced light function with variable light_ps1 <<
    """reaction rate constant for open PSI"""
    L = light_ps1
    v = L * Y0 - Y1 * k_F1
    return v


# FLUORESCENCE
# Old PS2 fluorescence
def fluorescence_ps2_old(B0, B2, PSIIq, k2, kF, kH0, kHst, PSIItot):
    ps2cs = 0.5
    kH = kHst * (PSIIq / PSIItot)
    fluo = (ps2cs * kF * B0) / (kF + kH0 + k2 + kH) + (ps2cs * kF * B2) / (
        kF + kH0 + kH
    )
    return fluo


# Total cell fluorescence

# Add an estimation of the PS2 fluorescence
# Necessary: The internal states of PS2 with added measuring light
def fluorescence_ps2(B1, B3, B1_tot, B3_tot, kF, fluo_influence):
    return ((B1_tot - B1) * kF + (B3_tot - B3) * kF) * fluo_influence["PS2"]


# Add an estimation of the PS1 fluorescence
# Necessary: The internal states of PS2 with added measuring light
def fluorescence_ps1(Y1, Y1_tot, k_F1, fluo_influence):
    return (Y1_tot - Y1) * k_F1 * fluo_influence["PS1"]


# Add an estimation of the PBS fluorescence
def fluorescence_pbs(PBS_free, complex_abs_ML, fluo_influence, lcf):
    return PBS_free * complex_abs_ML["pbs"] * fluo_influence["PBS"] * lcf


# Estimate the total fluorescence >> changed: definition of fluorescence including PS1 and free PBS
def fluorescence_tot(FPS2, FPS1, FPBS):
    return FPS2 + FPS1 + FPBS


# Add reaction: Flavodiiron heterodimer 1/3
# Function of gradual Flv activation and inactivation
def Flvactivation(Flva, Fd_red, Fd_ox, kFlvactivation, kFlvdeactivation):
    return kFlvactivation * Fd_red * (1 - Flva) - kFlvdeactivation * Fd_ox * Flva


def vFlv(Fd_red, O2, Ho, Flva, k_O2):
    """electron flow from Fd to O2 via Flv1/3-Heterodimere"""
    return k_O2 * Fd_red * O2 * Ho * Flva


# Add reaction: NADPH dehydrogenase 2
def vNDH(q, ho, nadh, kndh):
    """electron flow via NDH-2"""
    return kndh * q * nadh * ho


# Add reaction: Ferredoxin NADPH reductase
# Calculatte the standard Gibbs free energy
def dG0_FNR(pHcytoplasm, E0_Fd, F, E0_NADP, dG_pH):
    # Calculate deltaG0
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_NADP * F + dG_pH * pHcytoplasm
    dG0 = -2 * DG1 + DG2
    return dG0


# Calculate the Gibbs free energy
def dG_FNR(Fd_red, NADP, Fd_ox, NADPH, dG0_FNR, RT):
    # Caclulate delta G
    S = Fd_red**2 * NADP
    P = Fd_ox**2 * NADPH
    return dG0_FNR + RT * np.log(P / S)


# Calculate the reaction rate
def vFNR(Fd_red, NADP, Fd_ox, NADPH, dG_FNR, dG0_FNR, k_FN_fwd, k_FN_rev, RT):
    # Calculate the forward reaction rate
    S = Fd_red * NADP
    P = Fd_ox * NADPH
    return calculate_v(S, P, dG_FNR, dG0_FNR, k_FN_fwd, k_FN_rev, RT)


# Add reaction: Proton leakage across the thylakoid membrane
def vPass(Hi_mol, Ho_mol, kpass):
    """passive proton flow"""
    return kpass * (Hi_mol - Ho_mol)


# Add reaction: NADPH dehydrogenase complex 1
def vNQ(q, ho, fd_red, knq):
    """electron flow via NDH-1 (long cycle)"""
    return knq * (q * fd_red * ho)


# Add reaction: Oxygen efflux
def vO2out(O2, O2ext, kO2out):
    """
    exchange of oxygen with the environment, viewed in outward direction
    assumes a constant external oxygen concentration
    """
    return kO2out * (O2 - O2ext)


# Add reaction: Carbon dioxide concentration by CCM
def vCCM(CO2, CO2ext, kCCM, fCin):
    """
    exchange of CO2 with the environment, viewed in inward direction
    factors in a concentration of CO2 in the cell by the CCM by factor fCin
    assumes a constant external CO2 concentration
    """
    return kCCM * (CO2ext - (CO2 / fCin))


# Define the overarching function adding the general ETC construct to a modelbase model
def add_electron_transport_chain(
    m, init_param=None, pbs_behaviour="static", reduced_size=False, verbose=True
):
    """
    Adds the general structure for the Synechocystis electron transport chain to a modelbase model
    Does not include:
        - ATPase
        - ATP and NADPH consuming reactions
        - Photorespiration
    """

    ### PARAMETERS AND COMPOUNDS ###

    # Add the parameters and primary tracked compounds to the model
    # Define Parameters
    p_list = [
        ### Total concentrations of conserved quantities ###
        "PSIItot",
        "PSItot",
        "Q_tot",
        "PC_tot",
        "Fd_tot",
        "NADP_tot",
        "NAD_tot",
        "AP_tot",
        ### Rate constants ###
        # PS2 rate constants
        "kH0",
        "kHst",
        "kF",
        "k2",
        "kPQred",
        # PS1 rate constants
        "k_F1",
        "kPCox",
        "kFdred",
        # Other ETC rate constants
        "k_ox1",
        "k_Q",
        "k_NDH",
        "k_SDH",
        "k_O2",
        "k_FN_fwd",
        "k_FN_rev",
        "k_pass",
        "k_NQ",
        "k_aa",
        "kRespiration",
        "kO2out",
        "kCCM",
        "kQuench",
        "kUnquench",
        # Rate constants of Fd-mediated enzyme activiation reactions
        "kFlvactivation",
        "kFlvdeactivation",
        ### Kinetic constants ###
        "KMPGA",
        ### Standard electrode potentials ###
        "E0_QA",
        "E0_PQ",
        "E0_PC",
        "E0_P700",
        "E0_FA",
        "E0_Fd",
        "E0_O2/H2O",
        "E0_NADP",
        "E0_NAD",
        "E0_succinate/fumarate",
        ### Physical and other constants ###
        "F",
        "R",
        "bHi",
        "bHo",
        "cf_lumen",
        "cf_cytoplasm",
        ### Environmental constants ###
        "T",
        "O2ext",
        "CO2ext",
        "fCin",
        ### Light absorption parameters ###
        "fluo_influence",
        "pigment_content",
        "lcf"
    ]
    c_list = [
        "PSII",
        "Q_ox",
        "Hi",
        "Ho",
        "O2",
        "PC_ox",
        "Fd_ox",
        "NADPH",
        "NADH",
        "ATP",
        "CO2",
        "succinate",
        "fumarate",
        "3PGA",
        "Flva",
    ]

    if pbs_behaviour == "static":
        p_list += ["PBS_PS1", "PBS_PS2", "PBS_free"]
    elif pbs_behaviour == "dynamic":
        c_list += ["PBS_PS1", "PBS_PS2"]
        if verbose:
            print("updating PBS to dynamic representation")
    else:
        raise ValueError("pbs_behaviour must be either 'static' or 'dynamic'")

    p = {k: v for k, v in parameters.p.items() if k in p_list}
    # >> changed: added light absorption parameters <<
    # Add light parameters via lip
    p.update(
        {
            ### Default lights ###
            "pfd": lip.light_spectra(
                "warm_white_led", 100
            ),  # [umol(photons) m^-2 s^-1] light intensity (photon flux density) per wavelength [400 nm - 700 nm] (set)
            "pfd_ML": lip.light_gaussianLED(
                625, 1
            ),  # [umol(photons) m^-2 s^-1] MEASURING LIGHT intensity (photon flux density) per wavelength [400 nm - 700 nm] (set)
        }
    )

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update(
            {k: v for k, v in init_param.items() if k in p_list + ["pfd", "pfd_ML"]}
        )

    m.add_parameters(p)

    m.add_compounds(c_list)

    # Add the product R*T as a parameter since this is often used in the calculation of equilibrium constants
    m.add_derived_parameter(
        parameter_name="RT", function=np.multiply, parameters=["R", "T"]
    )

    # Add the parameter dG_pH which is used in the calculation of equilibrium constants when protons take part
    m.add_derived_parameter(
        parameter_name="dG_pH",
        function=dG_pH,
        parameters=["R", "T"],
    )

    # Add the ratio of photosystems (PS1:PS2) which is used in light handling >> changed: took into account PS2 dimers and PS1 trimers <<
    m.add_derived_parameter(
        parameter_name="ps_ratio",
        function=ps_ratio,
        parameters=["PSItot", "PSIItot"],
    )

    # Add the calculation of light absorption by the complexes >> changed: added, updated pigment association to new calculation <<
    m.add_derived_parameter(
        parameter_name="complex_abs",
        function=complex_absorption,
        parameters=["pfd", "ps_ratio", "pigment_content"],
    )

    # Add the calculation of MEASURING LIGHT light absorption by the complexes >> changed: added <<
    m.add_derived_parameter(
        parameter_name="complex_abs_ML",
        function=complex_absorption,
        parameters=["pfd_ML", "ps_ratio", "pigment_content"],
    )

    # Add the molar proton concentrations, pHs and the pH difference
    m.add_algebraic_module(
        module_name="molarHlumen",
        function=calculate_molarHlumen,
        compounds=["Hi"],
        parameters=["cf_lumen"],
        derived_compounds=["Hi_mol"],
    )
    m.add_algebraic_module(
        module_name="molarHcytoplasm",
        function=calculate_molarHcytoplasm,
        compounds=["Ho"],
        parameters=["cf_cytoplasm"],
        derived_compounds=["Ho_mol"],
    )
    m.add_algebraic_module(
        module_name="pHlumen",
        function=calculate_pH,
        compounds=["Hi_mol"],
        derived_compounds=["pHlumen"],
    )
    m.add_algebraic_module(
        module_name="pHcytoplasm",
        function=calculate_pH,
        compounds=["Ho_mol"],
        derived_compounds=["pHcytoplasm"],
    )
    m.add_algebraic_module(
        module_name="deltapH",
        function=deltapH,
        compounds=["pHlumen", "pHcytoplasm"],
        derived_compounds=["dpH"],
    )

    # Add the calculation of normalised absorption by the photosystems >> changed: added to replace "light" function <<
    # Includes PBS association
    m.add_algebraic_module_from_args(
        module_name="ps_normabsorption",
        function=ps_normabsorption,
        args=["time", "PBS_PS1", "PBS_PS2", "complex_abs", "PSItot", "PSIItot", "lcf"],
        derived_compounds=["light_ps1", "light_ps2"],
    )

    # Add the calculation of the normalised absorption of the measuring light and the total of actinic and measuring light (tot)
    m.add_algebraic_module_from_args(
        module_name="ps_normabsorption_ML",
        function=ps_normabsorption,
        args=["time", "PBS_PS1", "PBS_PS2", "complex_abs_ML", "PSItot", "PSIItot", "lcf"],
        derived_compounds=["light_ps1_ML", "light_ps2_ML"],
    )

    m.add_algebraic_module_from_args(
        module_name="ps_normabsorption_tot",
        function=ps_normabsorption_tot,
        args=["light_ps1", "light_ps2", "light_ps1_ML", "light_ps2_ML"],
        derived_compounds=["light_ps1_tot", "light_ps2_tot"],
    )

    # Add compounds which sum with a tracked compound to a common total
    m.add_algebraic_module(  # Add reduced plastoquinone
        module_name="dQ",
        function=derived,
        compounds=["Q_ox"],
        derived_compounds=["Q_red"],
        parameters=["Q_tot"],
    )
    m.add_algebraic_module(  # Add reduced plastocyanin
        module_name="dPC",
        function=derived,
        compounds=["PC_ox"],
        derived_compounds=["PC_red"],
        parameters=["PC_tot"],
    )
    m.add_algebraic_module(  # Add reduced ferredoxin
        module_name="dFd",
        function=derived,
        compounds=["Fd_ox"],
        derived_compounds=["Fd_red"],
        parameters=["Fd_tot"],
    )
    m.add_algebraic_module(  # Add NADP (oxidised NADPH)
        module_name="dNADPH",
        function=derived,
        compounds=["NADPH"],
        derived_compounds=["NADP"],
        parameters=["NADP_tot"],
    )
    m.add_algebraic_module(  # Add NAD (oxidised NADH)
        module_name="dNADH",
        function=derived,
        compounds=["NADH"],
        derived_compounds=["NAD"],
        parameters=["NAD_tot"],
    )
    m.add_algebraic_module(  # Add ADP
        module_name="dAP",
        function=derived,
        compounds=["ATP"],
        derived_compounds=["ADP"],
        parameters=["AP_tot"],
    )
    m.add_algebraic_module(  # Add quenched PSII
        module_name="PSIIq",
        function=derived,
        compounds=["PSII"],
        derived_compounds=["PSIIq"],
        parameters=["PSIItot"],
    )

    if pbs_behaviour == "dynamic":
        m.add_algebraic_module_from_args(
            module_name="PBS_free",
            function=PBS_free,
            args=["PBS_PS1", "PBS_PS2"],
            derived_compounds=["PBS_free"],
        )

    ### REACTIONS ###

    # Add reaction: Photosystem 2 quenching by state transitions
    m.add_reaction(
        rate_name="vPSIIquench",
        function=PSIIquench,
        stoichiometry={"PSII": -1},
        modifiers=["PSII", "PSIIq", "Q_red", "Q_ox"],
        dynamic_variables=["PSII", "PSIIq", "Q_red", "Q_ox"],
        parameters=["kQuench", "kUnquench"],
        reversible=True,
    )

    # Add reaction: Photosystem 2
    # Including the algebraic function to calculate the PS2 QSS
    m.add_algebraic_module(
        module_name="Keq_PQred",
        function=Keq_PQred,
        compounds=["pHcytoplasm"],
        derived_compounds=["Keq_PQred"],
        parameters=["E0_QA", "F", "E0_PQ", "dG_pH", "RT"],
    )
    if reduced_size:
        _ps2states_alg = _ps2states_alg_reduced
        Bs = ["B1", "B3"]
    else:
        _ps2states_alg = _ps2states_alg_all
        Bs = ["B0", "B1", "B2", "B3"]
    Bs_tot = [B + "_tot" for B in Bs]
    m.add_parameter("_ps2states_alg", _ps2states_alg)

    m.add_algebraic_module_from_args(  # >> changed: replaced light function arguments with variable light_ps2 <<
        module_name="ps2states",
        function=ps2states,
        args=[
            "PSIIq",
            "Q_ox",
            "Q_red",
            "Keq_PQred",
            "light_ps2",
            "PSIItot",
            "k2",
            "kF",
            "kH0",
            "kHst",
            "kPQred",
            "_ps2states_alg",
        ],
        derived_compounds=Bs,
    )

    m.add_reaction(
        rate_name="vPS2",
        function=vPS2,
        stoichiometry={
            "Q_ox": -1,
            "Ho": -2 / m.get_parameter("bHo"),
            "Hi": 2 / m.get_parameter("bHi"),
            "O2": 0.5,
        },
        modifiers=["B1"],
        dynamic_variables=["B1"],
        parameters=["k2"],
        reversible=True,
    )

    # Add reaction: Succinate dehydrogenase
    m.add_algebraic_module(
        module_name="Keq_vSDH",
        function=Keq_vSDH,
        compounds=["pHcytoplasm"],
        derived_compounds=["Keq_vSDH"],
        parameters=["E0_PQ", "F", "E0_succinate/fumarate", "RT", "dG_pH"],
    )

    m.add_reaction(
        rate_name="vSDH",
        function=vSDH,
        stoichiometry={
            "Q_ox": -1,
            "succinate": -1,
            "fumarate": 1,
        },  # /m.get_parameter("bH")
        modifiers=["fumarate", "Q_red", "Keq_vSDH"],
        dynamic_variables=["Q_ox", "succinate", "fumarate", "Q_red", "Keq_vSDH"],
        parameters=["k_SDH"],
        reversible=True,
    )

    # Add reaction: respiration
    # An approximation of glycolysis and the tricarboxylic acid cycle
    m.add_reaction(
        rate_name="vRespiration",
        function=vRespiration,
        stoichiometry={
            "3PGA": -1.000,
            "fumarate": -7.402e-02,
            "CO2": 3.000,
            "succinate": 7.402e-02,
            "ATP": 0.567,
            "NADPH": 2.237,
            "NADH": 2.689,
            "Ho": 4.926 / m.get_parameter("bHo"),
        },
        modifiers=["ADP", "NAD", "NADP"],
        dynamic_variables=["3PGA", "fumarate", "ADP", "NAD", "NADP"],
        parameters=["kRespiration", "KMPGA"],
        reversible=False,
    )

    # Add reaction: bd-type terminal oxidase
    m.add_reaction(
        rate_name="vbd",
        function=vbd,
        stoichiometry={
            "Q_ox": 2,
            "O2": -1,
            "Ho": -4 / m.get_parameter("bHo"),
            "Hi": 4 / m.get_parameter("bHi"),
        },
        modifiers=["Q_red"],  # , "Q_ox", "Keq_vbd"
        dynamic_variables=["O2", "Q_red", "Ho"],  # , "Q_ox", "Keq_vbd"
        parameters=["k_ox1"],
        reversible=False,
    )

    # Add reaction: Cytochrome b6f complex
    m.add_reaction(
        rate_name="vb6f",
        function=vb6f,
        stoichiometry={
            "Q_ox": 1,
            "Hi": 4 / m.get_parameter("bHi"),
            "PC_ox": -2,
            "Ho": -2 / m.get_parameter("bHo"),
        },
        modifiers=[
            "Q_red",
        ],
        dynamic_variables=["PC_ox", "Ho", "Q_red"],
        parameters=["k_Q"],
        reversible=True,
    )

    # Add reaction: aa3-type terminal oxidase
    m.add_reaction(
        rate_name="vaa",
        function=vaa,
        stoichiometry={
            "PC_ox": 4,
            "Hi": 1 / m.get_parameter("bHi"),
            "O2": -1,
            "Ho": -5 / m.get_parameter("bHo"),
        },
        modifiers=["PC_ox", "Hi", "PC_red"],  # , "Keq_vaa"
        dynamic_variables=["PC_red", "O2", "Ho"],  # , "PC_ox", "Hi", "Keq_vaa"
        parameters=["k_aa"],
        reversible=False,
    )

    # Add reaction: Photosystem 1
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

    # Internal PS1 states >> changed: rpleaced with new function accounting for fluorescence excitation quenching <<
    m.add_algebraic_module(  # >> changed: replaced light function arguments with variable light_ps1 <<
        module_name="ps1states",
        function=ps1states,
        compounds=["Fd_ox", "Fd_red", "PC_ox", "PC_red", "light_ps1"],
        derived_compounds=["Y0", "Y1", "Y2"],
        parameters=["Keq_PCP700", "Keq_FAFd", "PSItot", "k_F1", "kPCox", "kFdred"],
    )

    m.add_reaction(  # >> changed: replaced light function arguments with variable light_ps1 <<
        rate_name="vPS1",
        function=vPS1,
        stoichiometry={"Fd_ox": -1, "PC_ox": 1},
        modifiers=["Y0", "Y1", "light_ps1"],
        dynamic_variables=["Y0", "Y1", "light_ps1"],
        parameters=["k_F1"],
        reversible=True,
    )

    # FLUORESCENCE
    # Old PS2 fluorescence (can't be computed if reduced size, B0 missing)
    if not reduced_size:
        m.add_algebraic_module_from_args(
            module_name="fluorescence_ps2_old",
            function=fluorescence_ps2_old,
            args=["B0", "B2", "PSIIq", "k2", "kF", "kH0", "kHst", "PSIItot"],
            derived_compounds=["FPS2_old"],
        )

    # Total cell fluorescence

    # Add an estimation of the PS2 fluorescence
    # Necessary: The internal states of PS2 with added measuring light
    m.add_algebraic_module_from_args(  # >> changed: replaced light function arguments with variable light_ps2 <<
        module_name="ps2states_tot",
        function=ps2states,
        args=[
            "PSIIq",
            "Q_ox",
            "Q_red",
            "Keq_PQred",
            "light_ps2_tot",
            "PSIItot",
            "k2",
            "kF",
            "kH0",
            "kHst",
            "kPQred",
            "_ps2states_alg",
        ],
        derived_compounds=Bs_tot,
    )

    m.add_algebraic_module_from_args(
        module_name="fluorescence_ps2",
        function=fluorescence_ps2,
        args=["B1", "B3", "B1_tot", "B3_tot", "kF", "fluo_influence"],
        derived_compounds=["FPS2"],
    )

    # Add an estimation of the PS1 fluorescence
    # Necessary: The internal states of PS2 with added measuring light
    m.add_algebraic_module(  # >> changed: replaced light function arguments with variable light_ps1 <<
        module_name="ps1states_tot",
        function=ps1states,
        compounds=["Fd_ox", "Fd_red", "PC_ox", "PC_red", "light_ps1_tot"],
        derived_compounds=["Y0_tot", "Y1_tot", "Y2_tot"],
        parameters=["Keq_PCP700", "Keq_FAFd", "PSItot", "k_F1", "kPCox", "kFdred"],
    )

    m.add_algebraic_module_from_args(
        module_name="fluorescence_ps1",
        function=fluorescence_ps1,
        args=["Y1", "Y1_tot", "k_F1", "fluo_influence"],
        derived_compounds=["FPS1"],
    )

    # Add an estimation of the PBS fluorescence
    m.add_algebraic_module_from_args(
        module_name="fluorescence_pbs",
        function=fluorescence_pbs,
        args=["PBS_free", "complex_abs_ML", "fluo_influence", "lcf"],
        derived_compounds=["FPBS"],
    )

    # Estimate the total fluorescence >> changed: definition of fluorescence including PS1 and free PBS
    m.add_algebraic_module_from_args(
        module_name="fluorescence_tot",
        function=fluorescence_tot,
        args=["FPS2", "FPS1", "FPBS"],
        derived_compounds=["Fluo"],
    )

    # Add reaction: Flavodiiron heterodimer 1/3
    # Function of gradual Flv activation and inactivation
    m.add_reaction(
        rate_name="vFlvactivation",
        function=Flvactivation,
        stoichiometry={"Flva": 1},
        modifiers=["Flva", "Fd_red", "Fd_ox"],
        dynamic_variables=["Flva", "Fd_red", "Fd_ox"],
        parameters=["kFlvactivation", "kFlvdeactivation"],
        reversible=True,
    )

    m.add_reaction(
        rate_name="vFlv",
        function=vFlv,
        stoichiometry={
            "Fd_ox": 4,
            "O2": -1,
            "Ho": -4 / m.get_parameter("bHo"),
        },  # /m.get_parameter("bH")
        modifiers=["Fd_red", "Flva"],  # , 'Fd_ox', "Keq_vFlv"
        dynamic_variables=["Fd_red", "O2", "Ho", "Flva"],  # , "Fd_ox", "Keq_vFlv"
        parameters=["k_O2"],
        reversible=False,
    )

    # Add reaction: NADPH dehydrogenase 2
    m.add_reaction(
        rate_name="vNDH",
        function=vNDH,
        stoichiometry={
            "Q_ox": -1,
            "NADH": -1,
            "Ho": -1 / m.get_parameter("bHo"),
        },  # /m.get_parameter("bH")
        modifiers=[],
        dynamic_variables=["Q_ox", "Ho", "NADH"],
        parameters=["k_NDH"],
        reversible=True,
    )

    # Add reaction: Ferredoxin NADPH reductase
    # Calculatte the standard Gibbs free energy
    m.add_algebraic_module(
        module_name="dG0_FNR",
        function=dG0_FNR,
        compounds=["pHcytoplasm"],
        parameters=["E0_Fd", "F", "E0_NADP", "dG_pH"],
        derived_compounds=["dG0_FNR"],
    )

    # Calculate the Gibbs free energy
    m.add_algebraic_module(
        module_name="dG_FNR",
        function=dG_FNR,
        compounds=["Fd_red", "NADP", "Fd_ox", "NADPH", "dG0_FNR"],
        parameters=["RT"],
        derived_compounds=["dG_FNR"],
    )

    # Calculate the reaction rate
    m.add_reaction(
        rate_name="vFNR",
        function=vFNR,
        stoichiometry={"Fd_ox": 2, "NADPH": 1, "Ho": -1 / m.get_parameter("bHo")},
        modifiers=["Fd_red", "NADP", "Fd_ox", "NADPH", "dG_FNR", "dG0_FNR"],
        dynamic_variables=["Fd_red", "NADP", "Fd_ox", "NADPH", "dG_FNR", "dG0_FNR"],
        parameters=["k_FN_fwd", "k_FN_rev", "RT"],
        reversible=True,
    )

    # Add reaction: Proton leakage across the thylakoid membrane
    m.add_reaction(
        rate_name="vPass",
        function=vPass,
        stoichiometry={
            "Hi": -1 / m.get_parameter("bHi"),
            "Ho": 1 / m.get_parameter("bHo"),
        },
        modifiers=["Hi_mol", "Ho_mol"],
        dynamic_variables=["Hi_mol", "Ho_mol"],
        parameters=["k_pass"],
        reversible=False,
    )

    # Add reaction: NADPH dehydrogenase complex 1
    m.add_reaction(
        rate_name="vNQ",
        function=vNQ,
        stoichiometry={
            "Fd_ox": 2,
            "Q_ox": -1,
            "Hi": 1 / m.get_parameter("bHi"),
            "Ho": -3 / m.get_parameter("bHo"),
        },
        modifiers=["Fd_red"],
        dynamic_variables=["Q_ox", "Ho", "Fd_red"],
        parameters=["k_NQ"],
        reversible=True,
    )

    # Add reaction: Oxygen efflux
    m.add_reaction(
        rate_name="vO2out",
        function=vO2out,
        stoichiometry={"O2": -1},
        modifiers=["O2"],
        dynamic_variables=["O2"],
        parameters=["O2ext", "kO2out"],
        reversible=True,
    )

    # Add reaction: Carbon dioxide concentration by CCM
    m.add_reaction(
        rate_name="vCCM",
        function=vCCM,
        stoichiometry={"CO2": 1},
        modifiers=["CO2"],
        dynamic_variables=["CO2"],
        parameters=["CO2ext", "kCCM", "fCin"],
        reversible=True,
    )

    return m
