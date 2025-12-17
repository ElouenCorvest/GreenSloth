from fitting import create_pamfit, plot_pamfit, create_pamprotocol_from_data
from utils import find_params_to_fit_byorder, find_params_to_fit_byelasticities
from mxlbricks import get_saadat2021, get_matuszynska2016npq
import mxlbricks.names as n
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from mxlpy import Simulator, plot, Model
from lmfit import Parameters

# find_params_to_fit_byelasticities(
#     to_fit_str=n.fluorescence(),
#     model=get_saadat2021(),
#     omit_strs=["pH", "T", "R", "F", "E^0_PQ", "E^0_QA", "HPR", "PSII_total", "LHC_tot"]
# )

# create_pamfit(
#     model=get_saadat2021(),
#     pfd_str=n.pfd(),
#     pam_params_to_fit=["kZSat","gamma1","gamma3","gamma0","gamma2"],
# )

fluo_data = pd.read_csv(Path(__file__).parent / "Data/fluo_col0_1.csv", index_col=0) # Taken from https://doi.org/10.1111/nph.18534
# Data taken with Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana plants.
# SP standard length = 720ms Maximal setting is standard (level 10) = 5000 µmol m-2 s-1 on IMAG-MAX/L TODO: Check if it is correct
fluo_data["F1"] = fluo_data["F1"] / fluo_data["Fm'1"].iloc[0]
fluo_data["Fm'1"] = fluo_data["Fm'1"] / fluo_data["Fm'1"].iloc[0]
fluo_data["NPQ3"] = (fluo_data["Fm'1"].iloc[0] - fluo_data["Fm'1"]) / fluo_data["Fm'1"]

sp_lenth = 720 / 1000  # seconds
sp_intensity = 5000  # µmol m-2 s-1

#Convert index to time in seconds
fluo_data.index = pd.to_timedelta(fluo_data.index)
fluo_data.index = fluo_data.index - fluo_data.index[0]
fluo_data.index = fluo_data.index.total_seconds()

# Create Pam Protocol
fit_protocol = create_pamprotocol_from_data(
    data=fluo_data,
    par_column="PAR",
    pfd_str=n.pfd(),
    time_sp=sp_lenth, #720ms SP to seconds
    sp_pluse=sp_intensity # 5000 µmol m-2 s-1 on IMAG-MAX/L
)

params = Parameters()
pam_params_to_fit = {
    "gamma0": 0.00777777,
    "gamma1": 0.00346832,
    "gamma2": 26.2661944,
    "kZSat": 1.97053946,
    "gamma3": 1.1521e-07,
}
# pam_params_to_fit = {"kZSat": 0.4902177498998883, "gamma1": 0.3428963092714419, "gamma3": 1.112694825167182e-09, "gamma0": 0.021932229994591657, "gamma2": 8.170009234404276}
# pam_params_to_fit = {"kZSat": 0.8222023294152467, "gamma1": 0.014586573364833155, "gamma3": 0.010465445391434569, "gamma0": 0.000690274445878547, "gamma2": 12.28245278745518} # Correct fit
for param, val in pam_params_to_fit.items():
    params.add(param, value=val, vary=True, min=0)
    #max=val*1.5, min=val*0.5


fig, axs = plot_pamfit(
    model=get_saadat2021(),
    new_params=params,
    pfd_str=n.pfd(),
    fit_protocol=fit_protocol,
    fluo_data=fluo_data,
    sp_lenth=sp_lenth,
)

plt.show()