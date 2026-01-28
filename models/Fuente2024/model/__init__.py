
from collections.abc import Iterable

import numpy as np
from mxlpy import InitialAssignment, Model, Variable
from scipy.optimize import least_squares

from .derived_quantities import (
    _osc_light,
    _rcii_closed,
    _rcii_open,
    _sigma_PSII,
    include_derived_quantities,
)
from .rates import (
    _v1,
    _v2,
    _v3,
    _v5,
    _v7,
    _v_PSI,
    _v_PSII,
    include_rates,
    mass_action_1s,
)

__all__ = ["Fuente2024"]

def initial_equations(initial_guess: Iterable, param_dict: dict) -> list[float]:
    
    Q_active, PQ_ox, PSI_ox, h_lumen, ATP = initial_guess
    
    PQ_tot = param_dict["PQ_tot"]
    h_stroma = param_dict["h_stroma"]
    Atot = param_dict["Atot"]
    nPSI = param_dict["nPSI"]
    stoic_PSII = param_dict["stoic_PSII"]
    NPQ_max = param_dict["NPQ_max"]
    bH = param_dict["bH"]
    V_stroma = param_dict["V_stroma"]
    V_lumen = param_dict["V_lumen"]
    k1p = param_dict["k1p"]
    k1m = param_dict["k1m"]
    k2p = param_dict["k2p"]
    k2m = param_dict["k2m"]
    k3 = param_dict["k3"]
    K_NPQ = param_dict["K_NPQ"]
    n_NPQ = param_dict["n_NPQ"]
    k4 = param_dict["k4"]
    k5 = param_dict["k5"]
    cEqP = param_dict["cEqP"]
    k6 = param_dict["k6"]
    k7 = param_dict["k7"]
    pfd = param_dict["pfd"]
    k_X = param_dict["k_X"]
    L_PSI = param_dict["L_PSI"]
    stoic_PSI = param_dict["stoic_PSI"]
    sigma_PSI = param_dict["sigma_PSI"]
    N_A = param_dict["N_A"]
    
    light = _osc_light(pfd=pfd, pfd_add=0, f=0, time=0)
    PQ_red = PQ_tot - PQ_ox
    PSI_red = nPSI - PSI_ox
    ADP = Atot - ATP
    sigma_PSII = _sigma_PSII(NPQ_max=NPQ_max, Q_active=Q_active)
    RCII_closed = _rcii_closed(k1p=k1p, PQ_ox=PQ_ox, sigma_PSII=sigma_PSII, light=light, k1m=k1m, PQ_red=PQ_red)
    RCII_open = _rcii_open(k1p=k1p, PQ_ox=PQ_ox, sigma_PSII=sigma_PSII, k1m=k1m, PQ_red=PQ_red)
    
    v_psii = _v_PSII(stoic_PSII=stoic_PSII, sigma_PSII=sigma_PSII, light=light, RCII_closed=RCII_closed)
    v_ps1 = _v_PSI(stoic_PSI=stoic_PSI, sigma_PSI=sigma_PSI, light=light, PSI_ox=PSI_ox, L_PSI=L_PSI)
    v1 = _v1(k1p=k1p, RCII_closed=RCII_closed, PQ_ox=PQ_ox, k1m=k1m, RCII_open=RCII_open, PQ_red=PQ_red)
    v2 = _v2(k2p=k2p, PQ_red=PQ_red, PSI_ox=PSI_ox, k2m=k2m, PQ_ox=PQ_ox, PSI_red=PSI_red)
    v3 = _v3(k3=k3, h_lumen=h_lumen, Q_active=Q_active, K_NPQ=K_NPQ, n=n_NPQ)
    v4 = mass_action_1s(Q_active, k4)
    v5 = _v5(k5=k5, ADP=ADP, ATP=ATP, H_stroma=h_stroma, H_lumen=h_lumen, cEqP=cEqP)
    v6 = mass_action_1s(ATP, k6)
    v7 = _v7(k7=k7, H_lumen=h_lumen, H_stroma=h_stroma)
    vX = mass_action_1s(PSI_red, k_X)
    
    alpha = bH / (N_A * V_lumen)
    beta = 14/3 * bH * V_stroma / V_lumen
    
    dqactive_dt = v3 - v4
    dpqox_dt = 1/2 * (v2 - v1) + vX
    dpsiox_dt = v_ps1 - v2
    dhlumen_dt = alpha * v_psii + alpha * v2 - beta * v5 - bH * v7
    datp_dt = v5 - v6
    # print(dqactive_dt)
    
    return [dqactive_dt, dpqox_dt, dpsiox_dt, dhlumen_dt, datp_dt]

def initial_combined(extract_str: str, param_dict: dict) -> float:
    
    bounds = [
        (0, 1),  # Q_active
        (0, param_dict["PQ_tot"]),  # PQ_ox
        (0, param_dict["nPSI"]),  # PSI_ox
        (param_dict["h_stroma"], param_dict["h_stroma"] * 100),  # h_lumen
        (0, param_dict["Atot"]),  # ATP
    ]
    
    bounds_low = [b[0] for b in bounds]
    bounds_high = [b[1] for b in bounds]
    
    res = least_squares(
        fun = initial_equations,
        x0 = initials(
            PQ_tot=param_dict["PQ_tot"],
            h_stroma=param_dict["h_stroma"],
            Atot=param_dict["Atot"],
            nPSI=param_dict["nPSI"],
        ),
        args=(param_dict,),
        bounds=(bounds_low, bounds_high),
        method="trf",
        xtol=1e-8
    )
    
    pointer = {
        "qactive": 0,
        "pqox": 1,
        "psiox": 2,
        "hlumen": 3,
        "atp": 4,
    }
    
    return np.real(res.x[pointer[extract_str]])

def initials(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float):
    PQ_ox_stst = PQ_tot / 2
    h_lumen_stst = h_stroma * 10
    qactive_stst = 0.5
    atp_stst = Atot / 2
    psi_ox_stst = nPSI / 2
    
    return qactive_stst, PQ_ox_stst, psi_ox_stst, h_lumen_stst, atp_stst

def initial_qactive(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float, stoic_PSII: float, NPQ_max: float, bH: float, V_stroma: float, V_lumen: float, k1p: float, k1m: float, k2p: float, k2m: float, k3: float, K_NPQ: float, n_NPQ: float, k4: float, k5: float, cEqP: float, k6: float, k7: float, pfd: float, k_X: float, L_PSI: float, stoic_PSI: float, sigma_PSI: float, N_A: float) -> float:
    
    param_dict = {
        "PQ_tot": PQ_tot,
        "h_stroma": h_stroma,
        "Atot": Atot,
        "nPSI": nPSI,
        "stoic_PSII": stoic_PSII,
        "NPQ_max": NPQ_max,
        "bH": bH,
        "V_stroma": V_stroma,
        "V_lumen": V_lumen,
        "k1p": k1p,
        "k1m": k1m,
        "k2p": k2p,
        "k2m": k2m,
        "k3": k3,
        "K_NPQ": K_NPQ,
        "n_NPQ": n_NPQ,
        "k4": k4,
        "k5": k5,
        "cEqP": cEqP,
        "k6": k6,
        "k7": k7,
        "pfd": pfd,
        "k_X": k_X,
        "L_PSI": L_PSI,
        "stoic_PSI": stoic_PSI,
        "sigma_PSI": sigma_PSI,
        "N_A": N_A,
    }
    
    return initial_combined("qactive", param_dict)

def initial_pqox(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float, stoic_PSII: float, NPQ_max: float, bH: float, V_stroma: float, V_lumen: float, k1p: float, k1m: float, k2p: float, k2m: float, k3: float, K_NPQ: float, n_NPQ: float, k4: float, k5: float, cEqP: float, k6: float, k7: float, pfd: float, k_X: float, L_PSI: float, stoic_PSI: float, sigma_PSI: float, N_A: float) -> float:
    
    param_dict = {
        "PQ_tot": PQ_tot,
        "h_stroma": h_stroma,
        "Atot": Atot,
        "nPSI": nPSI,
        "stoic_PSII": stoic_PSII,
        "NPQ_max": NPQ_max,
        "bH": bH,
        "V_stroma": V_stroma,
        "V_lumen": V_lumen,
        "k1p": k1p,
        "k1m": k1m,
        "k2p": k2p,
        "k2m": k2m,
        "k3": k3,
        "K_NPQ": K_NPQ,
        "n_NPQ": n_NPQ,
        "k4": k4,
        "k5": k5,
        "cEqP": cEqP,
        "k6": k6,
        "k7": k7,
        "pfd": pfd,
        "k_X": k_X,
        "L_PSI": L_PSI,
        "stoic_PSI": stoic_PSI,
        "sigma_PSI": sigma_PSI,
        "N_A": N_A,
    }
    
    return initial_combined("pqox", param_dict)

def initial_psiox(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float, stoic_PSII: float, NPQ_max: float, bH: float, V_stroma: float, V_lumen: float, k1p: float, k1m: float, k2p: float, k2m: float, k3: float, K_NPQ: float, n_NPQ: float, k4: float, k5: float, cEqP: float, k6: float, k7: float, pfd: float, k_X: float, L_PSI: float, stoic_PSI: float, sigma_PSI: float, N_A: float) -> float:
    
    param_dict = {
        "PQ_tot": PQ_tot,
        "h_stroma": h_stroma,
        "Atot": Atot,
        "nPSI": nPSI,
        "stoic_PSII": stoic_PSII,
        "NPQ_max": NPQ_max,
        "bH": bH,
        "V_stroma": V_stroma,
        "V_lumen": V_lumen,
        "k1p": k1p,
        "k1m": k1m,
        "k2p": k2p,
        "k2m": k2m,
        "k3": k3,
        "K_NPQ": K_NPQ,
        "n_NPQ": n_NPQ,
        "k4": k4,
        "k5": k5,
        "cEqP": cEqP,
        "k6": k6,
        "k7": k7,
        "pfd": pfd,
        "k_X": k_X,
        "L_PSI": L_PSI,
        "stoic_PSI": stoic_PSI,
        "sigma_PSI": sigma_PSI,
        "N_A": N_A,
    }
    
    return initial_combined("psiox", param_dict)

def initial_hlumen(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float, stoic_PSII: float, NPQ_max: float, bH: float, V_stroma: float, V_lumen: float, k1p: float, k1m: float, k2p: float, k2m: float, k3: float, K_NPQ: float, n_NPQ: float, k4: float, k5: float, cEqP: float, k6: float, k7: float, pfd: float, k_X: float, L_PSI: float, stoic_PSI: float, sigma_PSI: float, N_A: float) -> float:
    
    param_dict = {
        "PQ_tot": PQ_tot,
        "h_stroma": h_stroma,
        "Atot": Atot,
        "nPSI": nPSI,
        "stoic_PSII": stoic_PSII,
        "NPQ_max": NPQ_max,
        "bH": bH,
        "V_stroma": V_stroma,
        "V_lumen": V_lumen,
        "k1p": k1p,
        "k1m": k1m,
        "k2p": k2p,
        "k2m": k2m,
        "k3": k3,
        "K_NPQ": K_NPQ,
        "n_NPQ": n_NPQ,
        "k4": k4,
        "k5": k5,
        "cEqP": cEqP,
        "k6": k6,
        "k7": k7,
        "pfd": pfd,
        "k_X": k_X,
        "L_PSI": L_PSI,
        "stoic_PSI": stoic_PSI,
        "sigma_PSI": sigma_PSI,
        "N_A": N_A,
    }
    
    return initial_combined("hlumen", param_dict)

def initial_atp(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float, stoic_PSII: float, NPQ_max: float, bH: float, V_stroma: float, V_lumen: float, k1p: float, k1m: float, k2p: float, k2m: float, k3: float, K_NPQ: float, n_NPQ: float, k4: float, k5: float, cEqP: float, k6: float, k7: float, pfd: float, k_X: float, L_PSI: float, stoic_PSI: float, sigma_PSI: float, N_A: float) -> float:
    
    param_dict = {
        "PQ_tot": PQ_tot,
        "h_stroma": h_stroma,
        "Atot": Atot,
        "nPSI": nPSI,
        "stoic_PSII": stoic_PSII,
        "NPQ_max": NPQ_max,
        "bH": bH,
        "V_stroma": V_stroma,
        "V_lumen": V_lumen,
        "k1p": k1p,
        "k1m": k1m,
        "k2p": k2p,
        "k2m": k2m,
        "k3": k3,
        "K_NPQ": K_NPQ,
        "n_NPQ": n_NPQ,
        "k4": k4,
        "k5": k5,
        "cEqP": cEqP,
        "k6": k6,
        "k7": k7,
        "pfd": pfd,
        "k_X": k_X,
        "L_PSI": L_PSI,
        "stoic_PSI": stoic_PSI,
        "sigma_PSI": sigma_PSI,
        "N_A": N_A,
    }
    
    return initial_combined("atp", param_dict)


def Fuente2024() -> Model:
    m = Model()

    m.add_parameters(
        {
            "stoic_PSII": 1,
            "stoic_PSI": 1,
            "PQ_tot": 7,
            "H_stroma": 0.015848931924611134,
            "AP_tot": 1000,
            "V_lumen": 2.62e-21,
            "V_stroma": 2.09e-20,
            "sigma_PSI_0": 1,
            "k1p": 25000,
            "k1m": 2500,
            "k2p": 100,
            "k2m": 10,
            "k3": 0.05,
            "k4": 0.004,
            "k5": 100,
            "k6": 10,
            "k7": 500,
            "k_X": 1,
            "L_PSI": 10000,
            "bH": 0.01,
            "NPQ_max": 0.6,
            "cEqP": 4.3e-08,
            "keq_NPQ": 1,
            "n_NPQ": 5.3,
            "N_A": 6.02214076e+17,
            "PPFD": 50,
            "PPFD_add": 0,
            "f": 1,
            "PSI_total": 1,
            "Fluo_0": 0.25,
            "Q_total": 1,
        }
    )

    m.add_variables(
        {
            "Q_active": InitialAssignment(fn=initial_qactive, args=['PQ_tot', 'H_stroma', 'AP_tot', 'PSI_total', 'stoic_PSII', 'NPQ_max', 'bH', 'V_stroma', 'V_lumen', 'k1p', 'k1m', 'k2p', 'k2m', 'k3', 'keq_NPQ', 'n_NPQ', 'k4', 'k5', 'cEqP', 'k6', 'k7', 'PPFD', 'k_X', 'L_PSI', 'stoic_PSI', 'sigma_PSI_0', 'N_A'], unit="REPLACE"),
            "PQ": InitialAssignment(fn=initial_pqox, args=['PQ_tot', 'H_stroma', 'AP_tot', 'PSI_total', 'stoic_PSII', 'NPQ_max', 'bH', 'V_stroma', 'V_lumen', 'k1p', 'k1m', 'k2p', 'k2m', 'k3', 'keq_NPQ', 'n_NPQ', 'k4', 'k5', 'cEqP', 'k6', 'k7', 'PPFD', 'k_X', 'L_PSI', 'stoic_PSI', 'sigma_PSI_0', 'N_A'], unit="REPLACE"),
            "PSI_ox": InitialAssignment(fn=initial_psiox, args=['PQ_tot', 'H_stroma', 'AP_tot', 'PSI_total', 'stoic_PSII', 'NPQ_max', 'bH', 'V_stroma', 'V_lumen', 'k1p', 'k1m', 'k2p', 'k2m', 'k3', 'keq_NPQ', 'n_NPQ', 'k4', 'k5', 'cEqP', 'k6', 'k7', 'PPFD', 'k_X', 'L_PSI', 'stoic_PSI', 'sigma_PSI_0', 'N_A'], unit="REPLACE"),
            "H_lumen": InitialAssignment(fn=initial_hlumen, args=['PQ_tot', 'H_stroma', 'AP_tot', 'PSI_total', 'stoic_PSII', 'NPQ_max', 'bH', 'V_stroma', 'V_lumen', 'k1p', 'k1m', 'k2p', 'k2m', 'k3', 'keq_NPQ', 'n_NPQ', 'k4', 'k5', 'cEqP', 'k6', 'k7', 'PPFD', 'k_X', 'L_PSI', 'stoic_PSI', 'sigma_PSI_0', 'N_A'], unit="REPLACE"),
            "ATP_st": InitialAssignment(fn=initial_atp, args=['PQ_tot', 'H_stroma', 'AP_tot', 'PSI_total', 'stoic_PSII', 'NPQ_max', 'bH', 'V_stroma', 'V_lumen', 'k1p', 'k1m', 'k2p', 'k2m', 'k3', 'keq_NPQ', 'n_NPQ', 'k4', 'k5', 'cEqP', 'k6', 'k7', 'PPFD', 'k_X', 'L_PSI', 'stoic_PSI', 'sigma_PSI_0', 'N_A'], unit="REPLACE"),
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m