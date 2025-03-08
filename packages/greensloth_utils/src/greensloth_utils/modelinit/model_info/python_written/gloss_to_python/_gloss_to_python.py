from pathlib import Path
from greensloth_utils import write_python_from_gloss


for i in ['comps', 'rates', 'params', 'derived_comps', 'derived_params']:
    write_python_from_gloss(
        path_to_write=Path(__file__).parent / f'{i}.txt',
        path_to_glass=Path(__file__).parents[2] / f'{i}.csv',
        var_list_name=f'{i}_table'
    )