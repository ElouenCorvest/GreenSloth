from mxlpy import Model, Simulator, make_protocol
from utils import calc_pam_vals2, create_pamprotocol_from_data, pam_sim
from lmfit import minimize, Parameters
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import copy
import numpy as np
from model_validation import save_matplotlib_figure

def pamfit_func_lstsq(
    params,
    model: Model,
    fit_data: pd.DataFrame,
    pfd_str: str,
    debug: bool = False,
):
    # Create Pam Protocol
    fit_protocol = create_pamprotocol_from_data(
        data=fit_data,
        par_column="PAR",
        pfd_str=pfd_str,
        time_sp=720/1000,
        sp_pluse=5000
    )
    
    model_new = copy.deepcopy(model)
    model_new.update_parameters(params.valuesdict())
    
    res = pam_sim(
        fit_protocol=fit_protocol,
        model=model_new,
        pfd_str=pfd_str,
    )
    
    if res is None:
        print("No result from simulation")
        return np.ones(len(fit_data)) * 1e6
    
    res = res.get_variables()
    F, Fm, NPQ = calc_pam_vals2(res["Fluo"], protocol=make_protocol(fit_protocol), pfd_str=pfd_str, do_relative=False)
    
    # TODO: Standardize difference to account for different scales inform
    mean = fit_data["NPQ3"].mean()
    std = fit_data["NPQ3"].std()
    diff = (NPQ.values - mean) / std - (fit_data["NPQ3"].values - mean) / std
    # diff = NPQ.values - fit_data["NPQ3"].values

    return diff

def create_pamfit(
    model: Model,
    pfd_str: str,
    pam_params_to_fit: list[str]
):
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
    
    initial_params = Parameters()
    for param in pam_params_to_fit:
        val = model.get_raw_parameters()[param].value
        initial_params.add(param, value=val, vary=True, min=0)
        #max=val*1.5, min=val*0.5
    
    params = initial_params
    for _ in range(1):
        out = minimize(
            fcn=pamfit_func_lstsq,
            params=params,
            args=(model, fluo_data, pfd_str, True),
            method="leastsq",
        )
    
        if out.success:
            print("Optimization successful")
            print(out.params)
            
        params = out.params
        
    fitted_model = copy.deepcopy(model)
    fitted_model.update_parameters(out.params.valuesdict())
    
    # Create Pam Protocol
    fit_protocol = create_pamprotocol_from_data(
        data=fluo_data,
        par_column="PAR",
        pfd_str=pfd_str,
        time_sp=sp_lenth, #720ms SP to seconds
        sp_pluse=sp_intensity # 5000 µmol m-2 s-1 on IMAG-MAX/L
    )
    
    fig, axs = plot_pamfit(
        model=model,
        new_params=out.params,
        pfd_str=pfd_str,
        fit_protocol=fit_protocol,
        fluo_data=fluo_data,
        sp_lenth=sp_lenth,
    )
    
    name = "fitAbs_StandardScale"
    
    plt.savefig(Path(__file__).parent / "test2" / f"{name}.png", dpi=300)
    
    with open(Path(__file__).parent / "test2" / f"{name}_params.csv", "w") as f:
        df_params = pd.DataFrame.from_dict({param: [out.params[param].value] for param in out.params})
        df_params.to_csv(f, index=False)
    
    return out.params
    
def plot_pamfit(
    model: Model,
    new_params: Parameters,
    pfd_str: str,
    fit_protocol: list[tuple[float, dict]],
    fluo_data: pd.DataFrame,
    sp_lenth: float,
):
    fitted_model = copy.deepcopy(model)
    fitted_model.update_parameters(new_params.valuesdict())
    
    res = pam_sim(
        fit_protocol=fit_protocol,
        model=fitted_model,
        pfd_str=pfd_str,
    )
    res = res.get_variables()
    F, Fm, NPQ = calc_pam_vals2(res["Fluo"], protocol=make_protocol(fit_protocol), pfd_str=pfd_str, do_relative=True)
    
    data_color = "#84569F"
    fitted_color = "#C9E3A0"
    og_color = "#72C0B7"
    
    fig, axs = plt.subplot_mosaic([["Fluo", "NPQ"], ["Diff", "Diff"]], figsize=(10, 5))
        
    #Fitted Data
    axs["Fluo"].plot(F, label="Fitted Fluo", color=fitted_color)
    axs["Fluo"].plot(Fm, label="Fitted Fm", lw=0, marker="^", color=fitted_color)
    axs["NPQ"].plot(NPQ, label="Fitted NPQ", lw=1, marker="+", color=fitted_color)
    
    # Experimental Data
    axs["Fluo"].plot(fluo_data.index, fluo_data["F1"], label="Measured Fluo", lw=0, marker="o", color=data_color)
    axs["Fluo"].plot(fluo_data.index + sp_lenth, fluo_data["Fm'1"], label="Measured Fm'", lw=0, marker="x", color=data_color)
    axs["NPQ"].plot(fluo_data["NPQ3"], label="Measured NPQ", lw=1, marker="s", color=data_color)
    
    # OG model version
    res_old = pam_sim(
        fit_protocol=fit_protocol,
        model=model,
        pfd_str=pfd_str,
    )
    
    res_old = res_old.get_variables()
    F_old, Fm_old, NPQ_old = calc_pam_vals2(res_old["Fluo"], protocol=make_protocol(fit_protocol), pfd_str=pfd_str, do_relative=True)
    
    axs["Diff"].plot(fluo_data.index, NPQ / fluo_data["NPQ3"].values, label="Fitted / Measured", lw=1, marker="o", color=fitted_color)
    axs["Diff"].plot(fluo_data.index, NPQ_old / fluo_data["NPQ3"].values, label="OG Model / Measured", lw=1, marker="x", color=og_color)
    
    axs["Diff"].set_ylim(-0.1, 2.1)
    axs["Diff"].axhline(1, color=data_color, ls="--", alpha=0.5)
    axs["Diff"].set_ylabel("Ratio of Model to Measured NPQ")
    
    axs["Fluo"].legend(loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1))
    axs["NPQ"].legend()
    axs["Diff"].legend()
    
    return fig, axs