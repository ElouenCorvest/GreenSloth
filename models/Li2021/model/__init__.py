
from mxlpy import Model, Variable, InitialAssignment
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Li2021"]


def Li2021() -> Model:
    m = Model()

    m.add_parameters(
        {
            "PPFD": 50,
            "k_recomb": 0.33,
            "triplet_yield": 0.45,
            "triplet_to_singletO2_yield": 1,
            "PSII_antenna_size": 0.5,
            "b6f_content": 0.433,
            "pKreg": 6.2,
            "Em7_PC": 0.37,
            "Em7_PQH2": 0.11,
            "max_b6f": 300,
            "pKPsbS": 6.2,
            "max_NPQ": 3,
            "pH_stroma": 7.8,
            "Em_Fd": -0.42,
            "k_NDH": 1000,
            "PGR_vmax": 0,
            "PSI_antenna_size": 0.5,
            "kQA": 1000,
            "Keq_QA_PQ": 200,
            "k_PC_to_P700": 5000,
            "k_Fd_to_NADP": 1000,
            "K__stroma": 0.1,
            "k_KEA": 2500000,
            "perm_K": 150,
            "lumen_protons_per_turnover": 0.000587,
            "k_VCCN1": 12,
            "k_CLCE": 800000,
            "n": 4.666666666666667,
            "ATP_synthase_max_turnover": 200,
            "buffering_capacity": 0.014,
            "Volts_per_charge": 0.047,
            "kZE": 0.004,
            "VDE_Hill": 4,
            "pKvde": 5.65,
            "VDE_max_turnover_number": 0.08,
            "k_leak": 30000000.0,
            "QA_total": 1,
            "PQ_tot": 7,
            "P700_total": 0.667,
            "PC_tot": 2,
            "Fd_tot": 1,
            "NADP_tot": 5,
            "Carotenoids_tot": 1,
        }
    )
    m.add_variables(
        {
            "QA_red": Variable(0, unit="REPLACE"),
            "PQH_2": Variable(0, unit="REPLACE"),
            "pH_lumen": Variable(7.8, unit="REPLACE"),
            "Dy": Variable(0, unit="REPLACE"),
            "K__lumen": Variable(0.1, unit="REPLACE"),
            "PC_ox": Variable(0, unit="REPLACE"),
            "P700_ox": Variable(0, unit="REPLACE"),
            "Zx": Variable(0, unit="REPLACE"),
            "singletO2": Variable(0, unit="REPLACE"),
            "Fd_red": Variable(0, unit="REPLACE"),
            "NADPH_st": Variable(1.5, unit="REPLACE"),
            "Cl__lumen": Variable(0.04, unit="REPLACE"),
            "Cl__stroma": Variable(0.04, unit="REPLACE"),
        }
    )
    m = include_derived_quantities(m)
    m = include_rates(m)

    return m