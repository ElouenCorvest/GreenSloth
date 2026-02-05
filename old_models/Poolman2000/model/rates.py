from mxlpy import Model

from .basic_funcs import (
    rapid_equilibrium_2s_2p,
    rapid_equilibrium_3s_3p,
    rapid_equilibrium_1s_1p,
    michaelis_menten_1s_1i,
    rapid_equilibrium_2s_1p,
    michaelis_menten_1s_2i,
)


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


def _rate_atp_synthase_2000(
    adp: float,
    pi: float,
    v16: float,
    km161: float,
    km162: float,
) -> float:
    return v16 * adp * pi / ((adp + km161) * (pi + km162))


def include_rates(m: Model):
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
            "H",
            "GAP",
            "NADP_st",
            "Pi_st",
            "kre_v_BPGAdehynase",
            "keq_v_BPGAdehynase",
        ],
        stoichiometry={
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
        args=["PGA", "N_translocator", "vmax_v_pga_ex", "km_v_pga_ex"],
        stoichiometry={
            "PGA": -1,
        },
    )
    m.add_reaction(
        name="v_gap_ex",
        fn=_rate_out_2,
        args=["GAP", "N_translocator", "vmax_v_pga_ex", "km_v_gap_ex"],
        stoichiometry={
            "GAP": -1,
        },
    )
    m.add_reaction(
        name="v_dhap_ex",
        fn=_rate_out_2,
        args=["DHAP", "N_translocator", "vmax_v_pga_ex", "km_v_dhap_ex"],
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
        name="v_ATPsynth",
        fn=_rate_atp_synthase_2000,
        args=[
            "ADP_st",
            "Pi_st",
            "vmax_v_ATPsynth",
            "km_v_ATPsynth_ADP_st",
            "km_v_ATPsynth_Pi_st",
        ],
        stoichiometry={
            "ATP_st": 1.0,
        },
    )

    return m
