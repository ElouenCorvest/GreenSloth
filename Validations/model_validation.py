import copy
import math
from pathlib import Path

import matplotlib.pyplot as plt
import neonutilities as nu
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from mdutils.mdutils import MdUtils
from mxlpy import Model, Simulator, make_protocol, mca, plot, scan, units
from scipy.signal import find_peaks, peak_prominences
from sympy import Integer, Pow
from sympy.physics.units import Unit, bar
from sympy.printing.latex import LatexPrinter
import os


# Custom Latex Printer to handle units with negative integer exponents properly (Still need to be improved for more complex cases)
class RefinedUnitLatexPrinter(LatexPrinter):
    def _print_Pow(self, expr):
        # Custom handling for Unit objects with negative integer exponents
        if (
            isinstance(expr.base, Unit)
            and isinstance(expr.exp, Integer)
            and expr.exp < 0
        ):
            base_str = self._print(expr.base)
            exp_str = self._print(expr.exp)
            return f"{base_str}^{{{exp_str}}}"
        # Fallback to default behavior for other Pow expressions
        return super()._print_Pow(expr)

    def _print_Mul(self, expr):
        # Separate terms with positive and negative exponents
        positive_terms = []
        negative_terms = []

        for arg in expr.args:
            # Check if the argument is a Pow of a Unit with a negative integer exponent
            if (
                isinstance(arg, Pow)
                and isinstance(arg.base, Unit)
                and isinstance(arg.exp, Integer)
                and arg.exp < 0
            ):
                negative_terms.append(arg)
            else:
                positive_terms.append(arg)

        # Print positive terms and negative terms
        # SymPy's default _print(Unit) for millimeter is \text{mm}, so no extra \cdot is needed within it.
        printed_positive_terms = [self._print(t) for t in positive_terms]
        printed_negative_terms = [self._print(t) for t in negative_terms]

        all_printed_terms = []
        if printed_positive_terms:
            all_printed_terms.extend(printed_positive_terms)
        if printed_negative_terms:
            all_printed_terms.extend(printed_negative_terms)

        if all_printed_terms:
            return r"\ ".join(all_printed_terms)
        else:
            # Fallback to default behavior if no specific handling is needed
            return super()._print_Mul(expr)


def custom_latex(expr):
    return RefinedUnitLatexPrinter().doprint(expr)


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


def make_pam_protocol(
    pfd: str,
    length_period: float = 120,
    length_pulse: float = 0.8,
    pulse_intensity: float = 3000,
    actinic_light: float = 1000,
    dark_light: float = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Use make_protocol from mxlpy to create a PAM protocol

    Create a PAM protocol using make_protocol from mxlpy. The protocol consists of 2 dark periods with a saturating pulse, followed by 10 light periods with a saturating pulse, followed by 10 dark periods of with a saturating pulse. The time units of the length_period and length_pulse should be the same as the model time unit.

    Args:
        pfd (str): Name of PPFD parameter in model
        length_period (float, optional): Length between pulses in model time unit. Defaults to 120 s.
        length_pulse (float, optional): Length of the pulse in model time unit. Defaults to 0.8 s.
        pulse_intensity (float, optional): Intensity of the pulse in model PPFD unit. Defaults to 3000 µmol m-2 s-1.
        actinic_light (float, optional): Intensity of the actinic light in model PPFD unit. Defaults to 1000 µmol m-2 s-1.
        dark_light (float, optional): Intensity of the dark light in model PPFD unit. Defaults to 40 µmol m-2 s-1.

    Returns:
        prtc (pd.DataFrame): PAM protocol as pd.DataFrame created using make_protocol from mxlpy
        shading (pd.DataFrame): Shading information for plotting the protocol as pd.DataFrame
    """
    length_nopulse = length_period - length_pulse

    dark_period = [
        (length_nopulse, {pfd: dark_light}),
        (length_pulse, {pfd: pulse_intensity}),
    ]
    light_period = [
        (length_nopulse, {pfd: actinic_light}),
        (length_pulse, {pfd: pulse_intensity}),
    ]

    prtc = make_protocol(dark_period * 2 + light_period * 10 + dark_period * 10)

    shading = prtc[prtc[pfd] != pulse_intensity].copy()
    shading["Color"] = shading[pfd].apply(
        lambda x: "black" if x == dark_light else "white"
    )

    return prtc, shading


def calc_pam_vals(
    fluo_result: pd.Series, peak_distance: float = 120
) -> tuple[pd.Series, pd.Series, pd.Series, pd.DataFrame]:
    """Calculate PAM values from fluorescence data.

    Use the fluorescence data from a PAM protocol to calculate Fm, NPQ, Fmin, and the quantum yields Y(NO), Y(NPQ) and Y(II). To find the Fm values, the peaks in the fluorescence data are found using scipy.signal.find_peaks. The distance between the peaks should be the same length as a period used in the PAM protocol, however may need to be adjusted based on the fluorescence data. Best to plot the Fluorescence data and the calculated Fm to check if the peaks are found correctly.

    Calculations and Assumptions:
        Fm(t): Maximum fluorescence at time t
        Fmin(t): Minimum fluorescence left of peak at time t
        NPQ(t) = (Fm(0) - Fm(t)) / Fm(t): Non-photochemical quenching at time t (Fm(0) is the first Fm value and is assumed to be the highest Fm value)
        Y(NO)(t) = Fmin(t) / Fm(0) : Quantum Yield of Non-Regulated Energy Loss at time t
        Y(NPQ)(t) = Fmin(t) / Fm(t) - Fmin(t) / Fm(0) : Quantum Yield of Regulated Heat Dissipation at time t
        Y(II)(t) = (Fm(t) - Fmin(t)) / Fm(t) : Quantum Yield of Photochemical Energy Conversion at time t

    Args:
        fluo_result (pd.Series): Fluorescence data as a pd.Series from mxlpy simulation.
        peak_distance (float, optional): Minimum distance between peaks, which should be the same length as a period used in the PAM protocol. However may need to be adjusted based on the fluorescence data. Defaults to 120 s.

    Returns:
        Fm (pd.Series): Maximum fluorescence values
        NPQ (pd.Series): Non-photochemical quenching values
        Fmin (pd.Series): Minimum fluorescence values
        quant_yields (pd.DataFrame): Quantum yields (Y(NO), Y(NPQ), Y(II))
    """

    # Find the indices of the Flourescence peaks (Fmaxs)
    peaks, _ = find_peaks(fluo_result, distance=peak_distance, height=0)

    # Fm series
    Fm = fluo_result.iloc[peaks]
    Fm.name = "Flourescence Peaks (Fm)"

    # Calculate NPQ
    NPQ = (Fm.iloc[0] - Fm) / Fm if len(Fm) > 0 else pd.Series(dtype=float)
    NPQ.name = "Non-Photochemical Quenching (NPQ)"

    # Find the minima around the peaks
    prominences, prominences_left, prominences_right = peak_prominences(
        (fluo_result), peaks, wlen=peak_distance
    )

    # Fmin is always the minima before the peak
    Fmin = fluo_result.iloc[prominences_left]
    Fmin.name = "Minimum Fluorescence before peaks (Fmin)"

    # Quantum Yield of Non-Regulated Energy Loss (Y(NO))
    Y_NO = Fmin / Fm.iloc[0] if len(Fm) > 0 else pd.Series(dtype=float)
    Y_NO.name = "Y(NO)"

    # Quantum Yield of Regulated Heat Dissipation (Y(NPQ))
    Y_NPQ = (
        Fmin / Fm.values - Fmin / Fm.iloc[0] if len(Fm) > 0 else pd.Series(dtype=float)
    )
    Y_NPQ.name = "Y(NPQ)"

    # Quantum Yield of Photochemical Energy Conversion (Y(II))
    Y_II = (Fm.values - Fmin) / Fm.values if len(Fm) > 0 else pd.Series(dtype=float)
    Y_II.name = "Y(II)"

    # pd.DataFrame of the three quantum yields
    quant_yields = pd.concat([Y_NO, Y_NPQ, Y_II], axis=1)
    quant_yields["Total"] = quant_yields.sum(axis=1)

    return Fm, NPQ, Fmin, quant_yields


def create_pam_fig(
    model: Model,
    pfd: str,
    flourescence: str,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    """Create a PAM figure from a MxLpy model.

    Use a MxLpy model to simulate a PAM protocol and create a figure with the fluorescence data and the calculated quantum yields. The figure consists of two subplots, the first subplot shows the fluorescence data with the Fm and Fmin points, as well as the PAM protocol shading. The second subplot shows the quantum yields as a stackplot.

    Args:
        model (Model): An MxLpy model to simulate the PAM protocol with.
        pfd (str): The name of PPFD parameter in the mxlpy model.
        flourescence (str): The name of the fluorescence variable in the mxlpy model.

    Returns:
        tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]: A tuple containing the figure and the axes.
    """

    # Make pam protocol for mxlpy simulation
    pam_prtc, shading = make_pam_protocol(pfd=pfd)

    # Create PAM simulator
    pam_sim = Simulator(model=model)

    # Simulate plant dark adaptation for 30 min
    pam_sim.update_parameter(pfd, 40)
    dark_adaptation_time = 30 * 60
    pam_sim.simulate(dark_adaptation_time)

    # Simulate pam protocol
    pam_sim.simulate_protocol(pam_prtc, time_points_per_step=100)
    if pam_sim.get_result() is not None:
        variables, fluxes = pam_sim.get_result()
        # Remove dark adaptation time from results
        variables.index = variables.index - dark_adaptation_time
        # Normalize fluorescence data to max value and remove negative time values
        fluo_res = variables[flourescence] / max(variables[flourescence])
        fluo_res = fluo_res.iloc[fluo_res.index >= 0]
    else:
        fluo_res = pd.Series()

    # Calculate PAM values
    Fm, NPQ, Fmin, quant_yields = calc_pam_vals(fluo_res)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 5))

    # Plot fluorescence data and Fm and Fmin points
    # TODO: Add Legend and axis labels
    ax1.plot(fluo_res, color="#ff8c00", lw=2)
    ax1.plot(Fm, color="#ff0000", lw=0, marker="x")
    ax1.plot(Fmin, color="green", lw=0, marker="^")
    plot.shade_protocol(shading[pfd], ax=ax1, add_legend=False, alpha=0.1)

    # Plot quantum yields as stackplot
    ax2.stackplot(
        quant_yields.index,
        quant_yields["Y(NO)"],
        quant_yields["Y(NPQ)"],
        quant_yields["Y(II)"],
        colors=["#c9303e", "#ffbf6e", "#56aa69"],
        baseline="zero",
    )

    # Set axis limits and ticks to minutes
    for ax in [ax1, ax2]:
        ax.set_ylim(0, 1.1)
        ax.set_xlim(0, max(fluo_res.index))
        ax.set_xlabel("Time [min]")
        xticks = [0, 4 * 60, 24 * 60, 44 * 60]
        ax.set_xticks(xticks, labels=[str(x / 60) for x in xticks])

    # Create PAM protocol shading above fluorescence plot
    width = 1 / len(shading)
    x_position = 0.0
    patches: list[Rectangle] = []
    patches_color = []
    rect_height = 0.05
    rect_y = 1.01

    # Iterate through shading protocol and create rectangles
    for index, val in shading.iterrows():
        color = val["Color"]

        # Create rectangle based on color of row in shading protocol
        rect = Rectangle(
            (x_position, rect_y),
            width,
            rect_height,
            facecolor=color,
            alpha=1,
            clip_on=False,
            transform=ax1.transAxes,
            edgecolor="black",
            lw=0.5,
        )

        # If patches list empty add first rectangle
        if patches == []:
            patches.append(rect)
            patches_color.append(color)
        # If the last rectangle has the same color, extend its width instead of adding a new one
        elif patches[-1].get_facecolor() == rect.get_facecolor():
            patches[-1].set_width(patches[-1].get_width() + width)
        # Else add new rectangle
        else:
            patches.append(rect)
            patches_color.append(color)

        x_position += width

    # Add rectangles to plot and add PPFD values as text
    for patch, color in zip(patches, patches_color):
        ax1.add_patch(patch)

        # Skip first patch as it is only a small slither due to the way the rectangles are created
        if patches.index(patch) == 0:
            continue

        # Get associated PPFD value from shading protocol
        val_associated = shading[shading["Color"] == color][pfd].iloc[0]

        # Choose text color based on rectangle color
        if color == "black":
            text_color = "white"
        else:
            text_color = "black"

        # Add text to center of rectangle
        ax1.text(
            patch.get_center()[0],
            patch.get_center()[1],
            str(val_associated) + r" $\mathbf{\mathrm{\mu mol\ m^{-2}\ s^{-1}}}$",
            ha="center",
            va="center",
            transform=ax1.transAxes,
            color=text_color,
            fontweight="bold",
        )

    # Create quantum yield legend above stackplot
    x_position = 0

    for color, label in zip(
        ["#c9303e", "#ffbf6e", "#56aa69"],
        [r"$\mathbf{Y(NO)}$", r"$\mathbf{Y(NPQ)}$", r"$\mathbf{Y(II)}$"],
    ):
        # Create rectangle for legend with 1/3 width of the plot
        rect = Rectangle(
            (x_position, rect_y),
            1 / 3,
            rect_height,
            facecolor=color,
            alpha=1,
            clip_on=False,
            transform=ax2.transAxes,
        )

        ax2.add_patch(rect)
        ax2.text(
            rect.get_center()[0],
            rect.get_center()[1],
            label,
            ha="center",
            va="center",
            transform=ax2.transAxes,
            color="black",
            fontweight="bold",
            alpha=0.75,
        )
        x_position += 1 / 3

    return fig, (ax1, ax2)


def create_day_simulation_fig(
    model: Model,
    pfd: str,
    vc: str | None = None,
    atp: str | None = None,
    nadph: str | None = None,
    flourescence: str | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Create a day simulation figure.

    Create a day simulation figure using a MxLpy model and PAR data from NEON (https://www.neonscience.org/). The figure consists of the PAR data as a filled area plot and the model results as line plots. The model results can include the Rubisco carboxylation rate, the ATP/NADPH ratio, and the fluorescence. If the model does not contain the variables, they will not be plotted and "n.a." will be written as the y-axis label.

    Args:
        model (Model): MxLpy model to simulate day with
        pfd (str): Name of the PPFD parameter in the MxLpy model
        vc (str | None, optional): Name of the Rubisco carboxylase activity rate in the MxLpy model. Defaults to None.
        atp (str | None, optional): Name of the ATP variable in the MxLpy model. Defaults to None.
        nadph (str | None, optional): Name of the NADPH variable in the MxLpy model. Defaults to None.
        flourescence (str | None, optional): Name of the fluorescence variable in the MxLpy model. Defaults to None.

    Returns:
        tuple[plt.Figure, plt.Axes]: Figure and axis of the day simulation plot
    """

    # TODO: Check for case if result = None
    # TODO: Seperate Simulation results to check if given name is in variables or fluxes or parameters or readouts or surrogates

    # Load PAR data from NEON at the KONZ site in June 2023 (https://data.neonscience.org/data-products/DP1.00024.001/RELEASE-2023)
    par_data = nu.load_by_product(
        dpid="DP1.00024.001",
        site="KONZ",
        startdate="2023-06",
        enddate="2023-06",
        token=None,
        check_size=False,
        progress=False,
    )

    # Select PAR Data per minute
    par_data = par_data["PARPAR_1min"]
    # Set startDateTime as index and drop columns with all NaN values
    par_data = par_data.set_index("startDateTime")
    par_data = par_data.dropna(axis=1, how="all")
    # Locate Date at 19.06
    day_data = par_data.loc["2023-06-19"]
    # Use only the same position values
    day_data = day_data[day_data["horizontalPosition"] == "000"]
    day_data = day_data[day_data["verticalPosition"] == "010"]
    # Limit data to between 12:00 and 23:59 # TODO: Only want day, which is good, but not realistic with hours set. Is data maybe skewed?
    day_data = day_data.between_time("12:00:00", "23:59:59")

    fig, ax = plt.subplots()
    # Plot PAR data
    ax.fill_between(
        day_data.index, day_data["PARMean"], 0, alpha=0.3, color="black", lw=0
    )

    # Format axis'
    ax.get_xaxis().set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M"))
    ax.set_xlim(day_data.index[0], day_data.index[-1])
    ax.set_xlabel("Time [hh:mm]")
    ax.set_ylabel(r"PPFD [$\mathrm{\mu mol \, m^{-2} \, s^{-1}}$]")

    # Create day simulation that folows the PAR data
    s = Simulator(model)
    day_prtc = make_protocol(
        [(60, {pfd: row["PARMean"]}) for index, row in day_data.iterrows()]
    )
    s.simulate_protocol(day_prtc)

    # Get results and set index to datetime
    res = s.get_result()
    variables = res.get_variables()
    variables.index = pd.to_datetime(
        variables.index, unit="s", origin="2023-06-19 12:00:00"
    )
    fluxes = res.get_fluxes()
    fluxes.index = pd.to_datetime(fluxes.index, unit="s", origin="2023-06-19 12:00:00")

    res_dict = {}

    for name, pointer in zip(
        [vc, atp, nadph, flourescence], ["Vc", "ATP", "NADPH", "Fluorescence"]
    ):
        if name is None:
            data = None
            unit = None
        elif name in variables.columns:
            data = variables[name]
            # unit = model._variables[name].unit Reimplement when sperated variables
        elif name in fluxes.columns:
            data = fluxes[name]
            unit = model._reactions[name].unit
        else:
            data = model._parameters[name].value
            unit = model._parameters[name].unit

        res_dict[pointer] = {"data": data, "unit": unit}

    # Colors of sim results
    vc_color = "#fa9442"
    atp_nadph_color = "#008aa1"
    fluo_color = "#1b3644"
    color_list = [vc_color, atp_nadph_color, fluo_color]

    axes_pos = 0.15
    yax_list = []

    # Create twin axis for each variable to plot
    for ax_idx, color in enumerate(color_list):
        ax_new = ax.twinx()
        ax_new.spines["right"].set_color(color)
        ax_new.spines["right"].set_position(("axes", 1 + axes_pos * ax_idx))
        ax_new.tick_params(axis="y", colors=color)
        yax_list.append(ax_new)

    # Plot variables if they are in the model else write n.a. as ylabel
    if vc is not None:
        yax_list[0].plot(res_dict["Vc"]["data"], color=vc_color)
        yax_list[0].set_ylabel(
            rf"Rubisco Carboxylase Activity [${res_dict['Vc']['unit']}$]",
            color=vc_color,
        )
    else:
        yax_list[0].set_ylabel("Rubisco Carboxylase Activity n.a.", color=vc_color)

    if atp is not None and nadph is not None:
        yax_list[1].plot(
            res_dict["ATP"]["data"] / res_dict["NADPH"]["data"], color=atp_nadph_color
        )
        yax_list[1].set_ylabel("ATP/NADPH", color=atp_nadph_color)
    else:
        yax_list[1].set_ylabel("ATP/NADPH n.a.", color=atp_nadph_color)

    if flourescence is not None:
        yax_list[2].plot(res_dict["Fluorescence"]["data"], color=fluo_color)
        yax_list[2].set_ylabel("Fluorescence", color=fluo_color)
    else:
        yax_list[2].set_ylabel("Fluorescence n.a.", color=fluo_color)

    return fig, ax


def create_mca_fig(
    model: Model,
    coeff_psii: str | None,
    coeff_psi: str | None,
    coeff_rubisco: str | None,
    coeff_cytb6f: str | None,
    coeff_atp_synthase: str | None,
    rubp: str | None,
    co2: str | None,
    pq: str | None,
    pc: str | None,
    atp: str | None,
    nadph: str | None,
    v_rubisco: str | None,
    v_psii: str | None,
    v_psi: str | None,
    v_cytb6f: str | None,
    v_atp_synthase: str | None,
) -> tuple[plt.Figure, plt.Axes]:
    """Create curated MCA figure from MxLpy model.

    Create a curated MCA figure from a MxLpy model using the response coefficients of several aspects of photosynthesis. If the model does not contain the given parameters or variables, they will not be plotted and the corresponding row/column will be faded out.

    The chosen MCA will look like this:

            | PSII | PSI | Rubisco |
    RuBP    |
    CO2     |

    Args:
        model (Model): MxLpy model to perform MCA on.
        coeff_psii (str | None): Name of response coefficient for PSII in the MxLpy model.
        coeff_psi (str | None): Name of PSI response coefficient in the MxLpy model.
        coeff_rubisco (str | None): Name of Rubisco response coefficient in the MxLpy model.
        coeff_cytb6f (str | None): Name of Cytb6f response coefficient in the MxLpy model.
        coeff_atp_synthase (str | None): Name of ATP Synthase response coefficient in the MxLpy model.
        rubp (str | None): Name of RuBP representation in the MxLpy model.
        co2 (str | None): Name of CO2 representation in the MxLpy model.
        pq (str | None): Name of PQ representation in the MxLpy model.
        pc (str | None): Name of PC representation in the MxLpy model.
        atp (str | None): Name of ATP representation in the MxLpy model.
        nadph (str | None): Name of NADPH representation in the MxLpy model.
        v_rubisco (str | None): Name of Rubisco flux in the MxLpy model.
        v_psii (str | None): Name of PSII flux in the MxLpy model.
        v_psi (str | None): Name of PSI flux in the MxLpy model.
        v_cytb6f (str | None): Name of Cytb6f flux in the MxLpy model.
        v_atp_synthase (str | None): Name of ATP Synthase flux in the MxLpy model.

    Returns:
        tuple[plt.Figure, plt.Axes]: Figure and Axes of the MCA plot.
    """

    # TODO Find other response coefficients to plot
    # TODO Find other variables and fluxes to plot

    # Create list of parameters to scan if there are not None
    to_scan = [
        i
        for i in [
            coeff_psii,
            coeff_psi,
            coeff_rubisco,
            coeff_cytb6f,
            coeff_atp_synthase,
        ]
        if i is not None
    ]

    # Do MCA of selected response coefficients
    variables, fluxes = mca.response_coefficients(
        model, to_scan=to_scan, disable_tqdm=True
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Point custom names to appropriate given response coefficients in MCA results
    plot_columns = {
        "PSII": coeff_psii,
        "PSI": coeff_psi,
        "Rubisco": coeff_rubisco,
        "Cytb6f": coeff_cytb6f,
        "ATP Synthase": coeff_atp_synthase,
    }

    # Point custom names to appropriate given variables in MCA results
    plot_vars_index = {
        "RuBP": rubp,
        "CO2": co2,
        "PQ": pq,
        "PC": pc,
        "ATP": atp,
        "NADPH": nadph,
    }

    # Point custom names to appropriate given fluxes in MCA results
    plot_flux_index = {
        r"$v_{\text{rubisco}}$": v_rubisco,
        r"$v_{\text{PSII}}$": v_psii,
        r"$v_{\text{PSI}}$": v_psi,
        r"$v_{\text{Cytb6f}}$": v_cytb6f,
        r"$v_{\text{ATP Synthase}}$": v_atp_synthase,
    }

    # Get only the variables that are in the MCA results
    index_in_vars = [
        i for i in plot_vars_index.values() if i is not None and i in variables.index
    ]
    columns_in_vars = [
        i for i in plot_columns.values() if i is not None and i in variables.columns
    ]

    # Get only the variables that are in the MCA results
    index_in_flux = [
        i for i in plot_flux_index.values() if i is not None and i in fluxes.index
    ]
    columns_in_flux = [
        i for i in plot_columns.values() if i is not None and i in fluxes.columns
    ]

    # Create copy of DataFrame to plot
    plot_vars = variables.loc[index_in_vars, columns_in_vars].copy()
    plot_fluxes = fluxes.loc[index_in_flux, columns_in_flux].copy()

    # Rename rows and columns to custom names
    plot_vars = plot_vars.rename(
        columns={v: k for k, v in plot_columns.items()},
        index={v: k for k, v in plot_vars_index.items()},
    )
    plot_fluxes = plot_fluxes.rename(
        columns={v: k for k, v in plot_columns.items()},
        index={v: k for k, v in plot_flux_index.items()},
    )

    # Add rows and columns with NaN values for variables not in MCA results
    for i in plot_columns.keys():
        if i not in plot_vars.columns:
            plot_vars[i] = np.nan
        if i not in plot_fluxes.columns:
            plot_fluxes[i] = np.nan

    for i in plot_vars_index.keys():
        if i not in plot_vars.index:
            plot_vars.loc[i, :] = np.nan
    for i in plot_flux_index.keys():
        if i not in plot_fluxes.index:
            plot_fluxes.loc[i, :] = np.nan

    # Plot heatmap of MCA results
    plot.heatmap(
        plot_vars,
        ax=ax1,
        cmap="YlGnBu_r",
        title="Variables",
    )
    plot.heatmap(
        plot_fluxes,
        ax=ax2,
        cmap="YlOrRd_r",
        title="Fluxes",
    )

    # Set axis labels and if values are NaN set alpha of text to 0.3
    for ax, plot_df in zip([ax1, ax2], [plot_vars, plot_fluxes]):
        for text in ax.get_yticklabels():
            if plot_df.loc[text.get_text(), :].isna().all():
                text.set_alpha(0.3)

        for text in ax.get_xticklabels():
            if plot_df.loc[:, text.get_text()].isna().all():
                text.set_alpha(0.3)

    plt.tight_layout()

    return fig, (ax1, ax2)


# def create_pamfit(
#     pfd: str | None,
#     model: Model,
#     parameter_to_fit: list[str],
# ):
#     fluo_data = pd.read_csv("Data/fluo_col0_1.csv", index_col=0)

#     # Convert index to time in seconds
#     fluo_data.index = pd.to_timedelta(fluo_data.index)
#     fluo_data.index = fluo_data.index - fluo_data.index[0]
#     fluo_data.index = fluo_data.index.total_seconds()

#     # Prepare a list to hold new rows
#     new_dict = {}

#     for index, row in fluo_data.iterrows():
#         for key, val in zip(["Time", "Fluo", "PAR"], [index, row["F1"], row["PAR"]]):
#             if key not in new_dict:
#                 new_dict[key] = [val]
#             else:
#                 new_dict[key].append(val)

#             # Add Fm vals to F
#         new_dict["Time"].append(index + 0.8)
#         new_dict["Fluo"].append(row["Fm'1"])
#         new_dict["PAR"].append(5000)

#     # Create a new DataFrame from the list of rows
#     cleaned_df = pd.DataFrame.from_dict(new_dict)
#     # Set 'Time' as index and sort to ensure correct order
#     cleaned_df = cleaned_df.set_index("Time").sort_index()
#     cleaned_df["PAR"] = cleaned_df["PAR"].replace(0, 40)
#     cleaned_df["rel. Fluo"] = cleaned_df["Fluo"] / max(cleaned_df["Fluo"])
#     print(cleaned_df)
#     # cleaned_df.index = cleaned_df.index + 60 * 30  # adjust time to account for dark adaptation period
#     # print(cleaned_df)

#     prtc_list = []
#     for index, row in cleaned_df.iterrows():
#         if cleaned_df.index.get_loc(index) == 0:
#             prtc_list.append((index, {pfd: 40}))
#         else:
#             prtc_list.append(
#                 (
#                     index - cleaned_df.index[cleaned_df.index.get_loc(index) - 1],
#                     {pfd: row["PAR"]},
#                 )
#             )

#     prtc = make_protocol(
#         prtc_list[1:]
#     )  # skip first entry as it is only for dark adaptation

#     # print(prtc)

#     # s = Simulator(model=model)

#     # y0 = (
#     #     s.simulate(60 * 30)
#     #     .get_result()
#     #     .get_variables(include_derived_variables=False, include_readouts=False)
#     #     .iloc[-1]
#     #     .to_dict()
#     # )

#     # res = (
#     #     s.simulate_protocol(prtc, time_points_per_step=100).get_result().get_variables()
#     # )

#     # print(res)

#     # parameter_dict = {
#     #     param: model._parameters[param].value for param in parameter_to_fit
#     # }

#     # print(fit.protocol_time_course(
#     #     model=model,
#     #     p0=parameter_dict,
#     #     data=cleaned_df[["Fluo"]],
#     #     protocol=prtc,
#     #     y0=y0,
#     # ))

#     fig, ax = plt.subplots()

#     # ax.plot(res.index, res["Fluo"])
#     ax.plot(cleaned_df["rel. Fluo"])

#     return


def save_matplotlib_figure(fig: plt.Figure, file_prepend: str, figcat: str) -> None:
    """Save matplotlib figure of model validation fig in 'Figures' directory as a svg.

    Args:
        fig (plt.Figure): Matplotlib figure to save
        file_prepend (str): str of file prepend for each fig. Recommended to be the model name.
        figcat (str): str of figure category. Recommended to be a descriptive name for the figure.
    """

    try:
        notebook_dir = Path(os.getcwd())
    except NameError:
        notebook_dir = Path(".")

    # 2. Construct the path for the 'Figure' directory
    figure_dir = notebook_dir / "Figures"

    # 3. Create the directory if it doesn't exist
    # `mkdir(exist_ok=True)` prevents an error if the directory already exists.
    figure_dir.mkdir(parents=True, exist_ok=True)

    # 4. Construct the full save path
    save_path = figure_dir / f"{file_prepend}_{figcat}.svg"

    # 5. Save the figure
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)  # Close the figure to free up memory


def create_save_figs(
    model: Model,
    pfd: str,
    file_prepend: str,
    co2: str | None,
    vc: str | None,
    pco2: str | None,
    H_cp_co2: str | None,
    gammastar: str | None,
    r_light: str | None,
    A: str | None,
    flourescence: str | None,
    atp: str | None,
    nadph: str | None,
    rubp: str | None,
    coeff_psii: str | None,
    coeff_psi: str | None,
    coeff_rubisco: str | None,
) -> None:
    """Create and save all model validation figs.

    Use a MxLpy model to create and save all model validation figs. The figs include:
    - FvCB comparison fig
    - PAM simulation fig
    - Day simulation fig
    - MCA of photosynthesis control coefficients fig

    Args:
        model (Model): MxLpy model to create figs from.
        pfd (str): Name for PPFD parameter in model.
        file_prepend (str): str of file prepend for each fig. Recommended to be the model name.
        co2 (str | None): Name for CO2 variable in model.
        vc (str | None): Name for rubisco carboxylation in model.
        pco2 (str | None): Name for CO2 partial pressure in model.
        H_cp_co2 (str | None): Name for Henry's law constant for CO2 in model.
        gammastar (str | None): Name for CO2 compensation point in model.
        r_light (str | None): Name for Rate of non-photorespiratory CO2 release in the light in model.
        A (str | None): Name for net carbon assimilation rate in model.
        flourescence (str | None): Name for fluorescence in model.
        atp (str | None): Name for ATP in model.
        nadph (str | None): Name for NADPH in model.
        rubp (str | None): Name for RuBP in model.
        coeff_psii (str | None): Name for PSII coefficient in model.
        coeff_psi (str | None): Name for PSI coefficient in model.
        coeff_rubisco (str | None): Name for Rubisco coefficient in model.
    """

    # FvCB comparison
    plot, ax = create_fvcb_fig(
        model=model,
        pfd=pfd,
        co2=co2,
        vc=vc,
        pco2=pco2,
        H_cp_co2=H_cp_co2,
        gammastar=gammastar,
        r_light=r_light,
        A=A,
    )
    save_matplotlib_figure(plot, file_prepend, "fvcb_compare")

    # PAM simulation
    pam_plot, ax = create_pam_fig(model=model, pfd=pfd, flourescence=flourescence)
    save_matplotlib_figure(pam_plot, file_prepend, "pam")

    # Day simulation
    plot, ax = create_day_simulation_fig(
        model=model, pfd=pfd, vc=vc, atp=atp, nadph=nadph, flourescence=flourescence
    )
    save_matplotlib_figure(plot, file_prepend, "day_simulation")

    # MCA of photosynthesis control coefficients
    plot, ax = create_mca_fig(
        model=model,
        coeff_psii=coeff_psii,
        coeff_psi=coeff_psi,
        coeff_rubisco=coeff_rubisco,
        rubp=rubp,
        co2=co2,
    )

    return


def create_report_summary(
    model: Model,
    pfd: str,
    file_prepend: str,
    co2: str | None = None,
    vc: str | None = None,
    pco2: str | None = None,
    H_cp_co2: str | None = None,
    gammastar: str | None = None,
    r_light: str | None = None,
    A: str | None = None,
    flourescence: str | None = None,
    atp: str | None = None,
    nadph: str | None = None,
    rubp: str | None = None,
    coeff_psii: str | None = None,
    coeff_psi: str | None = None,
    coeff_rubisco: str | None = None,
):
    """Create markdown file of Model validation.

    Use a MxLpy model to create and save all model validation figs and create a markdown summary file. The figs include:
    - FvCB comparison fig
    - PAM simulation fig

    Args:
        model (Model): MxLpy model to create figs from.
        pfd (str): Name for PPFD parameter in model.
        file_prepend (str): str of file prepend for each fig. Recommended to be the model name.
        co2 (str | None, optional): Name for CO2 variable in model. Defaults to None.
        vc (str | None, optional): Name for rubisco carboxylation in model. Defaults to None.
        pco2 (str | None, optional): Name for CO2 partial pressure in model. Defaults to None.
        H_cp_co2 (str | None, optional): Name for Henry's law constant for CO2 in model.. Defaults to None.
        gammastar (str | None, optional): Name for CO2 compensation point in model. Defaults to None.
        r_light (str | None, optional): Name for Rate of non-photorespiratory CO2 release in the light in model. Defaults to None.
        A (str | None, optional): Name for net carbon assimilation rate in model. Defaults to None.
        flourescence (str | None, optional): Name for fluorescence in model. Defaults to None.
        atp (str | None, optional): Name for ATP in model. Defaults to None.
        nadph (str | None, optional): Name for NADPH in model. Defaults to None.
        rubp (str | None, optional): Name for RuBP in model. Defaults to None.
        coeff_psii (str | None, optional): Name for PSII coefficient in model. Defaults to None.
        coeff_psi (str | None, optional): Name for PSI coefficient in model. Defaults to None.
        coeff_rubisco (str | None, optional): Name for Rubisco coefficient in model. Defaults to None.
    """

    # TODO: Add PAM assumptions
    # TODO: Add Day simulation
    # TODO: Add MCA

    # Create all the validation figs and save them
    create_save_figs(
        model=model,
        pfd=pfd,
        file_prepend=file_prepend,
        co2=co2,
        vc=vc,
        pco2=pco2,
        H_cp_co2=H_cp_co2,
        gammastar=gammastar,
        r_light=r_light,
        A=A,
        flourescence=flourescence,
        atp=atp,
        nadph=nadph,
        rubp=rubp,
        coeff_psii=coeff_psii,
        coeff_psi=coeff_psi,
        coeff_rubisco=coeff_rubisco,
    )

    # Create markdown summary file
    mdFile = MdUtils(
        file_name=f"{Path(__file__).parent / f'{file_prepend}_report_summary.md'}",
        title=f"{file_prepend} Report Summary",
    )
    mdFile.new_header(level=1, title="Simulations")

    # Carbon Assimilation via FvCB
    mdFile.new_header(level=2, title="Carbon Assimilation via FvCB")

    # Create table of parameters that are in the model
    table = ["Parameter", "Exists?"]

    for text, param in zip(
        [
            r"$\mathrm{CO}_2$",
            r"$v_\mathrm{c}$",
            r"$\mathrm{C_i}$",
            r"$H_\mathrm{s}^{cp}$",
            r"$\Gamma ^*$",
            r"$R_\mathrm{light}$",
            r"A",
        ],
        [co2, vc, pco2, H_cp_co2, gammastar, r_light, A],
    ):
        table.append(text)
        if param is None:
            if text in ["CO2", "Vc"]:
                table.append("&#10060;")
            else:
                table.append("&#10060;")
        else:
            table.append("&check;")

    # Explanation of FvCB comparison
    mdFile.new_paragraph(
        r"Comparison of modelled carbon assimilation ($A$) and carboxylation rate ($v_\mathrm{c}$) against the Farquhar, von Caemmerer and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025) [[1]](https://doi.org/10.1101/2025.03.11.642611). To be able to simulate carbon assimilation, there are two mandatory parameters that need to be present in the model: CO2 concentration and Vc. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The table below summarizes which parameters were found in the model. The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model."
    )

    mdFile.new_header(level=3, title="Assumptions")

    # List of assumptions made for FvCB comparison
    mdFile.new_list(
        [
            r"Infinite mesophyll conductance, therefore intercellular CO<sub>2</sub> partial pressure equals chloroplast partial pressure ($\mathrm{C_i} = \mathrm{C_c}$)",
            r"If no CO<sub>2</sub> concentration nor rate of rubisco carboxylation ($v_\mathrm{c}$) is present in the model, no comparison will be shown",
            r"If no $\mathrm{C_i}$ is present in the model, it will be added as a parameter assuming an initial value of CO<sub>2</sub> concentration divided by Henry's law constant for CO<sub>2</sub> ($H_\mathrm{s}^{cp}$)",
            r"If no $H_\mathrm{s}^{cp}$ is present in the model, it will be added as a parameter with a value of $3.4 \times 10^{-4}\ \mathrm{mmol\ Pa^ {-1}}$ [[2]](https://doi.org/10.5194/acp-23-10901-2023)",
            r"If no CO<sub>2</sub> compensation point in the absence of non-photorespiratory CO<sub>2</sub> release ($\Gamma ^*$) is present in the model, it will be added as a parameter with a value of $38.6\ \mathrm{\mu bar}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)",
            r"If no $R_\mathrm{light}$ is present in the model, it will be added as a parameter with a value of $1\ \mathrm{\mu mol\ m^{-2}\ s^{-1}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)",
            r"If no $A$ is present in the model, it will be added as a derived variable following the FvCB equation [[1]](https://doi.org/10.1101/2025.03.11.642611): $v_\mathrm{c} \cdot \left(1 - \frac{\Gamma ^*}{C_i}\right) - R_\mathrm{light}$",
            r"To be able to compare with original FvCB curves, the model needs to have $v_\mathrm{c}$ following the same units as the FvCB model ($\mathrm{\mu mol\ m^{-2}\ s^{-1}}$). The `mM_to_µmol_per_m2` can be used to convert from mM to $\mathrm{\mu mol\ m^{-2}}$ assuming a volume factor of $0.0112\ \mathrm{L\ m^{-2}}$ in the stroma [[3]](https://doi.org/10.1007/s11120-006-9109-1). If the given units are in mM, the conversion will be done automatically, by adding a derived parameter with the converted values.",
        ]
    )

    # Add FvCB comparison fig
    mdFile.new_line(
        f"{mdFile.new_inline_image(text='Assimilation', path=str(f'./Figures/{file_prepend}_fvcb_compare.svg'))}"
    )

    mdFile.new_table(columns=2, rows=8, text=table)

    # PAM Fluorescence
    mdFile.new_header(level=2, title="PAM Fluorescence")

    # Explanation of PAM simulation
    mdFile.new_paragraph(
        r"Simulation of a PAM flourescence protocol. The simulation is first run for 30 minutes in a dark adapted state (PPFD = 40) and then the PAM protocol starts. Each period consists of 2 minutes of light and then a saturating pulse of 0.8 seconds. The first two periods are in low light (PPFD = 40), followed by 10 periods in actinic light (PPFD = 1000) and then 10 periods in low light again (PPFD = 40). The left plot shows the normalised flourescence yield (orange) with the identified Fm peaks (crosses) and the calculated NPQ (blue). The right plot shows the quantum yields of non-regulated energy loss (Y(NO), red), regulated heat dissipation (Y(NPQ), orange) and photochemical energy conversion (Y(II), green), but only during the light phase. All results here are arbituary by using the proposed initial conditions of the model and using the Flourescence readout calculated through the model. Therefore, the values do not represent actual values but rather a qualitative behaviour of the model. The table below summarizes which parameters were found in the model."
    )

    # Add Simulation fig
    mdFile.new_line(
        f"{mdFile.new_inline_image(text='PAM Protocol', path=str(f'./Figures/{file_prepend}_pam.svg'))}"
    )

    # Day Simulation
    mdFile.new_header(level=2, title="Day Simulation")

    # Add to markdown file
    mdFile.create_md_file()

    return
