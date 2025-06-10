from mxlpy import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Matuszynska2016"]


def Matuszynska2016() -> Model:
    m = Model()

    m.add_parameters(
        {
            # Pool sizes
            "PSII_tot": 2.5,  # PSII reaction centres
            "PQ_tot": 20,  # PQ + PQH2
            "AP_tot": 50,  # total adenosine phosphate pool (ATP + ADP)
            "PsbS_tot": 1,  # LHCII normalized
            "X_tot": 1,  # toal xanthophylls
            "O2_ex": 8,  # external oxygen
            "Pi": 0.01,  # internal pool of phosphates
            # Rate constants and key parameters
            "k_Cytb6f": 0.104,
            "k_ActATPase": 0.01,
            "k_DeactATPase": 0.002,
            "k_ATPsynth": 20.0,
            "k_ATPconsum": 10.0,
            "k_PQH2": 250.0,
            "k_H": 5e9,
            "k_F": 6.25e8,
            "k_P": 5e9,
            "k_PTOX": 0.01,
            "pH_st": 7.8,
            "k_leak": 1000,
            "b_H": 100,
            "hpr": 14.0 / 3.0,
            # Parameter associated with xanthophyll cycle
            "k_DV": 0.0024,
            "k_EZ": 0.00024,
            "K_pHSat": 5.8,
            "nhx": 5.0,
            "K_ZSat": 0.12,
            # Parameter associated with PsbS protonation
            "nhl": 3,
            "k_deprot": 0.0096,
            "k_prot": 0.0096,
            "K_pHSatLHC": 5.8,
            # Fitted quencher contribution factors
            "gamma_0": 0.1,
            "gamma_1": 0.25,
            "gamma_2": 0.6,
            "gamma_3": 0.15,
            # Physical constants
            "F": 96.485,
            "R": 8.3e-3,  # J in KJ
            "T": 298,
            # Standard potentials
            "E0_QA": -0.140,
            "E0_PQ": 0.354,
            "E0_PC": 0.380,
            "DG_ATP": 30.6,
            # pfd
            "pfd": 100,
        }
    )

    m.add_variables(
        {
            "PQH_2": 0,  # reduced Plastoquinone
            "H_lu": 6.32975752e-05,  # luminal Protons
            "ATPase_ac": 0,  # ATPactivity
            "ATP_st": 25.0,  # ATP
            "psbS": 1,  # fraction of non-protonated PsbS
            "Vx": 1,  # fraction of Violaxanthin
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
