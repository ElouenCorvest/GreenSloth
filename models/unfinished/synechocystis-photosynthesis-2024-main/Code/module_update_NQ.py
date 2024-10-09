#!/usr/bin/env python

import numpy as np
import parameters
from modelbase.ode import ratefunctions as rf


def vNQ_MM(Q_ox, Fd_red, vNQ_max, KMNQ_Qox, KMNQ_Fdred):
    return (
        vNQ_max
        * rf.michaelis_menten(Q_ox, 1, KMNQ_Qox)
        * rf.michaelis_menten(Fd_red, 1, KMNQ_Fdred)
    )


def update_NQ_MM(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating NQ to Michaelis Menten")

    # Remove the old description
    m.remove_reactions(["vNQ"])
    m.remove_parameters(["k_NQ"])

    p_list = ["vNQ_max", "KMNQ_Qox", "KMNQ_Fdred"]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    # Add the new description
    m.add_reaction_from_args(
        rate_name="vNQ",
        function=vNQ_MM,
        stoichiometry={
            "Fd_ox": 2,
            "Q_ox": -1,
            "Hi": 1 / m.get_parameter("bHi"),
            "Ho": -3 / m.get_parameter("bHo"),
        },
        args=["Q_ox", "Fd_red", "vNQ_max", "KMNQ_Qox", "KMNQ_Fdred"],
        reversible=False,
    )
    return m, y0
