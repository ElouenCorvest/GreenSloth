
from mxlpy import Model
from mxlpy.surrogates import qss
import numpy as np
import math
from typing import cast, Iterable
    
from .basic_funcs import (
    div,
    moiety_1,
)

def _pi_bellasio2019(total, pga, dhap, ru5p, rubp, atp):
    return total - pga - dhap - ru5p - 2 * rubp - atp

def _Et(vmax_rub, kcat_rub, V_m):
    return (vmax_rub / kcat_rub) / V_m

def _km_rubp_extra(pga, nadp, adp, pi, km_rubp, ki_pga, ki_nadp, ki_adp, ki_pi):
    return km_rubp * (1 + pga / ki_pga + nadp / ki_nadp + adp / ki_adp + pi / ki_pi)

def _f_rubp(rubp, Et, k_extra_rubp):
    top = Et + k_extra_rubp + rubp - np.sqrt((Et + k_extra_rubp + rubp)**2 - 4 * rubp * Et)
    bottom = 2 * Et
    return top / bottom

def non_rect_hyperbole(x, alpha, V0, theta):
    # print(np.sqrt((alpha * x + 1 - V0)**2 - 4 * alpha * x * theta))
    # top = alpha * x + 1 - V0 - np.sqrt((alpha * x + 1 - V0)**2 - 4 * alpha * x * theta)
    # bottom = 2 * theta
    return (alpha * x + 1 - V0) / (2*theta) - np.sqrt((alpha * x + 1 - V0)**2 - 4 * alpha * x * theta * (1-V0)) / (2* theta) + V0

def _Ract_eq(co2, ppfd, alpha_ppfd, V0_ppfd, theta_ppfd, alpha_co2, V0_co2, theta_co2):
    f_ppfd = non_rect_hyperbole(ppfd, alpha_ppfd, V0_ppfd, theta_ppfd)
    f_co2 = non_rect_hyperbole(co2, alpha_co2, V0_co2, theta_co2)
    return f_ppfd * f_co2

def _i20(pfd, s):
    return pfd * s

def _i10(i_20, y_ii_ll, y_i_ll):
    return i_20 * y_ii_ll / y_i_ll

def _chi(f_cyc, y_ii_ll):
    return f_cyc / (1 + f_cyc + y_ii_ll)

def _i1(chi, i10):
    return (1 + chi) * i10

def _f_cyc(j_atp, j_nadph, v_atp, v_fnr):
    return max(0, -1 + 15**(v_atp / j_atp - v_fnr / j_nadph))

def _i2(y_ii_ll, chi, i20):
    return (1 / y_ii_ll - chi) * i20 * y_ii_ll

def _y_ii(y_ii_ll, v_atp, j_atp, v_fnr, j_nadph, pfd, alpha, V0, theta):
    f_ppfd = non_rect_hyperbole(pfd, alpha, V0, theta)
    return y_ii_ll * (v_atp / j_atp) * (v_fnr / j_nadph) * (1 - max(0, f_ppfd))

def _j2(i2, y_ii):
    return i2 * y_ii

def _j1(j2, f_cyc):
    return j2 / 1 - f_cyc

def _f_pseudocyc(j_nadph, o2, v_fnr, f_pseudocycNR):
    return f_pseudocycNR + 4 * o2 * (1 - v_fnr / j_nadph)

def _j_nadph_steady(j1, f_cyc, f_pseudocyc):
    top = 1 - f_cyc - f_pseudocyc
    bottom = 2
    return (j1 * top / bottom) / 1000 # Added from Excel

def _j_atp_steady(j2, j1, f_cyc, fq, f_ndh, h):
    jcyt = (1 - fq) * j1
    jq = fq * j1
    jndh = f_cyc * f_ndh * j1
    
    return ((j2 + jcyt + 2 * jq + 2 * jndh) / h) / 1000 # Added from Excel

def _gs_steady(tau0, f_rubp, chi_beta, phi, pi_e, Kh, Ds, gs0):

    tau = tau0 + f_rubp
    top = chi_beta * tau * (phi + pi_e)
    bottom = 1 + chi_beta * tau * (1 / Kh) * Ds
    
    return max(gs0, top / bottom)

def _calc_ass(vc, vo, RLight):
    return vc - 0.5 * vo - RLight


def include_derived_quantities(m: Model):
    
    m.add_derived(
        name="ADP_st",
        fn=moiety_1,
        args=['ATP_st', 'AP_tot'],
    )

    m.add_derived(
        name="NADP_st",
        fn=moiety_1,
        args=['NADPH_st', 'NADP_tot'],
    )

    m.add_derived(
        name="Pi_st",
        fn=_pi_bellasio2019,
        args=['Pi_tot', 'PGA', 'DHAP', 'RU5P', 'RUBP', 'ATP_st'],
    )

    m.add_derived(
        name="Et",
        fn=_Et,
        args=['vmax_v_RuBisCO_c', 'kcat_v_RuBisCO_c', 'V_m'],
    )

    m.add_derived(
        name="km_v_RuBisCO_c_RUBP_extra",
        fn=_km_rubp_extra,
        args=['PGA', 'NADP_st', 'ADP_st', 'Pi_st', 'km_v_RuBisCO_c_RUBP', 'ki_v_RuBisCO_c_PGA', 'ki_v_RuBisCO_c_NADP_st', 'ki_v_RuBisCO_c_ADP_st', 'ki_v_RuBisCO_c_Pi_st'],
    )

    m.add_derived(
        name="f_rubp",
        fn=_f_rubp,
        args=['RUBP', 'Et', 'km_v_RuBisCO_c_RUBP_extra'],
    )

    m.add_derived(
        name="O2",
        fn=div,
        args=['p_o2', 'Kh_o2'],
    )

    m.add_derived(
        name="Ract_eq",
        fn=_Ract_eq,
        args=['CO2', 'PPFD', 'alpha_ppfd_rub', 'V0_ppfd_rub', 'theta_ppfd_rub', 'alpha_co2', 'V0_co2', 'theta_co2'],
    )

    m.add_derived(
        name="I2_0",
        fn=_i20,
        args=['PPFD', 's'],
    )

    m.add_derived(
        name="I1_0",
        fn=_i10,
        args=['I2_0', 'PhiPSII_LL', 'PhiPSI_LL'],
    )

    m.add_derived(
        name="chi",
        fn=_chi,
        args=['f_cyc', 'PhiPSII_LL'],
    )

    m.add_derived(
        name="I1",
        fn=_i1,
        args=['chi', 'I1_0'],
    )

    m.add_derived(
        name="f_cyc",
        fn=_f_cyc,
        args=['J_ATP', 'J_NADPH', 'v_ATPsynth', 'v_FNR'],
    )

    m.add_derived(
        name="I2",
        fn=_i2,
        args=['PhiPSII_LL', 'chi', 'I2_0'],
    )

    m.add_derived(
        name="PhiPSII",
        fn=_y_ii,
        args=['PhiPSII_LL', 'v_ATPsynth', 'J_ATP', 'v_FNR', 'J_NADPH', 'PPFD', 'alpha_ppfd_PhiPSII', 'V0_ppfd_PhiPSII', 'theta_ppfd_PhiPSII'],
    )

    m.add_derived(
        name="J2",
        fn=_j2,
        args=['I2', 'PhiPSII'],
    )

    m.add_derived(
        name="J1",
        fn=_j1,
        args=['J2', 'f_cyc'],
    )

    m.add_derived(
        name="f_pseudocyc",
        fn=_f_pseudocyc,
        args=['J_NADPH', 'O2', 'v_FNR', 'f_pseudocycNR'],
    )

    m.add_derived(
        name="J_NADPH_steady",
        fn=_j_nadph_steady,
        args=['J1', 'f_cyc', 'f_pseudocyc'],
    )

    m.add_derived(
        name="J_ATP_steady",
        fn=_j_atp_steady,
        args=['J2', 'J1', 'f_cyc', 'fq', 'f_ndh', 'h'],
    )

    m.add_derived(
        name="gs_steady",
        fn=_gs_steady,
        args=['tau0', 'f_rubp', 'chi_beta', 'phi', 'pi_e', 'Kh', 'Ds', 'gs0'],
    )

    m.add_derived(
        name="A",
        fn=_calc_ass,
        args=['v_RuBisCO_c', 'rubisco_oxygenase', 'RLight'],
    )


    return m