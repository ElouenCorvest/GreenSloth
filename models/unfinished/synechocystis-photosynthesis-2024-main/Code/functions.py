### Import packages and functions ###
from datetime import datetime
from math import gcd
from typing import Union, List, Dict, cast
import dill
import pickle
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os
from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Rectangle
from modelbase.ode import Model, Simulator, mca
from modelbase.ode import ratefunctions as rf
from modelbase.ode import ratelaws as rl
from modelbase.ode.simulators.simulator import _Simulate
from scipy.integrate import simpson
from tqdm.notebook import tqdm

from warnings import warn

import functions_light_absorption as lip

# CHANGE LOG
# 014 28.02.2022 | moved most functions from notebooks to this file for common usage
#     05.04.2022 | added function to imuitate a PAM simulateion with a second model at the same time points
#     10.04.2022 | added functions to compare two similar models or simulations


### Define and set defaults for plotting ###
plt_defaults = {
    "figure": {"figsize": (10, 7)},
    "subplot": {"facecolor": "white"},
    "plot": {"linewidth": 4},
    "grid": {
        "color": (0, 0, 0),
        "alpha": 0.33,
        "linestyle": "dashed",
        "linewidth": 1,
    },
    "tick": {
        "direction": "out",
        "length": 6,
        "width": 2,
        "labelsize": 14,
        "color": "0.15",
        "pad": 7,
    },
    "label": {"fontsize": 14},
    "title": {"fontsize": 18},
    "legend": {
        "loc": "upper left",
        "bbox_to_anchor": (1.02, 1),
        "borderaxespad": 0,
        "ncol": 1,
        "fontsize": 12,
        "numpoints": 1,
        "scatterpoints": 1,
        "markerscale": 1,
        "frameon": False,
    },
}


def set_ax_default(ax):
    ax.yaxis.label.set(**plt_defaults["label"])
    ax.xaxis.label.set(**plt_defaults["label"])
    ax.tick_params(**plt_defaults["tick"])
    return ax


def get_plt_default(name, **kwargs):
    res = plt_defaults[name].copy()
    res.update(kwargs)
    return res


# Simulate a model with option of retry
def simulate_with_retry(s, integrator_kwargs, retry_kwargs, index=None, retry_unsuccessful=True, return_unsuccessful=True, verbose=True, **simulator_kwargs):
    """Simulate a modelbase model using the integrator settings in integrator_kwargs. If the simulator is unsuccessful, retry with one or more sets of alternative integrator settings in retry_kwargs

    Args:
        s (Simulator): _description_
        integrator_kwargs (dict): integrator settings to be passed into the simulate function
        retry_kwargs (dict,list): integrator settings to be passed into the simulate function upon retry. If a list is given, the settings are tried in order
        index (int, optional): an index to be printed in warnings. Defaults to None.
        retry_unsuccessful (bool, optional): should the simulation be retried if failed. Defaults to True.
        return_unsuccessful (bool, optional): should the simulator be returned if the simulation failed, otherwise None is returned. Defaults to True.
        verbose (bool, optional): should warnings be printed. Defaults to True.

    Returns:
        tuple: Simulator, simulation time vector, and concentration array
    """
    # Try default simulation
    t, y = s.simulate(**simulator_kwargs, **integrator_kwargs)

    if t is None:
        if retry_unsuccessful:
            # If only a single set of retry kwargs is given, make pack them into a list
            if isinstance(retry_kwargs, dict):
                retry_kwargs = [retry_kwargs]
            
            # Retry the simulation with each set of retry kwargs
            for j, _retry_kwargs in enumerate(retry_kwargs):
                if verbose:
                    warn(f"Retrying simulation {index if index is not None else ''} to t = {simulator_kwargs.get('t_end')} with retry_kwargs ({j})... ")
                _integrator_kwargs = integrator_kwargs.copy()
                _integrator_kwargs.update(_retry_kwargs)

                t, y = s.simulate(**simulator_kwargs, **_integrator_kwargs)
            
                # If a simulation succeeded, break the retry cycle
                if t is not None:
                    return s, t, y
        
        # If the function arrives here, all simulation attempts failed
        # If the requested return the unsuccessful simulator, else None
        if return_unsuccessful:
            warn(f"Simulation {index if index is not None else ''} to t = {simulator_kwargs.get('t_end')} was unsuccessful")
            return s, None, None
        else:
            return None, None, None
    
    # If the simulation was successful, return the simulator
    else:
        return s, t, y


### General overview plots ###
def plot_overview(s):
    # Get the plottable compounds
    compounds = s.model.compounds + s.model.derived_compounds

    # Plot the time series
    fig, axes = plt.subplots(2, 2)
    fig.set_size_inches(18.5, 10.5)

    # Plot the ETC mobile compounds
    fig, ax = s.plot_selection(
        [
            x
            for x in [
                "Q_ox",
                "PC_ox",
                "Fd_ox",
                "NADPH",
                "NADH",
                "ATP",
                "succinate",
                "fumarate",
            ]
            if x in compounds
        ],
        title="ETC compounds",
        xlabel="time [s]",
        ylabel="concentration [mmol mol(Chl)$^{-1}$]",
        ax=axes[0, 0],
    )

    # Plot the gases
    fig, ax = s.plot_selection(
        ["O2", "CO2"],
        title="O$_2$ and CO$_2$",
        xlabel="time [s]",
        ylabel="concentration [mmol mol(Chl)$^{-1}$]",
        ax=axes[0, 1],
    )

    # Plot the pHs
    fig, ax = s.plot_selection(
        ["pHlumen", "pHcytoplasm"],
        title="pH of lumen and cytoplasm",
        xlabel="time [s]",
        ylabel="pH",
        ax=axes[1, 0],
    )

    # Plot the Photorespiration intermediates
    fig, ax = s.plot_selection(
        [
            x
            for x in ["PG", "GLYC", "GLYX", "GLY", "SER", "HPA", "H2O2", "GA", "3PGA"]
            if x in compounds
        ],
        title="CBB & PR compounds",
        xlabel="time [s]",
        ylabel="concentration [mmol mol(Chl)$^{-1}$]",
        ax=axes[1, 1],
    )

    fig.tight_layout()

    return fig, axes


def plot_flux_overview(s, plot0_kwargs={}):
    # Plot the time series
    fig, axes = plt.subplots(2, 2)
    fig.set_size_inches(18.5, 10.5)

    # Plot the ETC fluxes
    fig, ax = s.plot_flux_selection(
        [
            "vPS2",
            "vSDH",
            "vRespiration",
            "vbd",
            "vb6f",
            "vaa",
            "vPS1",
            "vFlv",
            "vNDH",
            "vFNR",
            "vNQ",
        ],
        title="ETC fluxes",
        xlabel="time [s]",
        ylabel="flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]",
        ax=axes[0, 0],
    )

    # Plot the exchange reactions
    fig, ax = s.plot_flux_selection(
        ["vO2out", "vPass", "vCCM"],
        title="Exchange fluxes",
        xlabel="time [s]",
        ylabel="flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]",
        ax=axes[0, 1],
        **plot0_kwargs,
    )

    # Plot the pHs
    fig, ax = s.plot_flux_selection(
        ["vATPsynthase", "vATPconsumption", "vNADPHconsumption"],
        title="Synthesis and consumption",
        xlabel="time [s]",
        ylabel="flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]",
        ax=axes[1, 0],
    )

    # Plot the Photorespiration intermediates
    fig, ax = s.plot_flux_selection(
        [
            "phosphoglycolate_phosphatase",
            "glycolate_oxidase",
            "glycine_transaminase",
            "glycine_decarboxylase",
            "serine_glyoxylate_transaminase",
            "glycerate_dehydrogenase",
            "catalase",
            "glycerate_kinase",
            "vPRfirststep",
        ],
        title="CBB & PR compounds",
        xlabel="time [s]",
        ylabel="flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]",
        ax=axes[1, 1],
    )

    fig.tight_layout()

    return fig


# Plot oxidised/ "interesting" fractions of conserved moieties
def compound_ratio(s, target, tot):
    target_val = s.get_full_results_dict()[target]
    return target_val / s.model.get_parameter(tot)


def plot_compound_ratios(s, compounds_dict=None, fig=None, ax=None, force0=True):
    if fig is None or ax is None:
        fig, ax = plt.subplots()
        fig.set_size_inches(10.5, 10.5)

    # If no compounds are provided use default
    if compounds_dict is None:
        compounds_dict = {
            "Q_red": "Q_tot",
            "PC_red": "PC_tot",
            "Fd_red": "Fd_tot",
            "NADPH": "NADP_tot",
            "NADH": "NAD_tot",
            "ATP": "AP_tot",
        }

    # Iterate through paris and plot ratios
    for key, value in compounds_dict.items():
        ratio = compound_ratio(s, key, value)
        ax.plot(s.get_time(), ratio, label=key, linewidth=4)

    # Annotate plot
    ax.set_xlabel("time [s]")
    ax.set_ylabel("reduced fraction of pool")

    if force0:
        ax.set_ylim(ymin=0)

    if "ATP" in compounds_dict:
        secax_y = ax.secondary_yaxis("right")
        secax_y.set_ylabel("ATP fraction of adenosine pool", rotation=-90, labelpad=20)

        secax_y.yaxis.label.set_fontsize(15)
        secax_y.tick_params(axis="y", labelsize=15)

        legend_pos = (1.05, 1)
    else:
        legend_pos = (1.02, 1)

    # Increase font size
    ax.title.set_fontsize(15)
    ax.xaxis.label.set_fontsize(15)
    ax.yaxis.label.set_fontsize(15)
    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=15)

    # Add legend
    ax.legend(bbox_to_anchor=legend_pos, loc="upper left", frameon=False, fontsize=15)
    ax.grid(ls="--")

    return fig, ax


def get_stoichiometric_fluxes(s, cmp):
    stoich = s.model.get_compound_stoichiometry(cmp)
    fluxes = s.get_fluxes_dict()

    fluxes_scaled = {key: fluxes[key] * value for key, value in stoich.items()}
    return fluxes_scaled


def plot_stoichiometric_fluxes(s, cmp):
    # Get data
    fluxes_scaled = get_stoichiometric_fluxes(s, cmp)

    # Plot
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(18.5, 10.5)

    for key, value in fluxes_scaled.items():
        ax.plot(s.get_time(), value, label=key, linewidth=4)

    # Annotate plot
    ax.set_xlabel("time [s]")
    ax.set_ylabel("compound flux [mmol mol$_{Chl}^{-1} s^{-1}$]")

    # Increase font size
    ax.title.set_fontsize(15)
    ax.xaxis.label.set_fontsize(15)
    ax.yaxis.label.set_fontsize(15)
    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=15)

    # Add legend
    ax.legend(bbox_to_anchor=(1, 1), loc="upper left", frameon=False, fontsize=15)
    ax.grid(ls="--")

    return fig, ax


def plot_overview_isoATP(s):
    # Get the plottable compounds
    compounds = s.model.compounds + s.model.derived_compounds

    # Plot the time series
    fig, axes = plt.subplots(2, 2)
    fig.set_size_inches(18.5, 10.5)

    # Plot the ETC mobile compounds
    plot0_compounds = [
        "Q_ox",
        "PC_ox",
        "Fd_ox",
        "NADPH",
        "NADH",
        "ATP",
        "succinate",
        "fumarate",
    ]

    compounds = s.get_results_dict()
    time = s.get_time()
    ax = axes[0, 0]

    # Add ATP on a scaled axis
    compounds_max = np.max(
        [list(compounds[key]) for key in plot0_compounds if key != "ATP"]
    )

    scale_factor = compounds_max / np.max(compounds["ATP"]) * 1.1

    secax_y = axes[0, 0].secondary_yaxis(
        "right",
        functions=(lambda x: x / scale_factor, lambda x: x / scale_factor),
    )
    secax_y.set_ylabel(
        "ATP concentration [mmol mol(Chl)$^{-1}$]", rotation=-90, labelpad=20
    )

    for key, value in compounds.items():
        if key in plot0_compounds:
            if key != "ATP":
                ax.plot(time, value, label=key, linewidth=4)
            else:
                ax.plot(
                    time,
                    np.array(compounds["ATP"]) * scale_factor,
                    label="ATP",
                    linewidth=4,
                )

    # Format plot
    ax.set_title("ETC compounds")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("non-ATP concentration [mmol mol(Chl)$^{-1}$]")
    ax.set_ylim(ymin=0)

    # Increase font size
    ax.title.set_fontsize(18)
    ax.xaxis.label.set_fontsize(14)
    ax.yaxis.label.set_fontsize(14)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    secax_y.yaxis.label.set_fontsize(14)
    secax_y.tick_params(axis="y", labelsize=14)

    # Add legend
    ax.legend(bbox_to_anchor=(1.12, 1), loc="upper left", frameon=False, fontsize=12)
    ax.grid(ls="--")

    # Plot the gases
    fig, ax = s.plot_selection(
        ["O2", "CO2"],
        title="O$_2$ and CO$_2$",
        xlabel="time [s]",
        ylabel="concentration [mmol mol(Chl)$^{-1}$]",
        ax=axes[0, 1],
    )

    # Plot the pHs
    fig, ax = s.plot_selection(
        ["pHlumen", "pHcytoplasm"],
        title="pH of lumen and cytoplasm",
        xlabel="time [s]",
        ylabel="pH",
        ax=axes[1, 0],
    )

    # Plot the Photorespiration intermediates
    fig, ax = s.plot_selection(
        [
            x
            for x in ["PG", "GLYC", "GLYX", "GLY", "SER", "HPA", "H2O2", "GA", "3PGA"]
            if x in compounds
        ],
        title="CBB & PR compounds",
        xlabel="time [s]",
        ylabel="concentration [mmol mol(Chl)$^{-1}$]",
        ax=axes[1, 1],
    )

    fig.tight_layout()

    return fig, axes


# Plot the net synthesis of ATP and NADPH
def get_ATP_NADPH_synthesis(s):
    # Get fluxes
    ATP_flux = pd.DataFrame(get_stoichiometric_fluxes(s, "ATP"), index=s.get_time())
    ATP_flux[ATP_flux < 0] = 0

    NADPH_flux = pd.DataFrame(get_stoichiometric_fluxes(s, "NADPH"), index=s.get_time())
    NADPH_flux[NADPH_flux < 0] = 0

    dat = pd.concat(
        (ATP_flux.sum(axis=1, skipna=False), NADPH_flux.sum(axis=1, skipna=False)),
        axis=1,
    )
    dat.columns = ["ATP synth", "NADPH synth"]
    dat.loc[:, "ratio"] = dat.iloc[:, 0] / dat.iloc[:, 1]
    return dat


def plot_ATP_NADPH_synthesis(s):
    dat = get_ATP_NADPH_synthesis(s)

    # Plot
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(18.5, 10.5)

    lin = ax.plot(dat.iloc[:, :-1])
    ax2 = ax.twinx()
    lin2 = ax2.plot(dat.iloc[:, -1], c="k")

    # Annotate plot
    ax.set_xlabel("time [s]")
    ax.set_ylabel("flux [mmol mol$_{Chl}^{-1} s^{-1}$]")
    ax.set_ylim(ymin=0)

    ax2

    # Increase font size
    ax.title.set_fontsize(15)
    ax.xaxis.label.set_fontsize(15)
    ax.yaxis.label.set_fontsize(15)
    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=15)

    # Add legend
    ax.legend(
        lin + lin2,
        ["ATP production", "NADPH production", "ATP:NADPH"],
        bbox_to_anchor=(1, 1),
        loc="upper left",
        frameon=False,
        fontsize=15,
    )

    return fig, [ax, ax2]


def plot_CBB_regulation(s):
    # Plot the time series
    fig, axes = plt.subplots(2, 1)
    fig.set_size_inches(18.5 / 1.5, 21 / 1.5)

    compounds = s.get_full_results_dict()

    # Plot the CBB regulatory factors
    CBB_regulators = ["f_CBB_energy", "f_CBB_Fdratio", "f_CBB_gas"]
    fig, ax = s.plot_selection(
        CBB_regulators,
        title="CBB regulators",
        xlabel="time [s]",
        ylabel="regulator value",
        ax=axes[0],
    )

    CBB_reg_values = np.array([compounds[key] for key in CBB_regulators])
    CBB_total = np.prod(CBB_reg_values, axis=0)

    ax.plot(
        s.get_time(), CBB_total, label="total", linewidth=4, c="black", linestyle="--"
    )
    ax.set_ylim([-0.03, 1.03])

    # Plot the exchange reactions
    Oxy_regulators = ["f_CBB_energy", "f_CBB_Fdratio", "f_oxy_gas", "f_oxy_carbon"]
    fig, ax = s.plot_selection(
        ["f_CBB_energy", "f_CBB_Fdratio", "f_oxy_carbon", "f_oxy_gas"],
        title="Oxy regulators",
        xlabel="time [s]",
        ylabel="regulator value",
        ax=axes[1],
    )

    Oxy_reg_values = np.array([compounds[key] for key in Oxy_regulators])
    Oxy_total = np.prod(Oxy_reg_values, axis=0)

    ax.plot(
        s.get_time(), Oxy_total, label="total", linewidth=4, c="black", linestyle="--"
    )
    ax.set_ylim([-0.03, 1.03])

    fig.tight_layout()

    return fig


def plot_electron_fluxes(s, reactions=None):
    electon_reactions = {
        # Inlets
        "vPS2": 2,
        "vRespiration": 10,
        # Outlets
        "vbd": -4,
        "vaa": -4,
        "vFlv": -4,
        "vNADPHconsumption": -2,
        # "glycine_decarboxylase": -2,
        "vCBB": -10,
        "vOxy": -10,
        "vPRsalv": 2,
    }

    if reactions is not None:
        electon_reactions = {
            key: val for key, val in electon_reactions.items() if key in reactions
        }

    fluxes = s.get_fluxes_dict()
    fluxes_stoich = {
        key: fluxes[key] * value
        for key, value in electon_reactions.items()
        if key in fluxes
    }

    time = s.get_time()

    # Plot
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(18.5 / 1.5, 10.5 / 1.5)

    ax.axhline(0, c="black", linestyle="--", linewidth=3)

    for key, value in fluxes_stoich.items():
        ax.plot(time, value, label=key, linewidth=4)

    # Format plot
    ax.set_title("Electron fluxes")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("electron flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]")

    # Increase font size
    ax.title.set_fontsize(18)
    ax.xaxis.label.set_fontsize(14)
    ax.yaxis.label.set_fontsize(14)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    # Add legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, fontsize=12)
    ax.grid(ls="--")

    return fig, ax


# Add a lightbar with helper funtions
def create_imdat(times, lights):
    # Get the biggest time step covering all intervals
    timediff = np.diff(times)
    # If the smallest difference is smaller than one, scale the data by the nearest multiple of 10
    if timediff.min() < 1:
        fac = 10 ** np.ceil(np.abs(np.log10(0.004)))
        timediffset = np.unique(np.round(timediff * fac)).astype(int)
        timestep = gcd(*timediffset) / fac
    else:
        timediffset = np.unique(np.round(timediff)).astype(int)
        timestep = gcd(*timediffset)

    # repeat the lights according to the time step to create the image data
    lightrep = np.round(timediff / timestep).astype(int)
    # return lights, lightrep
    return np.repeat(lights, lightrep, axis=0).T


def remove_pulses(lights, light_max):
    integ = lights.apply(simpson, axis=1)
    return lights.loc[integ <= light_max, :]


def is_pulse(lights, light_max):
    return lights.apply(simpson, axis=1) >= light_max


def wavelength_to_rgb(wavelength, gamma=0.8):
    """taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    """
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.0
    else:
        A = 0.5
    if wavelength < 380:
        wavelength = 380.0
    if wavelength > 750:
        wavelength = 750.0
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)


def make_spectralmap():
    clim = (380, 750)
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1] + 1, 1)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
    return LinearSegmentedColormap.from_list("spectrum", colorlist)


def add_lightbar(
    s,
    ax,
    max_intens,
    max_intens_spec=None,
    remove_pulses=True,
    annotation=True,
    annotation_twoline=True,
    annotation_light_c="k",
    annotation_size=None,
    color="bw",
    size=0.06,
    scale="linear",
    time_offset=None,
    spectrum_maskalpha=0.6,
    pad_top=0,
    y_pos=None,
    box_linewidth=1,
    ticks_linewidth=1.5,
):
    # Get all the different modelled times and lights
    alltimes = s.get_time()
    times = get_phase_times(s, include_first=True)
    time_spans = [np.array([np.min(x), np.max(x)]) for x in s.time]
    lights = pd.concat([x["pfd"] for x in s.simulation_parameters], axis=1).T

    # Adjuste the times with offset if necessary
    if time_offset is None:
        pass
    elif alltimes[0] != (-time_offset):
        offset = s.get_time()[0] + time_offset
        alltimes = alltimes - offset
        times = times - offset
        time_spans = np.array(time_spans) - offset

    # Get the pulses If no scaling information is given, infer it
    # if max_intens is None:
    #     weighted_intens = lights.apply(simpson, axis=1) * np.diff(times)

    pulses = is_pulse(lights, max_intens)
    lights_nopulse = lights.loc[np.invert(pulses), :]

    # If mono coloured light bar is wanted
    # get overall intensity, and most intense colour
    if color == "mono":
        mono_colors = lights.T.idxmax().to_numpy()
        if remove_pulses:
            mono_colors = mono_colors[np.invert(pulses)]

        lights = lights.apply(simpson, axis=1)
        lights_nopulse = lights.loc[np.invert(pulses)]

    # If no scaling information is given, infer it
    if max_intens_spec is None:
        if color != "mono":
            max_intens_spec = lights_nopulse.max().max()
        else:
            max_intens_spec = lights_nopulse.max()

    # Set the position and height of the lightbar
    if y_pos is None:
        axylim = ax.get_ylim()
    else:
        _axylim = ax.get_ylim()
        axylim = (y_pos, _axylim[1])

    axxlim = ax.get_xlim()
    if size > 0.03:
        lower_left = (
            float(axylim[0] - (size - 0.03) * np.diff(np.array(axylim))) - pad_top
        )
    else:
        lower_left = axylim[0] - pad_top
    full_height = float(size * np.diff(np.array(axylim)))
    width = alltimes[-1] - alltimes[0]

    tick_bottom = lower_left + full_height
    tickpos = np.mean(np.array(time_spans)[pulses], axis=1)

    # Remove pulses if requested
    if remove_pulses:
        lights = lights_nopulse
        times = times[np.append(True, np.invert(pulses))]

    if color == "mono":
        mono_imdat = np.atleast_2d(create_imdat(times, mono_colors))

    # return times, lights.to_numpy()
    imdat = np.atleast_2d(create_imdat(times, lights.to_numpy()))

    # Positions of the lightbar
    spec_pos = np.array(
        [alltimes[0] - width * 0.03, alltimes[0], lower_left, lower_left + full_height]
    )
    pos = np.array([alltimes[0], alltimes[-1], lower_left, lower_left + full_height])

    # Plot
    spectralmap = make_spectralmap()

    if color == "bw":
        cmap = colormaps["Greys"].resampled(256).reversed()
        cmap.set_under("black")
        cmap.set_bad("black")
        cmap.set_over("white")
    elif color == "bw_r":
        cmap = colormaps["Greys"].resampled(256)
        cmap.set_under("white")
        cmap.set_bad("white")
        cmap.set_over("black")
    elif color == "spectrum":
        alphas = np.concatenate(
            [
                np.full((256, 3), spectrum_maskalpha),
                np.linspace(1, 0, 256).reshape(-1, 1),
            ],
            axis=1,
        )
        cmap = ListedColormap(alphas)
        cmap.set_under("black")
        cmap.set_bad("black")
        cmap.set_over(alphas[-1, :])

        ax.imshow(
            np.arange(400, 701, 1).reshape(-1, 1),
            cmap=spectralmap,
            extent=pos,
            aspect="auto",
        )
    elif color == "mono":
        alphas = np.concatenate(
            [
                np.full((256, 3), spectrum_maskalpha),
                np.linspace(1, 0, 256).reshape(-1, 1),
            ],
            axis=1,
        )
        cmap = ListedColormap(alphas)
        cmap.set_under("black")
        cmap.set_bad("black")
        cmap.set_over(alphas[-1, :])
        ax.imshow(
            mono_imdat,
            cmap=spectralmap,
            extent=pos,
            aspect="auto",
            vmin=400,
            vmax=701,
        )
    else:
        raise ValueError(f"unknown color '{color}'")

    if scale == "linear":
        vmin = 0
        vmax = max_intens_spec
    elif scale == "log":
        vmin = 0.01 if not color == "mono" else 1
        vmax = max_intens_spec
    else:
        raise ValueError(f"unknown scale '{scale}'")

    # Plot a spectrum legend then the data
    if not color == "mono":
        ax.imshow(
            np.arange(400, 701, 1).reshape(-1, 1),
            cmap=spectralmap,
            extent=spec_pos,
            aspect="auto",
        )
    ax.imshow(
        imdat,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        extent=pos,
        aspect="auto",
        interpolation="none",
        norm=scale,
    )
    # return imdat

    if color != "mono":
        rect_param = ((spec_pos[0], pos[2]), pos[1] - spec_pos[0], pos[3] - pos[2])

        ax.plot(
            spec_pos[[1, 1]],
            spec_pos[[2, 3]],
            color="black",
            linewidth=box_linewidth,
            scalex=False,
            scaley=False,
        )
    else:
        rect_param = ((pos[0], pos[2]), pos[1] - pos[0], pos[3] - pos[2])
    ax.add_patch(
        Rectangle(
            *rect_param,
            fill=False,
            edgecolor="black",
            alpha=1,
            in_layout=True,
            linewidth=box_linewidth,
        )
    )

    # Add the pulse ticks
    ax.plot(
        [tickpos, tickpos],
        [tick_bottom, tick_bottom + float(np.diff(np.array(axylim)) * 0.015)],
        color="black",
        linewidth=ticks_linewidth,
        scalex=False,
        scaley=False,
    )

    ax.set_xlim(axxlim)
    ax.set_ylim(lower_left, axylim[1])

    if annotation:
        if color != "mono":
            if scale == "linear":
                anno = "Light"
            else:
                anno = f"Light\n({scale})"
            ax.text(
                pos[1],
                lower_left + 0.01 * np.diff(np.array(axylim)),
                anno,
                clip_on=False,
                size=size * 100,
                rotation=-90,
            )
        else:
            # Annotate scale
            unique_colors = np.append(True, mono_colors[1:] != mono_colors[:-1])
            unique_ints = np.append(
                True, lights[1:].to_numpy() != lights[:-1].to_numpy()
            )
            unique_lights = np.logical_or(unique_colors, unique_ints)

            text_times = times / times.max()
            text_times = text_times[np.append(unique_lights, True)]
            text_times = text_times[:-1] + 0.5 * np.diff(text_times)

            text_xpos = pos[0] + text_times * (pos[1] - pos[0])
            text_ypos = pos[2] + 0.5 * (pos[3] - pos[2])

            for x, col, i in zip(
                text_xpos, mono_colors[unique_lights], lights[unique_lights]
            ):
                if i > 1:
                    anno_sep = "\n" if annotation_twoline else " "
                    label = f"{col:.0f} nm{anno_sep}({i:.0f})"
                    c = annotation_light_c
                else:
                    label = "dark"
                    c = "white"
                ax.text(
                    x,
                    text_ypos,
                    label,
                    clip_on=False,
                    size=size * 140 if annotation_size is None else annotation_size,
                    ha="center",
                    va="center",
                    c=c,
                )

    return ax


# Plot the linear, cyclic and respiratory fluxes
def get_stoich(s, compound):
    return s.model.get_compound_stoichiometry(compound)


def get_compound_flux(s, compound, flux):
    return s.get_fluxes_dict()[flux] * get_stoich(s, compound)[flux]


def get_flux_fraction(s, compound, target_flux, all_fluxes):
    # Get the fluxes ans the stoichiometries of the target compound
    fluxes = s.get_fluxes_dict()
    stoich = get_stoich(s, compound)

    # Calculate the compound flux from the target flux
    target = fluxes[target_flux] * stoich[target_flux]

    # Calculate the total flux into the target compound
    all_sum = np.sum(
        [fluxes[flux] * stoich[flux] for flux in all_fluxes if flux != target_flux],
        axis=0,
    )
    all_sum += target

    return target / all_sum


# def get_electron_pathways(s):
#     """Get the flows through the different electron pathways for each timepoint"""
#     fluxes = s.get_fluxes_dict()

#     pathways = {
#         # Electron flux through linear transport, characterised by its emergence in PS2 and through PS1 (PS2: 2 e-)
#         "linear": fluxes["vPS2"] * 2,
#         # Flux of respiration into the ETC
#         "respiratory": (
#             # SDH fraction of respiratory flux
#             (fluxes["vSDH"] * 2)
#             # NDH2 fraction of respiratory flux (assuming NADH emerges from respiration and PR)
#             + (
#                 fluxes["vNDH"]
#                 * 2
#                 * get_flux_fraction(s, "NADH", "vRespiration", ["vRespiration", "vPRsalv"])
#             )
#             # NDH1 & FQ fraction of respiratory flux
#             # Calculated alternatively as the reverse flux through FNR
#             + [-np.min([x, 0]) for x in fluxes["vFNR"] * 2]
#         ),
#         # Flux through cyclic transport, all flow through PS1 (1 e-), not emerging in PS2 (2 e-) or respiration (10 e-) and not lost through terminal oxidases
#         "cyclic": (
#             (fluxes["vNQ"] * 2 + fluxes["vFQ"] * 2)
#             * (-get_compound_flux(s, "Fd_ox", "vPS1"))
#             / (
#                 -get_compound_flux(s, "Fd_ox", "vPS1")
#                 + [-np.min([x, 0]) for x in get_compound_flux(s, "Fd_ox", "vFNR")]
#             )
#         ),
#     }

#     return pathways


# def plot_electron_pathways(
#     s, ts, xlabel="", ticklabels="", normalise=False, fig=None, ax=None
# ):
#     # Get the electron fluxes through the pathways
#     pathways = get_electron_pathways(s)
#     pathways_names = list(pathways.keys())

#     # Initialise the data container
#     data = np.zeros([len(ts), 3])

#     # Iterate through pathways an collect the wanted fluxes
#     for i, (key, val) in enumerate(pathways.items()):
#         data[:, i] = [x for x, t in zip(val, s.get_time()) if t in ts]

#     # Normalise the data rows
#     if normalise:
#         data = (data.transpose() / np.sum(data, axis=1)).transpose()
#         ylabel = "Fraction of electron flux through PSI"
#     else:
#         ylabel = "Electron flux [mmol mol(Chl)$^{-1}$ s$^{-1}$]"

#     # Initialise a plot
#     if fig is None or ax is None:
#         fig, ax = plt.subplots(**plt_defaults["figure"])
#     ax = set_ax_default(ax)

#     # Plot linear, cyclic and respiratory flow
#     ax.bar(
#         range(len(ts)),
#         data[:, 0],
#         width=0.4,
#         label=pathways_names[0],
#         **plt_defaults["plot"],
#     )
#     ax.bar(
#         range(len(ts)),
#         data[:, 1],
#         width=0.4,
#         label=pathways_names[1],
#         bottom=data[:, 0],
#         **plt_defaults["plot"],
#     )
#     ax.bar(
#         range(len(ts)),
#         data[:, 2],
#         width=0.4,
#         label=pathways_names[2],
#         bottom=np.sum(data[:, :2], axis=1),
#         **plt_defaults["plot"],
#     )

#     ax.set_xlabel(xlabel, **plt_defaults["label"])
#     ax.set_xticks(range(len(ts)))
#     ax.set_xticklabels(ticklabels)

#     ax.legend(**plt_defaults["legend"])
#     ax.set_ylabel(ylabel)

#     return fig, ax


def get_ss_electron_pathways(s, t=None):
    """Get the flows through the different electron pathways for given time points assuming steady state"""
    # If no time selection is given, use the respective simulation end times
    if t is None:
        t = np.array([x[-1] for x in s.time])

    fluxes = s.get_fluxes_df().loc[t, :]

    # Create two containers of zeros for the respective calculated flows
    # Differentiate into FNR rate being positive or negative
    pathways_FNRpos = pd.DataFrame(
        np.zeros((fluxes.shape[0], 4)),
        columns=["linear", "alternate", "cyclic", "respiratory"],
        index=t,
    )
    pathways_FNRneg = pathways_FNRpos.copy()

    # Get the amount of electron outflux by TOX
    outflux_TOX = fluxes["vbd"] * 4 + fluxes["vaa"] * 4 + fluxes["vFlv"] * 4

    # The the sign of vFNR for deciding which pathway calculation should be used
    pos_vFNR = fluxes["vFNR"] >= 0

    # Calculate the rates assuming a positive FNR rate
    if np.any(pos_vFNR):
        # Get the electron infux fraction of PS2
        influx_ps2 = (
            fluxes["vPS2"]
            * 2
            / (fluxes["vPS2"] * 2 + fluxes["vSDH"] * 2 + fluxes["vNDH"] * 2)
        )

        # Linear flow happens through FNR
        pathways_FNRpos["linear"] = fluxes["vFNR"] * 2 * influx_ps2

        # Cyclic flow happens through NQ
        pathways_FNRpos["cyclic"] = fluxes["vNQ"] * 2

        # Respiration happens through SDH and NDH2
        pathways_FNRpos["respiratory"] = fluxes["vSDH"] * 2 + fluxes["vNDH"] * 2

        # The alternate electron flow is the amount of TOX flux scaled to the amount of electron influx by PS2
        pathways_FNRpos["alternate"] = outflux_TOX * influx_ps2

    # Calculate the rates assuming a negative FNR rate
    if np.any(np.invert(pos_vFNR)):
        # Get the electron infux fraction of PS2
        influx_ps2 = (
            fluxes["vPS2"]
            * 2
            / (
                fluxes["vPS2"] * 2
                + fluxes["vSDH"] * 2
                + fluxes["vNDH"] * 2
                + -fluxes["vFNR"] * 2
            )
        )

        # If FNR is reversed, no linear flow can happen (keep at 0)

        # Cyclic flow happens through FQ and NQ, scaled to the amount of electron flow through PS1 compared to FNR
        pathways_FNRneg["cyclic"] = (fluxes["vNQ"] * 2) * (
            fluxes["vPS1"] / (fluxes["vPS1"] + -fluxes["vFNR"] * 2)
        )

        # Respiration happens through SDH and NDH2 and FNR
        pathways_FNRneg["respiratory"] = (
            fluxes["vSDH"] * 2 + fluxes["vNDH"] * 2 + -fluxes["vFNR"] * 2
        )

        # The alternate electron flow is the amount of TOX flux scaled to the amount of electron influx by PS2
        pathways_FNRneg["alternate"] = outflux_TOX * influx_ps2

    # Merge the dataframes according to the sign of vFNR
    pathways = pathways_FNRpos.copy()
    pathways.loc[np.invert(pos_vFNR), :] = pathways_FNRneg.loc[np.invert(pos_vFNR), :]

    return pathways


def plot_PAM(s):
    res = s.get_full_results_dict()
    PS2q = res["PSIIq"] / s.model.get_parameter("PSIItot")

    # Rescale the quenching to be on the same height as the fluorescence
    scale_factor = np.max(res["Fluo"]) / np.max(PS2q)

    # Plot Fluorescence and the quenching concentration
    fig, ax = plt.subplots(**plt_defaults["figure"])
    ax = set_ax_default(ax)

    ax.plot(s.get_time(), res["Fluo"], label="Fluorescence", **plt_defaults["plot"])
    ax.plot(
        s.get_time(), PS2q * scale_factor, label="Quenching", **plt_defaults["plot"]
    )

    # Set a second y axis to display the rescaled quenching
    secax_y = ax.secondary_yaxis(
        "right", functions=(lambda x: x / scale_factor, lambda x: x / scale_factor)
    )
    secax_y.set_ylabel("Fraction of quenched PSII", rotation=-90, labelpad=20)
    secax_y = set_ax_default(secax_y)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Fluorescence [AU]")
    ax.legend(**get_plt_default("legend", bbox_to_anchor=(1.07, 1)))

    return fig, ax


def get_productivity(s):
    fluxes = s.get_fluxes_dict()
    return (
        fluxes["vCBB"] + fluxes["vPRsalv"] - fluxes["vRespiration"] - fluxes["vOxy"] * 2
    )


def get_evaluation_timed(s, ts, func):
    res = func(s)
    return [x for x, t in zip(res, s.get_time()) if t in ts]


def plot_productivity_line(s, ts, xlabel="", ticks=None):
    # Get the productivity at the different times
    productivity = get_evaluation_timed(s, ts, get_productivity)

    if ticks is None:
        ticks = ts

    # Initialise a plot
    fig, ax = plt.subplots(**plt_defaults["figure"])
    ax = set_ax_default(ax)

    ax.plot(ticks, productivity, label="Productivity", **plt_defaults["plot"])

    ax.set_xlabel(xlabel)
    ax.set_ylabel("3PGA production [mmol mol(Chl)$^{-1}$ s$^{-1}$]")
    ax.legend(**plt_defaults["legend"])

    return fig, ax


# PSII yield
def get_PSII_yield(s):
    # (FM - F0) / FM
    m_params = s.model.parameters

    # Get the siulation outputs
    res = s.get_full_results_dict()
    # Calculate the maximal reachable fluorescence at every time point
    PSIIq = res["PSIIq"]
    ps2cs = 0.5
    kH = m_params["kHst"] * (PSIIq / m_params["PSIItot"])
    fluo_max = (ps2cs * m_params["kF"] * m_params["PSIItot"]) / (
        m_params["kF"] + m_params["kH0"] + kH
    )

    return (fluo_max - res["Fluo"]) / fluo_max


def plot_PSII_yield_line(s, ts, xlabel="", ticks=None):
    # Get the productivity at the different times
    PSIIyield = get_evaluation_timed(s, ts, get_PSII_yield)

    if ticks is None:
        ticks = ts

    # Initialise a plot
    fig, ax = plt.subplots(**plt_defaults["figure"])
    ax = set_ax_default(ax)

    ax.plot(ticks, PSIIyield, label="PSII yield", **plt_defaults["plot"])

    ax.set_xlabel(xlabel)
    ax.set_ylabel("PSII yield [unitless]")
    ax.legend(**plt_defaults["legend"])

    return fig, ax


### Simulate experiments ###
# def simulate_PAM(s, actinic:tuple, saturating:tuple, cycles, final_actinic=False):
#     # Unpack light intensities and durations
#     L_act, t_act = actinic
#     L_sat, t_sat = saturating

#     # Set the current end time
#     t_curr = s.time

#     if t_curr is None:
#         t_curr = 0
#     else:
#         t_curr = s.get_time()[-1]

#     # Iterate through the PAM cycles
#     for i in range(cycles):
#         # Actinic phase
#         t_curr += t_act
#         s.update_parameter("pfd", L_act)
#         s.simulate(t_curr)

#         # Saturating pulse
#         t_curr += t_sat
#         s.update_parameter("pfd", L_sat)
#         s.simulate(t_curr)

#     if final_actinic:
#         t_curr += t_act
#         s.update_parameter("pfd", L_act)
#         s.simulate(t_curr)

#     return s


def repeat_light_simulation(s, s_idol):
    """Repeat a light phase simulation with a second model

    Args:
        s (Simulator): The model to be simulated after the model
        s_idol (Simulator): A model simulated in time phases where only the pfd parameter is changed

    Raises:
        ValueError: Raises an error if s has been simulated before

    Returns:
        Simulator: The model s with simulated light phases and times equal to s_idol
    """
    # The resimulator model must be newly build and not run
    if s.time is not None:
        raise ValueError("The model s must not be run previously")

    # Get time and light to be resimulated
    for i, time in enumerate(s_idol.time):
        pfd = s_idol.simulation_parameters[i]["pfd"]

        # Simulate the lightphase
        s.update_parameter("pfd", pfd)
        s.simulate(time_points=time)

    return s


# Simulate the  model in light intensity phases
# def simulate_lightphases(m, y0, lights, phase_time):
#     m_phase = m.copy()
#     s_phase = Simulator(m_phase)
#     s_phase.initialise(y0)

#     ts_phase = np.arange(1,len(lights)+1) * phase_time

#     if isinstance(lights[0],(float, int)):
#         n_light = len(m.parameters["pfd"])
#         lights = [np.full(n_light, light) for light in lights]

#     for t,pfd in zip(ts_phase, lights):
#         s_phase.update_parameter("pfd", pfd)
#         t_phase, y_phase = s_phase.simulate(t)

#     return s_phase

# def get_irradiance(s):
#     irradiance = [np.sum(x["pfd"]) for x in s.simulation_parameters]
#     return np.array(irradiance)


def get_phase_times(s, include_first=False):
    times = [x[-1] for x in s.time]
    if include_first:
        times = np.append(s.time[0][0], times)
    return np.array(times)


### Compare two similar models or simulations ###
def compare_simulations(s1, s2, thresh=1e-2):
    # Differences in results
    res1 = s1.get_full_results_df()
    res2 = s2.get_full_results_df()

    # Normalise the differences
    # Add 1e-10 to avoid dividing by 0
    res_diff = (res1 - res2) / (res1 + 1e-10)

    # Determine if the maximal difference is above the thshold for some compounds
    res_signif = np.max(res_diff, axis=0) >= thresh

    # Differences in fluxes
    flx1 = s1.get_fluxes_df()
    flx2 = s2.get_fluxes_df()

    flx_diff = flx1 - flx2
    flx_diff = np.abs(flx_diff) / (np.abs(flx1) + 1e-10)

    # Determine if the maximal difference is above the thshold for some compounds
    flx_signif = np.max(flx_diff, axis=0) >= thresh

    return res_signif, flx_signif


def compare_models(m1, m2, y0, t=None, thresh=1e-2):
    """Compare two models in a given time"""
    # Initialise both models
    s1 = Simulator(m1)
    s2 = Simulator(m2)

    s1.initialise(y0)
    s2.initialise(y0)

    if t is None:
        t = np.linspace(0, 100, 1000)

    # Simulate both models
    y1, t1 = s1.simulate(time_points=t)
    y2, t2 = s2.simulate(time_points=t)

    # Get the differences in compounds and fluxes
    res_signif, flx_signif = compare_simulations(s1, s2, thresh=1e-2)

    return s1, s2, (res_signif, flx_signif)


# Plot the simulation
def plot_model_comparison(s1, s2, comp):
    # Get the significant compounds and fluxes
    cmp, flx = comp

    cmps = list(cmp[cmp].index)
    flxs = list(flx[flx].index)

    # Create a plot for the compounds with one subplot

    # Plot the significant compounds
    time = s1.get_time()
    compounds1 = s1.get_full_results_dict()
    compounds2 = s2.get_full_results_dict()

    fluxes1 = s1.get_fluxes_dict()
    fluxes2 = s2.get_fluxes_dict()

    # Create containes to store figures and axes
    figs = {}
    axs = {}

    for elms, nam in ((cmps, "cmps"), (flxs, "flxs")):
        # If there is no difference skip the plotting
        if len(elms) == 0:
            if nam == "cmps":
                warn("No differing compounds")
            else:
                warn("No differing fluxes")
            continue

        # Define the elements to be plotted
        if nam == "cmps":
            elements1, elements2 = compounds1, compounds2
            plot_title = "Differing Compounds"
        else:
            elements1, elements2 = fluxes1, fluxes2
            plot_title = "Differing Fluxes"

        # Try to make the layout as square as possible
        # If that isnt possible, make the column number smaller
        # and adjust the rows so there are enough plots
        elm_len = np.sqrt(len(elms))
        if elm_len.is_integer():
            elm_size = (int(elm_len), int(elm_len))
        else:
            if len(elms) % int(elm_len) == 0:
                elm_size = (len(elms) // int(elm_len), int(elm_len))
            else:
                elm_size = (len(elms) // int(elm_len) + 1, int(elm_len))

        # Initialise the plot
        fig, ax = plt.subplots(elm_size[0], elm_size[1])

        if len(elms) > 1:
            ax = ax.flatten()
        else:
            ax = np.array([ax])
        fig.set_size_inches(20, 14)
        fig.suptitle(plot_title, fontsize=16)

        for i in range(len(elms)):
            # For every element set up a plot
            elm = elms[i]
            ax[i].plot(time, elements1[elm], label="1")
            ax[i].plot(time, elements2[elm], label="2")
            ax[i].set_title(elm)

        fig.tight_layout()

        figs[nam] = fig
        axs[nam] = ax

    return figs, axs


# Save figures
def savefig_dated(fig, name, type=None, path="figures", format="%Y%m%d%H%M", **kwargs):
    """Save a figure with the current date as prefix

    Args:
        fig (matplotlib.figure.Figure): The figure to be saved
        path (str): The folder path the fig should be saved to including
        name (str): The name the figure should be saved to excluding the prefix
    """
    # Create the path
    now = datetime.now().strftime(format)

    if type is None:
        # Save the figure
        fig.savefig(fullpath, **kwargs)
    elif isinstance(type, list):
        for _type in type:
            fullpath = f"{path}/{now}_{name}.{_type}"
            
            # Save the figure
            fig.savefig(fullpath, **kwargs)
    else:
        raise ValueError("type should be a list of image types as strings")


# Get the essential parameters and remove all others from the model
def get_essential_params(m):
    # Get the essential parameters by removing all and checking for missing
    m2 = m.copy()
    rm_par = [
        x for x in m.get_parameters().keys() if x not in m.derived_parameters.keys()
    ]
    m2.remove_parameters(rm_par)
    return tuple(m2.check_missing_parameters())


def reduce_parameters(m):
    # Get the essential parameters (including derived)
    essential_params = list(get_essential_params(m))
    essential_params += m.derived_parameters.keys()

    # remove all parameters but the essential
    rm_par = [x for x in m.get_parameters().keys() if x not in essential_params]
    m.remove_parameters(rm_par)

    return m


# Add a function that sorts the algebraic modules until the modlbase bug is fixed
def sort_algmodules(m):
    # Make a copy of the algebraic modules and replace them in the model with a sorted dict
    print("Additionally sorting algebraic modules...")

    am_copy = m.algebraic_modules.copy()
    am_order = m._algebraic_module_order

    m.remove_algebraic_modules(list(reversed(am_order)))

    for key in am_order:
        m.add_algebraic_module(module_name=key, **am_copy[key])

    return m


# Edit plots after creation
# Capitalise the labels
def capfirst(s):
    return s[:1].upper() + s[1:]


def capitalise_axlables(axes):
    if not isinstance(axes, np.ndarray):
        axes_wrk = [axes]
    else:
        axes_wrk = axes.flatten()

    for ax in axes_wrk:
        ax.set_xlabel(capfirst(ax.get_xlabel()))

        if ax.get_ylabel() != "pH":
            ax.set_ylabel(capfirst(ax.get_ylabel()))
        else:
            ax.set_ylabel(ax.get_ylabel())
    return axes


def adjust_labelsizes(ax, size=17):
    ax.title.set_fontsize(size)
    ax.xaxis.label.set_fontsize(size)
    ax.yaxis.label.set_fontsize(size)
    ax.tick_params(axis="x", labelsize=size)
    ax.tick_params(axis="y", labelsize=size)

    try:
        ax.zaxis.label.set_fontsize(size)
        ax.tick_params(axis="z", labelsize=size)
    except AttributeError:
        pass
    return ax


# Protocol functions
# Create a protocol for PAM experiments
def create_protocol_PAM(
    actinic: tuple,
    saturating: tuple,
    cycles,
    init=0,
    first_actinic_time=None,
    final_actinic_time=None,
):
    # If init is a starting time use it as such, otherwise extract it from the given protocol
    if isinstance(init, (int, float)):
        t_start = init
    elif isinstance(init, pd.core.frame.DataFrame):
        t_start = init.iloc[-1, 0]
    else:
        raise ValueError("init must be starting time or a protocol")

    # Unpack light intensities and durations
    L_act, t_act = actinic
    L_sat, t_sat = saturating

    if first_actinic_time is not None:
        t_plan = [t_start] + [first_actinic_time, t_sat] + [t_act, t_sat] * (cycles - 1)
    else:
        t_plan = [t_start] + [t_act, t_sat] * cycles

    if final_actinic_time is not None:
        # If a final actinic phase should be added, add the time to the list
        t_plan.append(final_actinic_time)

    t_plan = np.array(t_plan).cumsum()[1:]
    t_plan = pd.DataFrame(t_plan, columns=["t_end"])

    # Accumulate the lights in a DataFrame
    lights = [L_act, L_sat] * cycles

    if final_actinic_time is not None:
        # If a final actinic phase should be added, add the light intensity to the list
        lights.append(L_act)

    # Make into a DataFrame, naming the columns "_light_index"
    lights = pd.concat(lights, axis=1).T
    lights.columns = ["_light_" + str(col) for col in lights.columns]
    lights = lights.reset_index().iloc[:, 1:]

    # Make into a pd.DataFrame type protocol wih lights and end times
    protocol = pd.concat([t_plan, lights], axis=1)
    protocol = protocol.reset_index().iloc[:, 1:]

    # If a starting protocol was given, append the new one
    if isinstance(init, pd.core.frame.DataFrame):
        protocol = pd.concat([init, protocol], axis=0)
        protocol = protocol.reset_index().iloc[:, 1:]
    return protocol


# Create a protocol for constant light
def create_protocol_const(
    light: pd.Series, time: float, init: Union[None, pd.DataFrame] = None
):
    if init is None:
        t_start = 0
    elif isinstance(init, pd.DataFrame):
        t_start = init.iloc[-1, 0]
    else:
        raise ValueError("init must be None or a protocol")

    t_end = t_start + time
    t_end = pd.DataFrame(t_end, index=[0], columns=["t_end"])

    # Reformat the lights
    lights = pd.DataFrame(light).T
    lights.columns = ["_light_" + str(col) for col in lights.columns]
    lights = lights.reset_index().iloc[:, 1:]

    protocol = pd.concat([t_end, lights], axis=1)

    if isinstance(init, pd.core.frame.DataFrame):
        protocol = pd.concat([init, protocol], axis=0)
        protocol = protocol.reset_index().iloc[:, 1:]

    return protocol


# # Create a protocol for phases of different light with the same length
# def create_protocol_lightphases(lights, common_time, init=0,):
#     # If init is a startin time use it as such, otherwise extract it from the given protocol
#     if isinstance(init, (int,float)):
#         t_start = init
#     elif isinstance(init, pd.core.frame.DataFrame):
#         t_start = init.iloc[-1,0]
#     else:
#         raise ValueError("init must be starting time or a protocol")

#     # crate a end-time plan for the given lights
#     if isinstance(lights, np.ndarray):
#         # Convert lights to DataFrame
#         lights = pd.DataFrame(lights, columns=[f"light_{i}" for i in range(lights.shape[1])])

#         # Crate an array with the increasing simulation times
#         t_plan = np.repeat(common_time, lights.shape[0])
#         t_plan = np.append(t_start, t_plan).cumsum()[1:]
#         t_plan = pd.DataFrame(t_plan, columns=["t_end"])
#     else:
#         raise ValueError("Only np.ndarray type light input supported for now")

#     # Make into a pd.DataFrame type protocol wih lights and end times
#     protocol = pd.concat([t_plan, lights], axis=1)
#     protocol.reset_index()

#     return protocol


def get_light(df: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """Get the light information in a protocol

    Args:
        df (Union[pd.Series,pd.DataFrame]): a protocol or a row of such

    Returns:
        Union[pd.Series,pd.DataFrame]: the contained light information in the appropriate shape
    """
    # Get the light columns / indexes, subset and rename
    if isinstance(df, pd.DataFrame):
        idx_bool = df.columns.str.startswith("_light_")
        idx = df.columns[idx_bool]
        light_names = idx.str.removeprefix("_light_")

        light = df.loc[:, idx_bool]
        try:
            light.columns = light_names.to_numpy().astype("int")
        except:
            light.columns = light_names.to_numpy().astype("float")
    elif isinstance(df, pd.Series):
        idx_bool = df.index.str.startswith("_light_")
        idx = df.index[idx_bool]
        light_names = idx.str.removeprefix("_light_")

        light = df.loc[idx_bool]
        try:
            light.index = light_names.to_numpy().astype("int")
        except:
            light.index = light_names.to_numpy().astype("float")

    return light


# Simulate a given protocol
simulator_kwargs = {
    "default": {
        "maxsteps": 10000,
        "atol": 1e-8,
        "rtol": 1e-8,
        "maxnef": 4,  # max error failures
        "maxncf": 1,  # max convergence failures
    },
    "assimulo_default": {
        "maxsteps": 10000,
        "maxnef": 7,
        "maxncf": 10,
        "atol": 1e-6,
        "rtol": 1e-6,
    },
    "loose": {"maxsteps": 20000, "maxnef": 10, "maxncf": 10},
    "very_loose": {
        "maxsteps": 20000,
        "maxnef": 10,
        "maxncf": 10,
        "atol": 1e-6,
        "rtol": 1e-6,
    },
}


def update_simulator_from_protocol(s, protocol, step):
    row = protocol.iloc[step, :]
    pfd = get_light(row)
    s.update_parameter("pfd", pfd)
    return s


def simulate_protocol(
    s,
    protocol,
    progbar=False,
    return_unsuccessful=False,
    retry_unsuccessful=False,
    retry_kwargs=simulator_kwargs["loose"],
    n_timepoints = None,
    verbose = False,
    **integrator_kwargs,
):
    # Set the current end time
    t_curr = s.time

    if t_curr is None:
        t_curr = 0
    else:
        t_curr = s.get_time()[-1]

    # Check if that time is not higher than the smallest protocol time
    if t_curr >= protocol["t_end"].iloc[-1]:
        raise ValueError(
            "The model was already simulated further than the earliest protocol time"
        )

    if progbar:
        iter = tqdm(protocol.iterrows(), total=protocol.shape[0])
    else:
        iter = protocol.iterrows()

    # Iterate through the protocol rows
    for i, row in iter:
        # Get the new light parameter
        pfd = get_light(row)
        s.update_parameter("pfd", pfd)

        # Simulate until the given end-time
        # If a number of points to be evaluated is given, generate the necessary points
        if n_timepoints is None:
            # s, t, y = s.simulate(row["t_end"], **integrator_kwargs)
            s, t, y = simulate_with_retry(s, t_end=row["t_end"], integrator_kwargs=integrator_kwargs, retry_kwargs=retry_kwargs, verbose=verbose)
        else:
            # t, y = s.simulate(row["t_end"], steps=n_timepoints, **integrator_kwargs)
            s, t, y = simulate_with_retry(s, t_end=row["t_end"], steps=n_timepoints, integrator_kwargs=integrator_kwargs, retry_kwargs=retry_kwargs, verbose=verbose)

        if t is None:
            if verbose:
                warn(f"protocol simulation unsuccessful, failed at step {i} to t = {row['t_end']}")
            if return_unsuccessful:
                s.update_parameter("pfd", pfd)
                return s
            else:
                return None

    return s


# Remove pulses from a Simulation
def _remove_beginning(s, i, cutofftime):
    if s.time[i][-1] < cutofftime:
        raise ValueError("End time must be larger than removal threshold")

    keepbool = s.time[i] > cutofftime

    # Remove
    s.time[i] = s.time[i][keepbool]
    s.results[i] = s.results[i][keepbool]

    if s.fluxes is not None:
        s.fluxes[i] = s.fluxes[i][keepbool]

    if s.full_results is not None:
        s.full_results[i] = s.full_results[i][keepbool]

    return s


def remove_pulses_from_simulation(
    s, light_max=1000, pad_trim_time=0, trim_beginning=0, remove_spanned_phases=False
):
    # Make all edits on a copy
    s = s.copy()

    # Determine the pulses and their time intervals
    lights = pd.DataFrame([x["pfd"] for x in s.simulation_parameters])
    remove = pulse = is_pulse(lights, light_max)

    endtimes = np.array([x[-1] for x in s.time])
    pulseendtimes = endtimes[pulse]

    # Pad the ending times and remove data from the adjacent simulation
    if pad_trim_time > 0:
        pulseendtimes += pad_trim_time
        afterpulses = np.where(pulse)[0] + 1

        for i, ap in enumerate(afterpulses):
            if s.time[ap][-1] <= pulseendtimes[i]:
                if not remove_spanned_phases:
                    raise UserWarning(
                        "The given pad_trim_time would lead to the complete deletion of a non-pulse phase. If this is accepatable, set remove_spanned_phases to True"
                    )
                else:
                    remove[ap] = True
            else:
                s = _remove_beginning(s, ap, pulseendtimes[i])

                keepbool = s.time[ap] > pulseendtimes[i]

                # Remove
                s.time[ap] = s.time[ap][keepbool]
                s.results[ap] = s.results[ap][keepbool]

                if s.fluxes is not None:
                    s.fluxes[ap] = s.fluxes[ap][keepbool]

                if s.full_results is not None:
                    s.full_results[ap] = s.full_results[ap][keepbool]

    # Trim the beginning
    if trim_beginning > 0:
        s = _remove_beginning(s, 0, trim_beginning)

    # Remove the pulses
    for obj in ["time", "results", "simulation_parameters", "fluxes", "full_results"]:
        val = getattr(s, obj)

        if val is None:
            next
        else:
            new = [v for v, b in zip(val, remove) if not b]
            setattr(s, obj, new)

    return s


# Remove the beginning of a simulation
def remove_beginning_from_simulation(s, cutofftime):
    s = s.copy()
    if 0 > cutofftime:
        raise ValueError("cutofftime must be larger than 0")
    if s.get_time()[-1] < cutofftime:
        raise ValueError("End time must be larger than cutofftime")

    keepphase = np.array([s.time[i][-1] > cutofftime for i in range(len(s.time))])
    cutting_phase = np.where(keepphase)[0][0]
    keepinphase = s.time[cutting_phase] > cutofftime

    # Remove pre-cutoff phases
    s.time = list((np.array(s.time, dtype=object) - cutofftime)[keepphase])
    s.time[0] = s.time[0][keepinphase]
    s.results = list(np.array(s.results, dtype=object)[keepphase])
    s.results[0] = s.results[0][keepinphase]

    if s.fluxes is not None:
        s.fluxes = list(np.array(s.fluxes, dtype=object)[keepphase])
        s.fluxes[0] = s.fluxes[0][keepinphase]

    if s.full_results is not None:
        s.full_results = list(np.array(s.full_results, dtype=object)[keepphase])
        s.full_results[0] = s.full_results[0][keepinphase]
    return s


# Preparing a model for steady state analysis
default_exch_dict = {
    "3PGA": {"k": 10, "thresh": 1000},
}

# Define the exchange kinetic as mass action
def _exch(S, k, thresh):
    return k * (S - thresh)


def add_exchange(m, exch_dict=default_exch_dict):
    # Make a copy of the model, in case the mca adaption version should not be applied to the original model
    m = m.copy()

    for key, val in exch_dict.items():
        # Add the exchange parameters
        m.add_parameters(
            {
                f"kExch_{key}": val["k"],
                f"threshExch_{key}": val["thresh"],
            }
        )

        # Add the exchange reaction
        m.add_reaction(
            rate_name=f"vExch_{key}",
            function=_exch,
            stoichiometry={
                key: -1,
            },
            dynamic_variables=[key],
            parameters=[f"kExch_{key}", f"threshExch_{key}"],
            reversible=True,
        )
    return m


# Save and load objects
def _get_suffix(method):
    if method in ["dill", "pickle", "json"]:
        return method
    else:
        raise ValueError(f"method {method} unsupported")


def _search_Simulators(obj, i):
    if i > 1:
        return False
    if isinstance(obj, _Simulate):
        return True
    elif isinstance(obj, list):
        for x in obj:
            if _search_Simulators(x, i + 1):
                return True
    elif isinstance(obj, dict):
        for x in obj.values():
            if _search_Simulators(x, i + 1):
                return True
    return False


def save_obj_dated(obj, name, path="", method="dill", format="%Y%m%d%H%M"):
    suffix = _get_suffix(method)
    now = datetime.now().strftime(format)
    fullpath_ns = f"{path}/{now}_{name}"
    fullpath = f"{fullpath_ns}.{suffix}"

    if _search_Simulators(obj, 0):
        raise ValueError(
            "The object contains a Simulator object, please use the function ''save_Simulator_dated'"
        )

    if method == "dill":
        with open(fullpath, "wb") as handle:
            dill.dump(obj, handle, protocol=dill.HIGHEST_PROTOCOL)
    else:
        raise ValueError(f"method {method} unsupported")


def _get_filepath_dated(name, suffix=None, path="", date=None, datelength=12):
    if suffix is not None:
        suffix = f".{suffix}"
    else:
        suffix = ""

    if date is None:
        # Find the matching files
        files = np.array(os.listdir(None if path == "" else path))
        matches = sorted(
            files[
                np.array(
                    [
                        bool(re.match(f"[0-9]{{{datelength}}}_{name}{suffix}$", file))
                        for file in files
                    ]
                )
            ]
        )

        if len(matches) == 0:
            raise FileNotFoundError(
                f"No file with the structure '{'X'*datelength}_{name}{suffix}' found in {path}"
            )

        fullpath = f"{path}/{matches[-1]}"
        fullpath_ns = fullpath.removesuffix(f"{suffix}")
    else:
        fullpath_ns = f"{path}/{date}_{name}"
        fullpath = f"{fullpath_ns}{suffix}"
    return fullpath_ns, fullpath


def load_obj_dated(name, path="", date=None, method="dill", datelength=12):
    suffix = _get_suffix(method)
    fullpath_ns, fullpath = _get_filepath_dated(name, suffix, path, date, datelength)

    # Get the file
    if method == "dill":
        with open(fullpath, "rb") as handle:
            obj = dill.load(handle)
    else:
        raise ValueError(f"method {method} unsupported")
    return obj


# Save Simulators
def _convert_Simulator_for_save(s, save_fluxes=False, save_full_results=False):
    time = s.get_time(concatenated=False)
    if time is None or s.results is None:
        raise ValueError("Cannot save results, since none are stored in the simulator")

    results = [i.tolist() for i in s.results]
    parameters = cast(List[Dict[str, float]], s.simulation_parameters)

    to_export = {
        "results": results,
        "time": [i.tolist() for i in time],
        "parameters": parameters,
        "model": s.model,
        "type": None,
    }

    if save_fluxes:
        if s.fluxes is None:
            s._calculate_fluxes()
        fluxes = [i.tolist() for i in s.fluxes]
        to_export.update({"fluxes": fluxes})

    if save_full_results:
        if s.full_results is None:
            s._calculate_full_results()
        full_results = [i.tolist() for i in s.full_results]
        to_export.update({"full_results": full_results})
    return to_export


def save_Simulator_dated(
    s, name, path, method="pickle", save_fluxes=False, save_full_results=False, format="%Y%m%d%H%M"
):
    suffix = _get_suffix(method)
    now = datetime.now().strftime(format)
    fullpath_ns = f"{path}/{now}_{name}"
    fullpath = f"{fullpath_ns}.{suffix}"

    if isinstance(s, _Simulate):
        to_export = _convert_Simulator_for_save(
            s, save_fluxes=save_fluxes, save_full_results=save_full_results
        )
        to_export["type"] = "Simulator"
    elif isinstance(s, list):
        to_export = {
            "data": [
                _convert_Simulator_for_save(
                    _s, save_fluxes=save_fluxes, save_full_results=save_full_results
                )
                for _s in s
            ]
        }
        to_export["type"] = "list"
    elif isinstance(s, dict):
        to_export = {
            "data": {
                k: _convert_Simulator_for_save(
                    _s, save_fluxes=save_fluxes, save_full_results=save_full_results
                )
                for k, _s in s.items()
            }
        }
        to_export["type"] = "dict"
    else:
        raise ValueError(f"unrecognised type of s: {type(s)}")

    if method == "json":
        with open(fullpath, "w") as f:
            json.dump(obj=to_export, fp=f)
    elif method == "pickle":
        with open(fullpath, "wb") as fb:
            pickle.dump(obj=to_export, file=fb)
    else:
        raise ValueError(f"Can only save to json or pickle, got {method}")


def _create_Simulator_for_load(to_import):
    m = to_import["model"]
    y0 = {k: v for k, v in zip(m.compounds, to_import["results"][0][0])}

    s = Simulator(m)
    s.initialise(y0)
    s.time = [np.array(i) for i in to_import["time"]]
    s.results = [np.array(i) for i in to_import["results"]]
    s.simulation_parameters = to_import["parameters"]

    if "fluxes" in to_import:
        s.fluxes = [np.array(i) for i in to_import["fluxes"]]
    if "full_results" in to_import:
        s.full_results = [np.array(i) for i in to_import["full_results"]]
    return s


def load_Simulator_dated(name, path, date=None, method="pickle", datelength=12):
    # Replace the dill method with pickle for default saving
    suffix = _get_suffix(method)
    fullpath_ns, fullpath = _get_filepath_dated(name, suffix, path, date, datelength)

    if method == "json":
        with open(fullpath, "r") as f:
            to_import = json.load(fp=f)
    elif method == "pickle":
        with open(fullpath, "rb") as fb:
            to_import = pickle.load(file=fb)
    else:
        raise ValueError(f"Can only load from to json or pickle, got {method}")

    # Create and populate the Simulator
    type = to_import.get("type")
    if type is None or type == "Simulator":
        s = _create_Simulator_for_load(to_import)
    elif to_import["type"] == "list":
        s = [_create_Simulator_for_load(_to_import) for _to_import in to_import["data"]]
    elif to_import["type"] == "dict":
        s = {
            k: _create_Simulator_for_load(_to_import)
            for k, _to_import in to_import["data"].items()
        }
    else:
        raise ValueError(f"unrecognised type of loaded object: {type(to_import)}")

    return s


# Adapted initial consitions
def get_steadystate_y0(
    m,
    y0,
    light=lip.light_spectra("solar", 0.1),
    steadystate_kwargs={"tolerance": 1e-3},
    verbose=False,
):
    _m = m.copy()
    _m = add_exchange(_m)
    _m.update_parameter("pfd", light)

    s = Simulator(_m)
    s.initialise(y0)
    _t, yss = s.simulate_to_steady_state(**steadystate_kwargs)
    if _t is None:
        raise RuntimeError("The model couldn't be simulated to steady state")
    if verbose:
        print(f"steady state simulation ran for {s.get_time()[-1]} time units")
    return s.get_results_df().squeeze().to_dict()


# Plot annotation for missing steady states
def add_na_annotation(ax, df, textsize=5, text="no\nsteady-state"):
    xpos = np.linspace(0, 1, 2 * df.shape[1] + 1)[1::2]
    ypos = np.linspace(0, 1, 2 * df.shape[0] + 1)[1::2]
    posmesh = np.meshgrid(xpos, ypos)

    nans = np.isnan(df.to_numpy())
    textpos = [posmesh[x][nans] for x in range(2)]

    # ax.scatter(*textpos, transform=ax.transAxes)
    for x, y in zip(*textpos):
        ax.text(
            x, y, text, transform=ax.transAxes, ha="center", va="center", size=textsize
        )
    return ax


# Heatmap plot with possibility for adapting colorbar label
def plot_heatmap(data, xlab=None, ylab=None, clab=None, ax=None):
    _data = data.values.astype(float)
    rows = data.index
    cols = data.columns

    if xlab is None:
        xlab = cols.name
    if ylab is None:
        ylab = rows.name

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    hm = ax.pcolormesh(_data)

    ax.set_xticks(np.arange(len(cols)) + 0.5)
    ax.set_xticklabels(cols)

    ax.set_yticks(np.arange(len(rows)) + 0.5)
    ax.set_yticklabels(rows)

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    fig.colorbar(hm, ax=ax, label=clab)
    return fig, ax
