import pandas as pd
import os
from typing import Optional
from pathlib import Path
from modelbase2 import Model
#from modelbase.ode import Model
from datetime import datetime
import re
from validators import url
import latexify

def df_to_dict(
    df: pd.DataFrame,
    keep_index: bool = False,
):
    if len(df) == 0:
        raise ValueError('The df "{df}" is empty. It cannot be translated to a dict.')
    elif len(df) > 1:
        raise ValueError('The df "{df}" contains more than one row. The dict will not be appropriate.')
    else:
        result_dict = {}

        tmp_dict = df.to_dict()

        if keep_index:
            return tmp_dict
        else:
            for key, value in tmp_dict.items():
                result_dict[key] = list(value.values())[0]

            return result_dict


def extract_from_glossary(
    paper_abbr: str,
    glossary_path: os.PathLike[str]
):
    glossary_df = pd.read_csv(glossary_path)

    result_dict = {}

    cor_row = glossary_df.loc[glossary_df['Paper Abbreviation'] == paper_abbr]

    if not cor_row.empty:

        result_dict = df_to_dict(cor_row)

        return result_dict

    else:
        print()
        print(f'"{paper_abbr}" is not found in the glossary')
        add_to_gloss = input('Do you wish to include it in the existing glossary? - Type "Yes" or "No": \n')

        if add_to_gloss in ['Yes', 'yes', 'y']:

            insert_to_glossary(
                paper_abbr,
                glossary_df,
                glossary_path=glossary_path,
            )

            return extract_from_glossary(
                paper_abbr=paper_abbr,
                glossary_path=glossary_path
            )

        else:

            print('Abbreviation cannot be found in glossary')

            return None

def insert_to_glossary(
    paper_abbr: str,
    glossary: pd.DataFrame,
    glossary_path: os.PathLike[str],
):
    header = glossary.columns

    dict_to_add = {}

    for column_name in header:

        if column_name == 'Paper Abbreviation':
            tmp_input = paper_abbr
        else:
            tmp_input = input(f'Type in the information that corresponds to the "{column_name}": \n')
            print()

        if not (glossary.loc[glossary[column_name] == tmp_input].empty) and 'Reference' not in column_name:

            print('We have found an entry corresponding to your input.')
            print()
            print(glossary.loc[glossary[column_name] == tmp_input])
            print()
            override_input = input(f'Do you wish to take these settings and add the new "{paper_abbr}"')

            if override_input in ['Yes', 'yes', 'y']:
                dict_to_add = df_to_dict(glossary.loc[glossary[column_name] == tmp_input], keep_index=True)

                dict_to_add['Paper Abbreviation'] = paper_abbr

                dict_to_add['Reference Paper'] = input('What is the reference of the new glossary entry?: \n')

                break

        else:
            dict_to_add[column_name] = [tmp_input]

    df_to_add = pd.DataFrame.from_dict(dict_to_add)
    df_combined = pd.concat([glossary, df_to_add], ignore_index = True)

    df_combined.to_csv(glossary_path, index=False)

def change_item(
    glossary_path: os.PathLike[str],
    glossary_column: str,
    old_item: str,
    new_item: str,
):
    glossary_df = pd.read_csv(glossary_path)

    glossary_df[[glossary_column]] = glossary_df[[glossary_column]].replace(
        to_replace=old_item,
        value=new_item,
    )

    glossary_df.to_csv(glossary_path, index = False)

def update_from_main_gloss(
    main_gloss_path,
    gloss_path,
    model_title,
    add_to_main = False,
):

    main_gloss = pd.read_csv(main_gloss_path, keep_default_na=False, dtype={'Glossary ID': 'Int64'})
    gloss = pd.read_csv(gloss_path, keep_default_na=False, converters={'Glossary ID': lambda i: int(i) if i != '' else ''})

    gloss_ids = gloss['Glossary ID']

    main_to_gloss_col_match = [i for i in main_gloss.columns if i in gloss.columns]

    for index, gloss_id in gloss_ids.items():
        main_ids = main_gloss['Glossary ID']

        if gloss_id == '':
            if add_to_main:
                try:
                    new_id = max(main_ids) + 1
                except:
                    new_id = 1

                gloss.loc[index, 'Glossary ID'] = new_id

                main_gloss_dic = {}

                for col_name in main_gloss.columns:
                    if col_name in gloss.columns:
                        new_val = gloss.loc[gloss['Glossary ID'] == new_id, col_name].values[0]

                    elif col_name == 'Reference':
                        new_val = f'{model_title}'

                    main_gloss_dic[col_name] = [new_val]

                new_df = pd.DataFrame(main_gloss_dic)

                main_gloss = pd.concat([main_gloss, new_df], join='inner')

        else:
            for i in main_to_gloss_col_match:
                new_val = main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, i].values[0]
                gloss.loc[index, i] = new_val

            main_refs = main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, 'Reference'].values[0]

            if model_title not in main_refs:
                main_refs += f', {model_title}'

            main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, 'Reference'] = main_refs

    gloss.to_csv(gloss_path, na_rep = '', index=False)
    if add_to_main:
        main_gloss.to_csv(main_gloss_path, na_rep = '', index=False)

    return

def gloss_fromCSV(
    path: Path,
    cite_dict: Optional[dict] = None,
    reference_col: str = 'Reference',
    omit_col: Optional[str] = None,
):
    table_df = pd.read_csv(path, keep_default_na=False)

    if omit_col is not None:
        table_df = table_df.drop(columns=[omit_col])

    if cite_dict is not None:
        table_df[reference_col] = table_df[reference_col].apply(cite, args=(), cite_dict=cite_dict)

    table_tolist = [table_df.columns.values.tolist()] + table_df.values.tolist()

    table_list = [i for k in table_tolist for i in k]

    return table_df, table_tolist, table_list

def cite(
    cit: str,
    cite_dict: dict,
):
    if cit == '' or not url(cit):
        return cit
    elif cit in cite_dict.keys():
        return f'[[{cite_dict[cit]}]]({cit})'
    else:
        num_cites_stored = len(cite_dict.keys())
        cite_dict[cit] = num_cites_stored + 1
        return f'[[{cite_dict[cit]}]]({cit})'

def write_python_from_gloss(
    path_to_write: Path,
    gloss: pd.DataFrame,
    var_list_name: str,
    overwrite_flag: bool = False
):
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
                print(f'Updated "{var_list_name}"')

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
            'Value': [f'${i}$' for i in params.values()],
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

def mathstr_to_py(s):
    if r'\frac' in s:
        s = s.replace(r'\frac{', '')
        s = s.replace('}{', ' / ')
    for i in [r' \times 10^', r' \cdot 10^']:
        s = s.replace(i, 'e')
    for i in ['$', '{', '}', r'\mathrm']:
        s = s.replace(i, '')
    for i in [r'\times', r'\cdot']:
        s = s.replace(i, '*')
    return fr'{s}'

def unitstr_to_py(s):
    s = s.replace(r'\mu ', 'µ')
    for i in [r'\mathrm', r'\left', r'\right', '^', "\\", '$', '{', '}']:
        s = s.replace(i, '')
    return fr'[{s}]'

def export_params(
    path_to_params: Path,
    path_to_write: Path,
    overwrite_flag = False,
):
    df = pd.read_csv(path_to_params, keep_default_na=False)

    inp = ''
    for idx, row in df.iterrows():
        inp += f"'{row['Python Var']}': {mathstr_to_py(row['Value'])},     # {unitstr_to_py(row['Unit'])} {row['Short Description']} \n"
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
                print(f'Updated Params to Python')
