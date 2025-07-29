from mxlpy import Model

from .basic_funcs import (
    mass_action_1s,
    moiety_1,
)


def _pi_cbb(
    phosphate_total: float,
    pga: float,
    bpga: float,
    gap: float,
    dhap: float,
    fbp: float,
    f6p: float,
    g6p: float,
    g1p: float,
    sbp: float,
    s7p: float,
    e4p: float,
    x5p: float,
    r5p: float,
    rubp: float,
    ru5p: float,
    atp: float,
) -> float:
    return phosphate_total - (
        pga
        + 2 * bpga
        + gap
        + dhap
        + 2 * fbp
        + f6p
        + g6p
        + g1p
        + 2 * sbp
        + s7p
        + e4p
        + x5p
        + r5p
        + 2 * rubp
        + ru5p
        + atp
    )


def _rate_translocator(
    pi: float,
    pga: float,
    gap: float,
    dhap: float,
    k_pxt: float,
    p_ext: float,
    k_pi: float,
    k_pga: float,
    k_gap: float,
    k_dhap: float,
) -> float:
    return 1 + (1 + k_pxt / p_ext) * (
        pi / k_pi + pga / k_pga + gap / k_gap + dhap / k_dhap
    )


def include_derived_quantities(m: Model):
    m.add_derived(
        name="ADP_st",
        fn=moiety_1,
        args=["ATP_st", "AP_tot"],
    )

    m.add_derived(
        name="NADP_st",
        fn=moiety_1,
        args=["NADPH_st", "NADP_tot"],
    )

    m.add_derived(
        name="Pi_st",
        fn=_pi_cbb,
        args=[
            "Pi_tot",
            "PGA",
            "BPGA",
            "GAP",
            "DHAP",
            "FBP",
            "F6P",
            "G6P",
            "G1P",
            "SBP",
            "S7P",
            "E4P",
            "X5P",
            "R5P",
            "RUBP",
            "RU5P",
            "ATP_st",
        ],
    )

    m.add_derived(
        name="vmax_v_RuBisCO_c",
        fn=mass_action_1s,
        args=["kcat_v_RuBisCO_c", "Enz0_v_RuBisCO_c"],
    )

    m.add_derived(
        name="vmax_v_FBPase",
        fn=mass_action_1s,
        args=["kcat_v_FBPase", "Enz0_v_FBPase"],
    )

    m.add_derived(
        name="vmax_v_SBPase",
        fn=mass_action_1s,
        args=["kcat_v_SBPase", "Enz0_v_SBPase"],
    )

    m.add_derived(
        name="vmax_v_PRKase",
        fn=mass_action_1s,
        args=["kcat_v_PRKase", "Enz0_v_PRKase"],
    )

    m.add_derived(
        name="vmax_v_pga_ex",
        fn=mass_action_1s,
        args=["kcat_N_translocator", "Enz0_N_translocator"],
    )

    m.add_derived(
        name="N_translocator",
        fn=_rate_translocator,
        args=[
            "Pi_st",
            "PGA",
            "GAP",
            "DHAP",
            "km_N_translocator_Pi_ext",
            "Pi_ext",
            "km_N_translocator_Pi_st",
            "km_v_pga_ex",
            "km_v_gap_ex",
            "km_v_dhap_ex",
        ],
    )

    m.add_derived(
        name="vmax_v_starch",
        fn=mass_action_1s,
        args=["kcat_v_starch", "Enz0_v_starch"],
    )

    m.add_derived(
        name="vmax_v_ATPsynth",
        fn=mass_action_1s,
        args=["kcat_v_ATPsynth", "Enz0_v_ATPsynth"],
    )

    return m
