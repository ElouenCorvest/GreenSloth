from mxlpy import Model
from mxlpy.surrogates import qss
import numpy as np
import math
from typing import cast, Iterable

from .basic_funcs import (
    moiety_2,
    mass_action_1s,
    mul,
    moiety_1,
    div,
)


def _dg_ph(r: float, t: float) -> float:
    return math.log(10) * r * t


def _ph_lumen(protons: float) -> float:
    return -math.log10(protons * 0.00025)


def _quencher(
    Psbs: float,
    Vx: float,
    Psbsp: float,
    Zx: float,
    y0: float,
    y1: float,
    y2: float,
    y3: float,
    kZSat: float,
) -> float:
    """co-operative 4-state quenching mechanism
    gamma0: slow quenching of (Vx - protonation)
    gamma1: fast quenching (Vx + protonation)
    gamma2: fastest possible quenching (Zx + protonation)
    gamma3: slow quenching of Zx present (Zx - protonation)
    """
    ZAnt = Zx / (Zx + kZSat)
    return y0 * Vx * Psbs + y1 * Vx * Psbsp + y2 * ZAnt * Psbsp + y3 * ZAnt * Psbs


def _keq_pq_red(
    E0_QA: float,
    F: float,
    E0_PQ: float,
    pHstroma: float,
    dG_pH: float,
    RT: float,
) -> float:
    dg1 = -E0_QA * F
    dg2 = -2 * E0_PQ * F
    dg = -2 * dg1 + dg2 + 2 * pHstroma * dG_pH

    return math.exp(-dg / RT)


def _ps2_crosssection(
    lhc: float,
    static_ant_ii: float,
    static_ant_i: float,
) -> float:
    return static_ant_ii + (1 - static_ant_ii - static_ant_i) * lhc


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


def _glutathion_moiety(
    gssg: float,
    gs_total: float,
) -> float:
    return gs_total - 2 * gssg


def _keq_atp(
    pH: float,
    DeltaG0_ATP: float,
    dG_pH: float,
    HPR: float,
    pHstroma: float,
    Pi_mol: float,
    RT: float,
) -> float:
    delta_g = DeltaG0_ATP - dG_pH * HPR * (pHstroma - pH)
    return Pi_mol * math.exp(-delta_g / RT)


def _keq_cytb6f(
    pH: float,
    F: float,
    E0_PQ: float,
    E0_PC: float,
    pHstroma: float,
    RT: float,
    dG_pH: float,
) -> float:
    DG1 = -2 * F * E0_PQ
    DG2 = -F * E0_PC
    DG = -(DG1 + 2 * dG_pH * pH) + 2 * DG2 + 2 * dG_pH * (pHstroma - pH)
    Keq = np.exp(-DG / RT)
    return cast(float, Keq)


def _keq_fnr(
    E0_Fd: float,
    F: float,
    E0_NADP: float,
    pHstroma: float,
    dG_pH: float,
    RT: float,
) -> float:
    dg1 = -E0_Fd * F
    dg2 = -2 * E0_NADP * F
    dg = -2 * dg1 + dg2 + dG_pH * pHstroma
    return math.exp(-dg / RT)


def _keq_pcp700(
    e0_pc: float,
    f: float,
    eo_p700: float,
    rt: float,
) -> float:
    dg1 = -e0_pc * f
    dg2 = -eo_p700 * f
    dg = -dg1 + dg2
    return math.exp(-dg / rt)


def _keq_faf_d(
    e0_fa: float,
    f: float,
    e0_fd: float,
    rt: float,
) -> float:
    dg1 = -e0_fa * f
    dg2 = -e0_fd * f
    dg = -dg1 + dg2
    return math.exp(-dg / rt)


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


def _ps2states(
    pq_ox: float,
    pq_red: float,
    ps2cs: float,
    q: float,
    psii_tot: float,
    k2: float,
    k_f: float,
    _kh: float,
    keq_pq_red: float,
    k_pq_red: float,
    pfd: float,
    k_h0: float,
) -> Iterable[float]:
    absorbed = ps2cs * pfd
    kH = k_h0 + _kh * q
    k3p = k_pq_red * pq_ox
    k3m = k_pq_red * pq_red / keq_pq_red

    state_matrix = np.array(
        [
            [-absorbed - k3m, kH + k_f, k3p, 0],
            [absorbed, -(kH + k_f + k2), 0, 0],
            [0, 0, absorbed, -(kH + k_f)],
            [1, 1, 1, 1],
        ],
        dtype=float,
    )
    a = np.array([0, 0, 0, psii_tot])

    return np.linalg.solve(state_matrix, a)


def _ps1states_2021(
    pc_ox: float,
    pc_red: float,
    fd_ox: float,
    fd_red: float,
    ps2cs: float,
    ps1_tot: float,
    k_fd_red: float,
    keq_f: float,
    keq_c: float,
    k_pc_ox: float,
    pfd: float,
    k0: float,
    o2: float,
) -> tuple[float, float, float]:
    """QSSA calculates open state of PSI
    depends on reduction states of plastocyanin and ferredoxin
    C = [PC], F = [Fd] (ox. forms)
    """
    kLI = (1 - ps2cs) * pfd

    y0 = (
        keq_c
        * keq_f
        * pc_red
        * ps1_tot
        * k_pc_ox
        * (fd_ox * k_fd_red + o2 * k0)
        / (
            fd_ox * keq_c * keq_f * pc_red * k_fd_red * k_pc_ox
            + fd_ox * keq_f * k_fd_red * (keq_c * kLI + pc_ox * k_pc_ox)
            + fd_red * k_fd_red * (keq_c * kLI + pc_ox * k_pc_ox)
            + keq_c * keq_f * o2 * pc_red * k0 * k_pc_ox
            + keq_c * keq_f * pc_red * kLI * k_pc_ox
            + keq_f * o2 * k0 * (keq_c * kLI + pc_ox * k_pc_ox)
        )
    )

    y1 = (
        ps1_tot
        * (
            fd_red * k_fd_red * (keq_c * kLI + pc_ox * k_pc_ox)
            + keq_c * keq_f * pc_red * kLI * k_pc_ox
        )
        / (
            fd_ox * keq_c * keq_f * pc_red * k_fd_red * k_pc_ox
            + fd_ox * keq_f * k_fd_red * (keq_c * kLI + pc_ox * k_pc_ox)
            + fd_red * k_fd_red * (keq_c * kLI + pc_ox * k_pc_ox)
            + keq_c * keq_f * o2 * pc_red * k0 * k_pc_ox
            + keq_c * keq_f * pc_red * kLI * k_pc_ox
            + keq_f * o2 * k0 * (keq_c * kLI + pc_ox * k_pc_ox)
        )
    )
    y2 = ps1_tot - y0 - y1

    return y0, y1, y2


def _rate_fluorescence(
    Q: float,
    B0: float,
    B2: float,
    ps2cs: float,
    k2: float,
    kF: float,
    kH: float,
) -> float:
    return ps2cs * kF * B0 / (kF + k2 + kH * Q) + ps2cs * kF * B2 / (kF + kH * Q)


def include_derived_quantities(m: Model):
    m.add_derived(
        name="RT",
        fn=mass_action_1s,
        args=["R", "T"],
    )

    m.add_derived(
        name="dG_pH",
        fn=_dg_ph,
        args=["R", "T"],
    )

    m.add_derived(
        name="pH_lumen",
        fn=_ph_lumen,
        args=["H_lumen"],
    )

    m.add_derived(
        name="Zx",
        fn=moiety_1,
        args=["Vx", "Carotenoids_tot"],
    )

    m.add_derived(
        name="Fd_red",
        fn=moiety_1,
        args=["Fd_ox", "Fd_tot"],
    )

    m.add_derived(
        name="PC_red",
        fn=moiety_1,
        args=["PC_ox", "PC_tot"],
    )

    m.add_derived(
        name="PsbSP",
        fn=moiety_1,
        args=["psbS", "PSBS_tot"],
    )

    m.add_derived(
        name="LHCp",
        fn=moiety_1,
        args=["LHC", "LHC_tot"],
    )

    m.add_derived(
        name="Q",
        fn=_quencher,
        args=[
            "psbS",
            "Vx",
            "PsbSP",
            "Zx",
            "gamma0",
            "gamma1",
            "gamma2",
            "gamma3",
            "kZSat",
        ],
    )

    m.add_derived(
        name="keq_PQH_2",
        fn=_keq_pq_red,
        args=["E0_QA", "F", "E0_PQ", "pH_stroma", "dG_pH", "RT"],
    )

    m.add_derived(
        name="PQH_2",
        fn=moiety_1,
        args=["PQ", "PQ_tot"],
    )

    m.add_derived(
        name="psIIcross",
        fn=_ps2_crosssection,
        args=["LHC", "staticAntII", "staticAntI"],
    )

    m.add_derived(
        name="TRX_red",
        fn=moiety_1,
        args=["TRX_ox", "Thioredoxin_tot"],
    )

    m.add_derived(
        name="E_CBB_active",
        fn=moiety_1,
        args=["E_CBB_inactive", "E_total"],
    )

    m.add_derived(
        name="NADP_st",
        fn=moiety_1,
        args=["NADPH_st", "NADP_tot"],
    )

    m.add_derived(
        name="ADP_st",
        fn=moiety_1,
        args=["ATP_st", "AP_tot"],
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
        name="ASC",
        fn=moiety_2,
        args=["MDA", "DHA", "ASC_tot"],
    )

    m.add_derived(
        name="GSH",
        fn=_glutathion_moiety,
        args=["GSSG", "Glutathion_tot"],
    )

    m.add_derived(
        name="keq_v_ATPsynth",
        fn=_keq_atp,
        args=["pH_lumen", "DeltaG0_ATP", "dG_pH", "HPR", "pH_stroma", "Pi_mol", "RT"],
    )

    m.add_derived(
        name="keq_v_b6f",
        fn=_keq_cytb6f,
        args=["pH_lumen", "F", "E0_PQ", "E0_PC", "pH_stroma", "RT", "dG_pH"],
    )

    m.add_derived(
        name="keq_v_FNR",
        fn=_keq_fnr,
        args=["E0_Fd", "F", "E0_NADP", "pH_stroma", "dG_pH", "RT"],
    )

    m.add_derived(
        name="vmax_v_FNR",
        fn=mass_action_1s,
        args=["kcat_v_FNR", "Enz0_v_FNR"],
    )

    m.add_derived(
        name="keq_PCP700",
        fn=_keq_pcp700,
        args=["E0_PC", "F", "E0_P700", "RT"],
    )

    m.add_derived(
        name="keq_v_Fdred",
        fn=_keq_faf_d,
        args=["E0_FA", "F", "E0_Fd", "RT"],
    )

    m.add_derived(
        name="vmax_v_Fdred",
        fn=mass_action_1s,
        args=["kcat_v_Fdred", "Enz0_v_Fdred"],
    )

    m.add_derived(
        name="Enz0_rubisco_active",
        fn=mul,
        args=["Enz0_rubisco", "E_CBB_active"],
    )

    m.add_derived(
        name="vmax_v_RuBisCO_c",
        fn=mass_action_1s,
        args=["kcat_v_RuBisCO_c", "Enz0_rubisco_active"],
    )

    m.add_derived(
        name="Enz0_v_FBPase_active",
        fn=mul,
        args=["Enz0_v_FBPase", "E_CBB_active"],
    )

    m.add_derived(
        name="vmax_v_FBPase",
        fn=mass_action_1s,
        args=["kcat_v_FBPase", "Enz0_v_FBPase_active"],
    )

    m.add_derived(
        name="Enz0_v_SBPase_active",
        fn=mul,
        args=["Enz0_v_SBPase", "E_CBB_active"],
    )

    m.add_derived(
        name="vmax_v_SBPase",
        fn=mass_action_1s,
        args=["kcat_v_SBPase", "Enz0_v_SBPase_active"],
    )

    m.add_derived(
        name="Enz0_v_PRKase_active",
        fn=mul,
        args=["Enz0_v_PRKase", "E_CBB_active"],
    )

    m.add_derived(
        name="vmax_v_PRKase",
        fn=mass_action_1s,
        args=["kcat_v_PRKase", "Enz0_v_PRKase_active"],
    )

    m.add_derived(
        name="vmax_v_pga_ex",
        fn=mass_action_1s,
        args=["kcat_IF_3P", "Enz0_IF_3P"],
    )

    m.add_derived(
        name="IF_3P",
        fn=_rate_translocator,
        args=[
            "Pi_st",
            "PGA",
            "GAP",
            "DHAP",
            "km_IF_3P_Pi_ext",
            "Pi_ext",
            "km_IF_3P_Pi_st",
            "km_v_pga_ex",
            "km_v_gap_ex",
            "km_v_dhap_ex",
        ],
    )

    m.add_derived(
        name="Enz0_v_starch_active",
        fn=mul,
        args=["Enz0_v_starch", "E_CBB_active"],
    )

    m.add_derived(
        name="vmax_v_starch",
        fn=mass_action_1s,
        args=["kcat_v_starch", "Enz0_v_starch_active"],
    )

    m.add_derived(
        name="vmax_v_MDAreduct",
        fn=mass_action_1s,
        args=["kcat_v_MDAreduct", "Enz0_v_MDAreduct"],
    )

    m.add_derived(
        name="vmax_v_GR",
        fn=mass_action_1s,
        args=["kcat_v_GR", "Enz0_v_GR"],
    )

    m.add_derived(
        name="vmax_v_DHAR",
        fn=mass_action_1s,
        args=["kcat_v_DHAR", "Enz0_v_DHAR"],
    )

    m.add_surrogate(
        name="ps2states",
        surrogate=qss.Surrogate(
            model=_ps2states,
            args=[
                "PQ",
                "PQH_2",
                "psIIcross",
                "Q",
                "PSII_total",
                "k2",
                "kF",
                "kH",
                "keq_PQH_2",
                "kPQred",
                "PPFD",
                "kH0",
            ],
            outputs=["B0", "B1", "B2", "B3"],
        ),
    )

    m.add_surrogate(
        name="ps1states",
        surrogate=qss.Surrogate(
            model=_ps1states_2021,
            args=[
                "PC_ox",
                "PC_red",
                "Fd_ox",
                "Fd_red",
                "psIIcross",
                "PSI_total",
                "kFdred",
                "keq_v_Fdred",
                "keq_PCP700",
                "kPCox",
                "PPFD",
                "kMehler",
                "O2_lumen",
            ],
            outputs=["Y0", "Y1", "Y2"],
        ),
    )

    m.add_readout(name="PQ_ox/tot", fn=div, args=["PQH_2", "PQ_tot"])

    m.add_readout(name="Fd_ox/tot", fn=div, args=["Fd_red", "Fd_tot"])

    m.add_readout(name="PC_ox/tot", fn=div, args=["PC_red", "PC_tot"])

    m.add_readout(name="NADPH/tot", fn=div, args=["NADPH_st", "NADP_tot"])

    m.add_readout(name="ATP/tot", fn=div, args=["ATP_st", "AP_tot"])

    m.add_readout(
        name="Fluo",
        fn=_rate_fluorescence,
        args=["Q", "B0", "B2", "psIIcross", "k2", "kF", "kH"],
    )

    return m
