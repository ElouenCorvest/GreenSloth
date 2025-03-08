from typing import Optional
from pathlib import Path
import pandas as pd
from datetime import datetime
import os
import re
from modelbase2 import Model
import latexify
from greensloth_utils.basicfuncs import proportional, continous_subtraction

def extract_select_to_gloss(
    select: dict,
    column_names: list,
    pythonvar_col: str,
    path_to_write: Path,
    value_col: Optional[str] = None,
) -> None:
    """Take a selection of a model and extract all the python vars to a csv glossary

    Args:
        select (dict): Part of the model to be examined
        column_names (list): Names of the new Columns in the glossary
        pythonvar_col (str): Name of the column to insert all the python vars. Has to be included in column_names!
        path_to_write (Path): Path of csv to write to. If suffix isn't ".csv", then it will be replaced!
        value_col (Optional[str], optional): Optional column name to add values to. Useful for parameters. Defaults to None.
    """  
      
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
    
    if path_to_write.suffix != 'csv':
        path_to_write = path_to_write.with_suffix('.csv')
    
    df.to_csv(path_to_write, na_rep="", index=False)
    return

def check_gloss_to_model(from_model: Path, edit_gloss: Path, check_col: str):
    df_model = pd.read_csv(from_model, keep_default_na=False)
    df_gloss = pd.read_csv(edit_gloss, keep_default_na=False)

    checked_model = set(df_model[check_col]) - set(df_gloss[check_col])
    checked_gloss = set(df_gloss[check_col]) - set(df_model[check_col])

    if len(checked_model) != 0 or len(checked_gloss) != 0:
        print(f"\n Inconsistencies found! In {from_model.name} and {edit_gloss.name}: ")
        print(f'"{checked_model}"')
        print(f'"{checked_gloss}"')
    else:
        print(
            f"\n No inconsistencies found in {from_model.name} and {edit_gloss.name}! :)"
        )

def update_txt_file(
    path_to_write: Path,
    inp: str,
) -> None:
    if not os.path.isfile(path_to_write):
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

def write_python_from_gloss(
    path_to_write: Path,
    path_to_glass: pd.DataFrame,
    var_list_name: str,
) -> None:

    gloss = pd.read_csv(path_to_glass, keep_default_na=False, converters={'Glossary ID': lambda i: int(i) if i != '' else ''})

    inp = ''
    for idx, row in gloss.iterrows():
        inp += f"{row['Python Var']} = remove_math({var_list_name}, r'{row['Paper Abbr.']}')\n"
    inp += '\n'

    update_txt_file(
        path_to_write=path_to_write,
        inp=inp
    )
    
def export_glossselect_from_model(m: Model, gloss_path: Path, write_path: Path):
    
    gloss = pd.read_csv(
        gloss_path,
        keep_default_na=False,
        converters={"Glossary ID": lambda i: int(i) if i != "" else ""},
    )

    inp = ""

    for name in gloss["Python Var"]:
        if m.ids[name] == "derived":
            var = m.derived[name]
        elif m.ids[name] == "reaction":
            var = m.reactions[name]
        else:
            raise TypeError(
                f'"{name}" is not a reaction or derived. It is a "{m.ids[name]}"'
            )

        if var.fn == proportional:
            rhs = ""
            for i in var.args:
                rhs += rf"{{{i}}} \cdot "
            rhs = rhs[:-7]

        elif var.fn == continous_subtraction:
            rhs = ""
            for i in var.args:
                rhs += rf"{{{i}}} - "
            rhs = rhs[:-3]

        else:
            try:
                ltx = latexify.get_latex(var.fn, reduce_assignments=True)
                if ltx.count(r"\\") > 0:
                    for i in [r"\begin{array}{l} ", r" \end{array}"]:
                        ltx = ltx.replace(i, "")
                    line_split = ltx.split(r"\\")
                else:
                    line_split = [ltx]

                final = line_split[-1]

                for i in line_split[:-1]:
                    lhs = i.split(" = ")[0].replace(" ", "")
                    rhs = i.split(" = ")[1]
                    final = final.replace(lhs, rhs)

                for old, new in zip(
                    (
                        r"\mathopen{}",
                        r"\mathclose{}",
                        r"{",
                        r"}",
                    ),
                    ("", "", r"{{", r"}}"),
                ):
                    final = final.replace(old, new)
                lhs = final.split("=")[0]
                rhs = final.split("=")[1]
                func_a_list = lhs[lhs.find("(") + 1 : -2].split(", ")

                for arg_model, arg_ltx in zip(var.args, func_a_list):
                    rhs = rhs.replace(arg_ltx, f"{{{arg_model}}}")

            except:  # noqa: E722
                rhs = f'ERROR because of function "{var.fn.__name__}"'

        inp += "```math\n"
        inp += rf"{{{name}}} = {rhs}"
        inp += "\n```\n"

    inp += "\n"

    update_txt_file(
        path_to_write=write_path,
        inp=inp
    )
