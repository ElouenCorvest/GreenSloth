
import sys
from collections.abc import Iterable
from concurrent import futures
from functools import partial

import pandas as pd
from modelbase2 import Model, Simulator, mca
from scipy.interpolate import interp1d
from tqdm import tqdm
import numpy as np
from bisect import bisect_left


def simulate_to_steady_state_variable_param(
    param_val: float,
    param_str: str,
    m: Model,
    rel_norm: bool = False,
    tolerance: float = 1e-12
) -> dict[str, float]:
    """
    Function to simulate to steady-state, with the option to update a parameter

    Args:
        m (Model): Model to simulate
        param_str (str): Parameter to be changed (Has to be in m.update_parameter())
        param_val (float): Value to change parameter to
        y0 (dict[str, float]): Initial conditions of compounds
        atol (float, optional): Absolute tolerance of Simulator. Defaults to 1e-12.
        rtol (float, optional): Relative tolerance of Simulator. Defaults to 1e-12.

    Returns:
        pd.Dataframe: Full Results of simulation
    """
    # s = Simulator(m)

    # s.update_parameter(param_str, param_val)
    # s.simulate_to_steady_state(tolerance = 1e-12, rel_norm = True)
    # res = s.get_full_concs()
    # if res is None:
    #     _ = dict()
    #     for i in m.get_variable_names():
    #         _[i] = None
    #     for i in m.get_derived_variable_names():
    #         _[i] = None
    #     return _
    # else:
    #     return res.iloc[-1].to_dict()
    
    s = Simulator(m)
    s.update_parameter(param_str, param_val)
    res = None
    for t_end in np.geomspace(10, 1e9, 5):
        s.simulate(t_end)
        y = s.get_concs()
        if y is None:
            continue
        diff = (y.iloc[-1] - y.iloc[-2]) / y.iloc[-1] if rel_norm else y.iloc[-1] - y.iloc[-2]
        if np.linalg.norm(diff, ord=2) < tolerance:
            res =  y.iloc[-1].to_dict()
            break
        
    if res is None:
        _ = dict()
        for i in m.get_variable_names():
            _[i] = None
            
        return _
    else:
        return res

            

def iterable_steady_scan_params(
    m: Model,
    param_str: str,
    param_vals: Iterable[float],
    rel_norm: bool = False,
    tolerance: float = 1e-8
) -> pd.DataFrame:
    """
    Steady-state scan of given model with ONE variable parameter

    Args:
        m (Model): Defined model to scan through
        y0 (dict[str, float]): Initial conditions for variables in m
        param_str (str): Name of parameter to be changed
        param_vals (Iterable[float]): Values to change specific parameter to
        atol (float, optional): Absolute tolerance of Simulator. Defaults to 1e-12.
        rtol (float, optional): Relative tolerance of Simulator. Defaults to 1e-12.

    Returns:
        pd.DataFrame: DataFrame with variable param (param_str) as index and each variable as seperate column
    """    

    fn = partial(simulate_to_steady_state_variable_param,
        m = m,
        param_str = param_str,
        rel_norm = rel_norm,
        tolerance = tolerance
    )

    if sys.platform in ["win32", "cygwin"]:
        return pd.DataFrame(tqdm(map(fn, param_vals), desc = "Steady-State Scan", total = len(param_vals)), index=param_vals)  # type: ignore
    else:
        with futures.ProcessPoolExecutor() as ex:
            return pd.DataFrame(tqdm(ex.map(fn, param_vals), desc = "Steady-State Scan", total = len(param_vals)), index=param_vals)  # type: ignore

def simulate_to_steady_state_with_results(
    s,
) -> None:

    s.simulate_to_steady_state()
    ss_res = s.get_full_concs()

    if ss_res is not None:
        s.simulate(ss_res.index[0])

def simulate_resp_coef_variable_param(
    param_val: float,
    param_str: str,
    m: Model,
    params_to_extract: list[str],
) -> dict:
    m.update_parameter(param_str, param_val)

    return mca.response_coefficients(
        m,
        parameters=params_to_extract,
        disable_tqdm=True
    )

def iterable_resp_coef_scan_params(
    m: Model,
    param_str: str,
    param_vals: Iterable[float],
    params_to_extract: list[str],
) -> pd.DataFrame:

    fn = partial(
        simulate_resp_coef_variable_param,
        param_str = param_str,
        m = m,
        params_to_extract = params_to_extract,
    )

    if sys.platform in ["win32", "cygwin"]:
        return pd.DataFrame(tqdm(map(fn, param_vals), desc = "Response Coefficient Scan", total = len(param_vals)), index=param_vals)  # type: ignore
    else:
        with futures.ProcessPoolExecutor() as ex:
            return pd.DataFrame(tqdm(ex.map(fn, param_vals), desc = "Response Coefficient Scan", total = len(param_vals)), index=param_vals)  # type: ignore

def find_intersections(
    xvals_1: pd.DataFrame,
    yvals_1: pd.DataFrame,
    xvals_2: pd.DataFrame,
    yvals_2: pd.DataFrame
) -> (Iterable, Iterable):
    interp_func_1 = interp1d(xvals_1, yvals_1, kind = 'linear')
    interp_func_2 = interp1d(xvals_2, yvals_2, kind = 'linear')
    
    xx = np.linspace(max(xvals_1.iloc[0], xvals_2.iloc[0]), min(xvals_1.iloc[-1], xvals_2.iloc[-1]), 1000)
    
    interp_1 = interp_func_1(xx)
    interp_2 = interp_func_2(xx)
    
    idx = np.argwhere(np.diff(np.sign(interp_1 - interp_2))).flatten()
    
    return xx[idx], interp_1[idx]

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before