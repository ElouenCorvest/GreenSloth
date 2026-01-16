from pathlib import Path

from GreenSlothUtils import mxlbrickswriter

from model import get_bellasio2019

mxlbrickswriter.redefine_names(
    vars_glossary_path=Path(__file__).parents[2] / "comps_glossary.csv",
    rates_glossary_path=Path(__file__).parents[2] / "rates_glossary.csv",
)

mxlbrickswriter.write_init(
    m=get_bellasio2019(),
    model_name="Bellasio2019",
    path=Path(__file__).parent / "__init__.py",
)

mxlbrickswriter.write_basic_funcs(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "basic_funcs.py",
)

mxlbrickswriter.write_reactions(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "rates.py",
)

mxlbrickswriter.write_derived(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "derived_quantities.py",
)

