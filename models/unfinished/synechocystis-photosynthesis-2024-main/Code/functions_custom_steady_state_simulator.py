import numpy as np
import pandas as pd
import sys
from modelbase.ode import Model, Simulator
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Dict, Optional, Tuple, Union, List, Iterable
from assimulo.solvers.sundials import CVodeError
from numpy.typing import NDArray
from typing_extensions import TypeAlias
from tqdm.auto import tqdm
from functools import partial
import warnings

import functions as fnc
from functions_fluorescence_simulation import make_lights
import functions_light_absorption as lip

Array: TypeAlias = NDArray[np.float64]
ArrayLike = Union[NDArray[np.float64], List[float]]

_DISPLACEMENT = 1e-4
_DEFAULT_TOLERANCE = 1e-8


def simulate_to_steady_state_custom(
    s,
    simulation_kwargs: Dict[str, Any]
    | None = {"t_end": 1e6, "tolerances": [[None, 1e-6]], "verbose": False},
    rel_norm: bool = False,
    return_simulator=False,
    retry_unsuccessful=False,
    return_unsuccessful=True,
    retry_kwargs=None,
    verbose=False,
    **integrator_kwargs,
):
    t_end = simulation_kwargs["t_end"]
    tolerances = simulation_kwargs["tolerances"]
    verbose = simulation_kwargs["verbose"]

    try:
        # t, y = s.simulate(t_end, **integrator_kwargs)
        s, t, y = fnc.simulate_with_retry(
            s,
            integrator_kwargs=integrator_kwargs,
            retry_kwargs=retry_kwargs,
            retry_unsuccessful=retry_unsuccessful,
            return_unsuccessful=return_unsuccessful,
            verbose=verbose,
            t_end=t_end,
            steps=100 # Testwise, have always the last 1% of the time range evaluated
        )
        if t is None:
            if verbose:
                warnings.warn("simulation failed")
            return (s, None, None) if return_simulator else (None, None)

        res = s.get_results_df().iloc[-2:, :]

        # Adapt the output of the original steady state function
        s.time = [np.array([t[-1]])]
        s.results = [np.array([y[-1]])]

        for tol in tolerances:
            if tol[0] is None:
                notcomp = [
                    x for tol in tolerances if tol[0] is not None for x in tol[0]
                ]
                comp = [x for x in s.model.get_compounds() if x not in notcomp]
                diff = res.iloc[-1].loc[comp] - res.iloc[-2].loc[comp]
            else:
                diff = res.iloc[-1].loc[tol[0]] - res.iloc[-2].loc[tol[0]]
            if rel_norm:
                diff = diff / res.iloc[-1].loc[diff.index]
            if np.linalg.norm(diff, ord=2) > tol[1]:
                if verbose:
                    warnings.warn(f"steady state not reached\n{diff}")
                return (s, None, None) if return_simulator else (None, None)
        return (
            (s, np.array([t[-1]]), np.array([y[-1]]))
            if return_simulator
            else (np.array([t[-1]]), np.array([y[-1]]))
        )
    except Exception as e:
        if verbose:
            warnings.warn(f"simulation failed:\n{e}")
        return (s, None, None) if return_simulator else (None, None)


def _find_steady_state(
    *,
    model: Model,
    y0: Union[ArrayLike, Dict[str, float]],
    tolerance: float,
    simulation_kwargs: Dict[str, Any] | None,
    rel_norm: bool = False,
    **integrator_kwargs: Dict[str, Any],
) -> Tuple[Optional[Array], Optional[Array]]:
    """Simulate the system to steadt state."""
    # print("_find_steady_state start")
    s = Simulator(model=model)
    s.initialise(y0=y0, test_run=False)
    t, y = simulate_to_steady_state_custom(
        s,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )
    # print("_find_steady_state end")
    return t, y


def get_response_coefficients(
    model: Model,
    parameter: str,
    y: Union[Dict[str, float], Array, List],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    simulation_kwargs: Dict[str, Any] | None = None,
    rel_norm: bool = False,
    **integrator_kwargs: Dict[str, Any],
) -> Tuple[Optional[Array], Optional[Array]]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    model_copy: Model = model.copy()
    old_value = model_copy.get_parameter(parameter_name=parameter)
    if normalized:
        t_ss, y_ss = _find_steady_state(
            model=model_copy,
            y0=y,
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        if t_ss is None or y_ss is None:
            return None, None
        fluxes_array_norm = model_copy.get_fluxes_array(y=y_ss, t=t_ss)
        fcd = model_copy.get_full_concentration_dict(y_ss)
        del fcd["time"]
        y_ss_norm = old_value / np.fromiter(fcd.values(), dtype="float")
        fluxes_array_norm = old_value / fluxes_array_norm

    ss: list[Array] = []
    fluxes: list[Array] = []
    for new_value in [
        old_value * (1 + displacement),
        old_value * (1 - displacement),
    ]:
        model_copy.update_parameter(parameter_name=parameter, parameter_value=new_value)
        t_ss, y_ss = _find_steady_state(
            model=model_copy,
            y0=y,
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        if t_ss is None or y_ss is None:
            return None, None
        fcd = model_copy.get_full_concentration_dict(y_ss)
        del fcd["time"]
        ss.append(np.fromiter(fcd.values(), dtype="float"))
        fluxes.append(model_copy.get_fluxes_array(y=y_ss, t=t_ss))

    conc_resp_coef: Array = (ss[0] - ss[1]) / (2 * displacement * old_value)
    flux_resp_coef: Array = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)

    if normalized:
        conc_resp_coef *= y_ss_norm  # type: ignore
        flux_resp_coef *= fluxes_array_norm  # type: ignore
    return np.atleast_1d(np.squeeze(conc_resp_coef)), np.atleast_1d(
        np.squeeze(flux_resp_coef)
    )


def get_response_coefficients_array(
    model: Model,
    parameters: List[str],
    y: Dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: Dict[str, Any] | None = None,
    **integrator_kwargs: Dict[str, Any],
) -> Tuple[Array, Array]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    if sys.platform in ["win32", "cygwin"] and multiprocessing:
        warnings.warn(
            """
                Windows does not behave well with multiple processes.
                Falling back to threading routine."""
        )

    crcs = np.full(
        shape=(len(parameters), len(model.get_all_compounds())), fill_value=np.nan
    )
    frcs = np.full(
        shape=(len(parameters), len(model.get_rate_names())), fill_value=np.nan
    )
    _get_response_coefficients = partial(
        get_response_coefficients,
        model,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )

    rcs: Iterable[tuple[Array | None, Array | None]]
    if sys.platform in ["win32", "cygwin"] or not multiprocessing:
        rcs = map(_get_response_coefficients, parameters)
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as pe:
            rcs = tqdm(
                pe.map(_get_response_coefficients, parameters),
                disable=disable_tqdm,
                total=len(parameters),
            )

    for i, (crc, frc) in enumerate(rcs):
        crcs[i] = crc
        frcs[i] = frc
    return crcs, frcs


def get_response_coefficients_df(
    model: Model,
    parameters: List[str],
    y: Dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: Dict[str, Any] | None = None,
    **integrator_kwargs: Dict[str, Any],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    crcs, frcs = get_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )
    crcs_df = pd.DataFrame(
        data=crcs,
        index=parameters,
        columns=model.get_all_compounds(),
    )
    frcs_df = pd.DataFrame(
        data=frcs,
        index=parameters,
        columns=model.get_rate_names(),
    )
    return crcs_df, frcs_df


def get_ssflux(m, y0, lightfun, target, light_params, tolerance=1e-4, rel_norm=False):
    light = lightfun(*light_params)
    s = Simulator(m.copy())
    s.update_parameter("pfd", light)
    s.initialise(y0)
    # t,y = s.simulate_to_steady_state(tolerance=tolerance, rel_norm=rel_norm, **fnc.simulator_kwargs["loose"])
    # s,t,y = simulate_to_steady_state_custom(s, simulation_kwargs={"t_end":1e6, "tolerances":[[["ATP", "CO2", "3PGA"], 1e-4],[None, 1e-6]], "verbose":True}, return_simulator=True, **fnc.simulator_kwargs["loose"])
    s, t, y = simulate_to_steady_state_custom(
        s,
        simulation_kwargs={
            "t_end": 1e6,
            "tolerances": [[["CBBa", "PSII", "OCP"], 1e-8], [None, 1e-6]],
            "verbose": True,
        },
        rel_norm=True,
        return_simulator=True,
        **fnc.simulator_kwargs["loose"],
    )
    if t is None:
        return np.nan
    else:
        return float(s.get_fluxes_dict()[target])


def get_ssfluxes(
    m,
    y0,
    lightfun,
    target,
    lightparam1,
    lightparam2,
    otherparams=None,
    multiprocessing=True,
    max_workers=None,
):
    light_params = np.meshgrid(lightparam1, lightparam2)
    _light_params = zip(*[x.flatten() for x in light_params])

    _get_ssflux = partial(get_ssflux, m, y0, lightfun, target)

    if sys.platform in ["win32", "cygwin"] or not multiprocessing:
        res = np.array(list(map(_get_ssflux, _light_params)), dtype=float)
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as pe:
            res = np.array(list(pe.map(_get_ssflux, _light_params)), dtype=float)

    res = res.reshape(-1, len(lightparam1))
    return pd.DataFrame(res, index=lightparam2, columns=lightparam1)


# Calculate the steady-state PQ reduction and Fluorescence in perturbed models
def calculate_ss_Q_red(m, y0, light, p={}):
    m = m.copy()
    m = fnc.add_exchange(m)
    s = Simulator(m)
    s.initialise(y0)

    s.update_parameters(p)
    s.update_parameter("pfd", light)

    # t,y = s.simulate_to_steady_state(tolerance=1e-4, **fnc.simulator_kwargs["loose"])
    s, t, y = simulate_to_steady_state_custom(
        s,
        simulation_kwargs={
            "t_end": 1e6,
            "tolerances": [[["CBBa", "PSII", "OCP"], 1e-8], [None, 1e-6]],
            "verbose": True,
        },
        rel_norm=True,
        return_simulator=True,
        **fnc.simulator_kwargs["loose"],
    )
    if t is None:
        return np.nan
    else:
        return float(s.get_full_results_df()["Q_red"])


def calculate_ss_outputs(m, y0, light, p={}):
    m = m.copy()
    m = fnc.add_exchange(m)
    s = Simulator(m)
    s.initialise(y0)

    s.update_parameters(p)
    s.update_parameter("pfd", light)

    # t,y = s.simulate_to_steady_state(tolerance=1e-4, **fnc.simulator_kwargs["loose"])
    s, t, y = simulate_to_steady_state_custom(
        s,
        simulation_kwargs={
            "t_end": 1e6,
            "tolerances": [[["CBBa", "PSII", "OCP"], 1e-8], [None, 1e-6]],
            "verbose": True,
        },
        rel_norm=True,
        return_simulator=True,
        **fnc.simulator_kwargs["loose"],
    )
    if t is None:
        return (np.nan, np.nan)
    else:
        qred = float(s.get_full_results_df()["Q_red"])

        # Calculate the Fm
        s.update_parameter("pfd", lip.light_gaussianLED(625, 15000))
        t, y = s.simulate(t + 0.3)

        if t is None:
            return (qred, np.nan)
        else:
            return (qred, float(s.get_full_results_df().iloc[-1, :].loc["Fluo"]))


def _get_parameter_variations(p_bounds, n):
    params = {k: np.linspace(*p, n) for k, p in p_bounds.items()}

    params_mesh = np.meshgrid(*params.values())
    _params_mesh = list(zip(*[x.flatten() for x in params_mesh]))
    _params_mesh = [{k: v for k, v in zip(params, x)} for x in _params_mesh]
    return _params_mesh


def _get_parametervariant_outputs(s, p_bounds, n, light, multiprocessing, max_workers):
    # Create a combination of the parameter values
    _params_mesh = _get_parameter_variations(p_bounds, n)

    # Return the steady-state Q_red value with each parameter combination
    y0 = s.get_results_df().iloc[0, :].to_dict()
    _calculate_ss_outputs = partial(calculate_ss_outputs, s.model, y0, light)

    if sys.platform in ["win32", "cygwin"] or not multiprocessing:
        res = np.array(list(map(_calculate_ss_outputs, _params_mesh)), dtype=float)
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as pe:
            res = np.array(
                list(pe.map(_calculate_ss_outputs, _params_mesh)), dtype=float
            )
    return res


def get_parametervariant_outputs(models, sims, n, multiprocessing, max_workers):
    Q_reds = {}
    Fm_res = {}
    for nam, model in models.items():
        s = sims[nam]

        if nam == "mnost":
            Q_reds[nam] = calculate_ss_Q_red(
                s.model, s.get_results_df().iloc[0, :].to_dict(), make_lights()[3]
            )
        else:
            res_orn = _get_parametervariant_outputs(
                s,
                model["param_bounds"],
                n,
                make_lights()[3],
                multiprocessing,
                max_workers,
            )
            Q_reds[nam], Fm_orn = [x.flatten() for x in np.split(res_orn, 2, axis=1)]
            res_blue = _get_parametervariant_outputs(
                s,
                model["param_bounds"],
                n,
                make_lights()[1],
                multiprocessing,
                max_workers,
            )
            Fm_blue = res_blue[:, 1]
            Fm_res[nam] = (Fm_blue - Fm_orn) / Fm_blue
    return Q_reds, Fm_res


def get_steadystate_y0(
    m,
    y0,
    light=lip.light_spectra("solar", 0.1),
    steadystate_kwargs={"tolerance": 1e-3},
    verbose=False,
):
    _m = m.copy()
    _m = fnc.add_exchange(_m)
    _m.update_parameter("pfd", light)

    s = Simulator(_m)
    s.initialise(y0)
    _t, yss = simulate_to_steady_state_custom(
        s,
        simulation_kwargs={
            "t_end": 1e6,
            "tolerances": [[["CBBa", "PSII", "OCP"], 1e-8], [None, 1e-6]],
            "verbose": True,
        },
        rel_norm=True,
        return_simulator=False,
        **fnc.simulator_kwargs["loose"],
    )
    if _t is None:
        raise RuntimeError("The model couldn't be simulated to steady state")
    if verbose:
        print(f"steady state simulation ran for {s.get_time()[-1]} time units")
    return s.get_results_df().squeeze().to_dict()
