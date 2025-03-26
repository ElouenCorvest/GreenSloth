import os
import sys
import inspect
from pathlib import Path
from greensloth_utils import extract_select_to_gloss, check_gloss_to_model


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, os.path.dirname(parentdir))

from model import Matuszynska2016  # noqa: E402


extract_select_to_gloss(
    select=Matuszynska2016().variables,
    column_names=[
        "Name",
        "Common Abbr.",
        "Paper Abbr.",
        "MetaCyc ID",
        "Python Var",
        "Glossary ID",
    ],
    pythonvar_col="Python Var",
    path_to_write=Path(__file__).parent / "model_comps.txt",
)

extract_select_to_gloss(
    select=Matuszynska2016().parameters,
    column_names=[
        "Short Description",
        "Common Abbr.",
        "Paper Abbr.",
        "Value",
        "Unit",
        "Python Var",
        "Reference",
    ],
    pythonvar_col="Python Var",
    path_to_write=Path(__file__).parent / "model_params.csv",
    value_col="Value",
)

extract_select_to_gloss(
    select=Matuszynska2016().derived_variables,
    column_names=[
        "Name",
        "Common Abbr.",
        "Paper Abbr.",
        "MetaCyc ID",
        "Python Var",
        "Glossary ID",
    ],
    pythonvar_col="Python Var",
    path_to_write=Path(__file__).parent / "model_derived_comps.csv",
)

extract_select_to_gloss(
    select=Matuszynska2016().derived_parameters,
    column_names=["Short Description", "Common Abbr.", "Paper Abbr.", "Python Var"],
    pythonvar_col="Python Var",
    path_to_write=Path(__file__).parent / "model_derived_params.csv",
)

extract_select_to_gloss(
    select=Matuszynska2016().reactions,
    column_names=[
        "Short Description",
        "Common Abbr.",
        "Paper Abbr.",
        "MetaCyc ID",
        "Python Var",
        "Glossary ID",
    ],
    pythonvar_col="Python Var",
    path_to_write=Path(__file__).parent / "model_rates.csv",
)

for i in ["comps", "rates", "params", "derived_comps", "derived_params"]:
    check_gloss_to_model(
        from_model=Path(__file__).parent / f"model_{i}.csv",
        edit_gloss=Path(__file__).parents[1] / f"{i}.csv",
        check_col="Python Var",
    )
