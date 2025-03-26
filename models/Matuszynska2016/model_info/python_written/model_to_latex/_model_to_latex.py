from pathlib import Path
import os
import sys
import inspect
from greensloth_utils import export_glossselect_from_model, export_odes_as_latex

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, os.path.dirname(parentdir))

from model import Matuszynska2016  # noqa: E402


for i in ["rates", "derived_comps", "derived_params"]:
    export_glossselect_from_model(
        m=Matuszynska2016(),
        write_path=Path(__file__).parent / f"{i}.txt",
        gloss_path=Path(__file__).parents[2] / f"{i}.csv",
    )

export_odes_as_latex(
    m=Matuszynska2016(), path_to_write=Path(__file__).parent / "model_odes.txt"
)
