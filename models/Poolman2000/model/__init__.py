from mxlpy import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Poolman2000"]


def Poolman2000() -> Model:
    m = Model()

    m.add_parameters(
        {
            "CO2": 0.2,
            "NADPH_st": 0.21,
            "H": 1.2589254117941661e-05,
            "AP_tot": 0.5,
            "NADP_tot": 0.5,
            "Pi_tot": 15.0,
            "Enz0_v_RuBisCO_c": 1.0,
            "kcat_v_RuBisCO_c": 2.72,
            "km_v_RuBisCO_c_RUBP": 0.02,
            "km_v_RuBisCO_c_CO2": 0.0107,
            "ki_v_RuBisCO_c_PGA": 0.04,
            "ki_v_RuBisCO_c_FBP": 0.04,
            "ki_v_RuBisCO_c_SBP": 0.075,
            "ki_v_RuBisCO_c_Pi_st": 0.9,
            "ki_v_RuBisCO_c_NADPH_st": 0.07,
            "kre_v_PGK1ase": 800000000.0,
            "keq_v_PGK1ase": 0.00031,
            "kre_v_BPGAdehynase": 800000000.0,
            "keq_v_BPGAdehynase": 16000000.0,
            "kre_v_TPIase": 800000000.0,
            "keq_v_TPIase": 22.0,
            "kre_v_Aldolase_FBP": 800000000.0,
            "keq_v_Aldolase_FBP": 7.1,
            "kre_v_Aldolase_SBP": 800000000.0,
            "keq_v_Aldolase_SBP": 13.0,
            "Enz0_v_FBPase": 1.0,
            "kcat_v_FBPase": 1.6,
            "km_v_FBPase_s": 0.03,
            "ki_v_FBPase_F6P": 0.7,
            "ki_v_FBPase_Pi_st": 12.0,
            "kre_v_TKase_E4P": 800000000.0,
            "keq_v_TKase_E4P": 0.084,
            "kre_v_TKase_R5P": 800000000.0,
            "keq_v_TKase_R5P": 0.85,
            "Enz0_v_SBPase": 1.0,
            "kcat_v_SBPase": 0.32,
            "km_v_SBPase_s": 0.013,
            "ki_v_SBPase_Pi_st": 12.0,
            "kre_v_Rpiase": 800000000.0,
            "keq_v_Rpiase": 0.4,
            "kre_v_RPEase": 800000000.0,
            "keq_v_RPEase": 0.67,
            "Enz0_v_PRKase": 1.0,
            "kcat_v_PRKase": 7.9992,
            "km_v_PRKase_RU5P": 0.05,
            "km_v_PRKase_ATP_st": 0.05,
            "ki_v_PRKase_PGA": 2.0,
            "ki_v_PRKase_RUBP": 0.7,
            "ki_v_PRKase_Pi_st": 4.0,
            "ki_v_PRKase_4": 2.5,
            "ki_v_PRKase_5": 0.4,
            "kre_v_PGIase": 800000000.0,
            "keq_v_PGIase": 2.3,
            "kre_v_PGMase": 800000000.0,
            "keq_v_PGMase": 0.058,
            "Pi_ext": 0.5,
            "km_v_pga_ex": 0.25,
            "km_v_gap_ex": 0.075,
            "km_v_dhap_ex": 0.077,
            "km_N_translocator_Pi_ext": 0.74,
            "km_N_translocator_Pi_st": 0.63,
            "kcat_N_translocator": 2.0,
            "Enz0_N_translocator": 1.0,
            "km_v_starch_G1P": 0.08,
            "km_v_starch_ATP_st": 0.08,
            "ki_v_starch": 10.0,
            "ki_v_starch_PGA": 0.1,
            "ki_v_starch_F6P": 0.02,
            "ki_v_starch_FBP": 0.02,
            "Enz0_v_starch": 1.0,
            "kcat_v_starch": 0.32,
            "km_v_ATPsynth_ADP_st": 0.014,
            "km_v_ATPsynth_Pi_st": 0.3,
            "kcat_v_ATPsynth": 2.8,
            "Enz0_v_ATPsynth": 1.0,
        }
    )

    m.add_variables(
        {
            "PGA": 0.6387788347932627,
            "BPGA": 0.0013570885908749779,
            "GAP": 0.011259431827358068,
            "DHAP": 0.24770748227012374,
            "FBP": 0.01980222074817044,
            "F6P": 1.093666906864421,
            "G6P": 2.5154338857582377,
            "G1P": 0.14589516537322303,
            "SBP": 0.09132688566151095,
            "S7P": 0.23281380022778891,
            "E4P": 0.02836065066520614,
            "X5P": 0.03647242425941113,
            "R5P": 0.06109130988031577,
            "RUBP": 0.2672164362349537,
            "RU5P": 0.0244365238237522,
            "ATP_st": 0.43633201706180874,
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
