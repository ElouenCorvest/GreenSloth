from __future__ import annotations

#from modelbase.ode import Model
from modelbase2 import Model
from . import derived_parameters, derived_quantities, rates
from .derived_quantities import Keq_func, pH, rev_pH
from .basic_funcs import quadratic

__all__ = [
    "Keq_func",
    "get_model",
    "pH",
    "quadratic",
    "rev_pH"
]


def get_model() -> Model:
    m = Model()
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
            "PQ_tot": 17.5,
            "AP_tot": 32,
            "KQ": 0.004,
            "n": 5,
            "bH": 0.01,
            "cPFD": 4 / 3,
            "DG0": 30.6,
            "Pi": 0.01,  # mM in M and conversion to mmol/(mol*Chl^-1)
            "H_st": 6.34e-5,  # Why sould this correspond to an pH of 7.8 (units mmol(mol*Chl^-1))
            "R": 0.0083,
            "Temp": 298,
            "PFD": 10,
        }
    )
    m.add_variables(
        {
            "A1": m.parameters["D"] / 2,
            "A2": m.parameters["D"] / 2,
            "PQ_ox": 0,
            "H_lu": 6.34e-5,
            "N": 0,
            "ATP_st": 0,
        }
    )
    m = derived_quantities.include_derived_quantities(m)
    m = rates.include_reactions(m)
    
    return m

def get_quasi_model() -> Model:
    m = Model()
    
    m.add_compounds([
        "H_lu",
        "N",
        "ATP_st",
    ])
    
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
            "PQ_tot": 17.5,
            "AP_tot": 32,
            "KQ": 0.004,
            "n": 5,
            "bH": 0.01,
            "cPFD": 4 / 3,
            "DG0": 30.6,
            "Pi": 0.01,  # mM in M and conversion to mmol/(mol*Chl^-1)
            "H_st": 6.34e-5,  # Why sould this correspond to an pH of 7.8 (units mmol(mol*Chl^-1))
            "R": 0.0083,
            "Temp": 298,
            "PFD": 10,
        }
    )
    m = derived_parameters.include_derived_parameters(m)
    m = derived_quantities.include_quasi_algebraic_modules(m)
    m = rates.include_quasi_reactions(m)
    return m