import pandas as pd
from pathlib import Path
from datetime import datetime
import os
import re

def write_python_from_gloss(
    path_to_write: Path,
    path_to_glass: pd.DataFrame,
    var_list_name: str,
    overwrite_flag: bool = False
):

    gloss = pd.read_csv(path_to_glass, keep_default_na=False, converters={'Glossary ID': lambda i: int(i) if i != '' else ''})

    inp = ''
    for idx, row in gloss.iterrows():
        inp += f"{row['Python Var']} = remove_math({var_list_name}, r'{row['Paper Abbr.']}')\n"
    inp += '\n'

    if overwrite_flag or not os.path.isfile(path_to_write):
        with open(path_to_write, 'w') as f:
            f.write(f'------- Start on {datetime.now()} -------\n\n')
            f.write(inp)
    else:
        with open(path_to_write, 'r') as f_tmp:
            read = f_tmp.read()
        flag_idxs = [m.start() for m in re.finditer('-------', read)]

        try:
            compare_block = read[flag_idxs[1] + 9:flag_idxs[2]]
        except:
            compare_block = read[flag_idxs[1] + 9:]

        if compare_block == inp:
            return
        else:
            with open(path_to_write, 'r+') as f:
                f.seek(0, 0)
                f.write(f'------- Update on {datetime.now()} -------\n\n' + inp + read)
                print(f'Updated "{path_to_write.name}"')

for i in ['comps', 'rates', 'params', 'derived_comps', 'derived_params']:
    write_python_from_gloss(
        path_to_write=Path(__file__).parent / f'{i}.txt',
        path_to_glass=Path(__file__).parents[2] / f'{i}.csv',
        var_list_name=f'{i}_table'
    )
