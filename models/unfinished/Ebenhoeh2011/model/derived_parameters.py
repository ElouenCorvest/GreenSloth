from modelbase.ode import Model
from . import basic_funcs as bf

def include_derived_parameters(m: Model) -> Model:
    m.add_derived_parameter(
        parameter_name="RT",
        function= bf.proportional,
        parameters=["R", "Temp"],
    )
    
    m.add_derived_parameter(
        parameter_name='k1',
        function= bf.proportional,
        parameters=['cPFD', 'PFD']
    )
    return m