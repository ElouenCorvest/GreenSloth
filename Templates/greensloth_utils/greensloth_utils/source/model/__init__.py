from modelbase2 import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = [
    '{{MODEL_NAME}}'
]

def {{MODEL_NAME}}() -> Model:
    m = Model()

    m.add_parameters(
        {

        }
    )

    m.add_variables(
        {

        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m
