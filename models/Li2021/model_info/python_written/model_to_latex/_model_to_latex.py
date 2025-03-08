from modelbase2 import Model
from pathlib import Path
import latexify
from datetime import datetime
import os
import sys
import inspect
import re
import pandas as pd

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, os.path.dirname(parentdir))

from model import Li2021  # noqa: E402
from model.basic_funcs import proportional, continous_subtraction  # noqa: E402




def export_odes_as_latex(path_to_write: Path, m: Model, overwrite_flag: bool = False):
    inp = ""

    stoics = m.get_stoichiometries()

    for comp, stoic in stoics.iterrows():
        line = "```math \n"

        clean = stoic[stoic != 0.0]
        rates = clean.index

        line += rf"{{ode({comp})}} = "
        for rate in rates:
            stoi = clean[rate]
            if line[-2] == "=":
                stoi = str(stoi)
            else:
                if stoi < 0:
                    stoi = f"- {abs(stoi)}"
                else:
                    stoi = f"+ {stoi}"

            line += rf"{stoi} \cdot {{{rate}}} "

            line = line.replace(r"1 \cdot ", "")

        line = line[:-1]
        line += " \n"
        line += "```\n"

        inp += line

    inp += "\n"

    if overwrite_flag or not os.path.isfile(path_to_write):
        with open(path_to_write, "w") as f:
            f.write(f"------- Start on {datetime.now()} -------\n\n")
            f.write(inp)
    else:
        with open(path_to_write, "r") as f_tmp:
            read = f_tmp.read()
        flag_idxs = [m.start() for m in re.finditer("-------", read)]

        try:
            compare_block = read[flag_idxs[1] + 9 : flag_idxs[2]]
        except:  # noqa: E722
            compare_block = read[flag_idxs[1] + 9 :]

        if compare_block == inp:
            return
        else:
            with open(path_to_write, "r+") as f:
                f.seek(0, 0)
                f.write(f"------- Update on {datetime.now()} -------\n\n" + inp + read)
                print(f'Updated "{path_to_write.name}"')


for i in ["rates", "derived_comps", "derived_params"]:
    export_glossselect_from_model(
        m=Li2021(),
        write_path=Path(__file__).parent / f"{i}.txt",
        gloss_path=Path(__file__).parents[2] / f"{i}.csv",
    )

export_odes_as_latex(m=Li2021(), path_to_write=Path(__file__).parent / "model_odes.txt")
