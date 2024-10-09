# %%
#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
from tqdm.auto import tqdm
import pebble
import pickle
from functools import partial
import warnings
import logging
import traceback

from datetime import datetime
from concurrent import futures
from pathlib import Path

sys.path.append("../Code")

# Import model functions
from function_residuals import calculate_residuals, setup_logger, residual_relative_weights
from get_current_model import get_model

# Import the email notifyer
from SMTPMailSender import SMTPMailSender

# %%
# Set the number of evaluated samples
n_mutations = 10000
include_default_model = True

# Set the maximum number of parallel threads and the timeout
n_workers = 100 # Maximum number of parallel threads
timeout = 600 # Timeout for each thread in seconds

# Set the prefix to be used for logging and results files
file_prefix = f"montecarlo_allpars_{datetime.now().strftime('%Y%m%d%H%M')}"
# file_prefix = f"residuals_test"

# Set the random number generator
rng = np.random.default_rng(2024)

# Setup the email sender
email = SMTPMailSender(
    SMTPserver='mail.gmx.net',
    username='tobiaspfennig@gmx.de',
    default_destination='tobiaspfennig@gmx.de'
)

# %%
parameter_ranges = {
    "PSIItot": (0.5, 2),
    "PSItot": (0.5, 2),
    "Q_tot": (0.5, 2),
    "PC_tot": (0.5, 2),
    "Fd_tot": (0.5, 2),
    "NADP_tot": (0.5, 2),
    "NAD_tot": (0.5, 2),
    "AP_tot": (0.5, 2),
    "O2ext": (0.5, 2),
    "bHi": (0.5, 2),
    "bHo": (0.5, 2),
    "cf_lumen": (0.5, 2),
    "cf_cytoplasm": (0.5, 2),
    "fCin": (0.5, 2),  # manually fitted
    "kH0": (0.5, 2),
    "kHst": (0.5, 2),
    "kF": (0.5, 2),
    "k2": (0.5, 2),
    "kPQred": (0.5, 2),
    "kPCox": (0.5, 2),
    "kFdred": (0.5, 2),
    "k_F1": (0.5, 2),  # manually fitted
    "k_ox1": (0.5, 2),
    "k_Q": (0.5, 2),  # manually fitted
    "k_NDH": (0.5, 2),
    "k_SDH": (0.5, 2),
    "k_FN_fwd": (0.5, 2),
    "k_FN_rev": (0.5, 2),
    "k_pass": (0.5, 2),  # manually fitted
    "k_aa": (0.5, 2),  # manually fitted
    "kRespiration": (0.5, 2),
    "kO2out": (0.5, 2),
    "kCCM": (0.5, 2),
    "fluo_influence": (0.5, 2),  # manually fitted
    "PBS_free": (0.5, 2),
    "PBS_PS1": (0.5, 2),
    "PBS_PS2": (0.5, 2),
    "lcf": (0.5, 2),  # manually fitted
    "KMPGA": (0.5, 2),  # manually fitted
    "kATPsynth": (0.5, 2),  # manually fitted
    "Pi_mol": (0.5, 2),
    "HPR": (0.5, 2),
    "kATPconsumption": (0.5, 2),  # manually fitted
    "kNADHconsumption": (0.5, 2),  # manually fitted
    "vOxy_max": (0.5, 2),
    "KMATP": (0.5, 2),
    "KMNADPH": (0.5, 2),
    "KMCO2": (0.5, 2),
    "KIO2": (0.5, 2),
    "KMO2": (0.5, 2),
    "KICO2": (0.5, 2),
    "vCBB_max": (0.5, 2),
    "kPR": (0.5, 2),
    "kUnquench": (0.5, 2),  # manually fitted
    "KMUnquench": (0.5, 2),  # manually fitted
    "kQuench": (0.5, 2),  # manually fitted
    "KHillFdred": (0.5, 2),  # manually fitted
    "nHillFdred": (0.5, 2),  # manually fitted
    "k_O2": (0.5, 2),
    "cChl": (0.5, 2),
    "CO2ext_pp": (0.5, 2),
    "S": (0.5, 2),
    "kCBBactivation": (0.5, 2),  # manually fitted
    "KMFdred": (0.5, 2),  # manually fitted
    "kOCPactivation": (0.5, 2),  # manually fitted
    "kOCPdeactivation": (0.5, 2),  # manually fitted
    "OCPmax": (0.5, 2),  # manually fitted
    "vNQ_max": (0.5, 2),  # manually fitted
    "KMNQ_Qox": (0.5, 2),  # manually fitted
    "KMNQ_Fdred": (0.5, 2),  # manually fitted
}

# %%
# Load the model to get default parameter values
m = get_model(get_y0=False, verbose=False, check_consistency=False)

# %%
# Define a function to generate a number of random log-spaced factors to be used with the parameters
def get_mutation_factors(n, start, end, rng):
    rand = rng.random(n)
    return np.exp(np.log(start) + rand*(np.log(end)-np.log(start)))

def get_parameter_mutations(n, parameter_ranges, rng, m=m):
    # Create a container for the mutations
    res = pd.DataFrame(index=np.arange(n), columns=parameter_ranges.keys(), dtype=object)

    for k,v in parameter_ranges.items():
        if k=="fluo_influence":
            _res = {l:m.parameters[k][l] * get_mutation_factors(n, *v, rng=rng) for l in m.parameters[k]}
            res[k] = pd.DataFrame(_res).T.to_dict()
        else:
            # Mutate the default parameter value with the random factors
            res[k] = m.parameters[k] * get_mutation_factors(n, *v, rng=rng)
    return res

# %%
# Define a function to be executed by each thread
def thread_function(x, **kwargs):
    # Unpack the input index and parameter values
    index, p = x

    try:
        # Execute the actual function
        result = calculate_residuals(parameter_update=p, thread_index=index, **kwargs)

        return index, result

        # Handle the result if needed
    except Exception as e:
        warnings.warn(f"An error occurred in thread {index} with parameter {p}: {e}")

# %%
# Create the parameters
params = get_parameter_mutations(n_mutations+include_default_model, parameter_ranges, rng, m)

# Include the default model in first position
if include_default_model:
    params.loc[0] = pd.Series({k: m.parameters[k] for k in params.columns})

# Save the parameters
params.to_csv(f"../Results/{file_prefix}_params.csv")

# %%
# Create the parameters
params = get_parameter_mutations(n_mutations+include_default_model, parameter_ranges, rng, m)

# Include the default model in first position
if include_default_model:
    params.loc[0] = pd.Series({k: m.parameters[k] for k in params.columns})

# Initialise container for residuals
results = pd.DataFrame(index=np.arange(n_mutations+include_default_model), columns=(residual_relative_weights.keys()), dtype=float)

if __name__ == "__main__":
    # Setup logging
    InfoLogger = InfoLogger = setup_logger("InfoLogger", Path(f"../out/{file_prefix}_info.log"), level=logging.INFO)
    ErrorLogger = setup_logger("ErrorLogger", Path(f"../out/{file_prefix}_err.log"), level=logging.ERROR)

    # Log the start of the run
    InfoLogger.info("Started run")

    email.send_email(
        body=f"Monte Carlo run {file_prefix} was successfully started",
        subject=f"Monte Carlo run started"
    )

    # Catch unnecessary warnings:
    with warnings.catch_warnings() as w:
        # Cause all warnings to always be triggered.
        # warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore")
        
        try:
            # Execute the thread_function for each parameter input
            with tqdm(total=n_mutations+include_default_model, disable=True) as pbar:
                with pebble.ProcessPool(max_workers=n_workers) as pool:
                    future = pool.map(
                        partial(
                            thread_function,
                            intermediate_results_file=f"../out/{file_prefix}_intermediate.csv",
                            logger_filename=f"../out/{file_prefix}",
                            return_all=True
                        ),
                        params.iterrows(),
                        timeout=timeout,
                    )
                    it = future.result()
                    
                    while True:
                        try:
                            index, res = next(it)
                            pbar.update(1)
                            results.loc[index,:] = res[1]
                        except futures.TimeoutError:
                            pbar.update(1)
                        except StopIteration:
                            break
                        except Exception as e:
                            pbar.update(1)
                            ErrorLogger.error("Error encountered in residuals\n" + str(traceback.format_exc()))
                        finally:
                            pbar.update(1)

            # Save the results
            results.to_csv(f"../Results/{file_prefix}_results.csv")

            # Classify the results into successes and failures for logging
            mcres_outcomes = pd.DataFrame(index=results.index, columns=["success", "failed", "time-out"])
            mcres_outcomes["timeout"] = np.isnan(results).any(axis=1)
            mcres_outcomes["failed"] = np.isinf(results).any(axis=1)
            mcres_outcomes["success"] = mcres_succ = np.invert(np.logical_or(mcres_outcomes["timeout"], mcres_outcomes["failed"]))

            InfoLogger.info(f"Finished run successfully. Success: {mcres_outcomes['success'].sum()}, Failed: {mcres_outcomes['failed'].sum()}, Timeout: {mcres_outcomes['timeout'].sum()}")

            email.send_email(
                body=f"Monte Carlo run {file_prefix} finished successfully. Success: {mcres_outcomes['success'].sum()}, Failed: {mcres_outcomes['failed'].sum()}, Timeout: {mcres_outcomes['timeout'].sum()}",
                subject=f"Monte Carlo run successful"
            )
        
        except Exception as e:
            ErrorLogger.error("Error encountered in Monte Carlo function\n" + str(traceback.format_exc()))
            InfoLogger.info("Finished run with Error")
            
            email.send_email(
                body=f"Monte Carlo run {file_prefix} encountered an Error:\n{e}",
                subject=f"Monte Carlo run Error"
            )
