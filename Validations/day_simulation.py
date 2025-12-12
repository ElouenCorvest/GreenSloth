from mxlpy import Model, Simulator, make_protocol
import pandas as pd
import matplotlib.pyplot as plt
import neonutilities as nu

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