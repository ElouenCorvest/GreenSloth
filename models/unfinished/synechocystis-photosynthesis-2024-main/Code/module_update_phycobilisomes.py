#!/usr/bin/env python

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import simpson
import parameters

# CHANGE LOG
# 017 26.09.2022 | moved ocp description to module_update_phycobilisomes
#                | split variable pbs and ocp addition into different functions
#     04.11.2022 | adapted to the models new light handling
#                | removed unnecessary parameter replacement and model updates
#     14.11.2022 | Added OCP activation reaction and further effects on light_PSX_ML and fluorescence_pbs
#     12.01.2023 | Added OCP quenching maximum
#     06.03.2023 | switched parameters to import from parameters.py


_data_Path = Path(__file__).parent / "data/"

# Define the fraction of free PBS as a derived variable
def PBS_free(PBS_PS1, PBS_PS2):
    return 1 - PBS_PS1 - PBS_PS2


# Add OCP activation
def OCP_absorbed_light(
    pfd: pd.Series,
) -> float:  # >> changed: finalised light absorption calculation <<
    return _OCPabsorption.mul(pfd, axis=0).apply(simpson).to_numpy()


# Define OCP activation as active, light involved process with passive reversal
def OCPactivation(
    OCP, pfd, kOCPactivation, kOCPdeactivation, lcf, OCPmax=1
):  # >> changed: added <<
    return (
        OCP_absorbed_light(pfd) * lcf * kOCPactivation * (OCPmax - OCP)
        - kOCPdeactivation * OCP
    )


# Add OCP effect on light absorption
def ps_normabsorption_ocp(time, PBS_PS1, PBS_PS2, OCP, complex_abs, PSItot, PSIItot, lcf):
    light_ps1 = (complex_abs["ps1"] + complex_abs["pbs"] * PBS_PS1 * (1 - OCP)) / PSItot
    light_ps2 = (
        complex_abs["ps2"] + complex_abs["pbs"] * PBS_PS2 * (1 - OCP)
    ) / PSIItot

    if isinstance(light_ps2, float) and isinstance(
        time, np.ndarray
    ):  # >> changed: added <<
        light_ps1 = np.repeat(light_ps1, len(time))
        light_ps2 = np.repeat(light_ps2, len(time))

    return light_ps1 * lcf, light_ps2 * lcf  # Get float values


# Add OCP effect on pbs fluorescence
def fluorescence_pbs_ocp(
    OCP, PBS_free, complex_abs_ML, fluo_influence, lcf
):  # >> changed: added <<
    return PBS_free * complex_abs_ML["pbs"] * fluo_influence["PBS"] * (1 - OCP) * lcf


# Update a model with static pbs treatment to variable PBS in light absorption
def update_variable_PBS(m, y0={}, init_param=None, verbose=True):
    ## Update the model ##
    if verbose:
        print("updating PBS to dynamic representation")

    # Replace the static parameter description
    PBS_PS1, PBS_PS2 = m.get_parameter("PBS_PS1"), m.get_parameter("PBS_PS2")
    m.remove_parameters(["PBS_PS1", "PBS_PS2", "PBS_free"])

    # Add the fractions of PBS attached to the photosystems as compounds
    m.add_compounds(["PBS_PS1", "PBS_PS2"])

    y0.update({"PBS_PS1": PBS_PS1 - 1e-5, "PBS_PS2": PBS_PS2 - 1e-5})

    # Add the fraction of free PBS as a derived variable
    m.add_algebraic_module_from_args(
        module_name="PBS_free",
        function=PBS_free,
        args=["PBS_PS1", "PBS_PS2"],
        derived_compounds=["PBS_free"],
    )

    # # Re-add pbs fluorescence to allow for correct sorting
    # to_readd = [
    #     k
    #     for k, v in m.algebraic_modules.items()
    #     if np.any([x in v["args"] for x in ["PBS_PS1", "PBS_PS2", "PBS_free"]])
    # ]
    # for module in to_readd:
    #     m.update_algebraic_module_from_args(
    #         module_name=module, args=m.get_algebraic_module_args(module)
    #     )

    # m.remove_algebraic_module("fluorescence_pbs")
    # def fluorescence_pbs(PBS_free, complex_abs_ML, fluo_influence):
    #     return PBS_free * complex_abs_ML["pbs"] * fluo_influence["PBS"]
    # m.add_algebraic_module_from_args(
    #     module_name="fluorescence_pbs",
    #     function=fluorescence_pbs,
    #     args=["PBS_free", "complex_abs_ML", "fluo_influence"],
    #     derived_compounds=["FPBS"],
    # )

    return m, y0


# Add OCP functionality
# Restricted to reducing PBS excitation
# Updates model with static or variable PBS
_OCPabsorption = pd.read_csv(_data_Path / "OCP_absorption.csv", index_col=0)


def add_OCP(m, y0={}, init_param=None, verbose=True):
    if verbose:
        print("updating light representation with OCP")

    # Add OCP as compound
    m.add_compound("OCP")

    y0["OCP"] = parameters.y0u["OCP"]

    # Add the new parameters
    p_list = [  # >> changed: added <<
        "kOCPactivation",
        "kOCPdeactivation",
        "OCPmax",
    ]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    # Add OCP activation
    m.add_reaction_from_args(  # >> changed: added <<
        rate_name="OCPactivation",
        function=OCPactivation,
        stoichiometry={"OCP": 1},
        args=["OCP", "pfd", "kOCPactivation", "kOCPdeactivation", "lcf", "OCPmax"],
    )

    # >> changed: replaced calculate_excite_ps and the depricated light function with an updated ps_normabsorption <<
    # Add the calculation of normalised absorption by the photosystems
    # Includes PBS association and OCP
    m.update_algebraic_module(
        module_name="ps_normabsorption",
        function=ps_normabsorption_ocp,
        args=["time", "PBS_PS1", "PBS_PS2", "OCP", "complex_abs", "PSItot", "PSIItot", "lcf"],
        check_consistency=False,
    )

    m.update_algebraic_module(  # >> changed: added <<
        module_name="ps_normabsorption_ML",
        function=ps_normabsorption_ocp,
        args=[
            "time",
            "PBS_PS1",
            "PBS_PS2",
            "OCP",
            "complex_abs_ML",
            "PSItot",
            "PSIItot",
            "lcf"
        ],
        check_consistency=False,
    )

    # Add OCP effect on pbs fluorescence
    m.update_algebraic_module(  # >> changed: added <<
        module_name="fluorescence_pbs",
        function=fluorescence_pbs_ocp,
        args=["OCP", "PBS_free", "complex_abs_ML", "fluo_influence", "lcf"],
        derived_compounds=["FPBS"],
        check_consistency=False,
    )

    # Sort the algebraic modules (temporary until bug is fixed)
    # m = sort_algmodules(m)
    return m, y0
