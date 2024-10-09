# CyclicPhotosyn 2021

Expansion of the photosynthesis model by Matuszynska et al. 2019 with a focus on cyclic electron flow and the Mehler reaction.  

## Use

Install [miniconda](https://docs.conda.io/en/latest/miniconda.html).


Create the conda environment from the supplied `environment.yml`

`conda env create -f environment.yml`

Run notebooks in the `analysis` folder via jupyter notebook

`jupyter notebook`

## Changelog

## 2021-05-31

- Multiplied the H2O2 stoichiometry coefficient by a conversion factor to convert units of lumen to stroma, cause H2O2 is released into stroma and has the same concentartion as ATP and NADPH

## 2021-05-30

- cosmetic changes: the dynamic equilibria Keq_ATPsynthase and Keq_B6f are now dependent variables

## 2021-05-07

- Replaced fCBB with thioredoxin enzyme activation
- Added generic consumption terms for ATP and NADPH

### 2021-04-28

- Changed fCBB to derived parameter from PFD

### 2021-04-13

- Added fCBB speedup factor

### 2021-04-01

- Reset to measured kcat values
- Kmehler tuned to a number that suits our physiological metabolite levels (1)

Notes

- Dependency on outer cycle in higher light conditions (even though the flux is not high)
- inner/outer cycle fluxes ratio more or less like the ones from literature
- No calvin cycle collapse in excess light, therefore no excess consumption of NADPH due to ROS scavenging
- Got rid of unrealistic and unhealthy ROS spikes during time course simulations by using steady state values after pfd 1500 as new initial conditions

### 2021-03-30

- Removed constants from MDA and GR

### 2021-03-29

- Ad-hoc estimated rate constants of vAPX to be in agreement with literature [^1] kM and kcat values
- Added vDHAR reaction from Valero 2009
    - Adjusted units to mM
- Added v3ASC reaction from Valero 2009
    - Adjusted units to mM
- Added vGR reaction from Valero 2009
    - Added km values in denominator to avoid division by zero
    - Adjusted units to mM
- Removed kprop parameter
- In order to carry reasonable flux (compensate the incoming amount of H2O2 concentration), the vmax of either the inner or outer circle needs to be increased. Due to the fact that in various literature the outer circle is considered to be the key reaction, we decided to increase the vmax of vGR and vDHAR by a factor of 10

### 2021-03-09

- Simplified steps from Valero to chain reaction (vMehler, vMDAreduct and vAscorbate)
- Added vMehler reaction
- Changed vFd_red to depend on A1 and A2 states of PSI
- Changed vPSI to not affect Fd anymore
- Added ps1analytic_mehler to account for O2 formation
- Modified vMDAreduct
    - Added km values in denominator to avoid division by zero

### 2021-02-23

- Added vAscorbate reaction
    - Designed rate law via Cramers rule
- Implemented reactions from Valero 2016
    - Adjusted units to mM

[^1] [Kitajima 2007](https://doi.org/10.1111/j.1742-4658.2007.06214.x)
