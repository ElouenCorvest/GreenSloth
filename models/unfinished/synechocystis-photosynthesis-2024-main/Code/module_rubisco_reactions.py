import numpy as np
from modelbase.ode import ratefunctions as rf
import parameters

# CHANGE LOG
# 000            | original model by elena
# 003 02.12.2021 | recalculated all parameter values
# 007 15.12.2021 | modified proton stoichiometries of CBB and PR
# 009 20.12.2021 | corrected proton stoichiometries of CBB and PR
#                | changed the input definition of the v_CBB and v_PR reactions
# 010 22.12.2021 | changed the CBB and PR stoichiopmetries to produce and use 3PGA, removed GAP from the module
#                | set the maximum CBB & PR activities to Fd redox ratios > 0.1
# 013 20.02.2022 | renamed the reaction "PR" (photorespiration) to "oxy" (oxygenation)
#                | renamed "v_CBB" and "v_oxy" to "vCBB" and "vOxy", respectively; renamed function "addCBBandPR" to "add_CBB_and_oxy"
#                | removed pH regulation (f_CBB_Tijskens_pH, regulation only via f_CBB_Fdratio)
# 014 26.04.2022 | Added a (de)activation reaction for both CBB and PR, replacing f_CBB_Fdratio
# 015 29.04.2022 | removed older change notes
#                | adjusted v_CBB_max for the assumed activity reduction by the adjusting factors during experimentally measured values
# 016 07.07.2022 | edited kCBBdeactivation to be the temporary value
# 017 06.03.2023 | switched parameters to import from parameters.py


##############################################
# Define functions approximating CBB and oxy
##############################################

#  Calvin-Benson-Bassham cycle (CBB)
def vCBB(f_CBB_energy, f_CBB_gas, f_CBB_light, vCBB_max):
    return vCBB_max * f_CBB_energy * f_CBB_gas * f_CBB_light


# Oxygenation by Rubisco, the first step of Photorespiration
def vOxy(f_oxy_carbon, f_oxy_energy, f_oxy_gas, f_oxy_light, vOxy_max):
    return vOxy_max * f_oxy_carbon * f_oxy_energy * f_oxy_gas * f_oxy_light


########################################################################
# Different possible functions to express the CBB and oxy regulation
########################################################################


## Functions used for CBB and partially for oxy
###############################################

## Influence of ATP and NADPH on the rates

# Irreversible Mass Action kinetics as the simpelest case
# Used in Vershubskii (2011)
def CBB_energy_MA(ATP, NADPH, MA_factor, **kwargs):
    return rf.mass_action_2(ATP, NADPH, k_fwd=MA_factor)


# Irreversible Mass Action kinetics including the stoichiometry
def CBB_energy_MA_stoich(ATP, NADPH, nATP, nNADPH, MA_factor, **kwargs):
    return rf.mass_action_2(ATP**nATP, NADPH**nNADPH, k_fwd=MA_factor)


# Michaelis-Menten
# Uses the general (reversible) Michaelis-Menten kinetics
def CBB_energy_MM(ATP, NADPH, KMATP, KMNADPH, **kwargs):
    return rf.michaelis_menten(ATP, 1, KMATP) * rf.michaelis_menten(NADPH, 1, KMNADPH)


# Michaelis-Menten including the stoichiometry
# Uses the general (reversible) Michaelis-Menten kinetics
def CBB_energy_MM_stoich(ATP, NADPH, KMATP, KMNADPH, nATP, nNADPH, **kwargs):
    return (
        rf.michaelis_menten(ATP, 1, KMATP) ** nATP
        * rf.michaelis_menten(NADPH, 1, KMNADPH) ** nNADPH
    )


## Influence of gas concentrations

# Michaelis-Menten with competetive O2 inhibition and compensation point
# Used in Vershubskii (2011), unnecessary if respiration isn't lumped in
def CBB_gas_Vershubskii(CO2, O2, KMCO2, KIO2, gamma, **kwargs):
    return (CO2 - gamma) / (CO2 + KMCO2 * (1 + O2 / KIO2))


# Michaelis-Menten with competetive O2 inhibition
def CBB_gas_MM_O2(CO2, O2, KMCO2, KIO2, **kwargs):
    return rf.competitive_inhibition(CO2, O2, 1, KMCO2, KIO2)


# Michaelis-Menten with competetive O2 inhibition including the stoichiometry
# Uses the general (reversible) Michaelis-Menten kinetics
def CBB_gas_MM_O2_stoich(CO2, O2, KMCO2, KIO2, nCO2, **kwargs):
    return rf.competitive_inhibition(CO2, O2, 1, KMCO2, KIO2) ** nCO2


# Michaelis-Menten
# But inhibition seems useful and necessary
def CBB_gas_MM(CO2, O2, KMCO2, **kwargs):
    return rf.michaelis_menten(CO2, 1, KMCO2)


# Michaelis-Menten including the stoichiometry
# But inhibition seems useful and necessary
def CBB_gas_MM_stoich(CO2, O2, KMCO2, nCO2, **kwargs):
    return (rf.michaelis_menten(CO2, 1, KMCO2)) ** nCO2


## Influence of light
## The CBB is inhibited by the formation of disulfite bonds in the absence of reducing equivalents

# Using NADPH as redox equivalent

# Ratio of reduced NADP to total NADP
def CBB_light_NADPratio(NADPH, NADP_tot, **kwargs):
    return NADPH / NADP_tot


# Michaelis Menten
def CBB_light_MM_NADPH(NADPH, KMNADPH_2, **kwargs):
    return rf.michaelis_menten(NADPH, 1, KMNADPH_2)


# Using Ferredoxin as redox equivalent
# In Plants the inhibitorycomplex is dissociated through Thioredoxin from Ferredoxin

# Ratio of reduced Fd to total Fd
def CBB_light_Fdratio(Fd_red, Fd_tot, **kwargs):
    # limit to 1
    ratio_at_max = 0.1
    res = np.array(Fd_red / (Fd_tot * ratio_at_max))
    res[res > 1] = 1
    return res


# Michaelis Menten
def CBB_light_MM_Fd(Fd_red, KMFd_red, **kwargs):
    return rf.michaelis_menten(Fd_red, 1, KMFd_red)


## The FBPase has a basic pH optimum

# Vershubskii (2011) pH function
def CBB_light_Vershubskii(Hs, **kwargs):
    a = 100
    b = np.exp(3.16 - 10**8 * Hs / 0.5)
    return (a * b + 1) / (b + 1)


# Tijskens (2001) pH function
def CBB_light_Tijskens_pH(Hs, KEH, KEOH, Kw, **kwargs):
    return 1 / (1 + Hs / KEH + Kw / (KEOH * Hs))


## Unique functions used for Photorespiration
###############################################

## Influence of gas concentrations

# Michaelis-Menten with competetive CO2 inhibition
def oxy_gas_MM_CO2(O2, CO2, KMO2, KICO2, **kwargs):
    return rf.competitive_inhibition(O2, CO2, 1, KMO2, KICO2)


# Michaelis-Menten with competetive CO2 inhibition including the stoichiometry
# Uses the general (reversible) Michaelis-Menten kinetics
def oxy_gas_MM_CO2_stoich(O2, CO2, KMO2, KICO2, nO2, **kwargs):
    return rf.competitive_inhibition(O2, CO2, 1, KMO2, KICO2) ** nO2


# Michaelis-Menten
# But inhibition seems useful and necessary
def oxy_gas_MM(O2, CO2, KMO2, **kwargs):
    return rf.michaelis_menten(O2, 1, KMO2)


# Michaelis-Menten including the stoichiometry
# But inhibition seems useful and necessary
def oxy_gas_MM_stoich(O2, CO2, KMO2, nO2, **kwargs):
    return (rf.michaelis_menten(O2, 1, KMO2)) ** nO2


# Influence of 3PGA as carbon source to be "respired"

# Michaelis-Menten
def oxy_carbon_MM(PGA, KMPGA, **kwargs):
    return rf.michaelis_menten(PGA, 1, KMPGA)


# Michaelis-Menten including the stoichiometry
def oxy_carbon_MM_stoich(PGA, KMPGA, nPGA, **kwargs):
    return rf.michaelis_menten(PGA, 1, KMPGA) ** nPGA


###########################
# Define model parameters
###########################

p_list = [
    "vCBB_max",  # [mmol mol(Chl)^-1 s^-1] 1/3 approximate maximal CO2 uptake rate (Zavrel, 2017; Fig. S-D) >> changed: adjusted for the assumed activity reduction by the adjusting factors during experimentally measured values <<
    "vOxy_max",  # [mmol mol(Chl)^-1 s^-1] 1/3 approximate Rubisco oxygenation rate (Savir, 2010)
    "KMATP",  # [mmol mol(Chl)^-1] order of magnitude of KM_ATP for phosphoribulo kinase (Wadano, 1998) and phospoglycerate kinase (Tsukamoto, 2013)
    "KMNADPH",  # [mmol mol(Chl)^-1] approxiate KM_NADPH for GAP2 in Synechocystis (Koksharova, 1998)
    "KMCO2",  # [mmol mol(Chl)^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco (Savir, 2010; Tab. S1)
    "KIO2",  # [mmol mol(Chl)^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco (Savir, 2010; Tab. S1)
    "KEH",  # [mmol mol(Chl)^-1] approximate proton concentration at first half maximal activity of FBPase (Uvardy, 1982)
    "KEOH",  # [mmol mol(Chl)^-1] approximate hydroxid ion concentration at second half maximal activity of FBPase (Uvardy, 1982)
    "Kw",  # [unitless] water dissociation constant (Wikipedia)
    "KMO2",  # [mmol mol(Chl)^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco (Savir, 2010; Tab. S1)
    "KICO2",  # [mmol mol(Chl)^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco (Savir, 2010; Tab. S1)
    "KMPGA",  # [mmol mol(Chl)^-1] arbitrary michaelis constant limiting oxygenation reactions for low 3PGA (ARBITRARY)
    # Rate constants of Fd-mediated enzyme activiation reactions
    "kCBBactivation",  # [s^-1] rate of CBB activation by reduced Fd (visually fitted) (TODO: GET SOURCE FOR TIMING)
    "kCBBdeactivation",  # >> changed: changed to the transient value in test_time_series (increased by factor 5) <<
]
p = {k: v for k, v in parameters.p.items() if k in p_list}

# Add an Fd-dependent regulation of CBB and PR
def CBBactivation(CBBa, Fd_red, Fd_ox, kCBBactivation, kCBBdeactivation):
    return kCBBactivation * Fd_red * (1 - CBBa) - kCBBdeactivation * Fd_ox * CBBa


###########################
# Transfer into modelbase
###########################


def add_CBB_and_oxy(m, init_param=None):
    # Add only new compounds
    compounds = ["ATP", "NADPH", "CO2", "O2", "Fd_red", "Ho", "3PGA", "PG", "CBBa"]
    new_compounds = np.array(
        [cmp not in m.compounds + m.derived_compounds for cmp in compounds]
    )
    m.add_compounds(np.array(compounds)[new_compounds])

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    # Add only new parameters
    params_subset = {key: value for key, value in p.items() if key not in m.parameters}

    m.add_parameters(params_subset)

    # Add the factors as algebraic modules
    m.add_algebraic_module(
        module_name="f_CBB_energy",
        function=CBB_energy_MM,
        compounds=["ATP", "NADPH"],
        derived_compounds=["f_CBB_energy"],
        modifiers=None,
        parameters=["KMATP", "KMNADPH"],
    )
    m.add_algebraic_module(
        module_name="f_CBB_gas",
        function=CBB_gas_MM_O2,
        compounds=["CO2", "O2"],
        derived_compounds=["f_CBB_gas"],
        modifiers=None,
        parameters=["KMCO2", "KIO2"],
    )
    # m.add_algebraic_module(
    #     module_name="f_CBB_Fdratio",
    #     function=CBB_light_Fdratio,
    #     compounds=["Fd_red"],
    #     derived_compounds=["f_CBB_Fdratio"],
    #     modifiers=None,
    #     parameters=["Fd_tot"],
    # )
    # m.add_algebraic_module(
    #     module_name="f_CBB_Tijskens_pH",
    #     function=CBB_light_Tijskens_pH,
    #     compounds=["Ho"],
    #     derived_compounds=["f_CBB_Tijskens_pH"],
    #     modifiers=None,
    #     parameters=["KEH", "KEOH", "Kw"],
    # )
    # m.add_algebraic_module(
    #     module_name="f_CBB_light",
    #     function=lambda x, y: x*y,
    #     compounds=["f_CBB_Tijskens_pH", "f_CBB_Fdratio"],
    #     derived_compounds=["f_CBB_light"],
    #     modifiers=None,
    #     parameters=[],
    # )
    m.add_algebraic_module(
        module_name="f_oxy_carbon",
        function=oxy_carbon_MM,
        compounds=["3PGA"],
        derived_compounds=["f_oxy_carbon"],
        modifiers=None,
        parameters=["KMPGA"],
    )
    m.add_algebraic_module(
        module_name="f_oxy_gas",
        function=oxy_gas_MM_CO2,
        compounds=["O2", "CO2"],
        derived_compounds=["f_oxy_gas"],
        modifiers=None,
        parameters=["KMO2", "KICO2"],
    )

    # Add an Fd-dependent regulation of CBB and PR
    m.add_reaction(
        rate_name="vCBBactivation",
        function=CBBactivation,
        stoichiometry={"CBBa": 1},
        modifiers=["CBBa", "Fd_red", "Fd_ox"],
        dynamic_variables=["CBBa", "Fd_red", "Fd_ox"],
        parameters=["kCBBactivation", "kCBBdeactivation"],
        reversible=True,
    )

    # Add the full reactions
    m.add_reaction(
        rate_name="vCBB",
        function=vCBB,
        stoichiometry={
            "CO2": -3,
            "ATP": -8,
            "NADPH": -5,
            "3PGA": 1,
            "Ho": -5 / m.get_parameter("bHo"),
        },
        modifiers=["f_CBB_energy", "f_CBB_gas", "CBBa"],
        dynamic_variables=["f_CBB_energy", "f_CBB_gas", "CBBa"],
        parameters=["vCBB_max"],
        reversible=False,
    )
    m.add_reaction(
        rate_name="vOxy",
        function=vOxy,
        stoichiometry={
            "O2": -3,
            "ATP": -8,
            "NADPH": -5,
            "3PGA": -2,
            "PG": 3,
            "Ho": -5 / m.get_parameter("bHo"),
        },
        modifiers=["f_oxy_carbon", "f_CBB_energy", "f_oxy_gas", "CBBa"],
        dynamic_variables=["f_oxy_carbon", "f_CBB_energy", "f_oxy_gas", "CBBa"],
        parameters=["vOxy_max"],
        reversible=False,
    )
    return m
