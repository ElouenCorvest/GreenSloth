import matplotlib.pyplot as plt
import modelbase
import numpy as np
from modelbase.ode import LabelModel, LinearLabelModel, Model, Simulator, mca
from modelbase.ode import ratefunctions as rf
from modelbase.ode import ratelaws as rl
import parameters

# get_ipython().run_line_magic("matplotlib", "inline")


# CHANGE LOG
# 000            | original model by elena
# 003 02.12.2021 | recalculated all parameter values
#                | removed option to rename rates & parameters ("{c1}")
# 017 06.03.2023 | switched parameters to import from parameters.py


def calculate_pHlumen(x):
    return -np.log(x * (2.9e-5)) / np.log(10)


def calculate_pHcytoplasm(x):
    return -np.log(x * (4.8e-6)) / np.log(10)


# ATP-synthase taken from plant model and fitted to my model with dynamic Hs
def vATPsynthase(Hi, Ho, ATP, ADP, DeltaG0_ATP, dG_pH, HPR, Pi_mol, RT, kATPsynth):
    """
    Reaction rate of ATP production
    Kinetic: simple mass action with PH dependant equilibrium
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [ATP], [ADP] in mmol/mol Chl
    """
    pHlumen = calculate_pHlumen(Hi)
    pHcytoplasm = calculate_pHcytoplasm(Ho)
    DG = DeltaG0_ATP - dG_pH * HPR * (pHcytoplasm - pHlumen)
    Keq = Pi_mol * np.exp(-DG / RT)
    return kATPsynth * (ADP - ATP / Keq)


def add_ATPase(m, init_param=None):
    p_list = [
        "kATPsynth",
        "Pi_mol",
        "DeltaG0_ATP",
        "HPR",
    ]
    p = {k: v for k, v in parameters.p.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})
    m.add_parameters(p)
    m.add_reaction(
        rate_name="vATPsynthase",
        function=vATPsynthase,
        stoichiometry={
            "Hi": -m.get_parameter("HPR") / m.get_parameter("bHi"),
            "Ho": m.get_parameter("HPR") / m.get_parameter("bHo"),
            "ATP": 1,
        },
        modifiers=["Ho", "ATP", "ADP"],
        dynamic_variables=["Hi", "Ho", "ATP", "ADP"],
        parameters=[
            "DeltaG0_ATP",
            "dG_pH",
            "HPR",
            "Pi_mol",
            "RT",
            "kATPsynth",
        ],
        reversible=True,
    )
    return m
