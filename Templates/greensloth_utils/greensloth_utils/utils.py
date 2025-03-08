from typing import Optional
from pathlib import Path
import pandas as pd

def extract_select_to_gloss(
    select: dict,
    column_names: list,
    pythonvar_col: str,
    path_to_write: Path,
    value_col: Optional[str] = None,
):
    tmp_dict = {
        key: value for key, value in zip(column_names, [[] for i in column_names])
    }

    for name, var in select.items():
        for i in column_names:
            if i == pythonvar_col:
                tmp_dict[i].append(name)
            elif i == value_col:
                tmp_dict[i].append(f"${var}$")
            else:
                tmp_dict[i].append("")

    df = pd.DataFrame(tmp_dict)
    df.to_csv(path_to_write, na_rep="", index=False)
    return