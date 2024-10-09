def ADP(ATP, AP_total):
    return [AP_total - ATP]


def P_i(
    PGA,
    BPGA,
    GAP,
    DHAP,
    FBP,
    F6P,
    G6P,
    G1P,
    SBP,
    S7P,
    E4P,
    X5P,
    R5P,
    RUBP,
    RU5P,
    ATP,
    phosphate_total,
):
    return [
        phosphate_total
        - (
            PGA
            + 2 * BPGA
            + GAP
            + DHAP
            + 2 * FBP
            + F6P
            + G6P
            + G1P
            + 2 * SBP
            + S7P
            + E4P
            + X5P
            + R5P
            + 2 * RUBP
            + RU5P
            + ATP
        )
    ]


def N(
    Phosphate_pool,
    PGA,
    GAP,
    DHAP,
    Kpxt,
    Pext,
    Kpi,
    Kpga,
    Kgap,
    Kdhap,
):
    return [
        (
            1
            + (1 + (Kpxt / Pext))
            * ((Phosphate_pool / Kpi) + (PGA / Kpga) + (GAP / Kgap) + (DHAP / Kdhap))
        )
    ]
