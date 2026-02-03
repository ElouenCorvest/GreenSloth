from pathlib import Path

from GreenSlothUtils import mxlpy_formatter

from model import get_bellasio2019

mxlpy_formatter.redefine_names(
    vars_glossary_path=Path(__file__).parents[2] / "comps_glossary.csv",
    rates_glossary_path=Path(__file__).parents[2] / "rates_glossary.csv",
)

mxlpy_formatter.write_init(
    m=get_bellasio2019(),
    model_name="Bellasio2019",
    path=Path(__file__).parent / "__init__.py",
)

mxlpy_formatter.write_basic_funcs(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "basic_funcs.py",
)

mxlpy_formatter.write_reactions(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "rates.py",
)

mxlpy_formatter.write_derived(
    m=get_bellasio2019(),
    path=Path(__file__).parent / "derived_quantities.py",
)

