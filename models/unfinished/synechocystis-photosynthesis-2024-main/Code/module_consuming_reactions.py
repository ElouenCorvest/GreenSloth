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
# 004 03.12.2021 | changed reaction vPRfirststep to produce PG insted of GAP
# 007 15.12.2021 | added stoichiometric protons to vNADPHconsumption
# 009 20.12.2021 | corrected the stoichiometric protons of vNADPHconsumption
#                | added the kinetic parameters kATPconsumption, kNADPHconsumption
#                | added proton dependency to NADPH consumption
# 017 02.08.2022 | REMOVED PREVIOUS REACTIONS
#                | moved consuming reactions from module_electron_transport_chain here
#     06.03.2023 | switched parameters to import from parameters.py

# Add reaction: ATP consumption by processes other than CBB
def vATPconsumption(ATP, kATPconsumption):
    return kATPconsumption * ATP


# Add reaction: NADH consumption by processes other than NDH
def vNADHconsumption(NADH, Ho, kNADHconsumption):
    return kNADHconsumption * NADH * Ho


def add_consuming_reactions(m, init_param=None):
    p_list = [
        # Rate constants of consumption reactions
        "kATPconsumption",
        "kNADHconsumption",
    ]
    p = {k: v for k, v in parameters.p.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    # Add the parameters
    m.add_parameters(p)

    # Add reaction: ATP consumption by processes other than CBB
    m.add_reaction(
        rate_name="vATPconsumption",
        function=vATPconsumption,
        stoichiometry={
            "ATP": -1,
        },
        parameters=["kATPconsumption"],
        reversible=False,
    )

    # Add reaction: NADH consumption by processes other than NDH
    m.add_reaction(
        rate_name="vNADHconsumption",
        function=vNADHconsumption,
        stoichiometry={"NADH": -1, "Ho": -1 / m.parameters["bHo"]},
        parameters=["kNADHconsumption"],
        reversible=False,
    )
    return m
