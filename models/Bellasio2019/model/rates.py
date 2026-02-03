
from mxlpy import Model, Derived
import numpy as np
from typing import cast
    
from .basic_funcs import (
    value,
    one_div,
)

def ract_gs_time_dependance(x, x_steady, inc, dec):
    if x < x_steady:
        return (x_steady - x) / inc
    else:
        return (x_steady - x) / dec

def atp_nadph_time_dependance(j_x, j_x_steady, kj_x):
    if j_x < j_x_steady:
        return (j_x_steady - j_x) / kj_x
    else:
        return (j_x_steady - j_x) / (0.1 * kj_x)

def _rubisco_carboxylation_bellasio(rubp, co2, Ract, km_co2, o2, km_o2, vmax_rc, f_rubp, k_extra_rubp):
    k_extra_co2 = km_co2 * (1 + o2 / km_o2)
    
    top = vmax_rc * Ract * f_rubp * rubp * co2
    bottom = (k_extra_co2 + co2) * (k_extra_rubp + rubp)
    
    return top / bottom

def neg_one_div(x: float) -> float:
    return -1.0 / x

def two_div(x: float) -> float:
    return 2.0 / x

def _rubisco_oxygenase_bellasio(co2, o2, S_co_gas, v_c, Kh_o2, Kh_co2):
    S_co_liq = S_co_gas / Kh_o2 * Kh_co2
    gamma_star = 1 / (2* S_co_liq)
    
    return v_c * 2 * gamma_star * o2 / co2

def neg_half_div(x: float) -> float:
    return -0.5 / x

def half_div(x: float) -> float:
    return 0.5 / x

def _prkase(atp, rubp, ru5p, pga, adp, pi, vmax, k_eq, km_atp, ki_adp, km_ru5p, ki_pga, ki_rubp, ki_pi):
    top = vmax * (atp * ru5p - adp * rubp / k_eq) # ERROR: Different from paper (typo?)
    bottom = (atp + km_atp * (1 + adp / ki_adp)) * (ru5p + km_ru5p * (1 + pga / ki_pga + rubp / ki_rubp + pi / ki_pi))
    return top / bottom

def neg_fivethirds_div(x):
    return -(5/3) * (1 / x)

def _v_pgareduction(atp, pga, nadph, adp, vmax, km_atp, km_pga, km_nadph, ki_adp):
    top = vmax * atp * pga * nadph
    bottom = (pga + km_pga * (1 + adp / ki_adp)) * (atp + km_atp * (1+ adp / ki_adp)) * (nadph + km_nadph * (1 + adp / ki_adp))
    return top / bottom

def _v_carbohydrate_synthesis(dhap, pi, adp, vmax, v_pgareduction, keq, km_dhap, ki_adp):
    top = vmax * (dhap - 0.4) * (1 - np.abs(v_pgareduction) * pi / keq)
    bottom = dhap + km_dhap * (1 + adp / ki_adp)
    return top / bottom

def _v_rpp(dhap, ru5p, vmax, k_eq, km_dhap):
    top = vmax *  (dhap - ru5p / k_eq)
    bottom = dhap + km_dhap
    return top / bottom

def _v_co2_hydration(co2, hco3, proton, vmax, k_eq, km_co2, km_hco3):
    top = vmax * (co2 - hco3 * proton / k_eq)
    bottom = km_co2 * (1 + co2 / km_co2 + hco3 / km_hco3)
    return top / bottom

def neg_onethirds_div(x):
    return -(1/3) * (1 / x)

def _v_fnr(nadph, nadp, j_nadph, k_eq, km_nadp, km_nadph):
    top = j_nadph * (nadp - nadph/k_eq)
    bottom = km_nadp * (1 + nadp / km_nadp + nadph/km_nadph)
    return top / bottom

def _v_atp(atp, adp, pi, j_atp, k_eq, km_adp, km_pi, km_atp):
    top = j_atp * (adp * pi - atp / k_eq)
    bottom = km_adp * km_pi * (1 + adp / km_adp + atp / km_atp + pi / km_pi + adp * pi / (km_adp * km_pi))
    return top / bottom

def _co2_diss(ci, co2, gm, Kh_co2):
    return (gm * (ci - co2 * Kh_co2)) / 1000

def _stom_diff(ci, gs, ca):
    return (gs * (ca - ci)) / 1000


def include_rates(m: Model):
    
    m.add_reaction(
        name="Ract_rate",
        fn=ract_gs_time_dependance,
        args=['Ract', 'Ract_eq', 'tau_i', 'tau_d'],
        stoichiometry={"Ract": 1, }
    )
    m.add_reaction(
        name="v_J_NADPH",
        fn=atp_nadph_time_dependance,
        args=['J_NADPH', 'J_NADPH_steady', 'Kj_NADPH'],
        stoichiometry={"J_NADPH": 1, }
    )
    m.add_reaction(
        name="v_J_ATP",
        fn=atp_nadph_time_dependance,
        args=['J_ATP', 'J_ATP_steady', 'Kj_ATP'],
        stoichiometry={"J_ATP": 1, }
    )
    m.add_reaction(
        name="v_gs",
        fn=ract_gs_time_dependance,
        args=['gs', 'gs_steady', 'Ki', 'Kd'],
        stoichiometry={"gs": 1, }
    )
    m.add_reaction(
        name="v_RuBisCO_c",
        fn=_rubisco_carboxylation_bellasio,
        args=['RUBP', 'CO2', 'Ract', 'km_v_RuBisCO_c_CO2', 'O2', 'km_v_RuBisCO_c_O2', 'vmax_v_RuBisCO_c', 'f_rubp', 'km_v_RuBisCO_c_RUBP_extra'],
        stoichiometry={"CO2": Derived(fn=neg_one_div, args=['V_m'], unit=None), "RUBP": Derived(fn=neg_one_div, args=['V_m'], unit=None), "PGA": Derived(fn=two_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="rubisco_oxygenase",
        fn=_rubisco_oxygenase_bellasio,
        args=['CO2', 'O2', 'S_co_gas', 'v_RuBisCO_c', 'Kh_o2', 'Kh_co2'],
        stoichiometry={"RUBP": Derived(fn=neg_one_div, args=['V_m'], unit=None), "PGA": Derived(fn=one_div, args=['V_m'], unit=None), "ATP_st": Derived(fn=neg_one_div, args=['V_m'], unit=None), "NADPH_st": Derived(fn=neg_half_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="glycine_decarboxylase",
        fn=value,
        args=['rubisco_oxygenase'],
        stoichiometry={"CO2": Derived(fn=half_div, args=['V_m'], unit=None), "PGA": Derived(fn=half_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_PRKase",
        fn=_prkase,
        args=['ATP_st', 'RUBP', 'RU5P', 'PGA', 'ADP_st', 'Pi_st', 'vmax_v_PRKase', 'keq_v_PRKase', 'km_v_PRKase_ATP_st', 'ki_v_PRKase_ADP_st', 'km_v_PRKase_RU5P', 'ki_v_PRKase_PGA', 'ki_v_PRKase_RUBP', 'ki_v_PRKase_Pi_st'],
        stoichiometry={"RUBP": Derived(fn=one_div, args=['V_m'], unit=None), "DHAP": Derived(fn=neg_fivethirds_div, args=['V_m'], unit=None), "ATP_st": Derived(fn=neg_one_div, args=['V_m'], unit=None), "RU5P": Derived(fn=neg_one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_pgareduction",
        fn=_v_pgareduction,
        args=['ATP_st', 'PGA', 'NADPH_st', 'ADP_st', 'vmax_v_pgareduction', 'km_v_pgareduction_ATP_st', 'km_v_pgareduction_PGA', 'km_v_pgareduction_NADPH_st', 'ki_v_pgareduction_ADP_st'],
        stoichiometry={"PGA": Derived(fn=neg_one_div, args=['V_m'], unit=None), "DHAP": Derived(fn=one_div, args=['V_m'], unit=None), "ATP_st": Derived(fn=neg_one_div, args=['V_m'], unit=None), "NADPH_st": Derived(fn=neg_one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_carbohydrate_synthesis",
        fn=_v_carbohydrate_synthesis,
        args=['DHAP', 'Pi_st', 'ADP_st', 'vmax_v_carbohydrate_synthesis', 'v_pgareduction', 'keq_v_carbohydrate_synthesis', 'km_v_carbohydrate_synthesis_DHAP', 'ki_v_carbohydrate_synthesis_ADP_st'],
        stoichiometry={"DHAP": Derived(fn=neg_one_div, args=['V_m'], unit=None), "ATP_st": Derived(fn=neg_half_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_rpp",
        fn=_v_rpp,
        args=['DHAP', 'RU5P', 'vmax_v_rpp', 'keq_v_rpp', 'km_v_rpp_DHAP'],
        stoichiometry={"RU5P": Derived(fn=one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_co2_hydration",
        fn=_v_co2_hydration,
        args=['CO2', 'HCO3', 'H', 'vmax_v_co2_hydration', 'keq_v_co2_hydration', 'km_v_co2_hydration_CO2', 'km_v_co2_hydration_HCO3'],
        stoichiometry={"CO2": Derived(fn=neg_one_div, args=['V_m'], unit=None), "HCO3": Derived(fn=one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_RLight",
        fn=value,
        args=['RLight'],
        stoichiometry={"CO2": Derived(fn=one_div, args=['V_m'], unit=None), "PGA": Derived(fn=neg_onethirds_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_FNR",
        fn=_v_fnr,
        args=['NADPH_st', 'NADP_st', 'J_NADPH', 'keq_v_FNR', 'km_v_FNR_NADP_st', 'km_v_FNR_NADPH_st'],
        stoichiometry={"NADPH_st": Derived(fn=one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="v_ATPsynth",
        fn=_v_atp,
        args=['ATP_st', 'ADP_st', 'Pi_st', 'J_ATP', 'keq_v_ATPsynth', 'km_v_ATPsynth_ADP_st', 'km_v_ATPsynth_Pi_st', 'km_v_ATPsynth_ATP_st'],
        stoichiometry={"ATP_st": Derived(fn=one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="CO2_dissolution",
        fn=_co2_diss,
        args=['Ci', 'CO2', 'gm', 'Kh_co2'],
        stoichiometry={"Ci": -1, "CO2": Derived(fn=one_div, args=['V_m'], unit=None), }
    )
    m.add_reaction(
        name="CO2_stomatal_diffusion",
        fn=_stom_diff,
        args=['Ci', 'gs', 'Ca'],
        stoichiometry={"Ci": 1, }
    )

    return m