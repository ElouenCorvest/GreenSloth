
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
            "phi_triplet": 0.45,
            "phi_1O2": 1,
            "sigma0_II": 0.5,
            "c_b6f": 0.433,
            "pKa_reg": 6.2,
            "Em_PC_pH7": 0.37,
            "Em_PQH2_pH7": 0.11,
            "Vmax_b6f": 300,
            "pKa_PsbS": 6.2,
            "NPQ_max": 3,
            "pH_st": 7.8,
            "Em_Fd": -0.42,
            "k_NDH1": 1000,
            "Vmax_PGR": 0,
            "sigma0_I": 0.5,
            "k_QA": 1000,
            "Keq_QA": 200,
            "k_PCtoP700": 5000,
            "k_FdtoNADP": 1000,
            "K_st": 0.1,
            "k_KEA3": 2500000,
            "P_K": 150,
            "ipt_lu": 0.000587,
            "k_VCCN1": 12,
            "k_ClCe": 800000,
            "HPR": 4.666666666666667,
            "Vmax_ATPsynth": 200,
            "b_H": 0.014,
            "vpc": 0.047,
            "k_EZ": 0.004,
            "nh_VDE": 4,
            "pKa_VDE": 5.65,
            "Vmax_VDE": 0.08,
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
            "Dpsi": Variable(0, unit="REPLACE"),
            "K_lu": Variable(0.1, unit="REPLACE"),
            "PC_ox": Variable(0, unit="REPLACE"),
            "Y2": Variable(0, unit="REPLACE"),
            "Zx": Variable(0, unit="REPLACE"),
            "singO2": Variable(0, unit="REPLACE"),
            "Fd_red": Variable(0, unit="REPLACE"),
            "NADPH_st": Variable(1.5, unit="REPLACE"),
            "Cl_lu": Variable(0.04, unit="REPLACE"),
            "Cl_st": Variable(0.04, unit="REPLACE"),
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m