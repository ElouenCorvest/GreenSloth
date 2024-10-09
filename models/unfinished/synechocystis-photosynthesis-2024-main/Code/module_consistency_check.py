#!/usr/bin/env python

import numpy as np
import pandas as pd


def check_concentrations(time, *concentrations):
    if np.any(time > 0):
        return 1
    else:
        negconcs = pd.Series(concentrations) < 0
        if negconcs.any():
            raise ValueError(f"{negconcs.sum()} Concentration(s) is/are below 0")
        else:
            return 1


def add_consistency_check(m):
    # Get the concentrations to check for non-negativity
    compounds = m.compounds
    concentrations = compounds + [
        "Hi_mol",
        "Ho_mol",
        "light_ps1",
        "light_ps2",
        "light_ps1_ML",
        "light_ps2_ML",
        "light_ps1_tot",
        "light_ps2_tot",
        "Q_red",
        "PC_red",
        "Fd_red",
        "NADP",
        "NAD",
        "ADP",
        "PSIIq",
    ]
    concentrations = np.array(concentrations)
    concentrations = concentrations[np.in1d(concentrations, m.get_all_compounds())]

    # Add consistency checks as algebraic modules
    m.add_algebraic_module_from_args(
        module_name="_check_concentrations",
        function=check_concentrations,
        derived_compounds=["_check_concentrations"],
        args=np.concatenate((["time"], concentrations)),
    )

    return m
