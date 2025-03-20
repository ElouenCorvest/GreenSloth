import os
import re
from datetime import datetime
from pathlib import Path

import latexify
import pandas as pd
from modelbase2 import Model
from modelbase2.types import Derived

from greensloth_utils import basicfuncs as bf
from greensloth_utils.basicfuncs import continous_subtraction, proportional


def extract_select_to_gloss(
    select: dict,
    column_names: list,
    pythonvar_col: str,
    path_to_write: Path,
    value_col: str | None = None,
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
        key: value
        for key, value in zip(column_names, [[] for i in column_names], strict=False)
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

    if path_to_write.suffix != "csv":
        path_to_write = path_to_write.with_suffix(".csv")

    df.to_csv(path_to_write, na_rep="", index=False)


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
        with open(path_to_write, "w") as f:
            f.write(f"------- Start on {datetime.now()} -------\n\n")
            f.write(inp)
    else:
        with open(path_to_write) as f_tmp:
            read = f_tmp.read()
        flag_idxs = [m.start() for m in re.finditer("-------", read)]

        try:
            compare_block = read[flag_idxs[1] + 9 : flag_idxs[2]]
        except:
            compare_block = read[flag_idxs[1] + 9 :]

        if compare_block == inp:
            return
        with open(path_to_write, "r+") as f:
            f.seek(0, 0)
            f.write(f"------- Update on {datetime.now()} -------\n\n" + inp + read)
            print(f'Updated "{path_to_write.name}"')


def write_python_from_gloss(
    path_to_write: Path,
    path_to_glass: pd.DataFrame,
    var_list_name: str,
) -> None:
    gloss = pd.read_csv(
        path_to_glass,
        keep_default_na=False,
        converters={"Glossary ID": lambda i: int(i) if i != "" else ""},
    )

    inp = ""
    for idx, row in gloss.iterrows():
        inp += f"{row['Python Var']} = remove_math({var_list_name}, r'{row['Paper Abbr.']}')\n"
    inp += "\n"

    update_txt_file(path_to_write=path_to_write, inp=inp)


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
                    strict=False,
                ):
                    final = final.replace(old, new)
                lhs = final.split("=")[0]
                rhs = final.split("=")[1]
                func_a_list = lhs[lhs.find("(") + 1 : -2].split(", ")

                for arg_model, arg_ltx in zip(var.args, func_a_list, strict=False):
                    rhs = rhs.replace(arg_ltx, f"{{{arg_model}}}")

            except:  # noqa: E722
                rhs = f'ERROR because of function "{var.fn.__name__}"'

        inp += "```math\n"
        inp += rf"{{{name}}} = {rhs}"
        inp += "\n```\n"

    inp += "\n"

    update_txt_file(path_to_write=write_path, inp=inp)


def export_odes_as_latex(path_to_write: Path, m: Model, overwrite_flag: bool = False):
    inp = ""

    stoics = m.get_stoichiometries()

    for comp, stoic in stoics.iterrows():
        line = "```math \n"

        clean = stoic[stoic != 0.0]
        rates = clean.index

        line += rf"{{ode({comp})}} ="

        for rate in rates:
            specific_stoic = m.reactions[rate].stoichiometry[comp]
            if type(specific_stoic) == Derived:
                try:
                    stoic_func = getattr(bf, specific_stoic.fn.__name__)
                    ltx = latexify.get_latex(stoic_func, reduce_assignments=True)
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
                        strict=False,
                    ):
                        final = final.replace(old, new)
                    lhs = final.split("=")[0]
                    rhs = final.split("=")[1][1:]
                    func_a_list = lhs[lhs.find("(") + 1 : -2].split(", ")

                    for arg_model, arg_ltx in zip(
                        specific_stoic.args, func_a_list, strict=False
                    ):
                        rhs = rhs.replace(arg_ltx, f"{{{arg_model}}}")

                except:  # noqa: E722
                    rhs = f'ERROR because of function "{specific_stoic.fn.__name__}"'

            else:
                rhs = specific_stoic

            stoi = str(rhs)
            if stoi[0] == "-":
                comb = " - "
                stoi = stoi[1:]
            elif line[-1] != "=":
                comb = " + "
            else:
                comb = " "

            if stoi == "1":
                stoi = ""
            else:
                stoi += r" \cdot "

            line += rf"{comb + stoi}{{{rate}}}"

        line += "\n"
        line += "```\n"

        inp += line

    inp += "\n"

    update_txt_file(path_to_write=path_to_write, inp=inp)


def remove_math(
    df, query_result, query_column="Paper Abbr.", answer_column="Common Abbr."
):
    res = df[df[query_column] == query_result][answer_column].values[0]

    return res.replace("$", "")


def gloss_fromCSV(
    path: Path,
    cite_dict: dict | None = None,
    reference_col: str = "Reference",
    omit_col: str | None = None,
):
    table_df = pd.read_csv(path, keep_default_na=False)

    if omit_col is not None:
        table_df = table_df.drop(columns=[omit_col])

    if cite_dict is not None:
        table_df[reference_col] = table_df[reference_col].apply(
            cite, args=(), cite_dict=cite_dict
        )

    table_tolist = [table_df.columns.values.tolist()] + table_df.values.tolist()

    table_list = [i for k in table_tolist for i in k]

    return table_df, table_tolist, table_list


def cite(
    cit: str,
    cite_dict: dict,
):
    if cit == "" or not url(cit):
        return cit
    if cit in cite_dict:
        return f"[[{cite_dict[cit]}]]({cit})"
    num_cites_stored = len(cite_dict.keys())
    cite_dict[cit] = num_cites_stored + 1
    return f"[[{cite_dict[cit]}]]({cit})"


def update_from_main_gloss(
    main_gloss_path,
    gloss_path,
    model_title,
    add_to_main=False,
):
    main_gloss = pd.read_csv(
        main_gloss_path, keep_default_na=False, dtype={"Glossary ID": "Int64"}
    )
    gloss = pd.read_csv(
        gloss_path,
        keep_default_na=False,
        converters={"Glossary ID": lambda i: int(i) if i != "" else ""},
    )

    gloss_ids = gloss["Glossary ID"]

    main_to_gloss_col_match = [i for i in main_gloss.columns if i in gloss.columns]

    for index, gloss_id in gloss_ids.items():
        main_ids = main_gloss["Glossary ID"]

        if gloss_id == "":
            if add_to_main:
                try:
                    new_id = max(main_ids) + 1
                except:  # noqa: E722
                    new_id = 1

                gloss.loc[index, "Glossary ID"] = new_id

                main_gloss_dic = {}

                for col_name in main_gloss.columns:
                    if col_name in gloss.columns:
                        new_val = gloss.loc[
                            gloss["Glossary ID"] == new_id, col_name
                        ].values[0]

                    elif col_name == "Reference":
                        new_val = f"{model_title}"

                    main_gloss_dic[col_name] = [new_val]

                new_df = pd.DataFrame(main_gloss_dic)

                main_gloss = pd.concat([main_gloss, new_df], join="inner")

        else:
            for i in main_to_gloss_col_match:
                new_val = main_gloss.loc[
                    main_gloss["Glossary ID"] == gloss_id, i
                ].values[0]
                gloss.loc[index, i] = new_val

            main_refs = main_gloss.loc[
                main_gloss["Glossary ID"] == gloss_id, "Reference"
            ].values[0]

            if model_title not in main_refs:
                main_refs += f", {model_title}"

            main_gloss.loc[main_gloss["Glossary ID"] == gloss_id, "Reference"] = (
                main_refs
            )

    gloss.to_csv(gloss_path, na_rep="", index=False)
    if add_to_main:
        inp = input("Are you sure you want to update the main gloss? y/[n] > ")
        if inp.upper() in ["Y", "YES"]:
            print("Main Gloss Changed")
            main_gloss.to_csv(main_gloss_path, na_rep="", index=False)
