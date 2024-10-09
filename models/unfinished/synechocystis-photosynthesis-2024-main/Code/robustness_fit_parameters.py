#!/usr/bin/python3
# %%

import pandas as pd
import numpy as np
import sys
from tqdm.auto import tqdm
import pebble
import pickle
from datetime import datetime
from functools import partial
import warnings
from scipy.optimize import minimize, NonlinearConstraint
from concurrent import futures
from pathlib import Path
import logging
import traceback
import time
from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText
from getpass import getpass

sys.path.append("../Code")

# Import model functions
from get_current_model import get_model
from function_residuals import calculate_residuals, setup_logger

# Import the email notifyer
from SMTPMailSender import SMTPMailSender


# %%
# Set the maximum number of parallel threads and the timeout
# n_workers = 4 # Maximum number of parallel threads
# timeout = 300 # Timeout for each thread in seconds
timeout_s = (2 * 24 * 60 * 60) # Timeout for minimisation in seconds, default 172800 (two days)

# Set the prefix to be used for logging and results files
file_prefix = f"minimise_{datetime.now().strftime('%Y%m%d%H%M')}"
# file_prefix = f"residuals_test"

# Setup the email sender
# email = SMTPMailSender(
#     SMTPserver='mail.gmx.net',
#     username='tobiaspfennig@gmx.de',
#     default_destination='tobiaspfennig@gmx.de'
# )

# %%
# Load the model to get default parameter values
m = get_model(get_y0=False, verbose=False, check_consistency=False)

# %%
def get_fitting_startvalue(fitting_parameter, m):
    if fitting_parameter == "fluo_influence":
        return pd.Series({f"__fluo_influence__{k}":v for k,v in m.parameters[fitting_parameter].items()})
    else:
        return pd.Series({fitting_parameter: m.parameters[fitting_parameter]})
    
def get_fitting_bounds(fitting_parameter, bound, m):
    if fitting_parameter == "fluo_influence":
        return pd.Series({f"__fluo_influence__{k}":bound for k in m.parameters[fitting_parameter].keys()})
    else:
        return pd.Series({fitting_parameter: bound})
    
def get_fitting_start_and_bounds(fitting_parameters,m):
    start_values = [get_fitting_startvalue(x,m) for x in fitting_parameters]
    bounds = [get_fitting_bounds(k,v,m) for k,v in fitting_parameters.items()]
    return pd.concat(start_values), pd.concat(bounds).values

def get_fitting_parameter_dict(values, names):
    # Put values into a pandas series for easier handling
    res = pd.Series(values, index=names)

    # Reconstitute fluo_influence
    fluo_influence_bool = res.index.str.startswith("__fluo_influence__")
    if fluo_influence_bool.any():
        # Extract the intermediate values
        _res = res[fluo_influence_bool]
        _res.index = _res.index.str.removeprefix("__fluo_influence__")
        
        res = res[np.invert(fluo_influence_bool)]
        res["fluo_influence"] = _res.to_dict()

    return res.to_dict()

# %%

# fitting_parameter_bounds = {
#     "fluo_influence": (1e-10,None),
#     "lcf": (1e-10,None),
#     "kUnquench": (1e-10,None),
#     "KMUnquench": (1e-10,None),
#     "kQuench": (1e-10,None),
#     "kOCPactivation": (1e-10,None),
#     "kOCPdeactivation": (1e-10,None),
#     "OCPmax": (1e-10,None),
# }

fitting_parameter_bounds = {
    # "PSIItot": (1e-10, None),
    # "PSItot": (1e-10, None),
    # "Q_tot": (1e-10, None),
    # "PC_tot": (1e-10, None),
    # "Fd_tot": (1e-10, None),
    # "NADP_tot": (1e-10, None),
    # "NAD_tot": (1e-10, None),
    # "AP_tot": (1e-10, None),
    # "O2ext": (1e-10, None),
    # "bHi": (1e-10, None),
    # "bHo": (1e-10, None),
    # "cf_lumen": (1e-10, None),
    # "cf_cytoplasm": (1e-10, None),
    "fCin": (1e-10, None),
    # "kH0": (1e-10, None),
    # "kHst": (1e-10, None),
    # "kF": (1e-10, None),
    # "k2": (1e-10, None),
    # "kPQred": (1e-10, None),
    # "kPCox": (1e-10, None),
    # "kFdred": (1e-10, None),
    "k_F1": (1e-10, None),
    # "k_ox1": (1e-10, None),
    "k_Q": (1e-10, None),
    # "k_NDH": (1e-10, None),
    # "k_SDH": (1e-10, None),
    # "k_FN_fwd": (1e-10, None),
    # "k_FN_rev": (1e-10, None),
    "k_pass": (1e-10, None),
    "k_aa": (1e-10, None),
    # "kRespiration": (1e-10, None),
    # "kO2out": (1e-10, None),
    # "kCCM": (1e-10, None),
    "fluo_influence": (1e-10, None),
    # "PBS_free": (1e-10, None),
    # "PBS_PS1": (1e-10, None),
    # "PBS_PS2": (1e-10, None),
    "lcf": (1e-10, None),
    "KMPGA": (1e-10, None),
    "kATPsynth": (1e-10, None),
    # "Pi_mol": (1e-10, None),
    # "HPR": (1e-10, None),
    "kATPconsumption": (1e-10, None),
    "kNADHconsumption": (1e-10, None),
    # "vOxy_max": (1e-10, None),
    # "KMATP": (1e-10, None),
    # "KMNADPH": (1e-10, None),
    # "KMCO2": (1e-10, None),
    # "KIO2": (1e-10, None),
    # "KMO2": (1e-10, None),
    # "KICO2": (1e-10, None),
    # "vCBB_max": (1e-10, None),
    # "kPR": (1e-10, None),
    "kUnquench": (1e-10, None),
    "KMUnquench": (1e-10, None),
    "kQuench": (1e-10, None),
    "KHillFdred": (1e-10, None),
    "nHillFdred": (1e-10, None),
    # "k_O2": (1e-10, None),
    # "cChl": (1e-10, None),
    # "CO2ext_pp": (1e-10, None),
    # "S": (1e-10, None),
    "kCBBactivation": (1e-10, None),
    "KMFdred": (1e-10, None),
    "kOCPactivation": (1e-10, None),
    "kOCPdeactivation": (1e-10, None),
    "OCPmax": (1e-10, None),
    "vNQ_max": (1e-10, None),
    "KMNQ_Qox": (1e-10, None),
    "KMNQ_Fdred": (1e-10, None),
}

start_values, bounds = get_fitting_start_and_bounds(fitting_parameter_bounds,m)

p, p_names = start_values.values, start_values.index

## CONSTRAINT
# Define a constraint function that evaluates if all residuals are improved
_, default_residuals = calculate_residuals(
        {},
        n_workers=5,
        timeout=300, # s
        logger_filename=f"../out/{file_prefix}",
        # intermediate_results_file=f"../out/{file_prefix}_intermediate.csv",
        save_intermediates=False,
        return_all=True
        )

# Test if all residuals are at max 1% worse than the default residuals
def constraint_fun(residuals, default_residuals=default_residuals, tolerance=0.01):
    return (((default_residuals * (1 + tolerance)) - residuals).dropna() >0 ).all()


## CALLBACK
# Define  callback function that terminates the minimisation after a set time
start_time = time.time()
def callback(p, intermediate_result=None, start_time=start_time, timeout_s=timeout_s):
    if int(time.time() - start_time) > timeout_s:
        raise StopIteration


# %%
# Function to calculate residuals with arguments tailored to the minimize function
def calculate_residuals_minimize(p, p_names, scale_factors=None, file_prefix="", use_constraint=True, constraint_penalty=10):
    # Undo the scaling
    if scale_factors is not None:
        p = p * scale_factors

    _p = get_fitting_parameter_dict(p, p_names)

    res, res_list = calculate_residuals(
        _p,
        n_workers=5,
        timeout=300, # s
        logger_filename=f"../out/{file_prefix}",
        save_intermediates=False,
        return_all=True
        )
    
    if use_constraint:
        # Apply the constraint by adding a penalty term if it isn't fulfilled
        constraint = constraint_fun(
            residuals=res_list,
            tolerance=0.01
        )

        if not constraint:
            res += constraint_penalty

    # Save the residuals
    with open(Path(f"../out/{file_prefix}_intermediates.csv",), "a") as f:
        f.writelines(f"{','.join([str(x) for x in p])},{res},{','.join(list(res_list.values.astype(str)))}\n")

    return res

def scale_bounds(bounds, x0, scale):
    # Scale the vector of bounds according to the scaling of the parameters
    return [tuple([b*(scale/_x0) if b not in [0,None] else b for b in bound]) for bound, _x0 in zip(bounds, x0)]

def fit_model_parameters(start_values, bounds=None, opt_kwargs={}, scale_to_value=None, file_prefix=""):
    
    # If the parameters should be scaled, replace them with the scaling value
    if scale_to_value is None:
        p = start_values.values
        scale_factors = None
    else:
        p = np.full(start_values.shape[0], scale_to_value)
        scale_factors = start_values.values / scale_to_value
        bounds = scale_bounds(bounds, start_values.values, scale_to_value)

    if bounds is not None:
        opt_kwargs.update({"bounds": bounds})

    fit = minimize(
        fun = calculate_residuals_minimize,
        x0 = p,
        args = (start_values.index, scale_factors, file_prefix),
        **opt_kwargs
    )

    # Rescale the results
    if scale_to_value is not None:
        fit.x = fit.x * scale_factors
    return fit

minimiser_options = {
    "Nelder-Mead": {
        "method":"Nelder-Mead",
        "callback": callback,
    },
    "trust-constr": {
        "method": "trust-constr",
        # "constraints":constraint,
        "callback": callback,
        "options":{
            "maxiter": 5000,
        }
    }
}

if __name__ == "__main__":
    # Setup logging
    InfoLogger = setup_logger("InfoLogger", Path(f"../out/{file_prefix}_info.log"), level=logging.INFO)
    ErrorLogger = setup_logger("ErrorLogger", Path(f"../out/{file_prefix}_err.log"), level=logging.ERROR)
    
    # Log the start of the minimising
    InfoLogger.info("Started run")
    # %%
    email.send_email(
            body=f"Minimisation run {file_prefix} was successfully started",
            subject="Minimisation started"
        )

    # Locally optimise the model
    try:
        with warnings.catch_warnings() as w:
            # Cause all warnings to always be triggered.
            # warnings.simplefilter("ignore", category=RuntimeWarning)
            warnings.simplefilter("ignore")
            fit = fit_model_parameters(
                start_values, 
                bounds=bounds, 
                scale_to_value=0.01, 
                file_prefix=file_prefix,
                opt_kwargs=minimiser_options["Nelder-Mead"]
                )
            
            # Save the results
            with open(Path(f"../Results/{file_prefix}_results.pickle",), "wb") as f:
                pickle.dump(fit, f)
            
            InfoLogger.info(f"Finished run: {fit.message}")

            email.send_email(
                body=f"Minimisation run {file_prefix} finished successfully:\n{fit.message}", 
                subject="Minimisation successful"
            )
    except StopIteration:
        pass
    except Exception as e:
        ErrorLogger.error("Error encountered\n" + str(traceback.format_exc()))
        InfoLogger.info("Finished run with Error")

        email.send_email(
            f"Minimisation run {file_prefix} encountered an Error:\n{e}", 
            "Minimisation Error"
        )

    # with open(Path(f"../Results/{file_prefix}_results.pickle",), "rb") as f:
    #     test = pickle.load(f)
    del email