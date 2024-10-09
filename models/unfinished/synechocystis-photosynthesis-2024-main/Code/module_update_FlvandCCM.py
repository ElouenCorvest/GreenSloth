#!/usr/bin/env python

import numpy as np
import parameters
from modelbase.ode import ratefunctions as rf

# CHANGE LOG
# 017 23.12.2022 | moved Flv and CCM updates to module_update_FlvandCCM
# 017 06.03.2023 | switched parameters to import from parameters.py

# Define the updated Flv description
def vFlv(Fd_red, O2, Ho, k_O2, KHillFdred, nHillFdred):
    """electron flow from Fd to O2 via Flv1/3-Heterodimere"""
    return k_O2 * O2 * Ho * rf.hill(S=Fd_red, vmax=1, kd=KHillFdred, n=nHillFdred)


# Define the updated CCM description including
# functions for solubility and partitioning
def CO2pK1(T, S):  # [unitless] MojicaPrieto2002
    return (
        -43.6977
        - 0.0129037 * S
        + 1.364e-4 * S**2
        + 2885.378 / T
        + 7.045159 * np.log(T)
    )


def CO2KHenry(T, S):  # [mol l^-1 atm^-1] König2019
    return np.exp(
        -58.0931
        + 90.5069 * 100 / T
        + 22.2940 * np.log(T / 100)
        + S * (0.027766 - 0.025888 * T / 100 + 0.0050578 * (T / 100) ** 2)
    )


def CO2sol(T, S, CO2pp):  # [mol l^-1]
    return CO2KHenry(T, S) * CO2pp


def CO2aq(CO2dissolved, Ho, K):  # [mol l^-1]
    return CO2dissolved * Ho / (Ho + K)


def vCCM(CO2, Ho, CO2ext_pp, kCCM, fCin, T, S, cChl):
    """
    exchange of CO2 with the environment, viewed in inward direction
    raises the total cellular CO2 concentration to the maximum allowed by external concentration or solubility
    assumes a constant external CO2 concentration
    """
    # Converssion factor mol l^-1 -> mmol mol(Chl)^-1
    perChl = 1 / cChl * 1e3

    # Assume the CCM-increased partial pressure within the cell
    CO2pp = CO2ext_pp * fCin

    # Calculate the CO2 equilibrium constant
    K1 = 10 ** (-CO2pK1(T, S)) * perChl  # [mmol mol(Chl)]

    # Calculate the maximally achievable CO2aq concentration
    CO2dissolved = CO2sol(T, S, CO2pp)
    CO2aq_max = CO2aq(CO2dissolved, Ho, K1) * perChl  # [mmol mol(Chl)]

    return kCCM * (CO2aq_max - CO2)


# Define the update adding functions
def update_Flv_hill(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating Flv to hill")

    # Remove the old description
    m.remove_reactions(["vFlv", "vFlvactivation"])
    m.remove_parameters(["k_O2", "kFlvactivation", "kFlvdeactivation"])
    m.remove_compound("Flva")

    p_list = ["KHillFdred", "nHillFdred", "k_O2"]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    # Add the updated description
    m.add_reaction_from_args(
        rate_name="vFlv",
        function=vFlv,
        stoichiometry={
            "Fd_ox": 4,
            "O2": -1,
            "Ho": -4 / m.get_parameter("bHo"),
        },
        args=["Fd_red", "O2", "Ho", "k_O2", "KHillFdred", "nHillFdred"],
        reversible=False,
    )
    return m, y0


def update_CCM(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating CCM to pH dependency")

    # Remove old definition
    m.remove_reaction("vCCM")

    # Add new parameters
    p_list = [
        "CO2ext_pp",
        "cChl",
        "S",
    ]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}
    m.add_parameters(p)

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.update_parameter("fCin", parameters.pu["fCin"])

    y0["CO2"] = parameters.y0u["CO2"]

    m.add_reaction_from_args(
        rate_name="vCCM",
        function=vCCM,
        stoichiometry={"CO2": 1},
        args=["CO2", "Ho", "CO2ext_pp", "kCCM", "fCin", "T", "S", "cChl"],
        reversible=True,
    )

    return m, y0
