from modelbase2 import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Li2021"]


def Li2021() -> Model:
    m = Model()

    m.add_parameters(
        {
            "Pi_st": 1.5,
            "Vmax_b6f": 300,
            "c_b6f": 0.433,
            "pKa_reg": 6.2,
            "Em_PC_pH7": 0.37,
            "Em_PQH2_pH7": 0.11,
            "Em_Fd": -0.42,
            "k_NDH1": 1000,
            "Vmax_PGR": 0,
            "Vmax_VDE": 0.08,
            "pKa_VDE": 5.65,
            "nh_VDE": 4,
            "k_EZ": 0.004,
            "pKa_PsbS": 6.2,
            "DeltaG0_ATP": 36,  # 30.6kJ/mol / RT
            "HPR": 14.0 / 3.0,  # Vollmar et al. 2009 (after Zhu et al. 2013)
            "Vmax_ATPsynth": 200,
            "F": 96.485,  # Faraday constant
            "NPQ_max": 3,
            "k_recomb": 0.33,
            "phi_triplet": 0.45,  # 45% of recomnbinations lead to P680 triplets
            "phi_1O2": 1,  # 100% of 3P680 give rise to 1O2
            "PAR": 10,
            "PSII_max": 1,
            "sigma0_II": 0.5,
            "k_QA": 1000,
            "K_QA": 200,
            "vpc": 0.047,
            "sigma0_I": 0.5,
            "ipt_lu": 0.000587,
            "b_H": 0.014,
            "ipt_st": 0.1 * 0.000587,
            "P_K": 150,
            "k_VCCN1": 12,
            "k_ClCe": 80000,
            "k_PCtoP700": 5000,
            "k_KEA3": 2500000,
            # "ppPSII": 0,
            "k_FdtoNADP": 1000,
            "k_CBB": 60,
            "k_Leak": 3 * 10**7,
            "pH_st": 7.8,
        }
    )

    m.add_variables(
        {
            "Vx": 1.0,
            "Zx": 0.0,
            "ATP_st": 4.15,
            "ADP_st": 4.15,
            "K_lu": 0.1,
            "K_st": 0.1,
            "Cl_lu": 0.04,
            "Cl_st": 0.04,
            "Dpsi": 0,
            "QA_ox": 1,
            "QA_red": 0,
            "PQH_2": 0,
            "PQ": 7,
            "PC_red": 2,
            "PC_ox": 0,
            "Fd_ox": 1,
            "Fd_red": 0,
            "pH_lu": 7.8,
            "NADPH_st": 1.5,
            "NADP_st": 3.5,
            "Y0": 0.667,
            "Y2": 0,
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
