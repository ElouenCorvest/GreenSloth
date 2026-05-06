from mxlpy import Model, Variable, InitialAssignment
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Davis2017"]


def Davis2017() -> Model:
    m = Model()

    m.add_parameters(
        {
            "PPFD": 0, # checked
            "k_recomb": 0.33, # checked
            "phi_triplet": 0.45, # checked
            "phi_1O2": 1, # checked
            "sigma0_II": 1, # checked
            "c_b6f": 1, # checked
            "pKa_reg": 6.5, # checked
            "Em_PC_pH7": 0.37, # checked
            "Em_PQH2_pH7": 0.11, # checked
            "Vmax_b6f": 500, # checked
            "pKa_PsbS": 6.4, # checked
            "NPQ_max": 5,   # checked
            "pH_stroma": 7.8, # checked
            "PSI_antenna_size": 1, # checked
            "k_QA": 1000, # checked
            "Keq_QA": 200, # checked
            "k_PCtoP700": 500, # checked
            "k_FdtoNADP": 1000, # checked or 5000
            "K_st": 0.04, # checked
            "k_KEA3": 0,# checked
            "P_K": 6000, # checked
            "lumen_protons_per_turnover": 1.4e-05, # checked
            "n":14/3, # checked
            "DeltaGATP": 42, # checked
            "Vmax_ATPsynth": 1000, # checked
            "b_H": 0.03, # checked
            "volt_per_charge": 0.033, # checked
            "k_EZ": 0.03, # checked
            "nh_VDE": 4, # checked
            "pKa_VDE": 5.8, # checked
            "Vmax_VDE": 1, # checked
            "QA_total": 1, # checked
            "PQ_tot": 6, # checked 
            "P700_total": 1, # checked 
            "PC_tot": 2,  # checked
            "Fd_tot": 1,  # checked
            "NADP_tot": 1,  # checked
            "Xanthophyll_tot": 1, # checked
            "k_CBB": 3000, # checked
        }
    )

    m.add_variables(
        {
            "QA_red": Variable(0, unit="REPLACE"), # checked
            "PQH_2": Variable(0, unit="REPLACE"), # checked
            "pH_lumen": Variable(7, unit="REPLACE"), # checked
            "Dpsi": Variable(0.1, unit="REPLACE"), # checked
            "K_lu": Variable(0.04, unit="REPLACE"), # checked
            "PC_ox": Variable(0, unit="REPLACE"), # checked
            "Zx": Variable(0, unit="REPLACE"), # checked
            # "PsbS": Variable(0, unit="REPLACE"), # checked
            "singO2": Variable(0, unit="REPLACE"), # checked
            'P700_ox': Variable(0, unit="REPLACE"), # checked
            "Fd_red": Variable(0, unit="REPLACE"), # checked
            "NADPH_st": Variable(0, unit="REPLACE"), # checked
            "LEF": Variable(0, unit="REPLACE"), # checked
            "ATP_made": Variable(0, unit="REPLACE"), # checked
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m