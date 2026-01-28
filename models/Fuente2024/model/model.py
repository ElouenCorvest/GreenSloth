from collections.abc import Callable, Iterable
import numpy as np
from mxlpy import Derived, InitialAssignment, Model, Parameter, Variable, units, Simulator
from scipy.optimize import fsolve, root, minimize, least_squares
from sympy.physics.units.quantities import Quantity

import mxlbricks.names as n
from mxlbricks.fns import mass_action_1s, moiety_1, value


def _osc_light(pfd: float, pfd_add: float, f: float, time: float) -> float:
    return pfd + pfd_add * np.cos(2 * np.pi * f * time)

def _sigma_PSII(NPQ_max: float, Q_active: float) -> float:
    return 1 - NPQ_max * Q_active

def _v_PSII(stoic_PSII: float, sigma_PSII: float, light: float, RCII_closed: float) -> float:
    return stoic_PSII * sigma_PSII * light * (1 - RCII_closed)

def _v_PSI(stoic_PSI: float, sigma_PSI: float, light: float, PSI_ox: float, L_PSI: float) -> float:
    return stoic_PSI * sigma_PSI * L_PSI * light / (L_PSI + light) * (stoic_PSI - PSI_ox)

def _v1(k1p: float, RCII_closed: float, PQ_ox: float, k1m: float, RCII_open: float, PQ_red: float) -> float:
    return k1p * RCII_closed * PQ_ox - (k1m * RCII_open * PQ_red)

def _v2(k2p: float, PQ_red: float, PSI_ox: float, k2m: float, PQ_ox: float, PSI_red: float) -> float:
    return k2p * PQ_red * PSI_ox - k2m * PQ_ox * PSI_red

def _v3(k3: float, h_lumen: float, Q_active: float, K_NPQ: float, n: float) -> float:
    return k3 * (1 - Q_active) / (1 + (K_NPQ / h_lumen)**n)

def _v5(k5: float, ADP: float, ATP: float, H_stroma: float, H_lumen: float, cEqP: float) -> float:
    return k5 * (ADP - ATP * (H_stroma / H_lumen)**(14/3) / cEqP)

def _v7(k7: float, H_lumen: float, H_stroma: float) -> float:
    return k7 * (H_lumen - H_stroma)

def _rcii_closed(k1p: float, PQ_ox: float, sigma_PSII: float, light: float, k1m: float, PQ_red: float) -> float:
    top = 1
    bottom = 1 + k1p * PQ_ox / (sigma_PSII * light + k1m * PQ_red)
    return top / bottom

def _rcii_open(k1p: float, PQ_ox: float, sigma_PSII: float, k1m: float, PQ_red: float) -> float:
    return k1p * PQ_ox / ((sigma_PSII + k1m * PQ_red) + k1p * PQ_ox)

def _flourescence(Fluo_0: float, RCII_closed: float, sigma_PSII: float) -> float:
    return Fluo_0 + RCII_closed * sigma_PSII

def _npq(npq_max: float, q_active: float):
    return npq_max * q_active /(1 - npq_max * q_active)

def _o2(nPSII: float, k1p: float, RCIIclosed: float, PQ: float, k1m: float, PQ_red: float):
    return (nPSII * ( k1p * RCIIclosed * PQ - k1m * (1 - RCIIclosed) * PQ_red))/4

def x_div_yz(x: float, y: float, z: float) -> float:
    return x / (y * z)

def proton_generation(V_stroma: float, V_lumen: float, bH: float) -> float:
    return -14/3 * V_stroma / V_lumen * bH

def half(x: float) -> float:
    return x / 2

def times_ten(x: float) -> float:
    return x * 10

def initials(PQ_tot: float, h_stroma: float, Atot: float, nPSI: float):
    PQ_ox_stst = PQ_tot / 2
    h_lumen_stst = h_stroma * 10
    qactive_stst = 0.5
    atp_stst = Atot / 2
    psi_ox_stst = nPSI / 2
    
    return qactive_stst, PQ_ox_stst, psi_ox_stst, h_lumen_stst, atp_stst

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

def get_fuente2024() -> Model:
    
    model = Model()
    
    model.add_variables({
        n.quencher("_active"): Variable(
            InitialAssignment(
                fn=initial_qactive,
                args=[n.total_pq(), n.h("_stroma"), n.total_adenosines(), n.ps1("_total"), "stoic_PSII", "NPQ_max", "bH", "V_stroma", "V_lumen", "k1p", "k1m", "k2p", "k2m", "k3", n.keq("NPQ"), "n_NPQ", "k4", "k5", "cEqP", "k6", "k7", n.pfd(), "k_X", "L_PSI", "stoic_PSI", "sigma_PSI_0", "N_A"]
            )
        ),
        n.pq_ox(): Variable(
            InitialAssignment(
                fn=initial_pqox,
                args=[n.total_pq(), n.h("_stroma"), n.total_adenosines(), n.ps1("_total"), "stoic_PSII", "NPQ_max", "bH", "V_stroma", "V_lumen", "k1p", "k1m", "k2p", "k2m", "k3", n.keq("NPQ"), "n_NPQ", "k4", "k5", "cEqP", "k6", "k7", n.pfd(), "k_X", "L_PSI", "stoic_PSI", "sigma_PSI_0", "N_A"]
            )
        ),
        n.ps1("_ox"): Variable(
            InitialAssignment(
                fn=initial_psiox,
                args=[n.total_pq(), n.h("_stroma"), n.total_adenosines(), n.ps1("_total"), "stoic_PSII", "NPQ_max", "bH", "V_stroma", "V_lumen", "k1p", "k1m", "k2p", "k2m", "k3", n.keq("NPQ"), "n_NPQ", "k4", "k5", "cEqP", "k6", "k7", n.pfd(), "k_X", "L_PSI", "stoic_PSI", "sigma_PSI_0", "N_A"]
            )
        ),
        n.h("_lumen"): Variable(
            InitialAssignment(
                fn=initial_hlumen,
                args=[n.total_pq(), n.h("_stroma"), n.total_adenosines(), n.ps1("_total"), "stoic_PSII", "NPQ_max", "bH", "V_stroma", "V_lumen", "k1p", "k1m", "k2p", "k2m", "k3", n.keq("NPQ"), "n_NPQ", "k4", "k5", "cEqP", "k6", "k7", n.pfd(), "k_X", "L_PSI", "stoic_PSI", "sigma_PSI_0", "N_A"]
            )
        ),
        n.atp("_stroma"): Variable(
            InitialAssignment(
                fn=initial_atp,
                args=[n.total_pq(), n.h("_stroma"), n.total_adenosines(), n.ps1("_total"), "stoic_PSII", "NPQ_max", "bH", "V_stroma", "V_lumen", "k1p", "k1m", "k2p", "k2m", "k3", n.keq("NPQ"), "n_NPQ", "k4", "k5", "cEqP", "k6", "k7", n.pfd(), "k_X", "L_PSI", "stoic_PSI", "sigma_PSI_0", "N_A"]
            )
        ),
    })
    
    model.add_parameters({
        "stoic_PSII": Parameter(
            1,
            unit=units.dimensionless,
        ),
        "stoic_PSI": Parameter(
            1,
            unit=units.dimensionless,
        ),
        n.total_pq(): Parameter(
            7,
            unit=units.dimensionless,
        ),
        n.h("_stroma"): Parameter(
            10**(-1.8),
            unit=units.mumol / units.liter,
        ),
        n.total_adenosines(): Parameter(
            1000,
            unit=units.mumol / units.liter,
        ),
        "V_lumen": Parameter(
            2.62e-21,
            unit=units.liter / Quantity("PSU"),
        ),
        "V_stroma": Parameter(
            2.09e-20,
            unit=units.liter / Quantity("PSU"),
        ),
        "sigma_PSI_0": Parameter(
            1,
        ),
        "k1p": Parameter(
            25000,
            unit=units.per_second,
        ),
        "k1m": Parameter(
            2500,
            unit=units.per_second,
        ),
        "k2p": Parameter(
            100,
            unit=units.per_second,
        ),
        "k2m": Parameter(
            10,
            unit=units.per_second,
        ),
        "k3": Parameter(
            0.05,
            unit=units.per_second,
        ),
        "k4": Parameter(
            0.004,
            unit=units.per_second,
        ),
        "k5": Parameter(
            100,
            unit=units.per_second,
        ),
        "k6": Parameter(
            10,
            unit=units.per_second,
        ),
        "k7": Parameter(
            500,
            unit=units.per_second,
        ),
        "k_X": Parameter(
            1,
            unit=units.per_second,
        ),
        "L_PSI": Parameter(
            10000,
            unit=units.mumol * units.sqm**-1 * units.per_second,
        ),
        "bH": Parameter(
            0.01,
            unit=units.dimensionless,
        ),
        "NPQ_max": Parameter(
            0.6,
            unit=units.dimensionless,
        ),
        "cEqP": Parameter(
            4.3e-8,
            unit=units.dimensionless,
        ),
        n.keq("NPQ"): Parameter(
            1,
            unit=units.mumol / units.liter,
        ),
        "n_NPQ": Parameter(
            5.3,
            unit=units.dimensionless,
        ),
        "N_A": Parameter(
            6.02214076 * 10**17,
            unit=units.mumol**-1,
        ),
        n.pfd(): Parameter(
            50,
            unit=units.mumol * units.sqm**-1 * units.per_second,
        ),
        n.pfd("_add"): Parameter(
            0,
            unit=units.mumol * units.sqm**-1 * units.per_second,
        ),
        "f": Parameter(
            1,
            unit=units.hertz,
        ),
        n.ps1("_total"): Parameter(
            1,
            unit=units.dimensionless,
        ),
        "Fluo_0": Parameter(
            0.25,
            unit=units.dimensionless,
        ),
        n.quencher("_total"): Parameter(
            1,
            unit=units.dimensionless,
        ),
    })
    
    # Derived
    
    model.add_derived(
        name=n.quencher("_inactive"),
        fn=moiety_1,
        args=[n.quencher("_active"), n.quencher("_total")],
    )
    
    model.add_derived(
        name=n.pq_red(),
        fn=moiety_1,
        args=[n.pq_ox(), n.total_pq()],
    )
    
    model.add_derived(
        name=n.ps1("_red"),
        fn=moiety_1,
        args=[n.ps1("_ox"), n.ps1("_total")],
    )
    
    model.add_derived(
        name=n.adp("_stroma"),
        fn=moiety_1,
        args=[n.atp("_stroma"), n.total_adenosines()],
    )
    
    model.add_derived(
        name="osc_light",
        fn=_osc_light,
        args=[n.pfd(), n.pfd("_add"), "f", "time"],
    )
    
    model.add_derived(
        name="sigma_PSII",
        fn=_sigma_PSII,
        args=["NPQ_max", n.quencher("_active")],
    )
    
    model.add_derived(
        name="RCII_closed",
        fn=_rcii_closed,
        args=["k1p", n.pq_ox(), "sigma_PSII", "osc_light", "k1m", n.pq_red()],
    )
    
    model.add_derived(
        name="RCII_open",
        fn=_rcii_open,
        args=["k1p", n.pq_ox(), "sigma_PSII", "k1m", n.pq_red()],
    )
    
    # Readouts
    
    model.add_derived(
        name=n.fluorescence(),
        fn=_flourescence,
        args=["Fluo_0", "RCII_closed", "sigma_PSII"],
    )
    
    model.add_derived(
        name="NPQ",
        fn=_npq,
        args=["NPQ_max", n.quencher("_active")]
    )
    
    model.add_derived(
        name=n.o2(),
        fn=_o2,
        args=[n.ps1("_total"), "k1p", "RCII_closed", n.pq_ox(), "k1m", n.pq_red()]
    )
    
    # Rates
    
    model.add_reaction(
        name="v_PSII",
        fn=_v_PSII,
        args=["stoic_PSII", "sigma_PSII", "osc_light", "RCII_closed"],
        stoichiometry={
            n.h("_lumen"): Derived(fn=x_div_yz, args=["bH", "V_lumen", "N_A"]),
        }
    )
    
    model.add_reaction(
        name="v_PSI",
        fn=_v_PSI,
        args=["stoic_PSI", "sigma_PSI_0", "osc_light", n.ps1("_ox"), "L_PSI"],
        stoichiometry={
            n.ps1("_ox"): 1,
        }
    )
    
    model.add_reaction(
        name="v1",
        fn=_v1,
        args=["k1p", "RCII_closed", n.pq_ox(), "k1m", "RCII_open", n.pq_red()],
        stoichiometry={
            n.pq_ox(): -1/2,
        }
    )
    
    model.add_reaction(
        name="v2",
        fn=_v2,
        args=["k2p", n.pq_red(), n.ps1("_ox"), "k2m", n.pq_ox(), n.ps1("_red")],
        stoichiometry={
            n.pq_ox(): 1/2,
            n.ps1("_ox"): -1,
            n.h("_lumen"): Derived(fn=x_div_yz, args=["bH", "V_lumen", "N_A"]),
        }
    )
    
    model.add_reaction(
        name="v3",
        fn=_v3,
        args=["k3", n.h("_lumen"), n.quencher("_active"), n.keq("NPQ"), "n_NPQ"],
        stoichiometry={
            n.quencher("_active"): 1,
        }
    )
    
    model.add_reaction(
        name="v4",
        fn=mass_action_1s,
        args=[n.quencher("_active"), "k4"],
        stoichiometry={
            n.quencher("_active"): -1,
        }
    )
    
    model.add_reaction(
        name="v5",
        fn=_v5,
        args=["k5", n.adp("_stroma"), n.atp("_stroma"), n.h("_stroma"), n.h("_lumen"), "cEqP"],
        stoichiometry={
            n.atp("_stroma"): 1,
            n.h("_lumen"): Derived(fn=proton_generation, args=["V_stroma", "V_lumen", "bH"]),
        }
    )

    model.add_reaction(
        name="v6",
        fn=mass_action_1s,
        args=[n.atp("_stroma"), "k6"],
        stoichiometry={
            n.atp("_stroma"): -1,
        }
    )
    
    model.add_reaction(
        name="v7",
        fn=_v7,
        args=["k7", n.h("_lumen"), n.h("_stroma")],
        stoichiometry={
            n.h("_lumen"): -1
        }
    )
    
    model.add_reaction(
        name="v_X",
        fn=mass_action_1s,
        args=[n.pq_red(), "k_X"],
        stoichiometry={
            n.pq_ox(): 1,
        }
    )
    
    return model
