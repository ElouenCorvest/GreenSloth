import copy
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from mxlpy import Model, scan, units
from sympy.physics.units import Unit, bar

def _calc_ass(vc: float, gammastar: float, r_light: float, co2: float):
    """Calculate carbon assimilation based on the min-W approach, as introduced by Farquhar, von Caemmerer and Berry in 1980 and "reevaluated" by Lochoki and McGrath in 2025 (https://doi.org/10.1101/2025.03.11.642611).

    Args:
        vc (float): Rubisco carboxylation rate [µmol m-2 s-1]
        gammastar (float): CO2 compensation point in the absence of non-photorespiratory CO2 release [µbar]
        r_light (float): Rate of non-photorespiratory CO2 release in the light [µmol m-2 s-1]
        co2 (float): CO2 partial pressure [µbar]

    Returns:
        float: Net carbon assimilation rate [µmol m-2 s-1]
    """
    return vc * (1 - gammastar / co2) - r_light


def inject_fvcb(
    model: Model,
    co2: str | None = None,
    vc: str | None = None,
    pco2: str | None = None,
    H_cp_co2: str | None = None,
    gammastar: str | None = None,
    r_light: str | None = None,
    A: str | None = None,
) -> tuple[
    Model,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
]:
    """Inject the FvCB model into a MxLpy model

    Args:
        model (Model): MxLpy model to inject the FvCB model into
        co2 (str | None, optional): CO2 concentration name in model. Defaults to None.
        vc (str | None, optional): Rubisco carboxylation rate name in model. Defaults to None.
        pco2 (str | None, optional): CO2 partial pressure name in model. Defaults to None.
        H_cp_co2 (str | None, optional): Henry's law constant for CO2 name in model. Defaults to None.
        gammastar (str | None, optional): CO2 compensation point name in model. Defaults to None.
        r_light (str | None, optional): Rate of non-photorespiratory CO2 release in the light name in model. Defaults to None.
        A (str | None, optional): Net carbon assimilation rate name in model. Defaults to None.

    Returns:
        tuple(model, co2, vc, pco2, H_cp_co2, gammastar, r_light, A): Injected model and variable names
    """
    # Copy inputted model to avoid modifying the original one
    model = copy.deepcopy(model)

    # If either co2 or vc is None, return without modifications
    if co2 is None or vc is None or A is not None:
        return (model, co2, vc, pco2, H_cp_co2, gammastar, r_light, A)

    # Check unit of vc, if in mM convert to µmol m-2 s-1 else assume in µmol m-2 s-1
    if model.get_raw_reactions()[vc].unit == (
        units.mmol / (units.liter * units.second)
    ):
        model.add_parameter(
            "Vstroma_factor", value=0.0112, unit=units.liter / units.sqm
        )

        model.add_derived(
            vc + " µmol m-2 s-1",
            fn=mM_to_µmol_per_m2,
            args=[vc, "Vstroma_factor"],
            unit=units.mmol / (units.sqm * units.second),
        )
        vc = vc + " µmol m-2 s-1"

    # Check what co2 is in model and get initial value
    if model.ids[co2] == "parameter":
        initial_val_co2 = model._parameters[co2].value
    elif model.ids[co2] == "variable":
        initial_val_co2 = model._variables[co2].initial_value

    # If pco2 is None add it as parameter based on initial co2 value and H_cp_co2
    if pco2 is None:
        # If H_cp_co2 is None add it as parameter
        if H_cp_co2 is None:
            model.add_parameter("H_cp_co2", 3.4e-4, unit=units.mmol / units.pascal)
            H_cp_co2 = "H_cp_co2"

        initial_val = initial_val_co2 / model._parameters[H_cp_co2].value
        model.add_parameter("pco2", initial_val, unit=units.micro * bar)
        pco2 = "pco2"

        # Remove original co2 from model and add it as derived from pco2 and H_cp_co2
        model._remove_id(name=co2)
        model.add_derived(
            co2, fn=calc_co2_conc, args=[pco2, H_cp_co2], unit=units.mmol / units.liter
        )

    if gammastar is None:
        model.add_parameter(
            gammastar := "gammastar",
            38.6,
            unit=units.micro * bar,
            source="https://doi.org/10.1101/2025.03.11.642611)",
        )

    if r_light is None:
        model.add_parameter(
            r_light := "r_light",
            1.0,
            unit=units.mmol / (units.sqm * units.second),
            source="https://doi.org/10.1101/2025.03.11.642611",
        )

    model.add_derived(
        A := "Assimilation",
        fn=_calc_ass,
        args=[vc, gammastar, r_light, pco2],
        unit=units.mmol / (units.sqm * units.second),
    )

    return (model, co2, vc, pco2, H_cp_co2, gammastar, r_light, A)


def calculate_assimilation_minW(
    pco2: float,
    v_cmax: float = 100,
    km_co2: float = 259,
    o2: float = 210,
    km_o2: float = 179,
    j: float = 170,
    gammastar: float = 38.6,
    tp: float = 11.8,
    alpha_old: float = 0,
    r_light: float = 1,
) -> tuple[float, float, float, float]:
    """Calculate carbon assimilation based on the min-W approach.

    Calculate carbon assimilation based on the min-W approach, as introduced by Farquhar, von Caemmerer and Berry in 1980 and "reevaluated" by Lochoki and McGrath in 2025 (https://doi.org/10.1101/2025.03.11.642611).

    Args:
        pco2 (float): [µbar] Partial pressure of CO2. Normally chloroplastic CO2 partial pressure (Cc), but may be interchanged with intercellular CO2 partial pressure (Ci) under simplification of infinite mesophyll conductance
        v_cmax (float, optional): [µmol m-2 s-1] Maximum rate of Rubisco carboxylation activity. Defaults to 100.
        km_co2 (float, optional): [µbar] Michaelis-Menten constant for CO2. Defaults to 259.
        o2 (float, optional): [mbar] Partial pressure of O2 in the vicinity of Rubisco. Defaults to 210.
        km_o2 (float, optional): [mbar] Michaelis-Menten constant for O2. Defaults to 179.
        j (float, optional): [µmol m-2 s-1] Potential rate of linear electron transport going to support RuBP regeneration at a given light intensity. Defaults to 170.
        gammastar (float, optional): [µbar] CO2 compensation point in the absence of non-photorespiratory CO2 release. Defaults to 38.6.
        tp (float, optional): [µmol m-2 s-1] Potential rate of TPU. Defaults to 11.8.
        alpha_old (float, optional): [] Fraction of remaining glycolate carbon not returned to the chloroplast after accounting for carbon released as co2. Defaults to 0.
        r_light (float, optional): [µmol m-2 s-1] Rate of non photorespiratory CO2 release in the light. Defaults to 1.

    Returns:
        A_n, wc, wj, wp: Carbon Assimilation rate and the three limiting rates
    """
    # Rubisco carboxylation limited rate
    wc = pco2 * v_cmax / (pco2 + km_co2 * (1 + o2 / km_o2))
    # RuBP regeneration limited rate
    wj = pco2 * j / (4 * pco2 + 8 * gammastar)
    # TPU limited rate
    if pco2 <= gammastar * (1 + 3 * alpha_old):
        wp = math.inf
    else:
        wp = 3 * pco2 * tp / (pco2 - gammastar * (1 + 3 * alpha_old))

    # Net assimilation rate
    vc = min(wc, wj, wp)
    A_n = vc * (1 - gammastar / pco2) - r_light

    return A_n, wc, wj, wp


def create_fvcb_fig(
    model: Model,
    pfd: str,
    co2: str | None,
    vc: str | None,
    pco2: str | None,
    H_cp_co2: str | None,
    gammastar: str | None,
    r_light: str | None,
    A: str | None,
):
    """_summary_

    Args:
        model (Model): MxLpy model with FvCB injected to create fig from
        pfd (str): Name of PPFD parameter in model
        co2 (str | None): Name of CO2 in model
        vc (str | None): Name of rubisco carboxylation rate in model
        pco2 (str | None): Name of CO2 partial pressure parameter in model
        H_cp_co2 (str | None): Name of Henry's law constant for CO2 name in model
        gammastar (str | None): Name of gammastar parameter in model
        r_light (str | None): Name of r_light parameter in model
        A (str | None): Name of A parameter in model

    Returns:
        _type_: _description_
    """

    # Range of pco2 to scan
    pco2_array = np.linspace(1, 800, 100)

    # Calculate FvCB model values
    A_fvcb = [calculate_assimilation_minW(pco2)[0] for pco2 in pco2_array]
    vc_fvcb = [min(calculate_assimilation_minW(pco2)[1:]) for pco2 in pco2_array]

    # Inject FvCB into model
    model, co2, vc, pco2, H_cp_co2, gammastar, r_light, A = inject_fvcb(
        model,
        co2=co2,
        vc=vc,
        pco2=pco2,
        H_cp_co2=H_cp_co2,
        gammastar=gammastar,
        r_light=r_light,
        A=A,
    )

    # If both vc and co2 are in model, run steady state scan
    if vc is not None and co2 is not None:
        model.update_parameter(pfd, 1000)
        variables, fluxes = scan.steady_state(
            model, to_scan=pd.DataFrame({pco2: pco2_array})
        )
        model_res = pd.concat([variables, fluxes], axis=1)
    else:  # Else no results
        model_res = None

    fig, ax = plt.subplots()

    # Stylings
    vc_model_color = "#a10b2b"
    A_model_color = "#ffab00"

    # Plot FvCB results
    ax.plot(
        pco2_array, A_fvcb, label="FvCB Assimilation", color="black", lw=5, alpha=0.7
    )
    ax.plot(
        pco2_array,
        vc_fvcb,
        label="FvCB Vc",
        color="lightgray",
        lw=5,
        alpha=0.7,
        ls="--",
    )
    # Plot model results if available
    if model_res is not None:
        ax.plot(
            model_res.index,
            model_res[vc],
            label="Model Vc",
            color=vc_model_color,
            lw=5,
            ls="--",
        )
        ax.plot(
            model_res.index,
            model_res[A],
            label="Model Assimilation",
            color=A_model_color,
            lw=5,
        )

    ax.set_ylim(-20, 50)
    ax.set_xlim(0, 800)
    ax.set_ylabel(r"Rate [$\mathrm{\mu mol\ m^{-2}\ s^{-1}}$]")
    ax.set_xlabel(r"$\mathrm{C_i}$ [$\mathrm{\mu bar}$]")

    # Custom legend
    x_length = 0.1

    # Coordinates (x, y) for legend elements in axes fraction
    legend_coords = [
        (0.55, 0.3),
        (0.7, 0.3),
        (0.9, 0.3),
        (0.55, 0.2),
        (0.7, 0.2),
        (0.9, 0.2),
        (0.55, 0.1),
        (0.7, 0.1),
        (0.9, 0.1),
    ]

    # Add text annotations for legend
    for idx, text in zip([1, 2, 3, 6], ["Vc", "Assimilation", "FvCB", "Model"]):
        ax.text(
            legend_coords[idx][0],
            legend_coords[idx][1],
            text,
            va="center",
            ha="center",
            transform=ax.transAxes,
        )

    # Add line segments for legend
    for idx, color in zip(
        [4, 5, 7, 8], ["lightgray", "black", vc_model_color, A_model_color]
    ):
        if color in ["lightgray", vc_model_color]:
            ls = "--"
        else:
            ls = "-"

        if color in [vc_model_color, A_model_color] and model_res is None:
            ax.text(
                legend_coords[idx][0],
                legend_coords[idx][1],
                "n.a.",
                va="center",
                ha="center",
                transform=ax.transAxes,
            )
            continue

        ax.add_line(
            Line2D(
                [
                    legend_coords[idx][0] - x_length / 2,
                    legend_coords[idx][0] + x_length / 2,
                ],
                [legend_coords[idx][1], legend_coords[idx][1]],
                color=color,
                lw=4,
                transform=ax.transAxes,
                ls=ls,
            )
        )

    return fig, ax