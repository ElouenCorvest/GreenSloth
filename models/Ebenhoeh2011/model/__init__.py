from __future__ import annotations

from . import rates as r
from .rates import pH
from modelbase.ode import DerivedStoichiometry, Model

__all__ = [
    "get_model",
    "pH",
]


def _add_derived_parameters(m: Model) -> Model:
    m.add_derived_parameter(
        parameter_name="RT",
        function=r.proportional,
        parameters=["R", "Temp"],
    )
    return m


def _add_reactions(m: Model) -> Model:
    m.add_reaction_from_args(
        rate_name="v1",
        function=r.v1,
        stoichiometry={"A1": -1, "A2": 1},
        args=["N", "A1", "PFD", "cPFD"],
    )

    m.add_reaction_from_args(
        rate_name="v2",
        function=r.v2,
        stoichiometry={"A2": -1},
        derived_stoichiometry={
            "H": DerivedStoichiometry(
                r.times_two,
                args=["bH"],
            ),
        },
        args=["A2", "k2"],
    )

    m.add_reaction_from_args(
        rate_name="v3",
        function=r.v3,
        stoichiometry={"A1": 1, "P": 1},
        args=["A1", "A2", "P", "D", "X", "k3p", "k3m"],
    )

    m.add_reaction_from_args(
        rate_name="v4",
        function=r.v4,
        stoichiometry={"P": -1},
        derived_stoichiometry={
            "H": DerivedStoichiometry(
                r.value,
                args=["bH"],
            ),
        },
        args=["P", "k4"],
    )

    m.add_reaction_from_args(
        rate_name="v5",
        function=r.v5,
        stoichiometry={"T": 1},
        derived_stoichiometry={
            "H": DerivedStoichiometry(
                r.times_minus_fourteen_thirds,
                args=["bH"],
            ),
        },
        args=["T", "H", "A", "k5", "DG0", "Hst", "RT", "Pi"],
    )

    m.add_reaction_from_args(
        rate_name="v6",
        function=r.v6,
        stoichiometry={"N": 1},
        args=["N", "H", "k6", "n", "KQ"],
    )

    m.add_reaction_from_args(
        rate_name="v7",
        function=r.v7,
        stoichiometry={"N": -1},
        args=["N", "k7"],
    )

    m.add_reaction_from_args(
        rate_name="v8",
        function=r.v8,
        stoichiometry={},
        derived_stoichiometry={
            "H": DerivedStoichiometry(
                r.neg,
                args=["bH"],
            ),
        },
        args=["H", "Hst", "k8"],
    )

    m.add_reaction_from_args(
        rate_name="v9",
        function=r.v9,
        stoichiometry={"T": -1},
        args=["T", "k9"],
    )
    return m


def get_model() -> Model:
    m = Model()
    m.add_compounds(
        [
            "A1",
            "A2",
            "P",
            "H",
            "N",
            "T",
        ]
    )
    m.add_parameters(
        {
            "k2": 3.4e6,
            "k3p": 1.56e5,
            "k3m": 3.12e4,
            "k4": 50,
            "k5": 80,
            "k6": 0.05,
            "k7": 0.004,
            "k8": 10,
            "k9": 20,
            "D": 2.5,
            "X": 17.5,
            "A": 32,
            "KQ": 0.004,
            "n": 5,
            "bH": 0.01,
            "cPFD": 4 / 3,
            "DG0": 30.6,
            "Pi": 0.01,  # mM in M and conversion to mmol/(mol*Chl^-1)
            "Hst": 6.34e-5,  # Why sould this correspond to an pH of 7.8 (units mmol(mol*Chl^-1))
            "R": 0.0083,
            "Temp": 298,
            "PFD": 10,
        }
    )
    m = _add_derived_parameters(m)
    m = _add_reactions(m)
    return m


# Compounds

comps = [
    "A1", # RCs in open state
    "A2", # RCs in separated charges state
    "P", # Inorganic phosphate
    "H", # Proton
    "N", # Quencher
    "T", # 
]

# Parameters

# Rates


def create_model() -> Model:
    m = Model()

    m.add_compounds

    return m
