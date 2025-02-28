from modelbase2 import Model
import os
import sys
import inspect
import re
import pandas as pd
from typing import Optional
from pathlib import Path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, os.path.dirname(parentdir))

from model import Li2021

def extract_select_to_gloss(
    select: dict,
    column_names: list,
    pythonvar_col: str,
    path_to_write: Path,
    value_col: Optional[str] = None
):
    tmp_dict = {key: value for key, value in zip(column_names, [[] for i in column_names])}

    for name, var in select.items():
        for i in column_names:
            if i == pythonvar_col:
                tmp_dict[i].append(name)
            elif i == value_col:
                tmp_dict[i].append(f'${var}$')
            else:
                tmp_dict[i].append('')

    df = pd.DataFrame(tmp_dict)
    df.to_csv(path_to_write, na_rep='', index=False)
    return

def check_gloss_to_model(
    from_model: Path,
    edit_gloss: Path,
    check_col: str
):
    df_model = pd.read_csv(from_model, keep_default_na=False)
    df_gloss = pd.read_csv(edit_gloss, keep_default_na=False)

    checked_model = set(df_model[check_col]) - set(df_gloss[check_col])
    checked_gloss = set(df_gloss[check_col]) - set(df_model[check_col])

    if len(checked_model) != 0 or len(checked_gloss) != 0:
        print(f'\n Inconsistencies found! In {from_model.name} and {edit_gloss.name}: ')
        print(f'"{checked_model}"')
        print(f'"{checked_gloss}"')
    else:
        print(f'\n No inconsistencies found in {from_model.name} and {edit_gloss.name}! :)')


extract_select_to_gloss(
    select=Li2021().variables,
    column_names=['Name', 'Common Abbr.', 'Paper Abbr.', 'MetaCyc ID', 'Python Var', 'Glossary ID'],
    pythonvar_col='Python Var',
    path_to_write=Path(__file__).parent / 'model_comps.csv'
)

extract_select_to_gloss(
    select=Li2021().parameters,
    column_names=['Short Description', 'Common Abbr.', 'Paper Abbr.', 'Value', 'Unit', 'Python Var', 'Reference'],
    pythonvar_col='Python Var',
    path_to_write=Path(__file__).parent / 'model_params.csv',
    value_col='Value'
)

extract_select_to_gloss(
    select=Li2021().derived_variables,
    column_names=['Name', 'Common Abbr.', 'Paper Abbr.', 'MetaCyc ID', 'Python Var', 'Glossary ID'],
    pythonvar_col='Python Var',
    path_to_write=Path(__file__).parent / 'model_derived_comps.csv',
)

extract_select_to_gloss(
    select=Li2021().derived_parameters,
    column_names=['Short Description', 'Common Abbr.', 'Paper Abbr.', 'Python Var'],
    pythonvar_col='Python Var',
    path_to_write=Path(__file__).parent / 'model_derived_params.csv',
)

extract_select_to_gloss(
    select=Li2021().reactions,
    column_names=['Short Description', 'Common Abbr.', 'Paper Abbr.', 'MetaCyc ID', 'Python Var', 'Glossary ID'],
    pythonvar_col='Python Var',
    path_to_write=Path(__file__).parent / 'model_rates.csv',
)

for i in ['comps', 'rates', 'params', 'derived_comps', 'derived_params']:
    check_gloss_to_model(
        from_model=Path(__file__).parent / f'model_{i}.csv',
        edit_gloss=Path(__file__).parents[1] / f'{i}.csv',
        check_col='Python Var'
    )
