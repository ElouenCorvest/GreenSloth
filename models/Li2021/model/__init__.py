from modelbase2 import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = [
    'Li2021'
]

def Li2021() -> Model:
    m = Model()

    m.add_parameters(
        {

        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
