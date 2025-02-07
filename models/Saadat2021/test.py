from modelbase.ode import Model
from models import get_model
from pathlib import Path
import os
import pandas as pd

def extract_params_from_model(
    model = Model,
    path_to_write = Path
):
    params = model.get_parameters()
    
    if os.path.isfile(path_to_write):
        agree = input(f'\nFile "{path_to_write}" already exists. Do you wish to overwrite it?\n[y/[n]] >> ')
        if agree.upper() not in ['Y', 'YES']:
            print('Okay! Doing nothing.')
            return
    
    empty_lst = ['' for i in params.keys()]
    
    df = pd.DataFrame({
        'Short Description': empty_lst,
        'Common Abbr.': empty_lst,
        'Paper Abbr.': empty_lst,
        'Value': list(params.values()),
        'Unit': empty_lst,
        'MetaCyc ID': empty_lst,
        'Python Var': list(params.keys()),
        'Reference': empty_lst,
        'Glossary ID': empty_lst,
    })
    
    df.to_csv(
        path_to_write,
        index=False
    )
    
extract_params_from_model(
    model=get_model(),
    path_to_write='test.csv'
)