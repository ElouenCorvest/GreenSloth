from modelbase2 import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = [
    'Li2021'
]

def Li2021() -> Model:
    m = Model()

    m.add_parameters(
        {
            "Pi":1.5,
            "max_b6f": 300,
            "b6f_content": 0.433,
            "pKreg": 6.2,
            "Em7_PC": 0.37,
            "Em7_PQH2": 0.11,
            "Em_Fd": -0.42,
            "k_NDH1": 1000,
            "PGR_vmax": 0,
            "VDE_max":0.08,
            "pKvde": 5.65,
            "VDE_Hill": 4,
            "kZE": 0.004,
            "pKPsbS":6.2,
            "dG0ATP": 36,  # 30.6kJ/mol / RT
            "HPR": 14.0 / 3.0,  # Vollmar et al. 2009 (after Zhu et al. 2013)
            "max_ATPsynthase": 200,
            "F": 96.485, # Faraday constant
            "max_NPQ": 3,
            "kRecomb":0.33,
            "triplet_yield":0.45, #45% of recomnbinations lead to P680 triplets
            "triplet_to_singletO2_yield":1, #100% of 3P680 give rise to 1O2
            "PAR": 10,
            "max_PSII":1,
            "PSII_antenna_size":0.5,
            "kQA":1000,
            "Keq_QA_PQ": 200,
            "volts_per_charge": 0.047,
            "PSI_antenna_size": 0.5,
            "lumen_ions_per_turnover":0.000587,
            "buffering_capacity": 0.014,
            "stroma_ions_per_turnover": 0.1*0.000587,
            "perm_K":150,
            "kVCCN1":12,
            "kClCe":80000,
            "k_PC_to_P700": 5000,
            "k_KEA3":2500000,
            "light_per_L": 0,
            "k_Fd_to_NADP":1000,
            "kCBB":60,
            "kLeak": 3*10**7,
            "pHstroma": 7.8,
        }
    )

    m.add_variables(
        {
            "Vx":1.0,
            "Zx":0.0,
            "ATP_st":4.15,
            "ADP_st":4.15,
            "K_lu":0.1,
            "K_st":0.1,
            "Cl_lu":0.04,
            "Cl_stroma":0.04,
            "Dpsi":0,
            "QA_ox":1,
            "QAm":0,
            "PQH_2": 0,
            "PQ": 7,
            "PC_red": 2,
            "PC_ox": 0,
            "Fd_ox":1,
            "Fd_red":0,
            "pH_lu": 7.8,
            "NADPH_st": 1.5,
            "NADP": 3.5,
            "Y0": 0.667,
            "Y2": 0
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
