from __future__ import annotations

#from modelbase.ode import DerivedStoichiometry, Model

from modelbase2 import Model, Derived

from . import basic_funcs as bf

def v3(
    A1: float, A3: float, PQ_ox: float, PQ_red: float, k3p: float, k3m: float
) -> float:  # PQ_ox seems to be reduce and PQ_red oxidized ?
    return k3p * A3 * PQ_red - k3m * A1 * PQ_ox

def v5(
    ATP_st: float, AP_tot: float, k5: float, Keq: float) -> float:
    return k5 * (AP_tot - ATP_st * (1 + 1 / Keq))

def v6(N0: float, H_lu: float, k6: float, n: float, KQ: float) -> float:
    return k6 * N0 * ((H_lu**n) / (H_lu**n + KQ**n))  # type: ignore

def v8(H_lu: float, H_st: float, k8: float) -> float:
    return k8 * (H_lu - H_st)

def include_reactions(m: Model) -> Model:
    m.add_reaction(
        "v1",
        fn=bf.proportional,
        stoichiometry={"A1": -1, "A2": 1},
        args=["N0", "A1", "k1"],
    )

    m.add_reaction(
        "v2",
        fn=bf.proportional,
        stoichiometry={"A2": -1, "H_lu": Derived(bf.two_times_value, args=["bH"])},
        args=["A2", "k2"],
    )

    m.add_reaction(
        "v3",
        fn=v3,
        stoichiometry={"A1": 1, "PQ_ox": 1},
        args=["A1", "A3", "PQ_ox", "PQ_red", "k3p", "k3m"],
    )

    m.add_reaction(
        "v4",
        fn=bf.proportional,
        stoichiometry={"PQ_ox": -1, "H_lu": Derived(bf.value, args=["bH"])},
        args=["PQ_ox", "k4"],
    )

    m.add_reaction(
        "v5",
        fn=v5,
        stoichiometry={"ATP_st": 1, "H_lu": Derived(bf.times_neg_fourteen_thirds, args=["bH"])},
        args=["ATP_st", "AP_tot", "k5", "Keq"],
    )

    m.add_reaction(
        "v6",
        fn=v6,
        stoichiometry={"N": 1},
        args=["N0", "H_lu", "k6", "n", "KQ"],
    )

    m.add_reaction(
        "v7",
        fn=bf.proportional,
        stoichiometry={"N": -1},
        args=["N", "k7"],
    )

    m.add_reaction(
        "v8",
        fn=v8,
        stoichiometry={"H_lu": Derived(bf.neg_value, args=["bH"])},
        args=["H_lu", "H_st", "k8"],
    )

    m.add_reaction(
        "v9",
        fn=bf.proportional,
        stoichiometry={"ATP_st": -1},
        args=["ATP_st", "k9"],
    )
    return m