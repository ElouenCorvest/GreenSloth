from modelbase2 import Model
from pathlib import Path
import latexify
from datetime import datetime
import os
import sys
import inspect
import re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, os.path.dirname(parentdir))

from model import Saadat2021
from model.basic_funcs import proportional, continous_subtraction

def export_select_as_latex(
    select: dict,
    path_to_write: Path
):
    inp = '```math \n'
    inp += r'   \begin{{align}}'
    inp += '\n'

    for name, var in select.items():
        if var.fn == proportional:
            rhs = ''
            for i in var.args:
                rhs += fr'{{{i}}} \cdot '
            rhs = rhs[:-7]

        elif var.fn == continous_subtraction:
            rhs = ''
            for i in var.args:
                rhs += fr'{{{i}}} - '
            rhs = rhs[:-3]

        else:
            try:

                ltx = latexify.get_latex(var.fn)
                if ltx.count(r'\\') > 0:
                    for i in [r'\begin{array}{l} ', r' \end{array}']:
                        ltx = ltx.replace(i, '')
                    line_split = ltx.split(r'\\')
                else:
                    line_split = [ltx]

                final = line_split[-1]

                for i in line_split[:-1]:
                    lhs = i.split(' = ')[0].replace(' ', '')
                    rhs = i.split(' = ')[1]
                    final = final.replace(lhs, rhs)

                for old, new in zip(
                    (r'\mathopen{}', r'\mathclose{}', r'{', r'}'),
                    ('', '', r'{{', r'}}')
                ):
                    final = final.replace(old, new)
                lhs = final.split('=')[0]
                rhs = final.split('=')[1]
                func_a_list = lhs[lhs.find('(')+1:-2].split(', ')

                for arg_model, arg_ltx in zip(var.args, func_a_list):
                    rhs = rhs.replace(arg_ltx, f'{{{arg_model}}}')

            except:
                rhs = f'ERROR because of function "{var.fn.__name__}"'

        inp += rf'       {{{name}}} &= {rhs} \\'
        inp += '\n'

    inp += r'   \end{{align}}'
    inp += '\n'
    inp += '```\n\n'

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

def export_odes_as_latex(
    path_to_write: Path,
    m: Model,
    overwrite_flag: bool = False
):

    inp = '```math \n'
    inp += r'   \begin{{align}}'
    inp += '\n'

    stoics = m.get_stoichiometries()

    for comp, stoic in stoics.iterrows():
        clean = stoic[stoic != 0.0]
        rates = clean.index

        line = rf"      {{ode({comp})}} &= "
        for rate in rates:
            stoi = clean[rate]
            if line[-2] == '=':
                stoi = str(stoi)
            else:
                if stoi < 0:
                    stoi = f'- {abs(stoi)}'
                else:
                    stoi = f'+ {stoi}'

            line += rf'{stoi} \cdot {{{rate}}} '

            line = line.replace(r'1 \cdot ', '')

        line = line[:-1] + r' \\'
        line += " \n"

        inp += line
    inp += r'   \end{{align}}'
    inp += '\n'
    inp += '```\n\n'

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

export_select_as_latex(
    select=Saadat2021().reactions,
    path_to_write=Path(__file__).parent / 'model_rates.txt'
)

export_select_as_latex(
    select=Saadat2021().derived_variables,
    path_to_write=Path(__file__).parent / 'model_derived_comps.txt'
)

export_select_as_latex(
    select=Saadat2021().derived_parameters,
    path_to_write=Path(__file__).parent / 'model_derived_params.txt'
)

export_odes_as_latex(
    m=Saadat2021(),
    path_to_write= Path(__file__).parent / 'model_odes.txt'
)
