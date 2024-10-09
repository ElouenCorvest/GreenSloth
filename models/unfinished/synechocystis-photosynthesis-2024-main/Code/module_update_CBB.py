#!/usr/bin/env python

import numpy as np
import parameters
from modelbase.ode import ratefunctions as rf

# CHANGE LOG
# 017 24.03.2023 | moved CBB updates to module_update_CBB

# Define the updated description
def CBBactivation(CBBa, Fd_red, kCBBactivation, KMFdred):
    return kCBBactivation * (rf.michaelis_menten(S=Fd_red, vmax=1, km=KMFdred) - CBBa)


def update_CBBactivation_MM(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating CBB to Michaelis Menten")

    # Remove the old description
    m.remove_reactions(["vCBBactivation"])
    m.remove_parameters(["kCBBactivation", "kCBBdeactivation"])

    p_list = ["kCBBactivation", "KMFdred"]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    # Add the new description
    m.add_reaction_from_args(
        rate_name="vCBBactivation",
        function=CBBactivation,
        stoichiometry={"CBBa": 1},
        args=["CBBa", "Fd_red", "kCBBactivation", "KMFdred"],
        reversible=True,
    )
    return m, y0


# Define the updated description with Hill kinetics
def CBBactivation_hill(CBBa, Fd_red, kCBBactivation, KHillFdred_CBB, nHillFdred_CBB):
    return kCBBactivation * (
        rf.hill(S=Fd_red, vmax=1, kd=KHillFdred_CBB, n=nHillFdred_CBB) - CBBa
    )


def update_CBBactivation_hill(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating CBB to hill")

    # Remove the old description
    m.remove_reactions(["vCBBactivation"])
    m.remove_parameters(["kCBBactivation", "kCBBdeactivation"])

    p_list = ["KHillFdred_CBB", "nHillFdred_CBB", "kCBBactivation"]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}
    # p = {
    #     'KHillFdred_CBB': 1.000e-04, # [mmol^nHillFdred_CBB mol(Chl)^-nHillFdred_CBB] Michaelis constant of CBB activation by reduced ferredoxin (Schuurmans2014)
    #     'nHillFdred_CBB': 4.000, # [unitless] Hill constant of Fd_red binding to CBB enzymes, e.g. PGK (guess)
    #     "kCBBactivation": 3.466e-02,  # [s^-1] rate constant of CBB activation by reduced ferredoxin (Nikkanen2020)
    # }

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    # Add the new description
    m.add_reaction_from_args(
        rate_name="vCBBactivation",
        function=CBBactivation_hill,
        stoichiometry={"CBBa": 1},
        args=["CBBa", "Fd_red", "kCBBactivation", "KHillFdred_CBB", "nHillFdred_CBB"],
        reversible=True,
    )
    return m, y0
