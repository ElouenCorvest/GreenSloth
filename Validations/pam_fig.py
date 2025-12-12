import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mxlpy import Model, Simulator, make_protocol, plot
from utils import calc_pam_vals2, pam_sim
import pandas as pd

def make_pam_protocol(
    pfd_str: str,
    length_period: float = 120,
    length_pulse: float = 0.8,
    pulse_intensity: float = 3000,
    actinic_light: float = 1000,
    dark_light: float = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create a PAM protocol and shade protocol for MxLpy simulations.
    
    The resulting protocol consists of 2 dark periods, followed by 10 light periods and 10 dark periods. Each period consists of a length without pulse followed by a pulse. The correct times are calcuated based on the provided lengths. This protocol has the following structure:
    [(length_nopulse, {pfd_str: dark_light}), (length_pulse, {pfd_str: pulse_intensity}), ...]
    This makes it compatible with the make_protocol function from mxlpy.
    
    The resulting shading information can be used to plot the protocol in a matplotlib figure. The shading information consists of a list of dictionaries with the following keys:
    - x1: start of the shading
    - x2: end of the shading
    - color: color of the shading (either "black" for dark periods or "white" for light periods)
    - PPFD: PPFD value for the period (either dark_light or actinic_light)
    
    The shading protocol gets created to match the created PAM protocol for easy plotting, but filters out the saturating pulses and combines consecutive periods of the same light level.

    Args:
        pfd_str (str): Name of PPFD parameter in model
        length_period (float, optional): Length between pulses in model time unit. Defaults to 120 s.
        length_pulse (float, optional): Length of the pulse in model time unit. Defaults to 0.8 s.
        pulse_intensity (float, optional): Intensity of the pulse in model PPFD unit. Defaults to 3000 µmol m-2 s-1.
        actinic_light (float, optional): Intensity of the actinic light in model PPFD unit. Defaults to 1000 µmol m-2 s-1.
        dark_light (float, optional): Intensity of the dark light in model PPFD unit. Defaults to 40 µmol m-2 s-1.

    Returns:
        prtc (list[tuple[float, dict]]): PAM protocol as list
        shading (list[dict]): Shading information for plotting the protocol as pd.DataFrame
    """
    length_nopulse = length_period - length_pulse

    dark_period = [
        (length_nopulse, {pfd_str: dark_light}),
        (length_pulse, {pfd_str: pulse_intensity}),
    ]
    light_period = [
        (length_nopulse, {pfd_str: actinic_light}),
        (length_pulse, {pfd_str: pulse_intensity}),
    ]

    prtc = dark_period * 2 + light_period * 10 + dark_period * 10
    
    shading = []
    for item in prtc:
        if item[1][pfd_str] == pulse_intensity:
            continue
        elif item[1][pfd_str] == dark_light:
            color = "black"
            pfd = dark_light
        else:
            color = "white"
            pfd = actinic_light
            
        if len(shading) == 0:
            shading.append({"x1": 0, "x2": length_period, "color": color, "PPFD": pfd})
        elif shading[-1]["color"] == color:
            shading[-1]["x2"] += length_period
        else:
            shading.append({"x1": shading[-1]["x2"], "x2": shading[-1]["x2"] + length_period, "color": color, "PPFD": pfd})

    return prtc, shading

def create_pam_fig(
    model: Model,
    pfd_str: str,
    flourescence_str: str,
    dark_light: float = 40,
    sat_pulse: float = 3000,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    """Create a PAM figure from a MxLpy model.

    Use a MxLpy model to simulate a PAM protocol and create a figure with the fluorescence data and the calculated NPQ values. The figure also includes shading to indicate the light and dark periods of the protocol.

    Args:
        model (Model): An MxLpy model to simulate the PAM protocol with.
        pfd (str): The name of PPFD parameter in the mxlpy model.
        flourescence (str): The name of the fluorescence variable in the mxlpy model.

    Returns:
        tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]: A tuple containing the figure and the axes.
    """

    # Make pam protocol for mxlpy simulation
    pam_prtc, shading = make_pam_protocol(pfd_str=pfd_str, dark_light=dark_light, pulse_intensity=sat_pulse)
    
    # Simulate pam protocol
    res = pam_sim(
        fit_protocol=pam_prtc,
        model=model,
        pfd_str=pfd_str,
        dark_pfd=dark_light,
    )
    
    if res is None:
        return
    
    else:
        res = res.get_combined()
    
    # Calculate PAM values
    F, Fm, NPQ = calc_pam_vals2(
        fluo_result=res[flourescence_str],
        protocol=make_protocol(pam_prtc),
        pfd_str=pfd_str,
        sat_pulse=2000,
        do_relative=True,
    )
    
    fig, axs = plt.subplot_mosaic([["Fluo"]], figsize=(10, 4))

    # colors
    flou_color = "#ff8c00"
    
    # Plot fluorescence data and Fm points
    axs["Fluo"].plot(F, color=flou_color, lw=2, zorder=10, label="Fluorescence (F)")
    axs["Fluo"].plot(Fm, color=flou_color, lw=0, marker="^", markersize=4, label="Fm", zorder=10)
    
    # Set axis limits and labels
    axs["Fluo"].set_ylim(0, 1.1)
    axs["Fluo"].set_ylabel("Relative Fluorescence (a.u.)", color=flou_color, fontdict={"fontweight": "bold"})
    axs["Fluo"].set_xlim(0, max(F.index))
    axs["Fluo"].set_xlabel("Time [min]")
    xticks = [0, 4 * 60, 24 * 60, 44 * 60]
    axs["Fluo"].set_xticks(xticks, labels=[str(x / 60) for x in xticks])
    
    # Plot NPQ on secondary y-axis
    ax_npq = axs["Fluo"].twinx()
    ax_npq.set_ylabel("NPQ", color="#1f77b4", fontdict={"fontweight": "bold"})
    ax_npq.set_ylim(0, max(NPQ) + 0.1)
    ax_npq.plot(NPQ, color="#1f77b4", lw=2, marker="o", markersize=4, label="NPQ", zorder=10)
        
    
    rect_height = 0.1
    rect_y = axs["Fluo"].get_ylim()[1]
    for shade in shading:
        axs["Fluo"].axvspan(
            shade["x1"],
            shade["x2"],
            color=shade["color"],
            alpha=0.3,
            lw=0,
        )
        
        rect = Rectangle(
            (shade["x1"], rect_y),
            shade["x2"] - shade["x1"],
            rect_height,
            facecolor=shade["color"],
            alpha=1,
            clip_on=False,
            transform=axs["Fluo"].transData,
            edgecolor="black",
            lw=0.5,
        )
        
        patch = axs["Fluo"].add_patch(rect)
        
        text = axs["Fluo"].text(
            x=patch.get_center()[0],
            y=patch.get_center()[1],
            s=str(shade["PPFD"]) + r" $\mathbf{\mathrm{\mu mol\ m^{-2}\ s^{-1}}}$",
            ha="center",
            va="center",
            color="black" if shade["color"] == "white" else "white",
            fontweight="bold",
        )
        
        text_width = text.get_tightbbox().x1 - text.get_tightbbox().x0
        patch_width = patch.get_tightbbox().x1 - patch.get_tightbbox().x0
        
        if text_width > patch_width:
            text.remove()

    return fig, axs