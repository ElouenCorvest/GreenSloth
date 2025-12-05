import pandas as pd
from mxlpy import Model

def calc_co2_conc(pco2: float, H_cp_co2: float = 3.4e-4):
    """Calculate the CO2 concentration based on CO2 partial pressure and Henry's law constant.

    Args:
        pco2 (float): CO2 partial pressure [µbar].
        H_cp_co2 (float, optional): Henry's law constant for CO2 at 25°C [mM * Pa-1]. Defaults to 3.4e-4 (https://doi.org/10.5194/acp-23-10901-2023).

    Returns:
        float: CO2 concentration in mM.
    """
    # Unit conversions
    H_cp_co2 = H_cp_co2 * 1e5  # [mM * bar-1]
    H_cp_co2 = H_cp_co2 * 1e-6  # [mM * µbar-1]

    return H_cp_co2 * pco2

def mM_to_µmol_per_m2(conc_mM: float, corr_factor: float = 0.0112):
    """Convert mM concentration to µmol m-2.

    Args:
        conc_mM (float): Concentration in mM.
        corr_factor (float, optional): Correction factor. Defaults to 0.0112, which is the factor for the stroma (https://doi.org/10.1007/s11120-006-9109-1).

    Returns:
        float: Concentration in µmol m-2.
    """
    return conc_mM * 1e3 * corr_factor

def calc_pam_vals2(
    fluo_result: pd.Series, protocol: pd.DataFrame, pfd_str: str, sat_pulse: float = 2000, do_relative: bool = False
) -> tuple[pd.Series, pd.Series]:
    """Calculate PAM values from fluorescence data.

    Use the fluorescence data from a PAM protocol to calculate Fm, NPQ. To find the Fm values, the protocol used for simulation is seperated into ranges between each saturating pulse. Then the maximum fluorescence value within each range is taken as Fm. Thes are then used to calculate NPQ.

    Args:
        fluo_result (pd.Series): Fluorescence data as a pd.Series from mxlpy simulation.
        protocol (pd.DataFrame): PAM protocol used for simulation. Created using make_protocol from mxlpy.
        pfd_str (str): The name of the PPFD parameter in the protocol.
        sat_pulse (float, optional): The threshold for saturating pulse in the protocol. Defaults to 2000.

    Returns:
        tuple[pd.Series, pd.Series]: Fm and NPQ as pd.Series
    """    
    
    F = fluo_result.copy()
    F.name = "Fluorescence"
    
    peaks = protocol[protocol[pfd_str] >= sat_pulse].copy()
    peaks.index = peaks.index.total_seconds()
    peaks = peaks.reset_index()
    
    Fm = {
        "start": [],
        "end": [],
        "time": [],
        "value": []
    }

    for idx, (time, _) in peaks.iterrows():
        if idx == 0:
            start_time = 0
        else:
            start_time = time - (time - peaks["Timedelta"].iloc[idx - 1]) / 2
            
        if idx == len(peaks) - 1:
            end_time = fluo_result.index[-1]
        else:
            end_time = time + (peaks["Timedelta"].iloc[idx + 1] - time) / 2
            
        Fm["start"].append(start_time)
        Fm["end"].append(end_time)
        Fm_slice = fluo_result.loc[start_time:end_time]
        Fm["time"].append(Fm_slice.idxmax())
        Fm["value"].append(Fm_slice.max())
        
    Fm = pd.DataFrame(Fm).set_index("time")
    Fm = Fm["value"]
    Fm.name = "Flourescence Peaks (Fm)"
    
    if do_relative:
        F = F / Fm.iloc[0]
        Fm = Fm / Fm.iloc[0]
    
    # Calculate NPQ
    NPQ = (Fm.iloc[0] - Fm) / Fm if len(Fm) > 0 else pd.Series(dtype=float)
    NPQ.name = "Non-Photochemical Quenching (NPQ)"
    
    return F, Fm, NPQ

def create_pamprotocol_from_data(
    data: pd.DataFrame,
    par_column: str,
    pfd_str: str,
    time_sp: float,
    sp_pluse: float
):
    time_simed = 0
    fit_protocol = []
    
    for time in data.index:
        if time != 0:
            if data.loc[time, par_column] == 0:
                pfd_val = 40
            else:
                pfd_val = data.loc[time, par_column]
            fit_protocol.append((time - time_simed - time_sp, {pfd_str: pfd_val}))
        fit_protocol.append((time_sp, {pfd_str: sp_pluse}))
        time_simed = time
        
    return fit_protocol

def param_recursion(
    model: Model,
    search_str: str,
    dict_out: dict,
    order: int = 0,
    max_order: int = 5,
):
    """Recursion fucntion to find parameters influencing a given variable, reaction, derived variable or readout in a MxLpy model.

    Args:
        model (Model): mxlpy model to recursivle search for parameters.
        search_str (str): Entity to search for parameters influencing it. Needs to be in the model.
        dict_out (dict): Dictionary to store found parameters in. Should already exist when calling the function.
        order (int, optional): Number of recursion order. Defaults to 0.
        max_order (int, optional): Maximum recursion order. Defaults to 5.
    """    
    if order > max_order:
        return
    dict_key = f"Order {order}"
    if dict_out.get(dict_key) is None:
        dict_out[f"Order {order}"] = []
        
    type_of_id = model.ids[search_str]

    if type_of_id == "readout":
        to_fit = model._readouts[search_str]
    elif type_of_id == "variable":
        stoics = model.get_stoichiometries_of_variable(search_str)
        for reac in stoics.keys():
            param_recursion(model, reac, order=order+1, dict_out=dict_out, max_order=max_order)
        return
    elif type_of_id == "derived":
        to_fit = model._derived[search_str]
    elif type_of_id == "reaction":
        to_fit = model._reactions[search_str]

    for arg in to_fit.args:
        if arg not in model.ids:
            continue
        elif model.ids[arg] == "parameter":
            dict_out[f"Order {order}"].append(arg)
        else:
            param_recursion(model, arg, order=order+1, dict_out=dict_out, max_order=max_order)

def find_params_to_fit(
    to_fit_str: str,
    model: Model,
    max_order: int = 5,
):
    """Recursviely looks through provided model to find parameters influencing a given variable, reaction, derived variable or readout. It will print the parameters found at each order up to the given maximum order. The smaller the order the nearer the parameter is to the fitted entity.

    Args:
        to_fit_str (str): Name of variable, reaction, derived variable or readout to fit. It needs to be in the model.
        model (Model): The mxlpy model that should be anlyzed fro fitting.
        max_order (int, optional): The maximum order of parameters to find. Defaults to 5.
    """    
    dict_out = {}
    param_recursion(model, to_fit_str, order=1, dict_out=dict_out, max_order=max_order)

    print(f"Parameters influencing {to_fit_str}:")
    for key, lst_args in dict_out.items():
        if lst_args != []:
            prt_str = f"{key}: "
            prt_str += ", ".join(set(lst_args))
            print(prt_str)
            
    print()