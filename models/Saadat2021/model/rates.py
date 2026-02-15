from mxlpy import Model, Derived, units
import numpy as np
from typing import cast

from .basic_funcs import (
    rapid_equilibrium_1s_1p,
    michaelis_menten_1s_1i,
    protons_stroma,
    rapid_equilibrium_2s_1p,
    mass_action_1s,
    michaelis_menten_1s_2i,
    neg_div,
    value,
    rapid_equilibrium_2s_2p,
    mass_action_2s,
    rapid_equilibrium_3s_3p,
)


def _rate_atp_synthase_2019(
    ATP: float,
    ADP: float,
    Keq_ATPsynthase: float,
    kATPsynth: float,
    convf: float,
) -> float:
    return kATPsynth * (ADP / convf - ATP / convf / Keq_ATPsynthase)


def _b6f(
    PC_ox: float,
    PQ_ox: float,
    PQ_red: float,
    PC_red: float,
    Keq_B6f: float,
    kCytb6f: float,
) -> float:
    return cast(
        float,
        np.maximum(
            kCytb6f * (PQ_red * PC_ox**2 - PQ_ox * PC_red**2 / Keq_B6f),
            -kCytb6f,
        ),
    )


def _four_div_by(x: float) -> float:
    return 4.0 / x


def _protonation_hill(
    vx: float,
    h: float,
    nh: float,
    k_fwd: float,
    k_ph_sat: float,
) -> float:
    return k_fwd * (h**nh / (h**nh + protons_stroma(k_ph_sat) ** nh)) * vx  # type: ignore


def _rate_cyclic_electron_flow(
    Pox: float,
    Fdred: float,
    kcyc: float,
) -> float:
    return kcyc * Fdred**2 * Pox


def _rate_protonation_hill(
    Vx: float,
    H: float,
    k_fwd: float,
    nH: float,
    kphSat: float,
) -> float:
    return k_fwd * (H**nH / (H**nH + protons_stroma(kphSat) ** nH)) * Vx  # type: ignore


def _rate_fnr_2019(
    Fd_ox: float,
    Fd_red: float,
    NADPH: float,
    NADP: float,
    KM_FNR_F: float,
    KM_FNR_N: float,
    vmax: float,
    Keq_FNR: float,
    convf: float,
) -> float:
    fdred = Fd_red / KM_FNR_F
    fdox = Fd_ox / KM_FNR_F
    nadph = NADPH / convf / KM_FNR_N
    nadp = NADP / convf / KM_FNR_N
    return (
        vmax
        * (fdred**2 * nadp - fdox**2 * nadph / Keq_FNR)
        / ((1 + fdred + fdred**2) * (1 + nadp) + (1 + fdox + fdox**2) * (1 + nadph) - 1)
    )


def _rate_ps2(
    b1: float,
    k2: float,
) -> float:
    return 0.5 * k2 * b1


def _two_div_by(x: float) -> float:
    return 2.0 / x


def _rate_ps1(
    a: float,
    ps2cs: float,
    pfd: float,
) -> float:
    return (1 - ps2cs) * pfd * a


def _rate_ferredoxin_reductase(
    Fd: float,
    Fdred: float,
    A1: float,
    A2: float,
    kFdred: float,
    Keq_FAFd: float,
) -> float:
    """rate of the redcution of Fd by the activity of PSI
    used to be equall to the rate of PSI but now
    alternative electron pathway from Fd allows for the production of ROS
    hence this rate has to be separate
    """
    return kFdred * Fd * A1 - kFdred / Keq_FAFd * Fdred * A2


def _rate_leak(
    protons_lumen: float,
    ph_stroma: float,
    k_leak: float,
) -> float:
    return k_leak * (protons_lumen - protons_stroma(ph_stroma))


def _neg_one_div_by(x: float) -> float:
    return -1.0 / x


def _rate_state_transition_ps1_ps2(
    ant: float,
    pox: float,
    p_tot: float,
    k_stt7: float,
    km_st: float,
    n_st: float,
) -> float:
    return k_stt7 * (1 / (1 + (pox / p_tot / km_st) ** n_st)) * ant


def _rate_poolman_5i(
    rubp: float,
    pga: float,
    co2: float,
    vmax: float,
    kms_rubp: float,
    kms_co2: float,
    # inhibitors
    ki_pga: float,
    fbp: float,
    ki_fbp: float,
    sbp: float,
    ki_sbp: float,
    pi: float,
    ki_p: float,
    nadph: float,
    ki_nadph: float,
) -> float:
    top = vmax * rubp * co2
    btm = (
        rubp
        + kms_rubp
        * (
            1
            + pga / ki_pga
            + fbp / ki_fbp
            + sbp / ki_sbp
            + pi / ki_p
            + nadph / ki_nadph
        )
    ) * (co2 + kms_co2)
    return top / btm


def _rate_prk(
    ru5p: float,
    atp: float,
    pi: float,
    pga: float,
    rubp: float,
    adp: float,
    v13: float,
    km131: float,
    km132: float,
    ki131: float,
    ki132: float,
    ki133: float,
    ki134: float,
    ki135: float,
) -> float:
    return (
        v13
        * ru5p
        * atp
        / (
            (ru5p + km131 * (1 + pga / ki131 + rubp / ki132 + pi / ki133))
            * (atp * (1 + adp / ki134) + km132 * (1 + adp / ki135))
        )
    )


def _rate_out(
    s1: float,
    n_total: float,
    vmax_efflux: float,
    k_efflux: float,
) -> float:
    return vmax_efflux * s1 / (n_total * k_efflux)


def _rate_out_2(
    s1: float,
    n_total: float,
    vmax_efflux: float,
    k_efflux: float,
) -> float:
    return vmax_efflux * s1 / (n_total * k_efflux)


def _rate_starch(
    g1p: float,
    atp: float,
    adp: float,
    pi: float,
    pga: float,
    f6p: float,
    fbp: float,
    v_st: float,
    kmst1: float,
    kmst2: float,
    ki_st: float,
    kast1: float,
    kast2: float,
    kast3: float,
) -> float:
    return (
        v_st
        * g1p
        * atp
        / (
            (g1p + kmst1)
            * (
                (1 + adp / ki_st) * (atp + kmst2)
                + kmst2 * pi / (kast1 * pga + kast2 * f6p + kast3 * fbp)
            )
        )
    )


def _rate_mda_reductase(
    mda: float,
    k3: float,
) -> float:
    return k3 * mda**2


def _rate_mda_reductase_2(
    nadph: float,
    mda: float,
    vmax: float,
    km_nadph: float,
    km_mda: float,
) -> float:
    """Compare Valero et al. 2016"""
    nom = vmax * nadph * mda
    denom = km_nadph * mda + km_mda * nadph + nadph * mda + km_nadph * km_mda
    return nom / denom


def _rate_ascorbate_peroxidase(
    A: float,
    H: float,
    kf1: float,
    kr1: float,
    kf2: float,
    kr2: float,
    kf3: float,
    kf4: float,
    kr4: float,
    kf5: float,
    XT: float,
) -> float:
    """lumped reaction of ascorbate peroxidase
    the cycle stretched to a linear chain with
    two steps producing the MDA
    two steps releasing ASC
    and one step producing hydrogen peroxide
    """
    nom = A * H * XT
    denom = (
        A * H * (1 / kf3 + 1 / kf5)
        + A / kf1
        + H / kf4
        + H * kr4 / (kf4 * kf5)
        + H / kf2
        + H * kr2 / (kf2 * kf3)
        + kr1 / (kf1 * kf2)
        + kr1 * kr2 / (kf1 * kf2 * kf3)
    )
    return nom / denom


def _rate_glutathion_reductase(
    nadph: float,
    gssg: float,
    vmax: float,
    km_nadph: float,
    km_gssg: float,
) -> float:
    nom = vmax * nadph * gssg
    denom = km_nadph * gssg + km_gssg * nadph + nadph * gssg + km_nadph * km_gssg
    return nom / denom


def _rate_dhar(
    dha: float,
    gsh: float,
    vmax: float,
    km_dha: float,
    km_gsh: float,
    k: float,
) -> float:
    nom = vmax * dha * gsh
    denom = k + km_dha * gsh + km_gsh * dha + dha * gsh
    return nom / denom


def include_rates(m: Model):
    m.add_reaction(
        name="v_FdTrReduc",
        fn=mass_action_2s,
        args=["TRX_ox", "Fd_red", "kf_v_FdTrReduc"],
        stoichiometry={
            "TRX_ox": -1,
            "Fd_ox": 1,
        },
    )
    m.add_reaction(
        name="v_Eact",
        fn=mass_action_2s,
        args=["E_CBB_inactive", "TRX_red", "kf_v_Eact"],
        stoichiometry={
            "E_CBB_inactive": -5,
            "TRX_ox": 5,
        },
    )
    m.add_reaction(
        name="v_Einact",
        fn=mass_action_1s,
        args=["E_CBB_active", "kf_v_Einact"],
        stoichiometry={
            "E_CBB_inactive": 5,
        },
    )
    m.add_reaction(
        name="v_ATPsynth",
        fn=_rate_atp_synthase_2019,
        args=["ATP_st", "ADP_st", "keq_v_ATPsynth", "kf_v_ATPsynth", "convf"],
        stoichiometry={
            "H_lumen": Derived(fn=neg_div, args=["HPR", "bH"], unit=None),
            "ATP_st": Derived(fn=value, args=["convf"], unit=None),
        },
    )
    m.add_reaction(
        name="v_b6f",
        fn=_b6f,
        args=["PC_ox", "PQ", "PQH_2", "PC_red", "keq_v_b6f", "kcat_v_b6f"],
        stoichiometry={
            "PC_ox": -2,
            "PQ": 1,
            "H_lumen": Derived(fn=_four_div_by, args=["bH"], unit=None),
        },
    )
    m.add_reaction(
        name="v_PsbSP",
        fn=_protonation_hill,
        args=["psbS", "H_lumen", "kh_v_PsbSP", "kf_v_PsbSP", "ksat_v_PsbSP"],
        stoichiometry={
            "psbS": -1,
        },
    )
    m.add_reaction(
        name="v_PsbSD",
        fn=mass_action_1s,
        args=["PsbSP", "kf_v_PsbSD"],
        stoichiometry={
            "psbS": 1,
        },
    )
    m.add_reaction(
        name="v_Cyc",
        fn=_rate_cyclic_electron_flow,
        args=["PQ", "Fd_red", "kf_v_Cyc"],
        stoichiometry={
            "PQ": -1,
            "Fd_ox": 2,
        },
    )
    m.add_reaction(
        name="v_Deepox",
        fn=_rate_protonation_hill,
        args=["Vx", "H_lumen", "kf_v_Deepox", "kh_v_Deepox", "ksat_v_Deepox"],
        stoichiometry={
            "Vx": -1,
        },
    )
    m.add_reaction(
        name="v_Epox",
        fn=mass_action_1s,
        args=["Zx", "kf_v_Epox"],
        stoichiometry={
            "Vx": 1,
        },
    )
    m.add_reaction(
        name="v_FNR",
        fn=_rate_fnr_2019,
        args=[
            "Fd_ox",
            "Fd_red",
            "NADPH_st",
            "NADP_st",
            "km_v_FNR_Fd_red",
            "km_v_FNR_NADP_st",
            "vmax_v_FNR",
            "keq_v_FNR",
            "convf",
        ],
        stoichiometry={
            "Fd_ox": 2,
            "NADPH_st": Derived(fn=value, args=["convf"], unit=None),
        },
    )
    m.add_reaction(
        name="v_NDH",
        fn=mass_action_1s,
        args=["PQ", "kf_v_NDH"],
        stoichiometry={
            "PQ": -1,
        },
    )
    m.add_reaction(
        name="v_PSII",
        fn=_rate_ps2,
        args=["B1", "k2"],
        stoichiometry={
            "PQ": -1,
            "H_lumen": Derived(fn=_two_div_by, args=["bH"], unit=None),
        },
    )
    m.add_reaction(
        name="v_PSI",
        fn=_rate_ps1,
        args=["Y0", "psIIcross", "PPFD"],
        stoichiometry={
            "PC_ox": 1,
        },
    )
    m.add_reaction(
        name="v_Mehler",
        fn=mass_action_2s,
        args=["Y1", "O2_lumen", "kMehler"],
        stoichiometry={
            "H2O2": Derived(fn=value, args=["convf"], unit=None),
        },
    )
    m.add_reaction(
        name="v_Fdred",
        fn=_rate_ferredoxin_reductase,
        args=["Fd_ox", "Fd_red", "Y1", "Y2", "vmax_v_Fdred", "keq_v_Fdred"],
        stoichiometry={
            "Fd_ox": -1,
        },
    )
    m.add_reaction(
        name="v_Leak",
        fn=_rate_leak,
        args=["H_lumen", "pH_stroma", "kf_v_Leak"],
        stoichiometry={
            "H_lumen": Derived(fn=_neg_one_div_by, args=["bH"], unit=None),
        },
    )
    m.add_reaction(
        name="v_PQ",
        fn=mass_action_2s,
        args=["PQH_2", "O2_lumen", "kPTOX"],
        stoichiometry={
            "PQ": 1,
        },
    )
    m.add_reaction(
        name="v_St12",
        fn=_rate_state_transition_ps1_ps2,
        args=["LHC", "PQ", "PQ_tot", "kStt7", "km_v_St12", "n_ST"],
        stoichiometry={
            "LHC": -1,
        },
    )
    m.add_reaction(
        name="v_St21",
        fn=mass_action_1s,
        args=["LHCp", "kPph1"],
        stoichiometry={
            "LHC": 1,
        },
    )
    m.add_reaction(
        name="v_RuBisCO_c",
        fn=_rate_poolman_5i,
        args=[
            "RUBP",
            "PGA",
            "CO2",
            "vmax_v_RuBisCO_c",
            "km_v_RuBisCO_c_RUBP",
            "km_v_RuBisCO_c_CO2",
            "ki_v_RuBisCO_c_PGA",
            "FBP",
            "ki_v_RuBisCO_c_FBP",
            "SBP",
            "ki_v_RuBisCO_c_SBP",
            "Pi_st",
            "ki_v_RuBisCO_c_Pi_st",
            "NADPH_st",
            "ki_v_RuBisCO_c_NADPH_st",
        ],
        stoichiometry={
            "RUBP": -1.0,
            "PGA": 2.0,
        },
    )
    m.add_reaction(
        name="v_PGK1ase",
        fn=rapid_equilibrium_2s_2p,
        args=["PGA", "ATP_st", "BPGA", "ADP_st", "kre_v_PGK1ase", "keq_v_PGK1ase"],
        stoichiometry={
            "PGA": -1.0,
            "ATP_st": -1.0,
            "BPGA": 1.0,
        },
    )
    m.add_reaction(
        name="v_BPGAdehynase",
        fn=rapid_equilibrium_3s_3p,
        args=[
            "BPGA",
            "NADPH_st",
            "H_stroma",
            "GAP",
            "NADP_st",
            "Pi_st",
            "kre_v_BPGAdehynase",
            "keq_v_BPGAdehynase",
        ],
        stoichiometry={
            "NADPH_st": -1.0,
            "BPGA": -1.0,
            "GAP": 1.0,
        },
    )
    m.add_reaction(
        name="v_TPIase",
        fn=rapid_equilibrium_1s_1p,
        args=["GAP", "DHAP", "kre_v_TPIase", "keq_v_TPIase"],
        stoichiometry={
            "GAP": -1,
            "DHAP": 1,
        },
    )
    m.add_reaction(
        name="v_Aldolase_FBP",
        fn=rapid_equilibrium_2s_1p,
        args=["GAP", "DHAP", "FBP", "kre_v_Aldolase_FBP", "keq_v_Aldolase_FBP"],
        stoichiometry={
            "GAP": -1,
            "DHAP": -1,
            "FBP": 1,
        },
    )
    m.add_reaction(
        name="v_Aldolase_SBP",
        fn=rapid_equilibrium_2s_1p,
        args=["DHAP", "E4P", "SBP", "kre_v_Aldolase_SBP", "keq_v_Aldolase_SBP"],
        stoichiometry={
            "DHAP": -1,
            "E4P": -1,
            "SBP": 1,
        },
    )
    m.add_reaction(
        name="v_FBPase",
        fn=michaelis_menten_1s_2i,
        args=[
            "FBP",
            "F6P",
            "Pi_st",
            "vmax_v_FBPase",
            "km_v_FBPase_s",
            "ki_v_FBPase_F6P",
            "ki_v_FBPase_Pi_st",
        ],
        stoichiometry={
            "FBP": -1,
            "F6P": 1,
        },
    )
    m.add_reaction(
        name="v_TKase_E4P",
        fn=rapid_equilibrium_2s_2p,
        args=["GAP", "F6P", "E4P", "X5P", "kre_v_TKase_E4P", "keq_v_TKase_E4P"],
        stoichiometry={
            "GAP": -1,
            "F6P": -1,
            "E4P": 1,
            "X5P": 1,
        },
    )
    m.add_reaction(
        name="v_TKase_R5P",
        fn=rapid_equilibrium_2s_2p,
        args=["GAP", "S7P", "R5P", "X5P", "kre_v_TKase_R5P", "keq_v_TKase_R5P"],
        stoichiometry={
            "GAP": -1,
            "S7P": -1,
            "R5P": 1,
            "X5P": 1,
        },
    )
    m.add_reaction(
        name="v_SBPase",
        fn=michaelis_menten_1s_1i,
        args=["SBP", "Pi_st", "vmax_v_SBPase", "km_v_SBPase_s", "ki_v_SBPase_Pi_st"],
        stoichiometry={
            "SBP": -1,
            "S7P": 1,
        },
    )
    m.add_reaction(
        name="v_Rpiase",
        fn=rapid_equilibrium_1s_1p,
        args=["R5P", "RU5P", "kre_v_Rpiase", "keq_v_Rpiase"],
        stoichiometry={
            "R5P": -1,
            "RU5P": 1,
        },
    )
    m.add_reaction(
        name="v_RPEase",
        fn=rapid_equilibrium_1s_1p,
        args=["X5P", "RU5P", "kre_v_RPEase", "keq_v_RPEase"],
        stoichiometry={
            "X5P": -1,
            "RU5P": 1,
        },
    )
    m.add_reaction(
        name="v_PRKase",
        fn=_rate_prk,
        args=[
            "RU5P",
            "ATP_st",
            "Pi_st",
            "PGA",
            "RUBP",
            "ADP_st",
            "vmax_v_PRKase",
            "km_v_PRKase_RU5P",
            "km_v_PRKase_ATP_st",
            "ki_v_PRKase_PGA",
            "ki_v_PRKase_RUBP",
            "ki_v_PRKase_Pi_st",
            "ki_v_PRKase_4",
            "ki_v_PRKase_5",
        ],
        stoichiometry={
            "RU5P": -1.0,
            "ATP_st": -1.0,
            "RUBP": 1.0,
        },
    )
    m.add_reaction(
        name="v_PGIase",
        fn=rapid_equilibrium_1s_1p,
        args=["F6P", "G6P", "kre_v_PGIase", "keq_v_PGIase"],
        stoichiometry={
            "F6P": -1,
            "G6P": 1,
        },
    )
    m.add_reaction(
        name="v_PGMase",
        fn=rapid_equilibrium_1s_1p,
        args=["G6P", "G1P", "kre_v_PGMase", "keq_v_PGMase"],
        stoichiometry={
            "G6P": -1,
            "G1P": 1,
        },
    )
    m.add_reaction(
        name="v_pga_ex",
        fn=_rate_out,
        args=["PGA", "IF_3P", "vmax_v_pga_ex", "km_v_pga_ex"],
        stoichiometry={
            "PGA": -1,
        },
    )
    m.add_reaction(
        name="v_gap_ex",
        fn=_rate_out_2,
        args=["GAP", "IF_3P", "vmax_v_pga_ex", "km_v_gap_ex"],
        stoichiometry={
            "GAP": -1,
        },
    )
    m.add_reaction(
        name="v_dhap_ex",
        fn=_rate_out_2,
        args=["DHAP", "IF_3P", "vmax_v_pga_ex", "km_v_dhap_ex"],
        stoichiometry={
            "DHAP": -1,
        },
    )
    m.add_reaction(
        name="v_starch",
        fn=_rate_starch,
        args=[
            "G1P",
            "ATP_st",
            "ADP_st",
            "Pi_st",
            "PGA",
            "F6P",
            "FBP",
            "vmax_v_starch",
            "km_v_starch_G1P",
            "km_v_starch_ATP_st",
            "ki_v_starch",
            "ki_v_starch_PGA",
            "ki_v_starch_F6P",
            "ki_v_starch_FBP",
        ],
        stoichiometry={
            "G1P": -1.0,
            "ATP_st": -1.0,
        },
    )
    m.add_reaction(
        name="v_3ASC",
        fn=_rate_mda_reductase,
        args=["MDA", "kf_v_3ASC"],
        stoichiometry={
            "MDA": -2,
            "DHA": 1,
        },
    )
    m.add_reaction(
        name="v_MDAreduct",
        fn=_rate_mda_reductase_2,
        args=[
            "NADPH_st",
            "MDA",
            "vmax_v_MDAreduct",
            "km_v_MDAreduct_NADPH_st",
            "km_v_MDAreduct_MDA",
        ],
        stoichiometry={
            "NADPH_st": -1,
            "MDA": -2,
        },
    )
    m.add_reaction(
        name="v_APXase",
        fn=_rate_ascorbate_peroxidase,
        args=[
            "ASC",
            "H2O2",
            "kf1",
            "kr1",
            "kf2",
            "kr2",
            "kf3",
            "kf4",
            "kr4",
            "kf5",
            "XT",
        ],
        stoichiometry={
            "H2O2": -1,
            "MDA": 2,
        },
    )
    m.add_reaction(
        name="v_GR",
        fn=_rate_glutathion_reductase,
        args=["NADPH_st", "GSSG", "vmax_v_GR", "km_v_GR_NADPH_st", "km_v_GR_GSSG"],
        stoichiometry={
            "NADPH_st": -1,
            "GSSG": -1,
        },
    )
    m.add_reaction(
        name="v_DHAR",
        fn=_rate_dhar,
        args=["DHA", "GSH", "vmax_v_DHAR", "km_v_DHAR_DHA", "km_v_DHAR_GSH", "K"],
        stoichiometry={
            "DHA": -1,
            "GSSG": 1,
        },
    )
    m.add_reaction(
        name="v_ATPcons",
        fn=mass_action_1s,
        args=["ATP_st", "kf_v_ATPcons"],
        stoichiometry={
            "ATP_st": -1,
        },
    )
    m.add_reaction(
        name="v_NADPHcons",
        fn=mass_action_1s,
        args=["NADPH_st", "kf_v_NADPHcons"],
        stoichiometry={
            "NADPH_st": -1,
        },
    )

    return m
