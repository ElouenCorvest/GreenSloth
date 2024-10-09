#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model of photoinhibtion 
"""

import numpy as np
from modelbase.ode import Model

from .parameters import *
from .rates import *
from .utils import pH

# initiate model
model = Model(pdict)

# add compounds
model.add_compounds(
    [
        "P",
        "H",
        "E",
        "A",
        "Pr",
        "V",
        "Fd",
        "PC",
        "NADPH",
        "Uact",
        "Uinh",
        "Udeg",
    ]
)

############################################################################################################
# add derived parameters
############################################################################################################

model.add_derived_parameter(
    parameter_name="RT", function=lambda r, t: r * t, parameters=["R", "T"]
)


model.add_derived_parameter(
    parameter_name="KeqQAPQ",
    function=KeqQAPQ,
    parameters=["F", "E0QAQAm", "E0PQPQH2", "pHstroma", "RT"],
)


model.add_derived_parameter(
    parameter_name="KeqFAFd",
    function=KeqFAFd,
    parameters=["E0FAFAm", "F", "E0FdFdm", "RT"],
)


model.add_derived_parameter(
    parameter_name="KeqPCP700",
    function=KeqPCP700,
    parameters=["E0PCPCm", "F", "E0P700pP700", "RT"],
)


model.add_derived_parameter(
    parameter_name="dG_pH",
    function=lambda r, t: np.log(10) * r * t,
    parameters=["R", "T"],
)


model.add_derived_parameter(
    parameter_name="KeqFNR",
    function=KeqFNR,
    parameters=["E0FdFdm", "F", "E0NADPNADPH", "pHstroma", "dG_pH", "RT"],
)


######################################################################################
# add algebraic modules
######################################################################################

model.add_algebraic_module(
    module_name="P_am",
    function=pqmoiety,
    compounds=["P"],
    derived_compounds=["Pox"],
    parameters=["PQtot"],
)

model.add_algebraic_module(
    module_name="A_am",
    function=atpmoiety,
    compounds=["A"],
    derived_compounds=["ADP"],
    parameters=["APtot"],
)

model.add_algebraic_module(
    module_name="PsbS_am",
    function=psbsmoiety,
    compounds=["Pr"],
    derived_compounds=["Pnr"],
    parameters=["PsbStot"],
)

model.add_algebraic_module(
    module_name="X_am",
    function=xcycmoiety,
    compounds=["V"],
    derived_compounds=["Z"],
    parameters=["Xtot"],
)

model.add_algebraic_module(
    module_name="pc_alm",
    function=pcmoiety,
    compounds=["PC"],
    derived_compounds=["PCox"],
    parameters=["PCtot"],
)

model.add_algebraic_module(
    module_name="Quencher",
    function=Quencher,
    compounds=["Pr", "V", "Uact"],
    derived_compounds=["Q"],
    parameters=[
        "Xtot",
        "PsbStot",
        "Kzsat",
        "gamma0",
        "gamma1",
        "gamma2",
        "gamma3",
        "gamma4",
        "slow_quenching",
    ],
)

# model.add_algebraic_module(
#     module_name = 'PSIIstates',
#     function = ps2states,
#     compounds = ["P","Uact","Q"],
#     derived_compounds = ["B0", "B1", "B2", "B3"],
#     parameters = ["PFD", "PQtot", "kPQred",
#                   "KeqQAPQ", "kH", "kF", "kP"]
#     )

model.add_algebraic_module(
    module_name="PSIIstates",
    function=ps2statesET,
    compounds=["P", "Uact", "Udeg", "Uinh", "Q"],
    derived_compounds=["B0", "B1", "B2", "B3", "Uip", "Uin", "Udp", "Udn"],
    parameters=["PFD", "PQtot", "kT", "kP", "kF", "kH", "kPQred", "KeqQAPQ", "beta"],
)


model.add_algebraic_module(
    module_name="Fluorescence",
    function=FInh2,
    compounds=["B0", "B2", "Uinh", "Udeg", "Q"],
    derived_compounds=["Fluo"],
    modifiers=None,
    parameters=["kF", "kH", "kP", "kT", "beta"],
)


model.add_algebraic_module(
    module_name="L",
    function=lambda X, PFD: PFD,
    compounds=["P"],
    derived_compounds=["L"],
    parameters=["PFD"],
)

model.add_algebraic_module(
    module_name="fd_alm",
    function=fdmoiety,
    compounds=["Fd"],
    derived_compounds=["Fdox"],
    parameters=["Fdtot"],
)


model.add_algebraic_module(
    module_name="fdredox_alm",
    function=lambda Fd, Fdtot: Fd / Fdtot,
    compounds=["Fd"],
    derived_compounds=["Fd_rel"],
    parameters=["Fdtot"],
)


model.add_algebraic_module(
    module_name="N_alm",
    function=Nmoiety,
    compounds=["NADPH"],
    derived_compounds=["NADP"],
    parameters=["NADPtot"],
)


model.add_algebraic_module(
    module_name="Uact_rel",
    function=lambda Uact, PSIItot: Uact / PSIItot,
    compounds=["Uact"],
    derived_compounds=["Uact_rel"],
    modifiers=None,
    parameters=["PSIItot"],
)

model.add_algebraic_module(
    module_name="Uinh_rel",
    function=lambda Uinh, PSIItot: Uinh / PSIItot,
    compounds=["Uinh"],
    derived_compounds=["Uinh_rel"],
    modifiers=None,
    parameters=["PSIItot"],
)

model.add_algebraic_module(
    module_name="Udeg_rel",
    function=lambda Uinh, PSIItot: Uinh / PSIItot,
    compounds=["Udeg"],
    derived_compounds=["Udeg_rel"],
    modifiers=None,
    parameters=["PSIItot"],
)

model.add_algebraic_module(
    module_name="P_rel",
    function=lambda P, PQtot: P / PQtot,
    compounds=["P"],
    derived_compounds=["P_rel"],
    modifiers=None,
    parameters=["PQtot"],
)

model.add_algebraic_module(
    module_name="ATP_rel",
    function=lambda ATP, APtot: ATP / APtot,
    compounds=["A"],
    derived_compounds=["A_rel"],
    modifiers=None,
    parameters=["APtot"],
)

model.add_algebraic_module(
    module_name="pH",
    function=pH,
    compounds=["H"],
    derived_compounds=["pH"],
    modifiers=None,
)

model.add_algebraic_module_from_args(
    module_name="ps1_alm",
    function=ps1states,
    derived_compounds=["Y0A"],
    args=[
        "PC",
        "Fd",
        "Fdox",
        "PCox",
        "PSItot",
        "kFdred",
        "kPCox",
        "PFD",
        "KeqFAFd",
        "KeqPCP700",
    ],
)

###############################################################################
# add rates
###############################################################################

model.add_reaction_from_args(
    rate_name="vPSII",
    function=vPSII,
    stoichiometry={"P": 1, "H": 2 / pdict["bH"]},
    args=["B1", "kP"],
)

model.add_reaction_from_args(
    rate_name="vB6f",
    function=vB6f,
    stoichiometry={"PC": 2, "P": -1, "H": 4 / pdict["bH"]},
    args=[
        "PCox",
        "PC",
        "P",
        "Pox",
        "pH",
        "kCytb6f",
        "F",
        "E0PQPQH2",
        "E0PCPCm",
        "pHstroma",
        "RT",
        "dG_pH",
    ],
)

model.add_reaction_from_args(
    rate_name="vATPsynthase",
    function=vATPsynthase,
    stoichiometry={"A": 1, "H": (-14 / 3) / pdict["bH"]},
    args=[
        "A",
        "H",
        "E",
        "kATPsynthase",
        "DG0ATP",
        "pHstroma",
        "RT",
        "Pi",
        "APtot",
        "activationATP_switch",
    ],
)

model.add_reaction_from_args(
    rate_name="vATPactivity",
    function=vATPactivity,
    stoichiometry={"E": 1},
    args=["E", "PFD", "kActATPase", "kDeactATPase"],
)

model.add_reaction_from_args(
    rate_name="vLeak",
    function=vLeak,
    stoichiometry={"H": -1 / pdict["bH"]},
    args=["H", "kleak", "pHstroma"],
)

model.add_reaction_from_args(
    rate_name="vATPcons",
    function=vATPcons,
    stoichiometry={"A": -1},
    args=["A", "kATPconsumption"],
)

model.add_reaction_from_args(
    rate_name="vVDE",
    function=vVDE,
    stoichiometry={"V": -1},
    args=["V", "H", "nHX", "KphSatZ", "kDeepoxV"],
)

model.add_reaction_from_args(
    rate_name="vZEP",
    function=vZEP,
    stoichiometry={"V": 1},
    args=["V", "kEpoxZ", "Xtot"],
)


model.add_reaction_from_args(
    rate_name="vPsbSProt",
    function=vPsbSProt,
    stoichiometry={"Pr": -1},
    args=["Pr", "H", "nHL", "KphSatLHC", "kProt"],
)

model.add_reaction_from_args(
    rate_name="vPsbSDeProt",
    function=vPsbSDeProt,
    stoichiometry={"Pr": 1},
    args=["Pnr", "kDeprot"],
)

model.add_reaction_from_args(
    rate_name="vFNR",
    function=vFNR,
    stoichiometry={"Fd": -2, "NADPH": 1},
    args=[
        "Fdox",
        "Fd",
        "NADPH",
        "NADP",
        "KM_F",
        "KM_N",
        "EFNR",
        "kcatFNR",
        "KeqFNR",
    ],
)

model.add_reaction_from_args(
    rate_name="vNADPHconsumption",
    function=vNADPHconsumption,
    stoichiometry={"NADPH": -1},
    args=["NADPH", "kNADPHconsumption"],
)

model.add_reaction_from_args(
    rate_name="vPTOX",
    function=vPTOX,
    stoichiometry={"P": -1},
    args=["P", "kPTOX", "O2ext"],
)

model.add_reaction_from_args(
    rate_name="vCyc",
    function=vCyc,
    stoichiometry={"P": 1, "Fd": -2},
    args=["Pox", "Fd", "kcyc"],
)


model.add_reaction_from_args(
    rate_name="mito",
    function=mito,
    stoichiometry={"A": 1},
    args=["PFD", "mito"],
)

model.add_reaction_from_args(
    rate_name="vPhotInh",
    function=vPhotInh,
    stoichiometry={"Uact": -1, "Uinh": 1},
    args=["B1", "B3", "kPI0"],
)

model.add_reaction_from_args(
    rate_name="vPhotInh2",
    function=vPhotInh2,
    stoichiometry={"Uinh": -1, "Udeg": 1, "A": -241},
    args=["Uinh", "A", "kDEG", "Km_PI"],
)

model.add_reaction_from_args(
    rate_name="vPhotInh3",
    function=vPhotInh3,
    stoichiometry={"Udeg": -1, "Uact": 1, "A": -1059},
    args=["Udeg", "A", "kREP", "Km_PI"],
)

model.add_reaction_from_args(
    rate_name="vPSI",
    function=vPSI,
    stoichiometry={"Fd": 1, "PC": -1},
    args=["Y0A", "PFD"],
)
