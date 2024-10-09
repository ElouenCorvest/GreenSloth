#!/usr/bin/env python

from collections import defaultdict
from datetime import datetime
from sys import argv

import numpy as np
import pandas as pd

# Import CBB to get the rate adjustment functions
import module_rubisco_reactions as CBB

# Import light description module
from functions_light_absorption import pigments_Fuente

# CHANGE LOG
# 000            | original model by elena
# 003 02.12.2021 | recalculated all parameter values
# 004 03.12.2021 | added the rate constant kglycerate_kinase and the concentrations of glycerate and 3PGA
# 005 07.12.2021 | increased E0_PQ according to other source
# 006 15.12.2021 | added the rate of CO2 exchange, the external CO2 concentration, and the factor of internally increased CO2
#                | changed the internal CO2 concentration
# 007 16.12.2021 | increased bHo
# 008 16.12.2021 | changed concentration parameters NADP_tot, c_AP_tot, c_Hi, c_Ho, c_PC_ox, c_Fd_ox, c_NADPH, c_ATP
#                | updated all kinetic parameters in other files changed by these modifications
# 009 17.12.2021 | changed kinetic parameters QFN, k_O2
# 010 22.12.2021 | changed parameters concerning GAP to 3PGA, removed GAP from the module
#     14.01.2022 | changed kinetic parameters k_O2, k_ox1, k_aa, k_krebs
# 011 23.01.2022 | removed stoichiometric exponents in k_aa, k_O2, k_FQ, k_FN
#                | added initial ebenhöhhh c_PSII
#                | changed kinetic parameter k_krebs
#     24.01.2022 | added dark concentrations od Hi and Ho and adapted kinetic parameters k_ox1, k_aa
# 012 28.01.2022 | added light conversion parameters excite_ps1 and excite_ps2 and their source values
#                | changed volume fraction of thylakoids f_V_lumen from new source (affects V_cyt, V_lumen and the depending parameters cf_lumen, cf_cytoplasm, k_ox1, k_O2, k_aa)
#                | changed bHo to reflect the new volume ratio
#                | added the kinetic parameters kQuench, kUnquench
#                | optically restructured the calculation of parameters taking up multiple rows
#     07.02.2022 | changed reaction vNQ to oxidise Fd_red instead of Q_red
#                | used a different source for plastoquinone concentrations (affects c_Q_tot, c_Q_red, c_Q_ox and all dependencies)
#     08.02.2022 | from the same source added concentrations c_Q_red_dark and c_Q_ox_dark for normalisation of dark-measured rates (affects k_SDH, k_ox1, k_NQ, k_NDH, k_FQ)
#     10.02.2022 | changed the source for kinetic parameter k_Q
#     11.02.2022 | corrected amount of NADPH reduced and normalisation concentrations in k_FN
# 013 17.02.2022 | added source for compound concentration of PG
#                | added estimation of the PG recycle reaction rate kPR replacing the yokota model
#     18.02.2022 | added compounds NAD and NADH with conserved total NADtot
#                | replaced NADPH normalisation in k_NDH with NADH
#     20.02.2022 | replaced k_krebs with kResp because reaction cyclicSuccinate was replaced with vRespiration
#     23.02.2022 | added the calculation of the stoichiometry of respiration, taking into account the different respiratory pathways
#                | corrected cs_ps1 and cs_ps2 for wrong source plot annotation
#     24.02.2022 | renamed v_CBB_max and v_PR_max to vCBB_max and vOxy_max because of changes to the module
#     01.03.2022 | changed kinetic constants kQuench and kUnquench to visually fitted values
# 014 28.02.2022 | increased the temporary c_3PGA extensively as it represents all sugars of the cell
#     08.04.2022 | increased the OPP fraction of respiration in respiratory_fluxes according to data from dark adapted cells
#                | modified the calculation of the respiratory rate constant to take into account the OPP fraction
#                | changed the cytoplasmic pH in light and darkness from different source
#     10.04.2022 | removed "changed" comments prior to change 014
#                | adapted the calculation of k_NDH, k_FQ, k_NQ, k_Q
#                | replaced k_FN with k_FN_fwd and k_FN_rev
#     14.04.2022 | corrected excite_ps1 by replacing normalisation by c_PSIItot with c_PSItot
#     26.04.2022 | added parameters kATPconsumption, kNADHconsumption, kFlvactivation, kFlvdeactivation, kCBBactivation, and kCBBdeactivation
#                | added compounds Flva and CBBa representing the activation state
# 015 29.04.2022 | removed older change notes
#                | adjusted v_CBB_max for the assumed activity reduction by the adjusting factors during experimentally measured values
#                | increased the fraction of PBS excitation transferred to PS2
#     04.05.2022 | removed Ho/bHo division in respiration since the models bHo is rounded
# 016 07.07.2022 | edited values of k_Q, kCBBdeactivation, kQuench, and kUnquench to be the temporary values
# 017 07.11.2022 | added parameter k_F1
#     23.11.2022 | added organism information
#     06.02.2023 | reduced k_FN_rev
#     07.02.2023 | added condition info and classified the type of objects
#     13.02.2023 | added all concentrations to c and renamed them from "c_"
#                | corrected the value of kHst
#                | removed trailing whitespaces in descriptions
#     06.03.2023 | adapted E0 values to Lewis2022
#                | updated NQ value to reflect CEF measured by Theune2021
#                | updated k_F1 to lower value, representing low PS1 fluorescence
#     09.03.2023 | reduced respiration by factor 20 to adjust for lover substrate concentrations
#                | increaser terminal oxidase rate constants to match respiration Q_red redox level
#     14.03.2023 | corrected vCBB_max with measured chl content
#     24.03.2023 | reduced k_NQ to fit source value better
#                | added parameters of CBB update module
#     13.04.2023 | added information about usage and replacement of parameters/ concentrations
#     01.06.2023 | removed increasing factor from k_ox1
# 018 09.01.2024 | corrected descriptions of rate constants

#############################
# Calculate parameter values
#############################

# Define the structure of the entries for each parameter
def default_param():
    return {
        "value": None,
        "unit": "",
        "descr": "",
        "organism": "",
        "condition": "",
        "source": "",
        "ref": "",
        "type": "",
        "used": {"if": None, "not": None},
    }


# Create the dict for storing cell parameters of modules
p = defaultdict(default_param)

# Create the dict for storing cell parameters of update modules
pu = defaultdict(default_param)

# Create the dict for storing concentrations of modules
c = defaultdict(default_param)

# Create the dict for storing concentrations of update modules
cu = defaultdict(default_param)

# Define a function for unpacking some values
def unpack(name, parameter_set=p):
    """Get the values of a parameters saved in p

    Args:
        name (str or list of str): The name of a parameter or a list of such names

    Returns:
        float of list of float: If name is a str, the value of the parameter with that name, otherwise if name is a list get the values for the parameter names in that list
    """
    # Get the parameter value of name if it's a str
    if isinstance(name, str):
        return parameter_set.get(name).get("value")
    # Get the parameter values of the names in name if it's a list
    elif isinstance(name, list):
        return [parameter_set.get(x).get("value") for x in name]
    else:
        raise ValueError("name must be str or list of str")


def make_valuedict(parameter_set: dict, type_select: "list|str" = None):
    if type_select is None:
        return {key: value.get("value") for key, value in parameter_set.items()}
    elif isinstance(type_select, str):
        return {
            key: value.get("value")
            for key, value in parameter_set.items()
            if value.get("type") == type_select
        }
    elif isinstance(type_select, list) and np.all(
        [type(x) is str for x in type_select]
    ):
        return {
            key: value.get("value")
            for key, value in parameter_set.items()
            if value.get("type") in type_select
        }
    else:
        raise ValueError("type select must be of type Str or List[Str]")


### Parameters used for normalisation ###


# Cell volume and chlorophyll content
p["V_cell"] = {
    "value": 5.6e-15,
    "unit": "l cell^-1",
    "descr": "synechocystis cell volume",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "HEPES-buffered BG11 medium; 34 [°C]; 45 [μmol photons m^−2 s^−1] white light; 0.4 [l min^-1] CO2 enriched",
    "source": "5.6e-15 [l cell^-1] synechocystis cell volume",
    "ref": "Moal2012",
    "type": "helper",
    "used": {"if": None, "not": None},
}
p["n_chl"] = {
    "value": 1.4e7,
    "unit": "cell^-1",
    "descr": "total chlorophyll content",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium; 30 [°C], 30 [μmol(photons) m^-2 s^-1];",
    "source": "1.4e7 [cell^-1] total chlorophyll content",
    "ref": "Keren2004",
    "type": "helper",
    "used": {"if": None, "not": None},
}
p["NA"] = {
    "value": 6.022e23,
    "unit": "mol^-1",
    "descr": "avogadros number",
    "organism": "-",
    "condition": "-",
    "source": "6.0221e23 [mol^-1] avogadros number",
    "ref": "Richardson2019",
    "type": "helper",
    "used": {"if": None, "not": None},
}
# Make these parameters available also as variables
V_cell, n_chl, NA = unpack(["V_cell", "n_chl", "NA"])

n_chl_mol = n_chl / NA  # [mol cell^-1] total chlorophyll content in mol

# Compartment volumina
p["f_V_lumen"] = {
    "value": 0.09,
    "unit": "unitless",
    "descr": "thylakoid lumen fraction of the total cell volume",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG-11 + 5 [mM] glucose; 30 [°C]; 0.5 [μmol(photons) m^-2 s^-1]",
    "source": "0.09 [unitless] thylakoid lumen fraction of the total cell volume",
    "ref": "VanDeMeene2012",
    "type": "helper",
    "used": {"if": None, "not": None},
}
f_V_lumen = unpack("f_V_lumen")

p["V_cyt"] = {
    "value": (1 - f_V_lumen) * V_cell,
    "unit": "l cell^-1",
    "descr": "volume of the cytoplasm",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG-11 + 5 [mM] glucose;",
    "source": "f_V_lumen, V_cell",
    "ref": "derived",
    "type": "helper",
    "used": {"if": None, "not": None},
}
p["V_lumen"] = {
    "value": f_V_lumen * V_cell,
    "unit": "l cell^-1",
    "descr": "volume of the thylakoid lumen",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "f_V_lumen, V_cell",
    "ref": "derived",
    "type": "helper",
    "used": {"if": None, "not": None},
}
V_cyt, V_lumen = unpack(["V_cyt", "V_lumen"])


# Chlorophyll concentrations total and in compartments

cu["cChl"] = {
    "value": n_chl / V_cell / NA,
    "unit": "mol l^-1",
    "descr": "total molar concentration of chlorophyll",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "n_chl, V_cell, NA",
    "ref": "derived",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["chl_cyt"] = {
    "value": n_chl / V_cyt / NA,
    "unit": "mol l^-1",
    "descr": "molar concentration of chlorophyll",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "n_chl, V_cyt, NA",
    "ref": "derived",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c["chl_lumen"] = {
    "value": n_chl / V_lumen / NA,
    "unit": "mol l^-1",
    "descr": "molar concentration of chlorophyll",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "n_chl, V_lumen, NA",
    "ref": "derived",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c_chl = unpack("cChl", cu)
c_chl_cyt, c_chl_lumen = unpack(["chl_cyt", "chl_lumen"], c)

# Mass of chlorophyll A
p["M_chl"] = {
    "value": 893.509,
    "unit": "g mol^-1",
    "descr": "molar mass of chlorophyll a",
    "organism": "-",
    "condition": "-",
    "source": "893.509 [g mol^-1] molar mass of chlorophyll a (C55H72MgN4O5)",
    "ref": "Wieser2006",
    "type": "helper",
    "used": {"if": None, "not": None},
}
p["M_CO2"] = {
    "value": 44.01,
    "unit": "g mol^-1",
    "descr": "molar mass of CO2",
    "organism": "-",
    "condition": "-",
    "source": "44.01 [g mol^-1] molar mass of CO2 (CO2)",
    "ref": "Wieser2006",
    "type": "helper",
    "used": {"if": None, "not": None},
}
M_chl, M_CO2 = unpack(["M_chl", "M_CO2"])


# Conversion of midpoint potential to standard electrode potential
def midtoelec(n, m, pH=7):
    """
    Calculate the conversion factor from midpoint potential to standard electrode potential
    in a reduction involving n electrons and m protons
    """
    R = 0.0083  # [J K^-1 mmol^-1] ideal gas constant (Richardson2019)
    T = (  # [K] temperature (set)
        25 + 273.15  # [°C] temperature (set)
    )  # offset of Kelvin to Celsius scale
    F = 96.485  # [C mmol^-1] Faraday's constant (Richardson2019)

    conversion_factor = R * T * np.log(10) / F * pH  # [unitless] (Ebenhoh2014)
    return (m / n) * conversion_factor


# Define the functions used for calculation of pH/molar proton concentrations
def calculate_molarHlumen(H, cf_lumen):
    """
    Calculate the molar concentration of protons in the thylakoid lumen from the chlorophyll-normalised concentration. Uses a conversion factor dependent on the volume of the thylakoid lumen.
    """
    return H * cf_lumen  # (2.9e-5)


def calculate_molarHcytoplasm(H, cf_cytoplasm):
    """
    Calculate the molar concentration of protons in the cytoplasm from the chlorophyll-normalised concentration. Uses a conversion factor dependent on the volume of the cytoplasm.
    """
    return H * cf_cytoplasm  # (4.8e-6)


def calculate_pH(H_mol):
    return -np.log(H_mol) / np.log(10)


def deltapH(lumen, cytoplasm):
    d = cytoplasm - lumen
    return d


def calculate_Hlumen(pH, cf_lumen):
    """
    Calculate the chlorophyll-normalised concentration of protons in the thylakoid lumen from the pH concentration. Uses a conversion factor dependent on the volume of the thylakoid lumen.
    """
    H_mol = np.exp(pH * -np.log(10))
    return H_mol / cf_lumen


def calculate_Hcytoplasm(pH, cf_cytoplasm):
    """
    Calculate the chlorophyll-normalised concentration of protons in the cytoplasm from the pH concentration. Uses a conversion factor dependent on the volume of the cytoplasm.
    """
    H_mol = np.exp(pH * -np.log(10))
    return H_mol / cf_cytoplasm


# ---- Conversion factors ----

# A dict with conversion factors from source units
conversion_factors = {}

# A function taking the selected conversion factors and mutliplying them
def unit_conv(name=None, conversion_set=conversion_factors):
    """Get a unit conversion factor using factors saved in conversion_factors

    Args:
        name (str or list of str): The name of a conversion or a list of such names

    Returns:
        float of list of float: If name is a str, the conversion value with that name, otherwise if name is a list get the multiplied conversion factors for the names in that list
    """
    if name is None:
        return list(conversion_set.keys())
    # Get the parameter value of name if it's a str
    if isinstance(name, str):
        return conversion_set.get(name)
    # Get the parameter values of the names in name if it's a list
    elif isinstance(name, list):
        return np.prod(np.array([conversion_set.get(x) for x in name]))
    else:
        raise ValueError("name must be str or list of str")


# Add basic conversion factors
conversion_factors.update(
    {
        "h-1 -> s-1": 1 / 3600,  # [h s^-1]
        "min-1 -> s-1": 1 / 60,  # [min s^-1]
        "cell-1 -> mmol mol(Chl)-1": (
            1 / NA * 1e3 * 1 / n_chl_mol  # [mmol number^-1]  # [cell mol(Chl)⁻1]
        ),
        "umol g(Chl)-1 -> mmol mol(Chl)-1": (
            M_chl * 1e-3  # [g(Chl) mol(Chl)^-1]  # [mmol umol^-1]
        ),
        "mmol g(Chl)-1 -> mmol mol(Chl)-1": M_chl,  # [g(Chl) mol(Chl)^-1]
        "mol g(Chl)-1 -> mmol mol(Chl)-1": (
            M_chl * 1e3  # [g(Chl) mol(Chl)^-1]  # [mmol mol^-1]
        ),
        "mol l-1 -> mmol mol(Chl)-1": (
            1 / c_chl * 1e3  # [l mol(Chl)^-1]  # [mmol mol^-1]
        ),
        "mmol l-1 -> mmol mol(Chl)-1": 1 / c_chl,  # [l mol(Chl)^-1]
        "umol l-1 -> mmol mol(Chl)-1": (
            1 / c_chl * 1e-3  # [l mol(Chl)^-1]  # [mmol umol^-1]
        ),
    }
)

# Conversion factors to transfrom flux estimates [mmol mol(Chl)^-1 s^-1] to other units
conversion_factors.update(
    {
        # "mmol mol(Chl)-1 s-1 -> g(CO2) cell-1 s-1": (
        #     M_CO2 * 1e-3 * n_chl_mol  # [g mol^-1]  # [g mg^-1]  # [mol(Chl) cell^-1]
        # ),
        # "mmol mol(Chl)-1 s-1 -> umol mg(Chl)-1 h-1": (
        #     1 / M_chl * 3600  # [mol(Chl) g(Chl)^-1]  # [s h^-1]
        # ),
        # "mmol mol(Chl)-1 s-1 -> umol ug(Chl)^-1 min^-1": (
        #     1e-3 * 1 / M_chl * 60  # [mol mmol^-1]  # [mol(Chl) g(Chl)^-1]  # [s min^-1]
        # ),
        # "mmol mol(Chl)-1 s-1 -> umol mg(Chl)^-1 min^-1": (
        #     1 / M_chl * 60  # [mol mmol^-1]  # [mol(Chl) g(Chl)^-1]  # [s min^-1]
        # ),
        "mmol mol(Chl)-1 -> g(CO2) cell-1": (
            M_CO2 * 1e-3 * n_chl_mol  # [g mol^-1]  # [g mg^-1]  # [mol(Chl) cell^-1]
        ),
        "mmol mol(Chl)-1 -> mmol g(Chl)-1": (1 / M_chl),  # [mol(Chl) g(Chl)^-1]
        "mmol mol(Chl)-1 -> mol g(Chl)-1": (
            1e-3 * 1 / M_chl  # [mol mmol^-1]  # [mol(Chl) g(Chl)^-1]
        ),
        "s-1 -> h-1": 3600,  # [s h^-1]
        "s-1 -> min-1": 60,  # [s min^-1]
    }
)


# ---- Module: module_electron_transport_chain ----

### Total concentrations of conserved quantities ###
c["PSIItot"] = {
    "value": (0.83),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of photosystem II complexes",
    "organism": "",
    "condition": "",
    "source": "",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["PSItot"] = {
    "value": (3.27),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of photosystem I complexes",
    "organism": "",
    "condition": "",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["Q_tot"] = {
    "value": 13,
    "unit": "mmol mol(Chl)^-1",
    "descr": "total PHOTOACTIVE PQ concentration",
    "organism": "Synechocystis sp. PCC6803",
    "condition": "constant illumination, PPFD 40 µmol m-2s-1, at 32 °C. BG-11 medium supplemented with 20 mM Hepes-NaOH pH 7.5, ambient air (AIR)",
    "source": "13 [1000(Chl)^-1] total PHOTOACTIVE PQ concentration (Khorobrykh2020)",
    "ref": "Khorobrykh2020",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["PC_tot"] = {
    "value": (
        22000
        * unit_conv(  # [cell^-1] total concentration of plastocyanin (PC_ox + PC_red) (Zavrel2019)
            "cell-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of plastocyanin (PC_ox + PC_red)",
    "organism": "Synechocystis sp. PCC 6803 substrain GT-L",
    "condition": "red light of 27.5-1100μmol photons m^−2 s^−1 with blue light of 27.5 μmol photons m^−2 s^−1.",
    "source": "22000 [cell^-1] total concentration of plastocyanin (PC_ox + PC_red)",
    "ref": "Zavrel2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

[c_PSIItot, c_PSItot, c_Q_tot, c_PC_tot] = unpack(
    [
        "PSIItot",
        "PSItot",
        "Q_tot",
        "PC_tot",
    ],
    c,
)


c["Fd_tot"] = {
    "value": (
        1.1 * c_PSItot  # [unitless] ratio of total ferredoxin (Fd_ox + Fd_red) to PSI
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of ferredoxin (Fd_ox + Fd_red)",
    "organism": "Synechocystis 6803",
    "condition": "34 °C in liquid BG11 medium buffered with Hepes (pH 7.4) and white light  of 45 μmol photons m−2 s−1 (",
    "source": "1.1 [unitless] ratio of total ferredoxin (Fd_ox + Fd_red) to PSI",
    "ref": "Moal2012",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["NADP_tot"] = {
    "value": (
        30
        * unit_conv(  # [nmol mg(Chl)^-1] total concentration of NADP species (NADP + NADPH) (Kauny2014)
            "umol g(Chl)-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of NADP species (NADP + NADPH)",
    "organism": "Synechocystis sp PCC 6803",
    "condition": "32°C in a CO2-enriched atmosphere and under continuous light (50 μmol photons m−2 s−1) up to a maximum concentration of 12 μg chl./ml",
    "source": "30 [nmol mg(Chl)^-1] total concentration of NADP species (NADP + NADPH)",
    "ref": "Kauny2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["NAD_tot"] = {
    "value": (
        50
        * 0.25  # [mM OD^-1] total concentration of NAD species (NAD + NADH) (Fig. 3A, Tanaka2021)
        * unit_conv(  # [nmol mg(Chl)^-1 (nM OD^-1)^-1] conversion factor (Tab. 1, Tanaka2021)
            "umol g(Chl)-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of NAD species (NAD + NADH)",
    "organism": " Synechocystis sp. PCC 6803 wild-type",
    "condition": "growth: 1.5% Bacto agar BG-11 medium plates, 30 mL liquid BG-11 medium  at 30 °C with air bubbling, white light illumination at  20 µmol m−2 s−1. pre-culture inoculated optical density of 0.02 at 730 nm (OD730) in 30 mL BG-11, measurements: light intensity of 800 μmol m−2 s−1",
    "source": "50 [mM OD^-1] total concentration of NAD species (NAD + NADH)",
    "ref": "Tanaka2021",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["AP_tot"] = {
    "value": (
        400
        * 1  # [pmol (10^8 cells)^-1] cellular content of ATP (Doello2018)
        / 0.4
        * 1e-8  # [mol(ATP) mol(ATP + ADP)^-1] ratio of ATP to total adenosine pool (Cano2018)
        * 1  # [cells 10^8 cells] conversion to cell^-1
        / n_chl_mol
        * 1e-9  # [cell mol(Chl)^-1]  # [mmol pmol^-1]
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "total concentration of adenosine species (ADP + ATP)",
    "organism": "Synechocystis sp. PCC 6803",
    "condition": "BG11 supplemented with 5 mm NaHCO3, continuous illumination (40–50 μmol photons m−2 s−1) and shaking (130–140 rpm) at 27°C.",
    "source": "400 [pmol (10^8 cells)^-1] cellular content of ATP",
    "ref": "Doello2018",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

[c_Fd_tot, c_NADP_tot, c_NAD_tot, c_AP_tot] = unpack(
    [
        "Fd_tot",
        "NADP_tot",
        "NAD_tot",
        "AP_tot",
    ],
    c,
)

# Concentration of phycobilisomes (not included in the model)
# c_PSIItot = ( # [mmol mol(Chl)^-1] total concentration of phycobilisomes (Zavrel2019)
#     28500 * # [cell^-1] total concentration of phycobilisomes (Zavrel2019)
#     1/NA * 1/n_chl_mol * 1e3)


### Physical and other constants ###

p["F"] = {
    "value": 96.485,
    "unit": "C mmol^-1",
    "descr": "Faraday's constant",
    "organism": "-",
    "condition": "-",
    "source": "9.6485e4 [C mol^-1] Faraday's constant",
    "ref": "Richardson2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["R"] = {
    "value": 0.0083,
    "unit": "J K^-1 mmol^-1",
    "descr": "ideal gas constant",
    "organism": "-",
    "condition": "-",
    "source": "8.3145 [J K^-1 mol^-1] ideal gas constant",
    "ref": "Richardson2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["T"] = {
    "value": (
        25 + 273.15  # [°C] temperature (set)  # offset of Kelvin to Celsius scale
    ),
    "unit": "K",
    "descr": "temperature",
    "organism": "-",
    "condition": "-",
    "source": "25 [°C] temperature",
    "ref": "set",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["bHi"] = {
    "value": 100.0,
    "unit": "unitless",
    "descr": "buffering constant of the thylakoid lumen",
    "organism": "-",
    "condition": "-",
    "source": "estimated",
    "ref": "estimated",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["bHo"] = {
    "value": 100.0 * 1 / f_V_lumen,
    "unit": "unitless",
    "descr": "buffering constant of the cytoplasm, assumed to be 1/f_V_lumen times larger",
    "organism": "-",
    "condition": "-",
    "source": "f_V_lumen, estimated",
    "ref": "estimated",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["cf_lumen"] = {
    "value": c_chl_lumen * 1e-3,
    "unit": "mol(Chl) ml^-1",
    "descr": "conversion factor for [mmol mol(Chl)^-1] -> [mol l^-1] for the thylakoid lumen",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "chl_lumen",
    "ref": "derived",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["cf_cytoplasm"] = {
    "value": c_chl_cyt * 1e-3,
    "unit": "mol(Chl) ml^-1",
    "descr": "conversion factor for [mmol mol(Chl)^-1] -> [mol l^-1] for the cytoplasm",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "chl_cyt",
    "ref": "derived",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["fCin"] = {
    "value": 100.0,
    "unit": "unitless",
    "descr": "ratio of intracellular to external CO2 concentration with activity of the CCM",
    "organism": "cyanobacteria",
    "condition": "various",
    "source": "the CCM-increased intracellular bicarbonate concentration can exceed the external by 100 - 1000 times",
    "ref": "Hagemann2021",
    "type": "parameter",
    "used": {"if": None, "not": ["update_CCM"]},
}

# Physical constants also used
RT = unpack("R") * unpack("T")  # [J mmol^-1] often used in thermdynamic calculations
dG_pH = (
    np.log(10) * RT
)  # [J mmol^-1] Gibbs free energy change in a system from increasing the pH by one


# # Light -> Excitation conversion
# p["cs_ps1"] = {
#     "value": np.array([0.02, 0.0025]),
#     "unit": "m^2 mg(Chl)^-1",
#     "descr": "absorption cross-section of ps1 chlorophyll and carotenoids in [Blue, Orange] light",
#     "organism": "",
#     "condition": "",
#     "source": "np.array([0.02, 0.0025]) [m^2 mg(Chl)^-1] absorption cross-section of ps1 chlorophyll and carotenoids in [Blue, Orange] light",
#     "ref": "Fuente2021",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# p["cs_ps2"] = {
#     "value": np.array([0.0015, 0]),
#     "unit": "m^2 mg(Chl)^-1",
#     "descr": "absorption cross-section of ps2 chlorophyll and carotenoids in [Blue, Orange] light",
#     "organism": "",
#     "condition": "",
#     "source": "np.array([0.0015, 0]) [m^2 mg(Chl)^-1] absorption cross-section of ps2 chlorophyll and carotenoids in [Blue, Orange] light",
#     "ref": "Fuente2021",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# p["cs_pbs"] = {
#     "value": np.array([0.00125, 0.015]),
#     "unit": "m^2 mg(Chl)^-1",
#     "descr": "absorption cross-section of pbs phycobiliproteins in [Blue, Orange] light",
#     "organism": "",
#     "condition": "",
#     "source": "np.array([0.00125, 0.015]) [m^2 mg(Chl)^-1] absorption cross-section of pbs phycobiliproteins in [Blue, Orange] light",
#     "ref": "Fuente2021",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# cs_ps1, cs_ps2, cs_pbs = unpack(["cs_ps1", "cs_ps2", "cs_pbs"])

# p["pbs_to_ps2"] = {  #
#     "value": 0.65,
#     "unit": "unitless",
#     "descr": "fraction of energy absorbed by PBS transferred to PS2",
#     "organism": "",
#     "condition": "",
#     "source": "0.65 [unitless] fraction of energy absorbed by PBS transferred to PS2 (0.55 in Akhtar2021)",
#     "ref": "Akhtar2021",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# pbs_to_ps2 = unpack("pbs_to_ps2")

# p["pbs_to_ps1"] = {
#     "value": 1 - pbs_to_ps2,
#     "unit": "unitless",
#     "descr": "fraction of energy absorbed by PBS transferred to PS1",
#     "organism": "",
#     "condition": "",
#     "source": "1 - pbs_to_ps2 [unitless] fraction of energy absorbed by PBS transferred to PS1",
#     "ref": "Akhtar2021",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# pbs_to_ps1 = unpack("pbs_to_ps1")


# p["excite_ps1"] = {
#     "value": (
#         (cs_ps1 + pbs_to_ps1 * cs_pbs)
#         * M_chl  # [m^2 mg(Chl)^-1] absorption cross-section of ps1, including pbs energy transfer in [Blue, Orange] light (Fuente2021)
#         * 1  # [mg(Chl) mmol(Chl)^-1]
#         / c_PSItot  # [mmol(Chl) umol(PSI)^-1] normalise to the PS concentration to get account for the the photon/PS ratio
#     ),
#     "unit": "m^2 umol^-1",
#     "descr": "absorption cross-section of ps1, including pbs energy transfer in [Blue, Orange] light",
#     "organism": "",
#     "condition": "",
#     "source": "cs_ps1, pbs_to_ps1, cs_pbs",
#     "ref": "derived",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
# p["excite_ps2"] = {
#     "value": (
#         (cs_ps2 + pbs_to_ps2 * cs_pbs)
#         * M_chl  # [m^2 mg(Chl)^-1] absorption cross-section of ps2, including pbs energy transfer in [Blue, Orange] light (Fuente2021)
#         * 1  # [mg(Chl) mmol(Chl)^-1]
#         / c_PSIItot  # [mmol(Chl) umol(PSII)^-1] normalise to the PS concentration to get account for the the photon/PS ratio
#     ),
#     "unit": "m^2 umol^-1",
#     "descr": "absorption cross-section of ps2, including pbs energy transfer in [Blue, Orange] light",
#     "organism": "",
#     "condition": "",
#     "source": "cs_ps2, pbs_to_ps2, cs_pbs",
#     "ref": "derived",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }


### Initial cellular concentrations of compounds ###

# Explicitly stated compounds
c["PSII"] = {
    "value": 0.5 * c_PSIItot,
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of unquenched PSII (guessed from ca. 50% reduced plastoquinone)",
    "organism": "synechocystis sp. PCC 6803 substrain GT-L",
    "condition": "-",
    "source": "guessed from ca. 50 % reduced plastoquinone",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["Q_red"] = {
    "value": (
        0.446
        * c_Q_tot  # [unitless] fraction of PHOTOACTIVE plastoquinone reduced in 40 umol m^-2 s^-1 irradiation (Khorobrykh2020)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of reduced, PHOTOACTIVE plastoquinone in 40 umol m^-2 s^-1 irradiation",
    "organism": "Synechocystis sp. PCC6803",
    "condition": "ambient air (AIR)",
    "source": "0.446 [unitless] fraction of PHOTOACTIVE plastoquinone reduced in 40 umol m^-2 s^-1 irradiation",
    "ref": "Khorobrykh2020",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c["Q_red_dark"] = {
    "value": (
        0.223
        * c_Q_tot  # [unitless] fraction of PHOTOACTIVE plastoquinone reduced in darkness (Khorobrykh2020)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of reduced, PHOTOACTIVE plastoquinone in darkness",
    "organism": "Synechocystis sp. PCC6803",
    "condition": "ambient air (AIR)",
    "source": "0.223 [unitless] fraction of PHOTOACTIVE plastoquinone reduced in darkness",
    "ref": "Khorobrykh2020",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c["O2"] = {
    "value": (
        230
        * unit_conv(  # [umol l^-1] concentration of oxygen in air saturated water: 230 uM (Kihara2014)
            "umol l-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of oxygen in the cell",
    "organism": " Synechocystis",
    "condition": "correspond to the light conditions under which the oxygen production rate per cell is maximal",
    "source": "230 [umol l^-1] concentration of oxygen in air saturated water: 230 uM",
    "ref": "Kihara2014",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["PC_ox"] = {
    "value": (
        0.1 * c_PC_tot  # [unitless] fraction of oxidised plastocyanin (Schreiber2017)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of oxidised plastocyanin (aerobic)",
    "organism": "plant and cyanobacteria",
    "condition": "various",
    "source": "0.1 [unitless] fraction of oxidised plastocyanin (aerobic)",
    "ref": "Schreiber2017",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["Fd_ox"] = {
    "value": (
        0.9
        * c_Fd_tot  # [unitless] fraction of oxidised ferredoxin with O2 (Schreiber2017)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of oxidised ferredoxin (aerobic)",
    "organism": "plant & cyanobacteria",
    "condition": "various",
    "source": "0.9 [unitless] fraction of oxidised ferredoxin (aerobic)",
    "ref": "Schreiber2017",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["NADPH"] = {
    "value": (0.75 * c_NADP_tot),  # [unitless] fraction of reduced NADPH (Cooley2001)
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of NADPH",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "cells  grown  at  45mmol  of  photons  m-2s-1, liquid BG-11 medium (20) at 30°C, ambient air, harvested at anoptical density at 730 nm (OD730) of 0.5",
    "source": "0.75 [unitless] fraction of reduced NADPH",
    "ref": "Cooley2001",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["NADH"] = {
    "value": (
        0.32
        * c_NAD_tot  # [unitless] approximate fraction of reduced NADH (Fig. 3B, Tanaka2021)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of NADH",
    "organism": " Synechocystis sp. PCC 6803 wild-type",
    "condition": "growth: 1.5% Bacto agar BG-11 medium plates, 30 mL liquid BG-11 medium  at 30 °C with air bubbling, white light illumination at  20 µmol m−2 s−1. pre-culture inoculated optical density of 0.02 at 730 nm (OD730) in 30 mL BG-11, measurements: light intensity of 800 μmol m−2 s−1",
    "source": "0.32 [unitless] approximate fraction of reduced NADH",
    "ref": "Tanaka2021",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["ATP"] = {
    "value": (
        400
        * 1e-8  # [pmol (10^8 cells)^-1] concentration of ATP (Doello2018)
        * 1  # [cells 10^8 cells] conversion to cell^-1
        / n_chl_mol
        * 1e-9  # [cell mol(Chl)^-1]  # [mmol pmol^-1]
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of ATP",
    "organism": "Synechocystis sp. PCC 6803",
    "condition": "BG11 supplemented with 5 mm NaHCO3, continuous illumination (40–50 μmol photons m−2 s−1) and shaking (130–140 rpm) at 27°C.",
    "source": "400 [pmol (10^8 cells)^-1] concentration of ATP",
    "ref": "Doello2018",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["PG"] = {
    "value": (
        1e-6
        * unit_conv(  # [umol ug(Chl)^-1] estimated detection limit of the method used by Huege2011, the (phospho)glycolate concentration is below it (Fig. 3, Huege2011)
            "mol g(Chl)-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of (2-phospho) glycolate",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium; 29°C; illuminated with Osram L58 W32/3 at 130 µmol photons m-2 s-1 ambient air or 5% CO2 enriched ",
    "source": "1e-6 [umol ug(Chl)^-1] estimated detection limit of the method used by Huege2011, the (phospho)glycolate concentration is below it",
    "ref": "Huege2011",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["succinate"] = {
    "value": 2,
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of succinate",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["fumarate"] = {
    "value": 2,
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of fumarate",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["O2ext"] = {
    "value": (
        230
        * unit_conv(  # [umol l^-1] concentration of oxygen in air saturated water: 230 uM (Kihara2014)
            "umol l-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of oxygen in the surrounding medium",
    "organism": "-",
    "condition": "-",
    "source": "230 [umol l^-1] concentration of oxygen in air saturated water",
    "ref": "Kihara2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
c["GA"] = {
    "value": 0.5,
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of glycerate",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["3PGA"] = {
    "value": 2000,
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of 3-phospho glycerate (including all other sugars)",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["CO2ext"] = {
    "value": (
        322e-4
        * 0.0004  # [mol l^-1 atm^-1] solubility of CO2 in 25 °C water with ~10 ‰ Cl^- ions (Li1971)
        * unit_conv(  # [atm] partial pressure of CO2 (Wikipedia)
            "mol l-1 -> mmol mol(Chl)-1"
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "saturated concentration of CO2 in 25 °C water with ~10 ‰ Cl^- ions",
    "organism": "-",
    "condition": "-",
    "source": "322e-4 [mol l^-1 atm^-1] solubility of CO2 in 25 °C water with ~10 ‰ Cl^- ions",
    "ref": "Li1971",
    "type": "parameter",
    "used": {"if": None, "not": ["update_CCM"]},
}
c["CO2"] = {  # FIXME: Adapt to new CCM
    "value": (
        unpack("CO2ext", c)
        * unpack(  # [mmol mol(Chl)^-1] concentration of CO2 in 25 °C water with ~10 ‰ Cl^- ions at 0.0004 atm CO2 (Li1971)
            "fCin"
        )  # [unitless] factor of intracellular to external CO2 concentration by activity of the CCM (estimated)
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of CO2 in the cell increased by activity of the CCM",
    "organism": "-",
    "condition": "-",
    "source": "estimated",
    "ref": "estimated",
    "type": "initial concentration",
    "used": {"if": None, "not": ["update_CCM"]},
}
c["Flva"] = {
    "value": 0,
    "unit": "unitless",
    "descr": "fraction of Fd-activated Flv enzyme",
    "organism": "-",
    "condition": "-",
    "source": "0 [unitless] fraction of Fd-activated Flv enzyme",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": ["update_Flv_hill"]},
}
c["CBBa"] = {
    "value": 0,
    "unit": "unitless",
    "descr": "fraction of Fd-activated, lumped enzymes of the CBB",
    "organism": "-",
    "condition": "-",
    "source": "0 [unitless] fraction of Fd-activated, lumped enzymes of the CBB",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
[
    c_PSII,
    c_Q_red,
    c_Q_red_dark,
    c_O2,
    c_PC_ox,
    c_Fd_ox,
    c_NADPH,
    c_NADH,
    c_ATP,
    c_PG,
    c_succinate,
    c_fumarate,
    c_O2ext,
    c_GA,
    c_3PGA,
    c_CO2ext,
    c_CO2,
    c_Flva,
    c_CBBa,
] = unpack(
    [
        "PSII",
        "Q_red",
        "Q_red_dark",
        "O2",
        "PC_ox",
        "Fd_ox",
        "NADPH",
        "NADH",
        "ATP",
        "PG",
        "succinate",
        "fumarate",
        "O2ext",
        "GA",
        "3PGA",
        "CO2ext",
        "CO2",
        "Flva",
        "CBBa",
    ],
    c,
)

# Protons
c["Hi"] = {
    "value": calculate_Hlumen(5.0, unpack("cf_lumen")),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of lumenal protons in 10^4 uE cm^-1 s^-1 light",
    "organism": "Agmenellum quadruplicatum (strain PR-6, PCC 7002, ATCC 27264)",
    "condition": "suspension containing 0.82 mg Chl-ml^-1, External pH was 7.5,  grown in ASP-2 medium with 18 g L^-1(0.3 M) NaCl. Growth temperature 33°C, light intensity 50 to 100 uE cm^-2 s^-1, bubbled with 1% CO2 in air.",
    "source": "pH 5",
    "ref": "Belkin1987",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["Hi_dark"] = {
    "value": calculate_Hlumen(5.5, unpack("cf_lumen")),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of lumenal protons in darkness",
    "organism": "Agmenellum quadruplicatum (strain PR-6, PCC 7002, ATCC 27264)",
    "condition": "suspension containing 0.82 mg Chl-ml^-1, External pH was 7.5,  grown in ASP-2 medium with 18 g L^-1(0.3 M) NaCl. Growth temperature 33°C, light intensity 50 to 100 uE cm^-2 s^-1, bubbled with 1% CO2 in air.",
    "source": "pH 5.5",
    "ref": "Belkin1987",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c["Ho"] = {
    "value": calculate_Hlumen(7.5, unpack("cf_cytoplasm")),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of cytoplasmic protons in 10^4 uE cm^-1 s^-1 light",
    "organism": "Agmenellum quadruplicatum (strain PR-6, PCC 7002, ATCC 27264)",
    "condition": "suspension containing 0.82 mg Chl-ml^-1, External pH was 7.5,  grown in ASP-2 medium with 18 g L^-1(0.3 M) NaCl. Growth temperature 33°C, light intensity 50 to 100 uE cm^-2 s^-1, bubbled with 1% CO2 in air.",
    "source": "pH 7.5",
    "ref": "Belkin1987",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c["Ho_dark"] = {
    "value": calculate_Hlumen(7, unpack("cf_cytoplasm")),
    "unit": "mmol mol(Chl)^-1",
    "descr": "initial concentration of cytoplasmic protons in darkness",
    "organism": "Agmenellum quadruplicatum (strain PR-6, PCC 7002, ATCC 27264)",
    "condition": "suspension containing 0.82 mg Chl-ml^-1, External pH was 7.5,  grown in ASP-2 medium with 18 g L^-1(0.3 M) NaCl. Growth temperature 33°C, light intensity 50 to 100 uE cm^-2 s^-1, bubbled with 1% CO2 in air.",
    "source": "pH 7",
    "ref": "Jiang2013,Belkin1987",
    "type": "helper",
    "used": {"if": None, "not": None},
}
c_Hi, c_Hi_dark, c_Ho, c_Ho_dark = unpack(["Hi", "Hi_dark", "Ho", "Ho_dark"], c)

# Compounds sharing a conserved quantity
c["Q_ox"] = {
    "value": (c_Q_tot - c_Q_red),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of oxidised, PHOTOACTIVE plastoquinone in 40 umol m^-2 s^-1 irradiation",
    "organism": "Synechocystis sp. PCC6803",
    "condition": "ambient air (AIR)",
    "source": "0.446 [unitless] fraction of PHOTOACTIVE plastoquinone reduced in 40 umol m^-2 s^-1 irradiation",
    "ref": "Khorobrykh2020",
    "type": "initial concentration",
    "used": {"if": None, "not": None},
}
c_Q_ox = unpack(
    "Q_ox", c
)  # [mmol mol(Chl)^-1]  concentration of oxidised PHOTOACTIVE plastoquinone in 40 umol m^-2 s^-1 irradiation (Khorobrykh2020)
c_Q_ox_dark = (
    c_Q_tot - c_Q_red_dark
)  # [mmol mol(Chl)^-1]  concentration of oxidised PHOTOACTIVE plastoquinone in darkness (Khorobrykh2020)
c_PC_red = (
    c_PC_tot - c_PC_ox
)  # [mmol mol(Chl)^-1] initial concentration of reduced plastocyanin
c_Fd_red = (
    c_Fd_tot - c_Fd_ox
)  # [mmol mol(Chl)^-1] initial concentration of reduced ferredoxin
c_NADP = c_NADP_tot - c_NADPH  # [mmol mol(Chl)^-1] initial concentration of NADP
c_NAD = c_NAD_tot - c_NADH  # [mmol mol(Chl)^-1] initial concentration of NAD
c_ADP = c_AP_tot - c_ATP  # [mmol mol(Chl)^-1] initial concentration of ADP


### Stoichiometry of the lumped Respiration reaction ###
respiratory_fluxes = {  # [AU] rates of fluxes oxidising carbon compounds during respiration (Yang2002)
    "OPP": 90.2
    + (
        68.5 - 55.7
    ),  # [AU] metabolic flux through the oxidative pentose phosphate pathway and a combination of PPC and ME (Fig.1, Yang2002)
    "noTCA": 117.5,  # [AU] decarboxylating metabolic flux through neither OPP nor TCA (estimated as PDH flux) (Fig.1, Yang2002)
}
respiratory_fluxes[
    "TCA"
] = (  # [AU] etabolic flux through the complete TCA cycle (Ueda2018)
    respiratory_fluxes["noTCA"]
    * 0.05
    * 3  # When considering an alternative alpha-KG -> succinate pathway, the SDH reaction carries approximately 5% of PDH flux (Fig. 3, Ueda2018; You2015)
)  # One complete TCA cycle poduces 3 CO2 as compared to one in OPP and PDH

respiratory_flux_fractions = {
    key: value / np.sum(list(respiratory_fluxes.values()))
    for key, value in respiratory_fluxes.items()
}  # [unitless] fractions of the fluxes of the total respiratory flux


# Stoichiometry of the oxidative pentose phosphate pathway (Ueda2018)
OPP_stoichiometry = {"3PGA": -1, "CO2": 3, "NADPH": 5, "Ho": 5}  #

# Stoichiometry of the tricarboxylic acid cycle (Mills2020)
TCA_stoichiometry = {  #
    "3PGA": -1,
    "fumarate": -1,
    "CO2": 3,
    "succinate": 1,
    "ATP": 1,
    "NADPH": 1,
    "NADH": 3,
    "Ho": 4,
}

# Stoichiometry of 3PGA (completely) respired to CO2 within glycolysis or incomplete TCA skipping SDH
noTCA_stoichiometry = {"3PGA": -1, "CO2": 3, "ATP": 1, "NADH": 5, "Ho": 5}  #

# Calculate the combined stoichiometry
respiratory_stoichiometry = {
    key: (
        OPP_stoichiometry.get(key, 0) * respiratory_flux_fractions["OPP"]
        + TCA_stoichiometry.get(key, 0) * respiratory_flux_fractions["TCA"]
        + noTCA_stoichiometry.get(key, 0) * respiratory_flux_fractions["noTCA"]
    )
    for key in TCA_stoichiometry
}


### Standard electrode potentials ###

p["E0_QA"] = {
    "value": -0.14,
    "unit": "V",
    "descr": "standard electrode potential of the reduction of PS2 plastoquinone A",
    "organism": "various",
    "condition": "various",
    "source": "-0.14 [V] midpoint potential of the reduction of PS2 plastoquinone A",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["E0_PQ"] = {
    "value": (  # >> changed: adapted value to Lewis2022 <<
        0.12  # [V] midpoint potential of the reduction of free plastoquinone
        + midtoelec(
            2, 2, 7
        )  # [V] correction term from midpoint potential (pH 7) to the standard electrode potential (n=2; m=2)
    ),
    "unit": "V",
    "descr": "standard electrode potential of the reduction of free plastoquinone",
    "organism": "various",
    "condition": "various",
    "source": "0.12 [V] midpoint potential of the reduction of free plastoquinone",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["E0_PC"] = {
    "value": 0.35,
    "unit": "V",
    "descr": "standard electrode potential of the reduction of free plastocyanin",
    "organism": "various",
    "condition": "various",
    "source": "0.35 [V] midpoint potential of the reduction of free plastocyanin",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["E0_P700"] = {
    "value": 0.41,
    "unit": "V",
    "descr": "standard electrode potential of the reduction of the oxidised PS1 reaction center",
    "organism": "various",
    "condition": "various",
    "source": "0.48 [V] midpoint potential of the reduction of the oxidised PS1 reaction center",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["E0_FA"] = {
    "value": -0.58,
    "unit": "V",
    "descr": "standard electrode potential of the reduction of PS1 iron-sulfur cluster A",
    "organism": "various",
    "condition": "various",
    "source": "-0.58 [V] midpoint potential of the reduction of PS1 iron-sulfur cluster A",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["E0_Fd"] = {
    "value": -0.41,
    "unit": "V",
    "descr": "standard electrode potential of the reduction of free ferredoxin",
    "organism": "various",
    "condition": "various",
    "source": "-0.41 [V] midpoint potential of the reduction of free ferredoxin",
    "ref": "Lewis2022",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
# p["E0_O2/H2O"] = {
#     "value": (
#         0.816
#         + midtoelec(  # [V] midpoint potential of the reduction of oxygen to H2O (Falkowski2007)
#             4, 4
#         )  # [V] correction term from midpoint potential (pH 7) to the standard electrode potential (n=4; m=4)
#     ),
#     "unit": "V",
#     "descr": "standard electrode potential of the reduction of oxygen to H2O",
#     "organism": "-",
#     "condition": "-",
#     "source": "0.816 [V] midpoint potential of the reduction of oxygen to H2O",
#     "ref": "Falkowski2007",
#     "type": "parameter",
#     "used": {"if": None, "not": None},
# }
p["E0_NADP"] = {
    "value": (
        -0.32
        + midtoelec(  # [V] midpoint potential of the reduction of NADP to NADPH (Falkowski2007)
            2, 1
        )  # [V] correction term from midpoint potential (pH 7) to the standard electrode potential (n=2; m=1)
    ),
    "unit": "V",
    "descr": "standard electrode potential of the reduction of NADP to NADPH",
    "organism": "-",
    "condition": "-",
    "source": "-0.32 [V] midpoint potential of the reduction of NADP to NADPH",
    "ref": "Falkowski2007",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
# p["E0_NAD"] = {
#     "value": (
#         -0.32
#         + midtoelec(  # [V] midpoint potential of the reduction of NAD to NADH (Falkowski2007)
#             2, 1
#         )  # [V] correction term from midpoint potential (pH 7) to the standard electrode potential (n=2; m=1)
#     ),
#     "unit": "V",
#     "descr": "standard electrode potential of the reduction of NAD to NADH",
#     "organism": "",
#     "condition": "",
#     "source": "-0.32 [V] midpoint potential of the reduction of NAD to NADH",
#     "ref": "Falkowski2007",
#     "type": "depricated",
# "used": {"if": None, "not": None},
# }
p["E0_succinate/fumarate"] = {
    "value": (
        0.03
        + midtoelec(  # [V] midpoint potential of the reduction of fumarate to succinate (Falkowski2007)
            2, 2
        )  # [V] correction term from midpoint potential (pH 7) to the standard electrode potential (n=2; m=2)
    ),
    "unit": "V",
    "descr": "standard electrode potential of the reduction of fumarate to succinate",
    "organism": "-",
    "condition": "-",
    "source": "0.03 [V] midpoint potential of the reduction of fumarate to succinate",
    "ref": "Falkowski2007",
    "type": "parameter",
    "used": {"if": None, "not": None},
}


### Rate constants ###

# Calculate Keq_FNR which is necessary for the calculation of k_FN_rev
# Calculate the standard Gibbs free energy
def dG0_FNR(pHcytoplasm, E0_Fd, F, E0_NADP, dG_pH):
    DG1 = -E0_Fd * F
    DG2 = -2 * E0_NADP * F + dG_pH * pHcytoplasm
    dG0 = -2 * DG1 + DG2
    return dG0


# Calculate the equillibrium constant under dark conditions
Keq_FNR = np.exp(
    -dG0_FNR(
        calculate_pH(calculate_molarHcytoplasm(c_Ho_dark, unpack("cf_cytoplasm"))),
        unpack("E0_Fd"),
        unpack("F"),
        unpack("E0_NADP"),
        dG_pH,
    )
    / RT
)

# Calculate the rate constants
# PS2 rate constants
p["kH0"] = {
    "value": 5e8,
    "unit": "s^-1",
    "descr": "rate constant of (unregulated) excitation quenching by heat",
    "organism": "various",
    "condition": "various",
    "source": "5e8 [s^-1] rate of (unregulated) excitation quenching by heat",
    "ref": "Ebenhoh2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kHst"] = {
    "value": 1e9,  # >> changed: corrected the value <<
    "unit": "s^-1",
    "descr": "rate constant of state transition regulated excitation quenching by heat",
    "organism": "various",
    "condition": "various",
    "source": "1e9 [s^-1] rate of state transition regulated excitation quenching by heat",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kF"] = {
    "value": 6.25e8,
    "unit": "s^-1",
    "descr": "rate constant of excitation quenching by fluorescence",
    "organism": "various",
    "condition": "various",
    "source": "6.25e8 [s^-1] rate of excitation quenching by fluorescence",
    "ref": "Ebenhoh2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k2"] = {
    "value": 5e9 * 0.5,
    "unit": "s^-1",
    "descr": "rate constant of excitation quenching by photochemistry",
    "organism": "various",
    "condition": "various",
    "source": "5e9 [s^-1] rate of excitation quenching by photochemistry, adapted by factor 0.5 to achieve Fm/F0 ca. 1.6",
    "ref": "Ebenhoh2014,Bernat2009",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kPQred"] = {
    "value": 250,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PQ reduction via PS2",
    "organism": "various",
    "condition": "various",
    "source": "250 [mol(Chl) mmol^-1 s^-1] rate of PQ reduction via PS2",
    "ref": "Matuszynska2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

p["kQuench"] = {  # >> changed: changed to the transient value in test_time_series <<
    "value": 2.5e-5,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PS2 quenching by Q_red",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_statetransitions_hill"]},
}
p["kUnquench"] = {  # >> changed: changed to the transient value in test_time_series <<
    "value": 1.25e-3,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PS2 unquenching by Q_ox",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_statetransitions_hill"]},
}

# Rate constants of consumption reactions
p["kATPconsumption"] = {
    "value": 0.3,
    "unit": "s^-1",
    "descr": "rate constant of ATP consumption by processes other than the CBB",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kNADHconsumption"] = {
    "value": 10,
    "unit": "s^-1",
    "descr": "rate constant of NADH consumption by processes other than NDH",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

# Rate constants of Fd-mediated enzyme activiation reactions
p["kFlvactivation"] = {
    "value": 0.5,
    "unit": "s^-1",
    "descr": "rate constant of Flv activation by reduced Fd",
    "organism": "",
    "condition": "",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_Flv_hill"]},
}
p["kFlvdeactivation"] = {
    "value": 0.1,
    "unit": "s^-1",
    "descr": "rate constant of Flv deactivation by oxidised Fd",
    "organism": "",
    "condition": "",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_Flv_hill"]},
}
p["kCBBactivation"] = {
    "value": 5e-2,
    "unit": "s^-1",
    "descr": "rate constant of CBB activation by reduced Fd",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_CBBactivation_MM", "update_CBBactivation_hill"]},
}  # (TODO: GET SOURCE FOR TIMING)
p[
    "kCBBdeactivation"
] = {  # >> changed: changed to the transient value in test_time_series <<
    "value": 2.5e-3,
    "unit": "s^-1",
    "descr": "rate constant of CBB deactivation by oxidised Fd",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": ["update_CBBactivation_MM", "update_CBBactivation_hill"]},
}  # (TODO: GET SOURCE FOR TIMING)

# PS1 rate constants
p["kPCox"] = {
    "value": 2500,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PC oxidation via PS1",
    "organism": "various",
    "condition": "various",
    "source": "2500 [mol(Chl) mmol^-1 s^-1] rate of PC oxidation via PS1",
    "ref": "Matuszynska2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kFdred"] = {
    "value": 2.5e5,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of Fd reduction via PS1",
    "organism": "various",
    "condition": "various",
    "source": "2.5e5 [mol(Chl) mmol^-1 s^-1] rate of Fd reduction via PS1",
    "ref": "Matuszynska2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_F1"] = {  # >> changed: lowered value to 1 <<
    "value": 1,
    "unit": "s^-1",
    "descr": "rate constant of excitation quenching via fluorescence",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

# Other ETC rate constants
p["k_ox1"] = {
    "value": (
        3
        * unit_conv(  # [umol(O2) mg(Chl)^-1 h^-1] approximate rate of oxygen reduction via bd-type (Cyd) terminal oxidases (Ermakova2016)
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_Q_red_dark * 1 / c_O2 * 1 / c_Ho_dark)  # normalise by the substrates
    ),
    "unit": "mol(Chl)^2 mmol^-2 s^-1",
    "descr": "rate constant of oxygen reduction via bd-type (Cyd) terminal oxidases",
    "organism": "Synechocystis sp. PCC 6803 & mutants lacking respiratory terminal oxidases",
    "condition": "BG11 medium buffered with 10 mM TES-KOH (pH 8.2), continuous illumination of 50 mmol photons m-2 s-1 (photosynthetically active radiation), 3% CO2, and 30°C with gentle agitation (120 rpm).",
    "source": "3 [umol(O2) mg(Chl)^-1 h^-1] approximate rate of oxygen reduction via bd-type (Cyd) terminal oxidases",
    "ref": "Ermakova2016",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_Q"] = {  # >> changed: corrected and increased source value
    "value": (
        1
        / 10
        * 0.5  # [ms] 10 ms time for reduction of the half-total PC at the end of a 8100 umol m^-2 s^-1 red light pulse, INCREASED BY FACTOR 40 (Fig.3A, Setif2020)
        * c_PC_tot
        * 1  # [mmol mol(Chl)^⁻1] half of the total PC pool is reduced
        / 2
        * 1e3  # 2 PC are produced per cytob6f reaction
        * (  # [ms s^-1]  # normalise by the substrates
            1
            / (0.5 * c_PC_tot)
            * 1
            / c_Q_tot
            * 1  # assuming that the PQ pool is completely reduced by the strong light pulse
            / c_Ho_dark
        )
        * 10  # estimated factor for cytob6f not being the bottleneck -> likely PQ is not fully reduced (PS1 continuously being reduced) and the initial slope of PC reduction is steeper
    ),
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PC reduction by the cytochrome b6f complex",
    "organism": "WT and mutant strains from Syn. 6803",
    "condition": "grown at 25 °C in BG-11, buffered at pH 7.5 by 20 mM TES-KOH, on a rotary shaker with a light intensity of 150 μmoles photons m−2 s−1 in 2% CO2.",
    "source": "1/10 [ms] 10 ms time for reduction of the half-total PC at the end of a 8100 umol m^-2 s^-1 red light pulse, INCREASED BY FACTOR 10",
    "ref": "Setif2020",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_NDH"] = {
    "value": (
        20
        * 0.5  # [umol(electrons) mg(Chl)^-1 h^-1] rate of electron flux through NDH-2 (Cooley2001)
        * unit_conv(  # 2 electrons needed per reaction
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_Q_ox_dark * 1 / c_NADH * 1 / c_Ho_dark)  # normalise by the substrates
    ),
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PQ reduction by NDH-2",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "cells  grown  at  45mmol  of  photons  m-2s-1, liquid BG-11 medium (20) at 30°C, ambient air, harvested at anoptical density at 730 nm (OD730) of 0.5",
    "source": "20 [umol(electrons) mg(Chl)^-1 h^-1] rate of electron flux through NDH-2",
    "ref": "Cooley2001",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_SDH"] = {
    "value": (
        70
        * 0.5  # [umol(electrons) mg(Chl)^-1 h^-1] rate of electron flux through SDH (Cooley2001)
        * unit_conv(  # 2 electrons needed per reaction
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_Q_ox_dark * 1 / c_succinate)  # normalise by the substrates
    ),
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PQ reduction by SDH",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "cells  grown  at  45mmol  of  photons  m-2s-1, liquid BG-11 medium (20) at 30°C, ambient air, harvested at anoptical density at 730 nm (OD730) of 0.5",
    "source": "70 [umol(electrons) mg(Chl)^-1 h^-1] rate of electron flux through SDH",
    "ref": "Cooley2001",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_O2"] = {
    "value": (
        20
        * unit_conv(  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen consumtion by Flv 1/3 in dark-light transition (Ermakova2016)
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_Fd_red * 1 / c_O2 * 1 / c_Ho)  # normalise by the substrates
    ),
    "unit": "mol(Chl)^2 mmol^-2 s^-1",
    "descr": "rate constant of Fd oxidation by Flv 1/3",
    "organism": "Synechocystis sp. PCC 6803 & mutants lacking respiratory terminal oxidases",
    "condition": "BG11 medium buffered with 10 mM TES-KOH (pH 8.2), continuous illumination of 50 mmol photons m-2 s-1 (photosynthetically active radiation), 3% CO2, and 30°C with gentle agitation (120 rpm).",
    "source": "20 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen consumtion by Flv 1/3 in dark-light transition",
    "ref": "Ermakova2016",
    "type": "parameter",
    "used": {"if": None, "not": ["update_Flv_hill"]},
}
p["k_FN_fwd"] = {
    "value": (
        1
        / 8
        * 0.5  # [ms] 8 ms time for reduction of half the NADP reduced during a saturating flash (Kauny2014)
        * 25.5
        * 1  # [nmol l^-1] half of the apparent concentration of NADP reduced during a saturating flash (Kauny2014)
        / 3
        * 1  # approximate fluorescence enhancement factor (FEF) leding to overestimation of the reduced NADP (Kauny2014)
        / 2.2
        * M_chl  # [ug(Chl) ml^-1] concentration of chl in the sample (Kauny2014)
        * (  # [g(Chl) mol(Chl)^-1)]  # normalise by the substrates
            1
            / (c_NADP_tot * 0.6)
            * 1  # ca. 60% of the NADP is oxidised in darkness (Kauny2014)
            / c_Fd_tot
        )
    ),
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of NADP reduction by FNR",
    "organism": "Synechocystis sp PCC 6803",
    "condition": "32°C in a CO2-enriched atmosphere and under continuous light (50 μmol photons m−2 s−1) up to a maximum concentration of 12 μg chl./ml",
    "source": "1/8 [ms] 8 ms time for reduction of half the NADP reduced during a saturating flash",
    "ref": "Kauny2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_FN_rev"] = {
    "value": (  # >> changed: reduced rate by accounting for NADPH fraction
        8.3
        * 4  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction in the dark, should roughly match the rate of electron flux trough FNR (Ermakova2016)
        / 2
        * unit_conv(  # [unitless] reduction of one O2 corresponds to 4 electrons taken up, while one lumped FNR reaction carries 2
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * Keq_FNR  # Account for the division of k_FN_rev by Keq in calculate_v
        * (
            respiratory_stoichiometry["NADPH"] / 5
        )  # Account for the fraction of electrons flowing through NADPH (5 total)
        * (  # normalise by the substrates
            1
            / (c_NADP_tot * (1 - 0.6))
            * 1  # ca. 60% of the NADP is oxidised in darkness (Kauny2014)
            / c_Fd_tot  # Assuming that the ferredoxin pool is almost completely oxidised in the dark
        )
    ),
    "unit": "mol(Chl)^3 mmol^-3 s^-1",
    "descr": "rate constant of reverse flux through FNR in darkness",
    "organism": "Synechocystis sp PCC 6803",
    "condition": "32°C in a CO2-enriched atmosphere and under continuous light (50 μmol photons m−2 s−1) up to a maximum concentration of 12 μg chl./ml",
    "source": "8.3 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction in the dark, should roughly match the rate of electron flux trough FNR",
    "ref": "Kauny2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_pass"] = {
    "value": 0.01,
    "unit": "mmol mol(Chl)^-1 s^-1",
    "descr": "rate constant of protons leaking across the thylakoid membrane per delta pH",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["k_NQ"] = {
    "value": 100,
    "unit": "mol(Chl) mmol^-1 s^-1",
    "descr": "rate constant of PQ reduction by NDH",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "BG-11 medium; 28°C; ambient air; iluminated at 220 μE m−2 s−1",
    "source": "fit to: 35 % of electrons passing through PS1 are in cyclic flow",
    "ref": "Theune2021",
    "type": "parameter",
    "used": {"if": None, "not": ["update_NQ_MM"]},
}
p["k_aa"] = {
    "value": (
        4
        * unit_conv(  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction via aa3-type (COX) terminal oxidases (Ermakova2016)
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_PC_red * 1 / c_O2 * 1 / c_Ho_dark)  # normalise by the substrates
        * 2
    ),
    "unit": "mol(Chl)^2 mmol^-2 s^-1",
    "descr": "rate constant of oxygen reduction via aa3-type (COX) terminal oxidases",
    "organism": "Synechocystis sp. PCC 6803 & mutants lacking respiratory terminal oxidases",
    "condition": "BG11 medium buffered with 10 mM TES-KOH (pH 8.2), continuous illumination of 50 mmol photons m-2 s-1 (photosynthetically active radiation), 3% CO2, and 30°C with gentle agitation (120 rpm).",
    "source": "4 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction via aa3-type (COX) terminal oxidases, INCREASED BY FACTOR 2",
    "ref": "Ermakova2016",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kRespiration"] = {
    "value": (
        8.3
        * 4  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction in the dark, should match the rate of electron carriers produces by respiration(Ermakova2016)
        / 2
        * 1  # [NADPH O2^-1] reduction of one O2 corrsponds to 4 electrons taken up while one NADPH delivers 2 electrons (assuming that mainly NADPH introduces electrons into respiratory flow)
        / (respiratory_stoichiometry["NADPH"])
        * unit_conv(  # [reactions NADPH^-1] assuming that mainly NADPH introduces electrons into respiratory flow scale the flux so that the respirations NADPH output matches the expected electron output
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (
            1 / c_fumarate * 1 / c_ADP * 1 / c_NAD * 1 / c_NADP
        )  # normalise by the substrates
        / 20  # Fitting dark phase to expected value, due to lower ATP and NADPH levels in the dark
    ),
    "unit": "mol(Chl)^3 mmol^-3 s^-1",
    "descr": "rate constant of 3PGA oxidation and fumarate reduction by glycolysis and the TCA cycle",
    "organism": "Synechocystis sp. PCC 6803 & mutants lacking respiratory terminal oxidases",
    "condition": "BG11 medium buffered with 10 mM TES-KOH (pH 8.2), continuous illumination of 50 mmol photons m-2 s-1 (photosynthetically active radiation), 3% CO2, and 30°C with gentle agitation (120 rpm).",
    "source": "8.3 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen reduction in the dark, should match the rate of electron carriers produces by respiration, REDUCED BY FACTOR 20",
    "ref": "Ermakova2016",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kO2out"] = {
    "value": (
        250
        * 1  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen diffusion out of the cell, assuming O2 efflux of 62.05 mmol mol(Chl)^-1 s^-1 and an O2 difference of 0.064 uM (Kihara2014)
        / 0.064
        * c_chl  # [umol(O2) l^-1] oxygen concentration difference, used to normalise (Kihara2014)
        * 1e3  # [mol(Chl) l^-1]
        * unit_conv(["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"])  # [mmol mol^-1]
    ),
    "unit": "s^-1",
    "descr": "rate constant of oxygen diffusion out of the cell",
    "organism": "Synechocystis",
    "condition": "correspond to the light conditions under which the oxygen production rate per cell is maximal",
    "source": "250 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen diffusion out of the cell, assuming O2 efflux of 62.05 mmol mol(Chl)^-1 s^-1 and an O2 difference of 0.064 uM",
    "ref": "Kihara2014",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["kCCM"] = {
    "value": (p["kO2out"].get("value")),
    "unit": "s^-1",
    "descr": "rate constant of CO2 diffusion into the cell, assumed to be identical to kO2out",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

# Other light related
p["fluo_influence"] = {
    "value": {
        "PS2": 1,  # factor increasing PS2 fluorescence (no increase at 1)
        "PS1": 1,  # factor increasing PS1 fluorescence (no increase at 1)
        "PBS": 1.25,  # factor increasing PBS fluorescence (no increase at 1)
    },
    "unit": "unitless",
    "descr": "factors multiplied to the calculated fluorescence (no effect at 1)",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["PBS_free"] = {  # >> changed: added <<
    "value": 0.09,
    "unit": "unitless",
    "descr": "fraction of unbound PBS",
    "condition": "illumination with 633 nm LED at 25 µmol photon m−2 s−1; room temperature; air",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["PBS_PS1"] = {  # >> changed: added <<
    "value": 0.39,
    "unit": "unitless",
    "descr": "fraction of PBS bound to PSI",
    "condition": "illumination with 633 nm LED at 25 µmol photon m−2 s−1; room temperature; air",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["PBS_PS2"] = {  # >> changed: added <<
    "value": 0.51,
    "unit": "unitless",
    "descr": "fraction of PBS bound to PSII",
    "condition": "illumination with 633 nm LED at 25 µmol photon m−2 s−1; room temperature; air",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["pigment_content"] = {  # >> changed: added <<
    "value": pd.Series(
        {
            "chla": 1.000000,
            "beta_carotene": 0.176471,
            "allophycocyanin": 1.117647,
            "phycocyanin": 6.764706,
        }
    ),
    "unit": "mg(Pigment) mg(Chla)^-1",
    "descr": "relative pigment concentrations in a synechocystis cell",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "illumination with 633 nm LED at 25 µmol photon m−2 s−1; room temperature; air",
    "source": "",
    "ref": "Zavrel2023",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["lcf"] = {  # >> changed: added <<
    "value": 0.5,
    "unit": "excitations photons^-1",
    "descr": "light conversion factor",
    "organism": "",
    "condition": "",
    "source": "",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": None, "not": None},
}


# ---- Module: module_atp_synthase ----
p["kATPsynth"] = {
    "value": 10.0,
    "unit": "s^-1",
    "descr": "rate constant of ATP synthesis",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "10.0 [s^-1] rate of ATP synthesis",
    "ref": "fit to supply CBB",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["Pi_mol"] = {
    "value": 1.000e-02,
    "unit": "mmol mol(Chl)^-1",
    "descr": "molar conccentration of phosphate",
    "organism": "various",
    "condition": "various",
    "source": "1.000e-02 [mmol mol(Chl)^-1] molar concentration of phosphate",
    "ref": "Matuszynska2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["DeltaG0_ATP"] = {
    "value": 30.6,
    "unit": "kJ mol^-1",
    "descr": "energy of ATP formation",
    "organism": "-",
    "condition": "-",
    "source": "30.6 [kJ mol^-1] energy of ATP formation",
    "ref": "Matuszynska2019",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["HPR"] = {
    "value": 14.0 / 3.0,
    "unit": "unitless",
    "descr": "number of protons (14) passing through the ATP synthase per ATP (3) synthesized",
    "organism": "Synechocystis sp. strain PCC 6803",
    "condition": "were grown in BG-11 medium, at 30°C under continuous illumination (white light; 60 umol photons m^-2 s^-1) and continuous aeration with filtered air",
    "source": "14.0 protons per full rotation of ATP synthase",
    "ref": "Pogoryelov2007",
    "type": "parameter",
    "used": {"if": None, "not": None},
}


# ---- Module: CBB ----
p["vOxy_max"] = {
    "value": (
        1
        * 0.2  # [s^-1] approximate Rubisco oxygenation rate (Savir2010)
        * 1  # [mmol l^-1] approximate Rubisco active site concentration (Whitehead2014)
        / 3
        * unit_conv(  # 3 O2 consumed per lumped oxygenation reaction
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1 s^-1",
    "descr": "approximate Rubisco oxygenation rate",
    "organism": "various",
    "condition": "various",
    "source": "1 [s^-1] approximate Rubisco oxygenation rate",
    "ref": "Savir2010",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KMATP"] = {
    "value": (
        0.1
        * unit_conv(  # [mmol l^-1] order of magnitude of KM_ATP for phosphoribulo kinase (Wadano1998) and phospoglycerate kinase (Tsukamoto2013)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "order of magnitude of the michaelis constant for ATP consumption in the CBB cycle",
    "organism": "various",
    "condition": "various",
    "source": "0.1 [mmol l^-1] order of magnitude of KM_ATP for phosphoribulo kinase (Wadano1998) and phospoglycerate kinase",
    "ref": "Wadano1998,Tsukamoto2013",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KMNADPH"] = {
    "value": (
        0.075
        * unit_conv(  # [mmol l^-1] approxiate KM_NADPH for GAP2 in Synechocystis (Koksharova1998)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "approxiate michaelis constant for NADPH consumption in the CBB cycle",
    "organism": "Synechocystis 6803",
    "condition": "atmospheric CO2 or 1% CO2 in modified BG11 with and without 55 mM filter-sterilised glucose, at 30°C under high-intensity fluorescent light(50 uE m^-2s^-1)",
    "source": "0.075 [mmol l^-1] approxiate KM_NADPH for GAP2 in Synechocystis",
    "ref": "Koksharova1998",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KMCO2"] = {
    "value": (
        0.3
        * unit_conv(  # [mmol l^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco (Savir2010; Tab. S1)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "order of magnitude of the michaelis constant for CO2 consumption by cyanobacterial Rubisco",
    "organism": "various",
    "condition": "various",
    "source": "0.3 [mmol l^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco",
    "ref": "Savir2010",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KIO2"] = {
    "value": (
        1
        * unit_conv(  # [mmol l^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco (Savir2010; Tab. S1)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "order of magnitude of the michaelis inhibition constant of O2 for CO2 consumption by cyanobacterial Rubisco, assumed equal to KMO2",
    "organism": "various",
    "condition": "various",
    "source": "1 [mmol l^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco",
    "ref": "Savir2010",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
# p["KEH"] = {
#     "value": (
#         10**-7.5
#         * unit_conv(  # [mol l^-1] approximate proton concentration at first half maximal activity of FBPase (Udvardy1982)
#             ["mol l-1 -> mmol mol(Chl)-1"]
#         )
#     ),
#     "unit": "mmol mol(Chl)^-1",
#     "descr": "approximate michaelis constant for proton binding to FBPase",
#     "organism": "A. nidulans 14625 (Synechococcus sp. strain ANPCC6301)",
#     "condition": "sterile conditions in the liquid medium C of Kratz and Myers illuminated with cool-white fluorescent light (36 W/m2). Aeration kept at 37°C, was achieved by bubbling sterile air containing 5% CO2.",
#     "source": "10**-7.5 [mol l^-1] approximate proton concentration at first half maximal activity of FBPase",
#     "ref": "Udvardy1982",
#     "type": "depricated",
#     "used": {"if": None, "not": None},
# }
# p["Kw"] = {
#     "value": 10 ** (-14),
#     "unit": "unitless",
#     "descr": "water dissociation constant",
#     "organism": "-",
#     "condition": "-",
#     "source": "10**(-14) [unitless] water dissociation constant",
#     "ref": "Bandura2006",
#     "type": "depricated",
#     "used": {"if": None, "not": None},
# }
# p["KEOH"] = {
#     "value": (
#         1
#         / (10**-9.5)
#         * 10  # [mol l^-1] approximate proton concentration at second half maximal activity of FBPase (Udvardy1982)
#         ** (-14)
#         * unit_conv(  # [unitless] water dissociation constant
#             ["mol l-1 -> mmol mol(Chl)-1"]
#         )
#     ),
#     "unit": "mmol mol(Chl)^-1",
#     "descr": "approximate michaelis constant for hydroxid ions to induce proton dissociation from FBPase",
#     "organism": "A. nidulans 14625 (Synechococcus sp. strain ANPCC6301)",
#     "condition": "sterile conditions in the liquid medium C of Kratz and Myers illuminated with cool-white fluorescent light (36 W/m2). Aeration kept at 37°C, was achieved by bubbling sterile air containing 5% CO2.",
#     "source": "1/(10**-9.5) [mol l^-1] approximate proton concentration at second half maximal activity of FBPase",
#     "ref": "Udvardy1982",
#     "type": "depricated",
#     "used": {"if": None, "not": None},
# }
p["KMO2"] = {
    "value": (
        1
        * unit_conv(  # [mmol l^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco (Savir2010; Tab. S1)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol mol(Chl)^-1",
    "descr": "order of magnitude of the michaelis constant for O2 consumption by cyanobacterial Rubisco",
    "organism": "various",
    "condition": "various",
    "source": "1 [mmol l^-1] order of magnitude for KM_O2 of cyanobacterial Rubisco",
    "ref": "Savir2010",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KICO2"] = {
    "value": (
        0.3
        * unit_conv(  # [mmol l^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco (Savir2010; Tab. S1)
            ["mmol l-1 -> mmol mol(Chl)-1"]
        )
    ),
    "unit": "mmol l^-1",
    "descr": "order of magnitude of the michaelis inhibition constant of CO2 for O2 consumption by cyanobacterial Rubisco, assumed equal to KMCO2",
    "organism": "various",
    "condition": "various",
    "source": "0.3 [mmol l^-1] order of magnitude for KM_CO2 of cyanobacterial Rubisco",
    "ref": "Savir2010",
    "type": "parameter",
    "used": {"if": None, "not": None},
}
p["KMPGA"] = {
    "value": 0.1,
    "unit": "mmol mol(Chl)^-1",
    "descr": "arbitrary michaelis constant limiting oxygenation reactions for low 3PGA",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": None, "not": None},
}

# p["vCBB_max"] = {
#     "value": (
#         400  # [umol mg(Chl)^-1 h^-1] approximate maximal CO2 + HCO3- uptake rate (benschop2003)
#         * 4
#         / 10  # 10 electrons needed for one fixation with four generated per O2 split
#         * unit_conv(["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"])
#     ),
#     "unit": "mmol mol(Chl)^-1 s^-1",
#     "descr": "approximate maximal rate of the Calvin Benson Bassham cycle",
#     "organism": "",
#     "source": "",
#     "ref": "Benschop2013",
#     "type": "parameter",
#     "used": {"if": None, "not": None},
# }  #
p["vCBB_max"] = {
    "value": (
        0.2e-15  # [g(CO2) cell^-1 s^-1] approximate maximal CO2 uptake rate (Zavrel2017; Fig. S-D)
        / 3  # 3 CO2 consumed per lumped CBB reaction
        / CBB.CBB_energy_MM(
            c_AP_tot, c_NADP_tot, **make_valuedict(p)
        )  # Adjust for the energy regulation factor value at standard concentrations
        / CBB.CBB_gas_MM_O2(c_CO2, c_O2, **make_valuedict(p))
        / M_CO2
        / 60e-15  # [g(Chl) cell^-1] approximate Chl content (Zavrel2017; Fig. S-F)
        * M_chl  # [g(Chl) mol^-1]
        * 1e3  # Adjust for the gas regulation factor value at standard concentrations
    ),
    "unit": "mmol mol(Chl)^-1 s^-1",
    "descr": "approximate maximal rate of the Calvin Benson Bassham cycle",
    "organism": "Synechocystis sp. PCC 6803 substrains GT-L, GT-B and PCC-B",
    "condition": "32°C and concentration of CO2 in input gas 5 000 ppm, under 25 and 220 µmol photons m-2 s-1 of red light complemented with 25 µmol(photons) m-2 s-1 of blue light",
    "source": "0.2e-15 [g(CO2) cell^-1 s^-1] approximate maximal CO2 uptake rate",
    "ref": "Zavrel2017",
    "type": "parameter",
    "used": {"if": None, "not": None},
}  #


# ---- Module: photorespiratory_salvage ----
p["kPR"] = {
    "value": (
        4.80e-6
        * 0.5  # [umol min^-1 ug(Chl)^-1] estimated rate of photorespiration (glycolate appearance) under Air-like CO2 concentration (Huege2011)
        * unit_conv(  # [unitless] one lumped reaction recycles 2 (2-phospho)glycolate
            ["mol g(Chl)-1 -> mmol mol(Chl)-1", "min-1 -> s-1"]
        )
        * (
            1 / c_PG * 1 / c_ATP * 1 / c_NADPH * 1 / c_NAD
        )  # normalise to the reaction substrates
    ),
    "unit": "mol(Chl)^4 mmol^-4 s^-1",
    "descr": "rate constant of (2-phospho)glycolate recycling into 3PGA",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium; 29°C; illuminated with Osram L58 W32/3 at 130 µmol photons m-2 s-1 ambient air",
    "source": "4.80e-6 [umol min^-1 ug(Chl)^-1] estimated rate of photorespiration (glycolate appearance) under Air-like CO2 concentration",
    "ref": "Huege2011",
    "type": "parameter",
    "used": {"if": None, "not": None},
}


# ---- Module update: FlvandCCM ----
cu["CO2ext_pp"] = {  # >> changed: added <<
    "value": 0.05,
    "unit": "atm",
    "descr": "CO2 partial pressure in 5% CO2 enriched air used for bubbeling",
    "organism": "-",
    "condition": "-",
    "source": "",
    "ref": "set",
    "type": "parameter",
    "used": {"if": ["update_CCM"], "not": None},
}
cu["CO2"] = {
    "value": (unpack("CO2ext", c)),
    "unit": "mmol mol(Chl)^-1",
    "descr": "concentration of CO2 in the cell without activity of the CCM",
    "organism": "-",
    "condition": "-",
    "source": "estimated",
    "ref": "estimated",
    "type": "initial concentration",
    "used": {"if": ["update_CCM"], "not": None},
}
pu["KHillFdred"] = {  # >> changed: added <<
    "value": 2.5**4,
    "unit": "mmol^nHillFdred mol(Chl)^-nHillFdred",
    "descr": "Flv binding constant of Fd_red in Hill kinetics, assuming half activity around 2.5 mmol mol(Chl)^-1",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": ["update_Flv_hill"], "not": None},
}
pu["nHillFdred"] = {  # >> changed: added <<
    "value": 4,
    "unit": "unitless",
    "descr": "Hill constant of Fd_red binding to Flv, assuming stong cooperative binding (see Brown2019)",
    "organism": "-",
    "condition": "-",
    "source": "guess",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": ["update_Flv_hill"], "not": None},
}
pu["S"] = {  # >> changed: added <<
    "value": 35,
    "unit": "unitless",
    "descr": "salinity within a cell",
    "organism": "-",
    "condition": "-",
    "source": "taken from sea water since no cell estimations could be found",
    "ref": "MojicaPrieto2002",
    "type": "parameter",
    "used": {"if": ["update_CCM"], "not": None},
}
pu["k_O2"] = {
    "value": (
        20
        * unit_conv(  # [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen consumption by Flv 1/3 in dark-light transition (Ermakova2016)
            ["mmol g(Chl)-1 -> mmol mol(Chl)-1", "h-1 -> s-1"]
        )
        * (1 / c_O2 * 1 / c_Ho)  # normalise by the substrates
    ),
    "unit": "mol(Chl)^2 mmol^-2 s^-1",
    "descr": "rate constant of Fd oxidation by Flv 1/3",
    "organism": "Synechocystis sp. PCC 6803 & mutants lacking respiratory terminal oxidases",
    "condition": "BG11 medium buffered with 10 mM TES-KOH (pH 8.2), continuous illumination of 50 mmol photons m-2 s-1 (photosynthetically active radiation), 3% CO2, and 30°C with gentle agitation (120 rpm).",
    "source": "20 [umol(O2) mg(Chl)^-1 h^-1] rate of oxygen consumtion by Flv 1/3 in dark-light transition",
    "ref": "Ermakova2016",
    "type": "parameter",
    "used": {"if": ["update_Flv_hill"], "not": None},
}

# Update the fCin parameter to the new CCM definition
pu["fCin"] = {
    "value": 1000.0,
    "unit": "unitless",
    "descr": "ratio of intracellular to external CO2 partial pressure with activity of the CCM",
    "organism": "cyanobacteria",
    "condition": "various",
    "source": "the CCM-increased intracellular bicarbonate concentration can exceed the external by 100 - 1000 times",
    "ref": "Hagemann2021,Benschop2003",
    "type": "parameter",
    "used": {"if": ["update_CCM"], "not": None},
}


# ---- Module update: phycobilisomes ----
pu["kOCPactivation"] = {  # >> changed: added <<
    "value": 9.6e-05,
    "unit": "s^-1 (umol(Photons) m^-2 s^-1)^-1",
    "descr": "rate constant of OCP activation by absorbed light",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": ["add_OCP"], "not": None},
}
pu["kOCPdeactivation"] = {  # >> changed: added <<
    "value": 1.35e-3,
    "unit": "s^-1",
    "descr": "rate constant of OCP deactivation by thermal processes",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": ["add_OCP"], "not": None},
}
pu["OCPmax"] = {  # >> changed: added <<
    "value": 0.28,
    "unit": "unitless",
    "descr": "maximal fraction of PBS quenched by OCP",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium with 10 mM NaHCO3 2x sodium nitrate concentration; 30 °C; 220 µE m-2 s-1 blue green illumination",
    "source": "ca. 29% of PBS were quenched in WT with 220 µE m-2 s-1 blue green illumination, maximum assumed to be 10% higher",
    "ref": "Tian2011",
    "type": "parameter",
    "used": {"if": ["add_OCP"], "not": None},
}
cu["OCP"] = {
    "value": 0,
    "unit": "unitless",
    "descr": "initial activity of OCP",
    "organism": "-",
    "condition": "-",
    "source": "0 [unitless] fraction of OCP activity",
    "ref": "guess",
    "type": "initial concentration",
    "used": {"if": ["add_OCP"], "not": None},
}


# ---- Module update: statetransitions ----
pu["kUnquench"] = {  # >> changed: added <<
    "value": 0.1,
    "unit": "s^-1",
    "descr": "rate constant of internal PS2 unquenching",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": ["update_statetransitions_hill"], "not": None},
}
pu["KMUnquench"] = {  # >> changed: added <<
    "value": 0.2,
    "unit": "mmol mol(Chl)^-1",
    "descr": "binding constant of PS2 unquenching inhibition by Q_red",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": ["update_statetransitions_hill"], "not": None},
}
# pu["nUnquench"] = {  # >> changed: added <<
#     "value": 1,
#     "unit": "unitless",
#     "descr": "Hill constant of PS2 unquenching inhibition by Q_red",
#     "organism": "synechocystis sp. PCC 6803",
#     "condition": "various",
#     "source": "manually fitted",
#     "ref": "manually fitted",
#     "type": "parameter",
#     "used": {"if": ["update_statetransitions_hill"], "not": None},
# }
pu["kQuench"] = {  # >> changed: added <<
    "value": 2e-3,
    "unit": "mmol^-1 mol(Chl)^-1 s^-1",
    "descr": "rate constant of PS2 quenching by Q_red",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "various",
    "source": "manually fitted",
    "ref": "manually fitted",
    "type": "parameter",
    "used": {"if": ["update_statetransitions_hill"], "not": None},
}


# ---- Module update: CBB ----
pu["kCBBactivation"] = {  # >> changed: added <<
    "value": (
        np.log(2) / 20  # [s] approximate half time of CBB activation (Nikkanen2020)
    ),
    "unit": "s^-1",
    "descr": "rate constant of CBB activation by reduced ferredoxin",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium with 1.5 mM NaHCO3; 30 °C; 500 µmol m-2 s-1 white illumination",
    "source": "20 [s] approximate half time of activation after CO2 accumulation by CCM",
    "ref": "Nikkanen2020",
    "type": "parameter",
    "used": {"if": ["update_CBBactivation_MM", "update_CBBactivation_hill"], "not": None},
}
pu["KMFdred"] = {  # >> changed: added <<
    "value": 0.3,
    "unit": "mmol mol(Chl)^-1",
    "descr": "Michaelis constant of CBB activation by reduced ferredoxin",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium with 0.5 mM NaHCO3; 30 °C; 0-300 µmol m-2 s-1 625 nm illumination",
    "source": "At 10 µmol m-2 s-1 O2 production seems un-attenuated by inactivated CBB, value set accordingly",
    "ref": "Schuurmans2014",
    "type": "parameter",
    "used": {"if": ["update_CBBactivation_MM"], "not": None},
}
pu["KHillFdred_CBB"] = {  # >> changed: added <<
    "value": 1e-4,
    "unit": "mmol^nHillFdred_CBB mol(Chl)^-nHillFdred_CBB",
    "descr": "Apparent dissociation constant of reduced ferredoxin for CBB activation",
    "organism": "synechocystis sp. PCC 6803",
    "condition": "BG11 medium with 0.5 mM NaHCO3; 30 °C; 0-300 µmol m-2 s-1 625 nm illumination",
    "source": "At 10 µmol m-2 s-1 O2 production seems un-attenuated by inactivated CBB, value set accordingly",
    "ref": "Schuurmans2014",
    "type": "parameter",
    "used": {"if": ["update_CBBactivation_hill"], "not": None},
}
pu["nHillFdred_CBB"] = {  # >> changed: added <<
    "value": 4,
    "unit": "unitless",
    "descr": "Hill coefficient of CBB activation by reduced ferredoxin",
    "organism": "",
    "condition": "",
    "source": "",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": ["update_CBBactivation_hill"], "not": None},
}

# ---- Module update: NQ ----
vCBB_max = unpack("vCBB_max")

pu["vNQ_max"] = {
    "value": 50,
    "unit": "mmol mol(Chl)^-1 s^-1",
    "descr": "maximal rate of NDH-1",
    "organism": "",
    "condition": "",
    "source": "",
    "ref": "",
    "type": "parameter",
    "used": {"if": ["update_NQ_MM"], "not": None},
}
pu["KMNQ_Qox"] = {
    "value": c_Q_tot * 0.1,
    "unit": "mmol mol(Chl)^-1",
    "descr": "Michaelis constant for Q_ox reduction by NDH-1",
    "organism": "",
    "condition": "",
    "source": "",
    "ref": "guess",
    "type": "parameter",
    "used": {"if": ["update_NQ_MM"], "not": None},
}
pu["KMNQ_Fdred"] = {
    "value": c_Fd_tot * 0.4,
    "unit": "mmol mol(Chl)^-1",
    "descr": "Michaelis constant for Fd_red oxidation by NDH-1",
    "organism": "",
    "condition": "",
    "source": "",  # 0.059 [mM] KM of NDH-1 for Fd_red (10.1007/s11120-015-0090-4)
    "ref": "guess",
    "type": "parameter",
    "used": {"if": ["update_NQ_MM"], "not": None},
}


###################################################
# Check if the current parameters are up to date
###################################################


def _make_readable_value(x, num=False):
    if np.abs(x) > 1000 or np.abs(x) < 0.1:
        res = "%.3e" % x
    else:
        res = "%.3f" % x

    if num:
        return float(res)
    else:
        return res


def make_readable_value(x, num=False):
    if isinstance(x, (int, float)):
        return _make_readable_value(x, num)
    elif isinstance(x, dict):
        res = {k: _make_readable_value(v, num) for k, v in x}
    else:
        res = np.zeros(len(x))

        for i, sub_val in enumerate(x):
            res[i] = _make_readable_value(sub_val, num)

        return res


def check_parameters(p_check):
    p_new = {
        key: make_readable_value(p[key]["value"], True)
        for key in p_check.keys()
        if key not in ["pfd"]
    }

    if p_check == p_new:
        return True
    else:
        print("given dict | here")
        for key, value in p_new.items():
            vals_old = make_readable_value(p[key]["value"], False)
            vals_new = make_readable_value(value, False)
            if np.any(vals_old != vals_new):
                print("%s: %s | %s" % (key, vals_old, vals_new))


# check_parameters(p)
# check_parameters(pATP)
# check_parameters(parameters)
# check_parameters(pATP)

###########################
# Print parameter values
###########################


def _export_num(key, value, sep):
    return f"    '{key}': {str(make_readable_value(value))}{sep}"


def _exportiter_list(value):
    return [str(make_readable_value(v)) for i, v in enumerate(value)]


def _exportiter_dict(value):
    return [
        f"'{k}': {str(make_readable_value(v))}"
        for i, (k, v) in enumerate(value.items())
    ]


def _export_container(key, value, sep, iterfun, parenteses):
    prnt = f"    '{key}': {parenteses[0]}"

    items = iterfun(value)
    prnt += ", ".join(items)
    prnt += parenteses[1] + sep
    return prnt


def _export_list(key, value, sep):
    return _export_container(key, value, sep, _exportiter_list, ["[", "]"])


def _export_dict(key, value, sep):
    return _export_container(key, value, sep, _exportiter_dict, ["{", "}"])


def _export_pdSeries(key, value, sep):
    return _export_container(
        key, value.to_dict(), sep, _exportiter_dict, ["pd.Series({", "})"]
    )


def export_parameters_str(p_list, sep=",", annotate=True, include_parentheses=True):
    res = ""
    for key, value_dict in p_list.items():
        value = value_dict["value"]

        if isinstance(value, (int, float)):
            prnt = _export_num(key, value, sep)
        elif isinstance(value, list):
            prnt = _export_list(key, value, sep)
        elif isinstance(value, dict):
            prnt = _export_dict(key, value, sep)
        elif isinstance(value, pd.Series):
            prnt = _export_pdSeries(key, value, sep)
        else:
            raise ValueError(
                f"value of parameter {key} has type {type(value)} which has no export function"
            )
        if annotate:
            prnt += (
                f" # [{value_dict['unit']}] {value_dict['descr']} ({value_dict['ref']})"
            )
        res += prnt + "\n"
    if include_parentheses:
        res = "{\n" + res + "}"
    return res


def print_parameters(p_list, sep=",", annotate=True):
    print(
        export_parameters_str(
            p_list, sep=sep, annotate=annotate, include_parentheses=False
        )
    )
    print("")


def get_parameters(p_list):
    res = {}
    for key, value_dict in p_list.items():
        value = value_dict["value"]
        res[key] = make_readable_value(value, num=True)

    return res


# print("---- Module: module_electron_transport_chain ----")
# print_parameters([p_c, p_c_tot, p_k, p_E0, p_const])
# print("\n")

# print("---- Initial Concentrations ----")
# y0_compounds = [
# 'PSII',
#  'Q_ox',
#  'Hi',
#  'Ho',
#  'O2',
#  'PC_ox',
#  'Fd_ox',
#  'NADPH',
#  'NADH',
#  'ATP',
#  'CO2',
#  'succinate',
#  'fumarate',
#  '3PGA',
#  'PG',
#  'Flva',
#  'CBBa'
# ]
# p_y0 = {key:val for key, val in p_c.items() if key in y0_compounds}
# print_parameters([p_y0])
# print("\n")

# print("---- Module: module_atp_synthase ----")
# print_parameters([p_ATPsyn])
# print("\n")

# print("---- Module: base_yokota ----")
# print_parameters([p_yokota])
# print("\n")

# print("---- Module: CBB ----")
# print_parameters([p_CBB])

# print("---- Module: photorespiratory_salvage ----")
# print_parameters([p_PR])

# print("---- Stoichiometry of respiration ----")
# print_parameters([respiratory_stoichiometry])


#############
# Test Area
#############
# p_test = {}

# print("\n\n\n")
# print("---- TEST ----")
# print_parameters([p_test])

if __name__ == "__main__":
    # If run from console, output parameters to file
    stamp = f"# Model parameters\n# Exported on {format(datetime.now(), '%d.%m.%Y - %H:%M')}\n\n"

    # Check if numpy or pandas have to be imported
    imports = ""
    imports_necessary = False
    valuetypes = [type(x) for x in make_valuedict(p).values()]
    if pd.Series in valuetypes or pd.DataFrame in valuetypes:
        imports += "import pandas as pd\n"
    if np.ndarray in valuetypes:
        imports += "import numpy as np\n"

    if imports != "":
        imports += "\n"

    file_arg = [x.startswith("--file=") for x in argv]
    if np.any(file_arg):
        file_nam = argv[int(np.where(file_arg)[0][0])].removeprefix("--file=")
    elif len(argv) > 1 and not argv[1].startswith("--"):
        file_nam = argv[1]
    else:
        file_nam = "parameters.py"

    all = c.copy()
    all.update(p)
    param = {k: v for k, v in all.items() if v["type"] == "parameter"}
    conc = {k: v for k, v in all.items() if v["type"] == "initial concentration"}

    allu = cu.copy()
    allu.update(pu)
    paramu = {k: v for k, v in allu.items() if v["type"] == "parameter"}
    concu = {k: v for k, v in allu.items() if v["type"] == "initial concentration"}

    exp = (
        "p = { # Module parameters\n"
        + export_parameters_str(
            p_list=param, sep=",", annotate=True, include_parentheses=False
        )
        + "}\n\npu = { # Update-module parameters\n"
        + export_parameters_str(
            p_list=paramu, sep=",", annotate=True, include_parentheses=False
        )
        + "}\n\ny0 = { # Module initial concentrations\n"
        + export_parameters_str(
            p_list=conc, sep=",", annotate=True, include_parentheses=False
        )
        + "}\n\ny0u = { # Update-module initial concentrations\n"
        + export_parameters_str(
            p_list=concu, sep=",", annotate=True, include_parentheses=False
        )
        + "}"
    )

    # c_exp = "c = " + export_parameters_str(c, sep=",", annotate=True, include_parentheses=True)

    with open(file_nam, "w") as f:
        f.write(stamp + imports + exp)
