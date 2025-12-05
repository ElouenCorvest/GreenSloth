from fitting import create_pamfit
from utils import find_params_to_fit
from mxlbricks import get_saadat2021, get_matuszynska2016npq
import mxlbricks.names as n
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from mxlpy import Simulator, plot, Model

find_params_to_fit(
    to_fit_str=n.fluorescence(),
    model=get_matuszynska2016npq(),
)

create_pamfit(
    model=get_matuszynska2016npq(),
    pfd_str=n.pfd(),
    pam_params_to_fit=["gamma0"]
)

# fluo_data = pd.read_csv(Path(__file__).parent / "Data/fluo_col0_1.csv", index_col=0) # Taken from https://doi.org/10.1111/nph.18534
#     # Data taken with Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana plants.
#     # SP standard length = 720ms Maximal setting is standard (level 10) = 5000 µmol m-2 s-1 on IMAG-MAX/L TODO: Check if it is correct
    
# #Convert index to time in seconds
# fluo_data.index = pd.to_timedelta(fluo_data.index)
# fluo_data.index = fluo_data.index - fluo_data.index[0]
# fluo_data.index = fluo_data.index.total_seconds()

# fit_protocol = create_pamprotocol_from_data(
#         data=fluo_data,
#         par_column="PAR",
#         pfd_str=n.pfd(),
#         time_sp=720 / 1000, #720ms SP to seconds
#         sp_pluse=5000 # 5000 µmol m-2 s-1 on IMAG-MAX/L
#     )


# from mxlpy import mc
# from mxlpy.distributions import sample, Normal
# import numpy as np

# s = Simulator(model=get_saadat2021())
    
# s.update_parameter(n.pfd(), 40)
# s.simulate(60*30)

# dark_y0 = s.get_result().get_new_y0()

# def custom_worker(
#     model: Model,
#     protocol: pd.DataFrame,
#     *,
#     integrator,
#     y0: dict[str, float] | None,
#     time_points_per_step: int = 10,
# ):
#     s = Simulator(model=model, integrator=integrator, y0=y0)
    
#     res = None
    
#     while res is None and time_points_per_step < 1e5:
#         time_points_per_step += 1000
#         s.simulate_protocol(protocol, time_points_per_step=time_points_per_step)
#         res = s.get_result()

# tc = mc.time_course_over_protocol(
#     model=get_saadat2021(),
#     protocol=make_protocol(fit_protocol),
#     mc_to_scan=sample(
#         {
#             "gamma0": Normal(loc=0.10146955087696075, scale=0.597),
#             "gamma1": Normal(loc=1.2866655600529882, scale=22.6),
#             "gamma2": Normal(loc=6.334425460216103, scale=28),
#             "gamma3": Normal(loc=0.0011083456377316558, scale=0.0321),
#             "kZSat": Normal(loc=0.09986347119784678, scale=2.14),
#         }, n=10
#     ),
#     y0=dark_y0,
# )

# print(tc.variables["Fluo"].unstack().T)

# unstacked_fluo = tc.variables["Fluo"].unstack().T

# NPQ_df = None

# for column in unstacked_fluo.columns:
#     if unstacked_fluo[column].isna().all():
#         continue
    
#     F, Fm, NPQ = calc_pam_vals2(fluo_result=unstacked_fluo[column], protocol=make_protocol(fit_protocol), pfd_str=n.pfd(), sat_pulse=5000)
    
#     if NPQ.isna().all():
#         continue
#     elif NPQ_df is None:
#         NPQ.name = 0
#         NPQ_df = pd.DataFrame(NPQ)
#     else:
#         NPQ_df.insert(0, len(NPQ_df.columns), NPQ)
        
# fig, ax = plt.subplots()

# ax.plot(NPQ_df.mean(axis=1), label="Mean NPQ")
# ax.fill_between(
#         NPQ_df.index,
#         NPQ_df.mean(axis=1) - NPQ_df.std(axis=1),
#         NPQ_df.mean(axis=1) + NPQ_df.std(axis=1),
#         alpha=0.3,
#     )

# plt.show()
