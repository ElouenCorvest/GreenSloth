from fitting import create_pamfit
from utils import find_params_to_fit_byorder, find_params_to_fit_byelasticities
from mxlbricks import get_saadat2021, get_matuszynska2016npq
import mxlbricks.names as n
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from mxlpy import Simulator, plot, Model

# find_params_to_fit_byelasticities(
#     to_fit_str=n.fluorescence(),
#     model=get_saadat2021(),
#     omit_strs=["pH", "T", "R", "F", "E^0_PQ", "E^0_QA", "HPR", "PSII_total", "LHC_tot"]
# )

create_pamfit(
    model=get_saadat2021(),
    pfd_str=n.pfd(),
    pam_params_to_fit=["kZSat","gamma1","gamma3","gamma0","gamma2"],
)
