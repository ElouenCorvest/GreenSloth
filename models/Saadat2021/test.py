from modelbase.ode import Model
from models import get_model
from pathlib import Path
import os
import pandas as pd
from glossary_utils.glossary import export_params, export_rates_as_latex

def check_unused_params(
    m: Model
):

    all_param_names = m.get_parameter_names()

    used_params = set()
    for key, val in m.rates.items():
        for param in val['parameters']:
            used_params.add(param)

    for val in m.derived_parameters.values():
        for param in val.parameters:
            used_params.add(param)

    for key, val in m.algebraic_modules.items():
        for param in val['parameters']:
            used_params.add(param)

    modelbase_check = m.check_unused_parameters()


    unused_params = [i for i in all_param_names if i not in used_params]
    double_check = [i for i in modelbase_check if i not in unused_params]
    triple_check = [i for i in modelbase_check if i in unused_params]

    return unused_params, double_check, triple_check

# print(check_unused_params(get_model())[2])

# df = pd.read_csv('/home/elouen/Documents/PhotoModelBase/models/Saadat2021/model_info/params.csv', keep_default_na=False)
# df = df[~df['Python Var'].isin(check_unused_params(get_model())[2])]
# df.to_csv('/home/elouen/Documents/PhotoModelBase/models/Saadat2021/model_info/params.csv', na_rep = '', index=False)

# export_params(
#     '/home/elouen/Documents/PhotoModelBase/models/Saadat2021/model_info/params.csv',
#     path_to_write='/home/elouen/Documents/PhotoModelBase/models/Saadat2021/model_info/python_written/model_params.txt',
# )

export_rates_as_latex(
    m = get_model(),
    path_to_write='/home/elouen/Documents/PhotoModelBase/models/Saadat2021/model_info/python_written/model_rates.txt'
)
