from GreenSlothUtils.mxlbrickswriter import (
    write_init,
    write_derived,
    write_basic_funcs,
    write_reactions,
    redefine_names,
)
from mxlbricks import get_saadat2021
from pathlib import Path
from copy import deepcopy

redefine_names(
    vars_glossary_path=Path(__file__).parents[2] / "comps_glossary.csv",
    rates_glossary_path=Path(__file__).parents[2] / "rates_glossary.csv",
)

# Manually change the E^0
changed_model = get_saadat2021()

params_to_change = {
    # Old Str, New str
    "pH": "pH_stroma",
    "H": "H_stroma",
    "E^0_QA": "E0_QA",
    "E^0_PQ": "E0_PQ",
    "E^0_PC": "E0_PC",
    "E^0_P700": "E0_P700",
    "E^0_FA": "E0_FA",
    "E^0_Fd": "E0_Fd",
    "E^0_NADP": "E0_NADP",
}

changed_model.remove_parameters(list(params_to_change.keys()))

for old, new in params_to_change.items():
    changed_model.add_parameter(new, get_saadat2021().get_parameter_values()[old])

for reac in changed_model._reactions.values():
    old_args = deepcopy(reac.args)
    new_args = []
    for arg in old_args:
        if arg in params_to_change:
            new_args.append(params_to_change[arg])
        else:
            new_args.append(arg)
    reac.args = new_args

for derived in changed_model._derived.values():
    old_args = deepcopy(derived.args)
    new_args = []
    for arg in old_args:
        if arg in params_to_change:
            new_args.append(params_to_change[arg])
        else:
            new_args.append(arg)
    derived.args = new_args


write_init(
    m=changed_model, model_name="Saadat2021", path=Path(__file__).parent / "__init__.py"
)

write_derived(m=changed_model, path=Path(__file__).parent / "derived_quantities.py")

write_reactions(m=changed_model, path=Path(__file__).parent / "rates.py")

write_basic_funcs(m=changed_model, path=Path(__file__).parent / "basic_funcs.py")
