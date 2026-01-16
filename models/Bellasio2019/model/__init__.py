
from mxlpy import Model, Variable, InitialAssignment
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = ["Bellasio2019"]

def co2_initial(ca, Kh_co2):
    return 0.3 * ca / Kh_co2

def ci_initial(ca):
    return 0.65 * ca


def Bellasio2019() -> Model:
    m = Model()

    m.add_parameters(
        {
            "AP_tot": 1.5,
            "Pi_tot": 15,
            "p_o2": 210000,
            "Kh_o2": 833300,
            "V_m": 0.03,
            "PPFD": 1500,
            "RLight": 0.001,
            "s": 0.43,
            "PhiPSII_LL": 0.72,
            "PhiPSI_LL": 1,
            "alpha_ppfd_PhiPSII": 0.00125,
            "V0_ppfd_PhiPSII": -0.8,
            "theta_ppfd_PhiPSII": 0.7,
            "f_pseudocycNR": 0.01,
            "fq": 1,
            "f_ndh": 0,
            "h": 4,
            "Ca": 400,
            "alpha_ppfd_rub": 0.0018,
            "V0_ppfd_rub": 0.16,
            "theta_ppfd_rub": 0.95,
            "alpha_co2": 400,
            "V0_co2": -0.2,
            "theta_co2": 0.98,
            "tau_i": 360,
            "tau_d": 1200,
            "km_v_RuBisCO_c_CO2": 0.014,
            "km_v_RuBisCO_c_RUBP": 0.02,
            "km_v_RuBisCO_c_O2": 0.222,
            "ki_v_RuBisCO_c_PGA": 2.52,
            "ki_v_RuBisCO_c_NADP_st": 0.21,
            "ki_v_RuBisCO_c_ADP_st": 0.2,
            "ki_v_RuBisCO_c_Pi_st": 3.6,
            "vmax_v_RuBisCO_c": 0.2,
            "kcat_v_RuBisCO_c": 4.7,
            "S_co_gas": 2200,
            "vmax_v_PRKase": 1.17,
            "keq_v_PRKase": 6846,
            "km_v_PRKase_ATP_st": 0.625,
            "ki_v_PRKase_ADP_st": 0.1,
            "km_v_PRKase_RU5P": 0.034,
            "ki_v_PRKase_PGA": 2,
            "ki_v_PRKase_RUBP": 0.7,
            "ki_v_PRKase_Pi_st": 4,
            "vmax_v_pgareduction": 0.4,
            "km_v_pgareduction_ATP_st": 0.3,
            "km_v_pgareduction_PGA": 10,
            "km_v_pgareduction_NADPH_st": 0.05,
            "ki_v_pgareduction_ADP_st": 0.89,
            "vmax_v_carbohydrate_synthesis": 0.2235,
            "keq_v_carbohydrate_synthesis": 0.8,
            "km_v_carbohydrate_synthesis_DHAP": 22,
            "ki_v_carbohydrate_synthesis_ADP_st": 1,
            "vmax_v_rpp": 0.0585,
            "keq_v_rpp": 0.06,
            "km_v_rpp_DHAP": 0.5,
            "H": 5.012e-05,
            "vmax_v_co2_hydration": 200,
            "keq_v_co2_hydration": 0.00056,
            "km_v_co2_hydration_CO2": 2.8,
            "km_v_co2_hydration_HCO3": 34,
            "keq_v_FNR": 502,
            "km_v_FNR_NADP_st": 0.0072,
            "km_v_FNR_NADPH_st": 0.036,
            "Kj_NADPH": 200,
            "keq_v_ATPsynth": 5734,
            "km_v_ATPsynth_ADP_st": 0.014,
            "km_v_ATPsynth_Pi_st": 0.3,
            "km_v_ATPsynth_ATP_st": 0.3,
            "Kj_ATP": 200,
            "gm": 0.5,
            "Kh_co2": 30303.0303030303,
            "Kd": 150,
            "Ki": 900,
            "tau0": -0.1,
            "chi_beta": 0.5,
            "phi": 0,
            "pi_e": 1.2,
            "Kh": 12,
            "Ds": 10,
            "gs0": 0.01,
            "NADP_tot": 0.5,
        }
    )
    m.add_variables(
        {
            "CO2": InitialAssignment(fn=co2_initial, args=['Ca', 'Kh_co2'], unit="REPLACE"),
            "HCO3": Variable(0.1327, unit="REPLACE"),
            "RUBP": Variable(2, unit="REPLACE"),
            "PGA": Variable(4, unit="REPLACE"),
            "DHAP": Variable(4, unit="REPLACE"),
            "ATP_st": Variable(0.68, unit="REPLACE"),
            "NADPH_st": Variable(0.21, unit="REPLACE"),
            "RU5P": Variable(0.34, unit="REPLACE"),
            "Ract": Variable(1, unit="REPLACE"),
            "J_NADPH": Variable(0.1, unit="REPLACE"),
            "J_ATP": Variable(0.16, unit="REPLACE"),
            "Ci": InitialAssignment(fn=ci_initial, args=['Ca'], unit="REPLACE"),
            "gs": Variable(0.334934046786077, unit="REPLACE"),
        }
    )
    m = include_derived_quantities(m)
    m = include_rates(m)

    return m