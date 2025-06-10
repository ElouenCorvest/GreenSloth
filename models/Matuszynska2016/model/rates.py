from mxlpy import Derived, Model

from . import basic_funcs as bf


def v_PSII(B1, k_P):
    """Reduction of PQ due to ps2"""
    v = k_P * 0.5 * B1
    return v


def v_PQ(PQH_2, pfd, k_Cytb6f, k_PTOX, O2_ex, PQ_tot, K_cytb6f):
    """Oxidation of the PQ pool through cytochrome and PTOX"""
    kPFD = k_Cytb6f * pfd
    k_PTOX = k_PTOX * O2_ex
    a1 = kPFD * K_cytb6f / (K_cytb6f + 1)
    a2 = kPFD / (K_cytb6f + 1)
    v = (a1 + k_PTOX) * PQH_2 - a2 * (PQ_tot - PQH_2)
    return v


def v_ATPsynth(ATP_st, ATPase_ac, k_ATPsynth, K_ATPsynth, AP_tot):
    """Production of ATP by ATPsynthase"""
    v = ATPase_ac * k_ATPsynth * (AP_tot - ATP_st - ATP_st / K_ATPsynth)
    return v


def v_ATPact(ATPase_ac, pfd, k_ActATPase, k_DeactATPase):
    """Activation of ATPsynthase by light"""
    switch = pfd > 0
    v = (
        k_ActATPase * switch * (1 - ATPase_ac)
        - k_DeactATPase * (1 - switch) * ATPase_ac
    )
    return v


def v_Leak(H_lu, k_leak, H_st):
    """Transmembrane proton leak"""
    v = k_leak * (H_lu - H_st)
    return v


def v_ATPcons(ATP_st, k_ATPconsum):
    """ATP consuming reaction"""
    v = k_ATPconsum * ATP_st
    return v


def v_Xcyc(Vx, H_lu, nhx, K_pHSat_inv, k_DV, k_EZ, X_tot):
    """Xanthophyll cycle"""
    a = H_lu**nhx / (H_lu**nhx + K_pHSat_inv**nhx)
    v = k_DV * a * Vx - k_EZ * (X_tot - Vx)
    return v


def v_PsbSP(psbS, H_lu, nhl, K_pHSatLHC_inv, k_prot, k_deprot, PsbS_tot):
    """Protonation of PsbS protein"""
    a = H_lu**nhl / (H_lu**nhl + K_pHSatLHC_inv**nhl)
    v = k_prot * a * psbS - k_deprot * (PsbS_tot - psbS)
    return v


def include_rates(m: Model):
    m.add_reaction(
        name="v_PSII",
        fn=v_PSII,
        args=["B1", "k_P"],
        stoichiometry={
            "PQH_2": 1,
            "H_lu": Derived(fn=bf.two_divided_value, args=["b_H"]),
        },
    )

    m.add_reaction(
        name="v_PQ",
        fn=v_PQ,
        args=["PQH_2", "pfd", "k_Cytb6f", "k_PTOX", "O2_ex", "PQ_tot", "K_cytb6f"],
        stoichiometry={
            "PQH_2": -1,
            "H_lu": Derived(fn=bf.four_divided_value, args=["b_H"]),
        },
    )

    m.add_reaction(
        name="v_ATPsynth",
        fn=v_ATPsynth,
        args=["ATP_st", "ATPase_ac", "k_ATPsynth", "K_ATPsynth", "AP_tot"],
        stoichiometry={
            "ATP_st": 1,
            "H_lu": Derived(fn=bf.neg_fourteenthirds_divided_value, args=["b_H"]),
        },
    )

    m.add_reaction(
        name="v_ATPact",
        fn=v_ATPact,
        args=["ATPase_ac", "pfd", "k_ActATPase", "k_DeactATPase"],
        stoichiometry={"ATPase_ac": 1},
    )

    m.add_reaction(
        name="v_Leak",
        fn=v_Leak,
        args=["H_lu", "k_leak", "H_st"],
        stoichiometry={"H_lu": Derived(fn=bf.neg_divided_value, args=["b_H"])},
    )

    m.add_reaction(
        name="v_ATPcons",
        fn=v_ATPcons,
        args=["ATP_st", "k_ATPconsum"],
        stoichiometry={"ATP_st": -1},
    )

    m.add_reaction(
        name="v_Xcyc",
        fn=v_Xcyc,
        args=["Vx", "H_lu", "nhx", "K_pHSat_inv", "k_DV", "k_EZ", "X_tot"],
        stoichiometry={"Vx": -1},
    )

    m.add_reaction(
        name="v_PsbSP",
        fn=v_PsbSP,
        args=[
            "psbS",
            "H_lu",
            "nhl",
            "K_pHSatLHC_inv",
            "k_prot",
            "k_deprot",
            "PsbS_tot",
        ],
        stoichiometry={"psbS": -1},
    )

    return m
