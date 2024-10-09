def rapid_equilibrium_1_1(s1, p1, kRE, q):
    return kRE * (s1 - p1 / q)


def rapid_equilibrium_2_1(s1, s2, p1, kRE, q):
    return kRE * (s1 * s2 - p1 / q)


def rapid_equilibrium_2_2(s1, s2, p1, p2, kRE, q):
    return kRE * (s1 * s2 - (p1 * p2) / q)


def v_out(s1, N_total, VMax_efflux, K_efflux):
    return (VMax_efflux * s1) / (N_total * K_efflux)


def v1(
    RUBP,
    PGA,
    FBP,
    SBP,
    P,
    V1,
    Km1,
    Ki11,
    Ki12,
    Ki13,
    Ki14,
    Ki15,
    NADPH_pool,
):
    return (V1 * RUBP) / (
        RUBP
        + Km1
        * (
            1
            + (PGA / Ki11)
            + (FBP / Ki12)
            + (SBP / Ki13)
            + (P / Ki14)
            + (NADPH_pool / Ki15)
        )
    )


def v3(
    BPGA,
    GAP,
    phosphate_pool,
    proton_pool_stroma,
    NADPH_pool,
    NADP_pool,
    kRE,
    q3,
):
    return kRE * (
        (NADPH_pool * BPGA * proton_pool_stroma)
        - (1 / q3) * (GAP * NADP_pool * phosphate_pool)
    )


def v6(FBP, F6P, P, V6, Km6, Ki61, Ki62):
    return (V6 * FBP) / (FBP + Km6 * (1 + (F6P / Ki61) + (P / Ki62)))


def v9(SBP, P, V9, Km9, Ki9):
    return (V9 * SBP) / (SBP + Km9 * (1 + (P / Ki9)))


def v13(
    RU5P,
    ATP,
    Phosphate_pool,
    PGA,
    RUBP,
    ADP,
    V13,
    Km131,
    Km132,
    Ki131,
    Ki132,
    Ki133,
    Ki134,
    Ki135,
):
    return (V13 * RU5P * ATP) / (
        (RU5P + Km131 * (1 + (PGA / Ki131) + (RUBP / Ki132) + (Phosphate_pool / Ki133)))
        * (ATP * (1 + (ADP / Ki134)) + Km132 * (1 + (ADP / Ki135)))
    )


def v16(ADP, Phosphate_i, V16, Km161, Km162):
    return (V16 * ADP * Phosphate_i) / ((ADP + Km161) * (Phosphate_i + Km162))


def vStarchProduction(
    G1P,
    ATP,
    ADP,
    Phosphate_pool,
    PGA,
    F6P,
    FBP,
    Vst,
    Kmst1,
    Kmst2,
    Kist,
    Kast1,
    Kast2,
    Kast3,
):
    return (Vst * G1P * ATP) / (
        (G1P + Kmst1)
        * (
            (1 + (ADP / Kist)) * (ATP + Kmst2)
            + ((Kmst2 * Phosphate_pool) / (Kast1 * PGA + Kast2 * F6P + Kast3 * FBP))
        )
    )
