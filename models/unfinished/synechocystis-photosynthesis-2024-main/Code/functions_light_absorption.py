# %%
import numpy as _np
import pandas as _pd
from scipy.integrate import simpson as _simpson
from os import listdir as _listdir
import matplotlib.pyplot as _plt
import numpy.typing as _npt
from pathlib import Path as _Path
from numpy.typing import ArrayLike as _ArrayLike
from typing import Union as _Union
from warnings import warn as _warn
from re import sub as _sub
# %%
_MODPATH = (_Path(__file__)/"..").resolve()
_DATAPATH = _MODPATH / "data/"


# %%
# Define functions
def get_pigment_association(ps1_ratio:float, beta_carotene_method:str="original", pigments:_pd.Series=None, verbose:bool=True) -> _pd.DataFrame:
    """Create a DataFrame containing the fractions of pigments associated to the main complexes (PS1, PS2. PBS)

    Args:
        ps1_ratio (float): ratio of PS1:PS2
        beta_carotene_method (str): how to calculate the beta carotene energy donation, one of 'original' or 'stoichiometric'
        pigments (_pd.DataFrame): DataFrame with the pigment amounts [mg(pigment) mg(chlorophyll a)^-1] in named columns
        verbose (bool): issue a warning if provided and calculated beta carotene amounts don't match
    """
    # Adapt the ratio tab in _ps_comp
    _ps_comp.loc["ratio", "ps1"] = ps1_ratio

    # Chlorophyll a: Fraction of total pool
    chla = chla = _ps_comp.loc[["ratio", "n_chla"],:].prod(axis=0)
    chla = chla/chla.sum()


    # Beta carotene: Fraction of total pool wih adjustment factor
    beta_carotene = _ps_comp.loc[["ratio", "n_beta_carotene"],:].prod(axis=0)
    beta_carotene = beta_carotene/beta_carotene.sum()

    if beta_carotene_method == "original": 
        # Original in Fuente 2021: Fraction of total pool but only 75% in membrane
        beta_carotene = beta_carotene.mul(_ps_comp.loc["beta_carotene_in_membrane", :])

    elif beta_carotene_method == "stoichiometric":
        if pigments is not None:
            # Calculate the molar ratio of beta carotene following from the stoichiometry 
            bc_stoich = _ps_comp.loc[["ratio", "n_beta_carotene"],:].prod(axis=0) * (1/_ps_comp.loc["ratio",:].sum())
            bc_stoich = bc_stoich.mul(1/_ps_comp.loc["n_chla", :]).sum()

            # Compare with the measured value and calculate a proportionality factor
            bc_measured = pigments.loc["beta_carotene"] * _molmasses["chla"] / _molmasses["beta_carotene"]
            bc_fac = _np.min(_np.array([bc_stoich/bc_measured, 1]))

            if bc_stoich > bc_measured and verbose:
                _warn(f"The provided pigments have a molar beta carotene:chl a ratio of {_np.round(bc_measured,3)} while the photosystem stoichiometry requires {_np.round(bc_stoich,3)}")

            # Also take into account that only ps1 is excited by carotenoid absorption
            beta_carotene = beta_carotene * _pd.Series({"ps1": bc_fac, "ps2":0})
        else:
            raise ValueError("with beta_carotene_method 'stoichiometric', the pigments have to be provided")
    else:
        raise ValueError("beta_carotene_method has to be either 'original' or 'stoichiometric'")

    # Construct the full association map including pbs
    ass_map = _pd.DataFrame({"chla":chla, "beta_carotene":beta_carotene})
    
    pbs = _pd.Series([1,1], index=["allophycocyanin", "phycocyanin"], name="pbs")
    ass_map = _pd.concat([ass_map, _pd.DataFrame([pbs])], axis=0).fillna(0)

    return ass_map

def get_pigment_absorption(pigments:_pd.Series) -> _pd.DataFrame:
    """Get the per-pigment wavelength-specific light absorption coefficients for a certain pigment composition

    Args:
        pigments (_pd.DataFrame): DataFrame with the pigment amounts [mg(pigment) mg(chlorophyll a)^-1] in named columns

    Returns:
        _pd.DataFrame: a DataFrame with the chlorophyll a normalised absorption coefficients [m^2_mg(chlorophyll a)^-1]
    """
    # Multiply the per-pigment abosrption coefficients with the pigment concentration
    # Also add the new unit as a index level
    abs_coef_pigm = _abs_coef.droplevel(1, axis=1).mul(pigments, axis=1)
    abs_coef_pigm = _pd.concat({'absorption_coefficient_m2_mgChla-1': abs_coef_pigm}, names=['description'], axis=1).swaplevel(0,1,1)

    return abs_coef_pigm

def get_complex_absorption(light:"_npt.ArrayLike | _pd.DataFrame | _pd.Series", absorption:_pd.DataFrame, association:_pd.DataFrame) -> _pd.Series:
    """Get the absorption of each photosynthetic complex for a given input light

    Args:
        light (_npt.ArrayLike | _pd.DataFrame | _pd.Series): mapping of light wavelengths to intensities
        absorption (_pd.DataFrame): DataFrame containing the cellular, wavelength-specific absorption of each pigment
        association (_pd.DataFrame): DataFrame containing the association of each pigment to the photosynthetic complexes

    Returns:
        _pd.Series: _description_
    """
    # Get the light absorption of each pigment
    if isinstance(light, _pd.DataFrame):
        light = light.squeeze(_np.argmin(_abs_coef.shape))
    
    abs_light = absorption.mul(light, axis=0)
    abs_pigment = abs_light.apply(_simpson, axis=0)

    # With the association calculate the complexes light absorption
    abs_complex = association.dot(_pd.DataFrame({"absorption_m2_mgChla-1":abs_pigment.droplevel(1)}))

    return abs_complex.squeeze(1)


# Light sources
def light_gaussianLED(wavelength:float, intensity:float=1.0, spread:float=10) -> _npt.ArrayLike:
    """Get a range of normalised light intensities (400 nm, 700 nm) describing a gaussean LED

    Args:
        wavelength (float): wavelength with maximal intensity
        intensity (float, optional): integrated light intensity. Defaults to 1.
        spread (float, optional): spread (variance) of the distribution. Defaults to 10.

    Returns:
        ArrayLike: an array of wavelength-specific light intensities
    """      
    x = _np.arange(390,711)
    light = _pd.Series(_np.exp(-_np.power(x - wavelength, 2.) / (2 * _np.power(spread, 2.))), name="gausseanLED", index=_pd.Index(x, name="wavelength"))
    light = light / _simpson(light) * intensity
    return light.loc[400:700]

def light_spectra(which:str=None, intensity:float=1.0)-> _npt.ArrayLike:
    """Get the light spectrum of a common light source in the range of 400 nm - 700 nm with a set integrated intensity

    Args:
        which (str): name of the spectrum to be returned. One of 'solar', 'halogen_lamp', 'cool_white_led', 'warm_white_led', 'fluorescent_lamp', 'incandescent_bulb'
        intensity (float, optional): integrated light intensity. Defaults to 1.

    Returns:
        _npt.ArrayLike: an array of wavelength-specific light intensities
    """
    if which is None:
        print("possible spectra:\n",sorted(list(_lights_df.columns)))
        return _np.array([])
    try:
        return _lights_df.loc[:,which] * intensity
    except KeyError as e:
        raise KeyError(f"'{e}' is not a provided spectrum")

def import_spectrum_from_file(
        file, 
        format=None, 
        wlcol=0, 
        intcol=1, 
        interpol_method="linear"
    ):
    if format is None:
        format = _sub("^.*\.([\w]+)$","\\1",file)
    
    # Read formats
    if format=="csv":
        dat = _pd.read_csv(file, index_col=wlcol).iloc[:,intcol-1]
    else:
        raise ValueError(f"file format '{format}' not recognized")
    
    # Check if index range is sufficient
    if dat.index[0] > 400 or dat.index[-1] < 700:
        raise ValueError("The imported spectrum must cover the range 400 nm - 700 nm")

    # Interpolate if necessary
    ipol_points = [x for x in _np.arange(400,701) if x not in dat.index]
    if len(ipol_points) > 0:
        pad = _pd.Series(index=ipol_points, dtype="float64")
        dat_ipol = _pd.concat((dat,pad)).sort_index().interpolate(method = interpol_method)

        dat = dat_ipol.loc[_np.arange(400,701)]
        dat.index = _np.arange(400,701)
    else:
        dat = dat.loc[400:700]

    # Normalise to integral 1
    dat = dat / _simpson(dat)

    return dat


# Plot functions
def plot_spectra(df, spectrum_type=None, title=False, ax=None):
    df = df.copy()
    pot_spectrum_type = None

    # If df is a _pd.Series, treat it as a light spectrum
    if type(df) is _pd.Series:
        pot_spectrum_type = "light"
    else:
        # Remove additional index levels
        # Save the second index level as potential spectrum type
        if type(df.columns) is _pd.core.indexes.multi.MultiIndex:
            pot_spectrum_type = df.columns.levels[1].to_list()[0]
            df.columns = df.columns.droplevel(_np.arange(1,len(df.columns.levels)).tolist())

    # Make plot
    if ax is None:
        fig, ax = _plt.subplots()
    else:
        fig = ax.figure
    ax = df.plot(ax=ax)
    ax.set_xlabel("Light wavelength [nm]")

    # Set the ylabel according to the spectrum type
    if spectrum_type == "light" or (spectrum_type is None and pot_spectrum_type == "light"):
        ax.set_ylabel("Spectral photon flux density\n[µmol(Photons) m$^{-2}$ s$^{-1}$]")
        if title:
            ax.set_title(f"Light [{_np.round(_simpson(df), 2)} µmol(Photons)" + r" m$^{-2}$ s$^{-1}$]")
    elif spectrum_type == "ac_pigment" or (spectrum_type is None and pot_spectrum_type == "absorption_coefficient_m2_mgPigment-1"):
        ax.set_ylabel("Absorption coefficient [m$^2$ mg(Pigment)$^{-1}$]")
    elif spectrum_type == "ac_chl" or (spectrum_type is None and pot_spectrum_type == "absorption_coefficient_m2_mgChla-1"):
        ax.set_ylabel("Absorption coefficient [m$^2$ mg(Chl)$^{-1}$]")
    elif spectrum_type is None:
        ax.set_ylabel("ADD LABEL")
    else:
        raise ValueError(f"spectrum_type '{spectrum_type}' not recognised")

    return fig, ax

def plot_absorption(df, ax=None):
    if ax is None:
        fig, ax = _plt.subplots()
    else:
        fig = ax.figure
    ax = df.transpose().plot.bar(ax=ax, stacked=True)
    ax.set_xlabel("Irradiance")
    ax.set_ylabel("Light absorption per complex\n[µmol(Photons) mg(Chla)$^{-1}$ s$^{-1}$]")

    return fig, ax

# %%
# Get the pre-specified lights
_lights = [x[:-4] for x in _listdir(_DATAPATH/"lights/") if x!= "README.md"]
_lights_df = _pd.DataFrame({key:_pd.read_csv(_DATAPATH/f"lights/{key}.csv", index_col=0).squeeze(1) for key in _lights})

# %%
# Read absorption and default concentration data 
pigments_Fuente = _pd.read_csv(_DATAPATH/"pigment_concentrations.csv", index_col=0).squeeze(1)

_abs_coef = _pd.concat({pig:_pd.read_csv(_DATAPATH/f"per_pigment/{pig}.csv", index_col=0) for pig in pigments_Fuente.index}, axis=1)

# Get the molar masses
_molmasses = _pd.read_csv(_DATAPATH/"molar_masses.csv", index_col=0).squeeze(1)

# %%
# Read the photosystems compositions and calculate their pigment association
_ps_comp = _pd.read_csv(_DATAPATH/"photosystem_composition.csv", index_col=0)
association_Fuente = get_pigment_association(ps1_ratio=5)

# %%
# Define the default absorption
absorption_Fuente = get_pigment_absorption(pigments_Fuente)

# %%
# Define the default light spectra
lights_Fuente = {
    "S": light_spectra("solar", 1),
    "I": light_spectra("incandescent_bulb", 1),
    "F": light_spectra("fluorescent_lamp", 1),
    "H": light_spectra("halogen_lamp", 1),
    "C": light_spectra("cool_white_led", 1),
    "W": light_spectra("warm_white_led", 1),
    "B": light_gaussianLED(440, 1),
    "T": light_gaussianLED(480, 1),
    "G": light_gaussianLED(550, 1),
    "A": light_gaussianLED(590, 1),
    "O": light_gaussianLED(624, 1),
    "R": light_gaussianLED(674, 1),
}

# Define functions for getting the effective irradiance
def _I_depth_INT(I0, depth, absorption_coef, chlorophyll_sample):
    return I0 * 1/(-absorption_coef * chlorophyll_sample) * _np.exp(-depth * absorption_coef * chlorophyll_sample)

def get_mean_sample_light(I0:_Union[_pd.Series, _ArrayLike], depth:float, absorption_coef:_pd.Series, chlorophyll_sample:float, depth0:float=0) -> _pd.Series:
    """Calculate the light experienced by an average cell in a sample

    Args:
        I0 (Union[pd.Series, np.ArrayLike]): initial light as specific irradiance per wavelength OR a list of such
        depth (float): depth of the sample in which the irradiance is exponentially attenuated
        absorption_coef (pd.Series): specific absorption coefficients per wavelength
        chlorophyll_sample (float): chlorophyll content of the sample
        depth0 (float, optional): depth of the initial light. Defaults to 0.

    Returns:
        pd.Series: adjusted light vector OR a list of such
    """
    # Calculate the adjustment for a single irradiace or a list of such
    if isinstance(I0, _pd.Series):
        I_diff = _I_depth_INT(I0, depth, absorption_coef, chlorophyll_sample) - _I_depth_INT(I0, depth0, absorption_coef, chlorophyll_sample)
        return I_diff / (depth - depth0)

    elif isinstance(I0, (list,_np.ndarray)):
        if _np.all([isinstance(i, _pd.Series) for i in I0]):
            I_diff = [(_I_depth_INT(Icurr, depth, absorption_coef, chlorophyll_sample) - _I_depth_INT(Icurr, depth0, absorption_coef, chlorophyll_sample)) / (depth - depth0) for Icurr in I0]
            return I_diff
    
    raise ValueError("I0 must be a pd.Series or a list of such")
