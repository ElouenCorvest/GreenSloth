from mxlpy import Model, plot, mca
import matplotlib.pyplot as plt
import numpy as np
import copy

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
    
    model = copy.deepcopy(model)

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