from pathlib import Path

from mdutils.mdutils import MdUtils  # noqa: E402

from GreenSlothUtils import gloss_fromCSV, remove_math

###### Util Functions ######

def ode(
    first_var: str,
    second_var: str = "t"
) -> str:
    for i in [first_var, second_var]:
        if "$" in i:
            msg = f"Your given variable '{i}' has a '$' in it"
            raise ValueError(msg)

    return rf"\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}"

###### Model Infos ######

model_title = "Fuente2024"
model_doi = "https://doi.org/10.1016/j.plaphy.2024.109138"

###### Glossaries ######

cite_dict = {}

model_info = Path(__file__).parent / "model_info"
python_written = model_info / "python_written"

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / "comps.csv",
    omit_col="Glossary ID"
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(
    path=model_info / "derived_comps.csv",
    omit_col="Glossary ID"
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / "rates.csv",
    omit_col="Glossary ID"
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / "params.csv",
    cite_dict=cite_dict
)

derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info / "derived_params.csv")

###### Variables for ease of access ######

# -- Compounds --

Q_active = remove_math(comps_table, r'$FQ_{act}$')
PQ = remove_math(comps_table, r'$PQ$')
PSI_ox = remove_math(comps_table, r'$PI_{ox}$')
H_lumen = remove_math(comps_table, r'$H_L$')
ATP_st = remove_math(comps_table, r'$ATP$')

# -- Derived Compounds --

Q_inactive = remove_math(derived_comps_table, r'$FQ_{inact}$')
PQH_2 = remove_math(derived_comps_table, r'$PQH_2$')
PSI_red = remove_math(derived_comps_table, r'$PI_{red}$')
ADP_st = remove_math(derived_comps_table, r'$ADP$')
RCII_closed = remove_math(derived_comps_table, r'$RCII_{closed}$')
RCII_open = remove_math(derived_comps_table, r'$RCII_{open}$')
Fluo = remove_math(derived_comps_table, r'$ChlF$')
NPQ = remove_math(derived_comps_table, r'$NPQ$')
O2 = remove_math(derived_comps_table, r'$O_2$')

# -- Rates --

v_PSII_O2 = remove_math(rates_table, r'$v_\mathrm{PSII}$')
v_PSI = remove_math(rates_table, r'$v_\mathrm{PSI}$')
v_PSII_PQ = remove_math(rates_table, r'$v_1$')
v_PQH2_PSI = remove_math(rates_table, r'$v_2$')
v3 = remove_math(rates_table, r'$v_3$')
v4 = remove_math(rates_table, r'$v_4$')
v_ATPsynth = remove_math(rates_table, r'$v_5$')
v_ATPcons = remove_math(rates_table, r'$v_6$')
v_Leak = remove_math(rates_table, r'$v_7$')
v_PQ = remove_math(rates_table, r'$v_\mathrm{X}$')

# -- Parameters --

stoic_PSII = remove_math(params_table, r'$nPSII$')
stoic_PSI = remove_math(params_table, r'$nPSI$')
PQ_tot = remove_math(params_table, r'$PQ_{tot}$')
H_stroma = remove_math(params_table, r'$[H^+]_{stroma}$')
AP_tot = remove_math(params_table, r'$A_{tot}$')
V_lumen = remove_math(params_table, r'$V_L$')
V_stroma = remove_math(params_table, r'$V_S$')
sigma_PSI_0 = remove_math(params_table, r'$\sigma _I$')
k1p = remove_math(params_table, r'$k_1^+$')
k1m = remove_math(params_table, r'$k_1^-$')
k2p = remove_math(params_table, r'$k_2^+$')
k2m = remove_math(params_table, r'$k_2^-$')
k3 = remove_math(params_table, r'$k_3$')
k4 = remove_math(params_table, r'$k_4$')
k5 = remove_math(params_table, r'$k_5$')
k6 = remove_math(params_table, r'$k_6$')
k7 = remove_math(params_table, r'$k_7$')
k_X = remove_math(params_table, r'$k_X$')
L_PSI = remove_math(params_table, r'$L_{1/2}$')
bH = remove_math(params_table, r'$b_H$')
NPQ_max = remove_math(params_table, r'$FQ_{max}$')
cEqP = remove_math(params_table, r'$cEqP$')
keq_NPQ = remove_math(params_table, r'$K_Q$')
n_NPQ = remove_math(params_table, r'$n$')
N_A = remove_math(params_table, r'$\mathrm{N_A}$')
PPFD = remove_math(params_table, r'$u_0$')
PPFD_add = remove_math(params_table, r'$u_1$')
f = remove_math(params_table, r'$f$')
PSI_total = remove_math(params_table, r'$PSI_{tot}$')
Fluo_0 = remove_math(params_table, r'$\frac{F_0}{F_\mathrm{v}}$')
Q_total = remove_math(params_table, r'$FQ_{tot}$')
time = r"\mathrm{time}"

# --- Derived Parameters ---

osc_light = remove_math(derived_params_table, r'$Light$')
sigma_PSII = remove_math(derived_params_table, r'$\sigma _{II}$')

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_header(2, "Summary")

mdFile.new_paragraph(f"""The [{model_title}]({model_doi}) model is a kinetic model of photosynthesis that is based on Occam's razor, aiming to provide the minimal complexity to describe the core processes of this model. In this case, the model focuses on the dynamic light oscillation and its responses on the photosynthetic machinery. It focuses only on the light-dependent reactions, including simplified versions of photosystem II, photosystem I, the Plastoquinone pool, and proton and ATP concentration in the lumen and stroma. On top of that, it shows the activation of non-photochemical quenching (NPQ), the dynamics of chlorophyll fluorescence, and the rate of oxygen evolution.
                     
The model includes the oscillating light intensity as a sinusoidal function, where the amplitude and frequency are adjustable parameters. To allow for easier comparision to other models, that often see light intensity as a constant value, the oscillation is defined around a base light intensity. However, the strength of having light with a specific frequency lies in the additional information and therefore analysis possibilities that can be performed. In this case, the model is used to create Bode plots of the response of fluorescence to light oscillations and comparing these results to experimental data from *Chlamydomonas reinhardtii*.

This simple model stays true to its name and the authors aim to provide a base model that can be easily extended, while still showing a new approach to photosynthesis modelling. Their work shows that even with a simple model, new insights can be gained by using dynamic light protocols, which may have been overlooked in traditional steady-state models. To further extend the usability of the model, the authors provide a detailed notebook written in the Wolfram language, which also shows how to recreate some of the publication's figures.
                     """)

mdFile.new_header(2, "Installation")

mdFile.new_paragraph(f"""
All the files needed to run this model are located in [model](./model) folder. To use this model you only need to copy this folder and write the following to import the model in your Python script:

```python
from model import {model_title}
```

The packages required to run this model can either be installed by using the `pixi` environment located inside the [pyproject.toml](../pyproject.toml) file or by just installing the `mxlpy` package and all its dependencies.
                     """)

mdFile.new_header(3, "Compounds")

mdFile.new_header(4, "Part of ODE system")

mdFile.new_table(columns = len(comps_table.columns), rows = len(comps_table_tolist), text = comps_table_list)

mdFile.new_paragraph(fr"""
<details>
<summary>ODE System</summary>

```math 
{ode(H_lumen)} = \frac{{{bH}}}{{{V_lumen} {N_A}}} \cdot {v_PSII_O2} + \frac{{{bH}}}{{{V_lumen} {N_A}}} \cdot {v_PQH2_PSI} + \frac{{\frac{{-14}}{{3}} \cdot {V_stroma}}}{{{V_lumen}}} \cdot {bH} \cdot {v_ATPsynth} - {v_Leak}
```
```math 
{ode(PSI_ox)} = - {v_PQH2_PSI} + {v_PSI}
```
```math 
{ode(PQ)} = 0.5 \cdot {v_PQH2_PSI} - 0.5 \cdot {v_PSII_PQ} + {v_PQ}
```
```math 
{ode(Q_active)} = {v3} - {v4}
```
```math 
{ode(ATP_st)} = {v_ATPsynth} - {v_ATPcons}
```

</details>
                     """)

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
{Q_inactive} =  {Q_total} - {Q_active}
```
```math
{PQH_2} =  {PQ_tot} - {PQ}
```
```math
{PSI_red} =  {PSI_total} - {PSI_ox}
```
```math
{ADP_st} =  {AP_tot} - {ATP_st}
```
```math
{RCII_closed} =  \frac{{1}}{{1 + \frac{{{k1p} \cdot {PQ}}}{{{sigma_PSII} \cdot {osc_light} + {k1m} \cdot {PQH_2}}}}}
```
```math
{RCII_open} =  \frac{{{k1p} \cdot {PQ}}}{{{sigma_PSII} + {k1m} \cdot {PQH_2} + {k1p} \cdot {PQ}}}
```
```math
{Fluo} =  {Fluo_0} + {RCII_closed} \cdot {sigma_PSII}
```
```math
{NPQ} =  \frac{{{NPQ_max} \cdot {Q_active}}}{{1 - {NPQ_max} \cdot {Q_active}}}
```
```math
{O2} =  \frac{{{PSI_total} \cdot \left( {k1p} \cdot {RCII_closed} \cdot {PQ} - {k1m} \cdot \left( 1 - {RCII_closed} \right) {PQH_2} \right)}}{{4}}
```

</details>

                     """)

mdFile.new_header(3, "Parameters")

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, "Derived Parameters")

mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Equations of derived parameters</summary>

```math
{osc_light} =  {PPFD} + {PPFD_add} \cdot \cos \le{f}t( 2 \mathrm{{np}}.\mathrm{{pi}} {f} \cdot {time} \right)
```
```math
{sigma_PSII} =  1 - {NPQ_max} \cdot {Q_active}
```

</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
{v_PSII_O2} =  {stoic_PSII} \cdot {sigma_PSII} \cdot {osc_light} \cdot \left( 1 - {RCII_closed} \right)
```
```math
{v_PSI} =  \frac{{{stoic_PSI} \cdot {sigma_PSI_0} \cdot {L_PSI} \cdot {osc_light}}}{{{L_PSI} + {osc_light}}} \cdot \left( {stoic_PSI} - {PSI_ox} \right)
```
```math
{v_PSII_PQ} =  {k1p} \cdot {RCII_closed} \cdot {PQ} - {k1m} \cdot {RCII_open} \cdot {PQH_2}
```
```math
{v_PQH2_PSI} =  {k2p} \cdot {PQH_2} \cdot {PSI_ox} - {k2m} \cdot {PQ} \cdot {PSI_red}
```
```math
{v3} =  \frac{{{k3} \cdot \left( 1 - {Q_active} \right)}}{{1 + \left( \frac{{{keq_NPQ}}}{{{H_lumen}}} \right)^{{{n_NPQ}}}}}
```
```math
{v4} =  {k4} \cdot {Q_active}
```
```math
{v_ATPsynth} =  {k5} \cdot \left( {ADP_st} - \frac{{{ATP_st} \cdot \left( \frac{{{H_stroma}}}{{{H_lumen}}} \right)^{{\frac{{14}}{{3}}}}}}{{{cEqP}}} \right)
```
```math
{v_ATPcons} =  {k6} \cdot {ATP_st}
```
```math
{v_Leak} =  {k7} \cdot \left( {H_lumen} - {H_stroma} \right)
```
```math
{v_PQ} =  {k_X} \cdot {PQH_2}
```

</details>
"""
)
mdFile.new_header(3, "Figures")

mdFile.new_paragraph("""You can find the recreation of the figures from the original publication below. Due to differing copyright reasons the original figures cannot be included in this README file. Instead, the comparision has to be made using the original publication.""")

# mdFile.new_paragraph(rf"""
                     
# <details>
# <summary>Figure </summary>
                     
# <img style='float: center' src=''>

# </details>
# """)

mdFile.new_header(3, "Demonstrations")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle (06:00 to 20:00) using real Photosynthetically active radiation (PAR) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal ([https://doi.org/10.48443/vzfh-7675])(https://doi.org/10.48443/vzfh-7675) and is used to create a protocol for the light intensity ($\mathrm{{PPFD}}$) over the course of the day, in a minute interval. The simulation is run using the default parameters and initial conditions of the model, and the RuBisCO carboxylation rate ($v_\mathrm{{RuBisCO|carbox}}$), $\mathrm{{ATP_{{st}}}}$ and $\mathrm{{NADPH_{{st}}}}$ ratio, and Flourescence results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>FvCB Submodule</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_fvcb.svg' alt='FvCB Submodule' width='600'/>

Comparison of modelled carbon assimilation ($A$) and carboxylation rate ($v_\mathrm{{c}}$) against the Farquhar, von Caemmerer and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025) [[1]](https://doi.org/10.1101/2025.03.11.642611). To be able to simulate carbon assimilation, there are two mandatory parameters that need to be present in the model: CO2 concentration and $v_\mathrm{{c}}$. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The simulation is then run until steady-state, or quasi-steady-state if not otherwise possible, for different intercellular CO<sub>2</sub> partial pressure ($\mathrm{{C_i}}$). The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model.

**Assumptions:**

- If no CO<sub>2</sub> concentration nor rate of rubisco carboxylation ($v_\mathrm{{c}}$) is present in the model, no comparison will be shown
- Infinite mesophyll conductance, therefore intercellular CO<sub>2</sub> partial pressure equals chloroplast partial pressure ($\mathrm{{C_i}} = \mathrm{{C_c}}$)
- If no $\mathrm{{C_i}}$ is present in the model, it will be added as a parameter assuming an initial value of CO<sub>2</sub> concentration divided by Henry's law constant for CO<sub>2</sub> ($H_\mathrm{{s}}^{{cp}}$)
- If no $H_\mathrm{{s}}^{{cp}}$ is present in the model, it will be added as a parameter with a value of $3.4 \times 10^{{-4}}\ \mathrm{{mmol\ Pa^ {{-1}}}}$ [[2]](https://doi.org/10.5194/acp-23-10901-2023)
- If no CO<sub>2</sub> compensation point in the absence of non-photorespiratory CO<sub>2</sub> release ($\Gamma ^*$) is present in the model, it will be added as a parameter with a value of $38.6\ \mathrm{{\mu bar}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $R_\mathrm{{light}}$ is present in the model, it will be added as a parameter with a value of $1\ \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $A$ is present in the model, it will be added as a derived variable following the FvCB equation [[1]](https://doi.org/10.1101/2025.03.11.642611): $v_\mathrm{{c}} \cdot \left(1 - \frac{{\Gamma ^*}}{{C_i}}\right) - R_\mathrm{{light}}$
- To be able to compare with original FvCB curves, the model needs to have $v_\mathrm{{c}}$ following the same units as the FvCB model ($\mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$). The `mM_to_µmol_per_m2` can be used to convert from mM to $\mathrm{{\mu mol\ m^{{-2}}}}$ assuming a volume factor of $0.0112\ \mathrm{{L\ m^{{-2}}}}$ in the stroma [[3]](https://doi.org/10.1007/s11120-006-9109-1). If the given units are in mM, the conversion will be done automatically, by adding a derived parameter with the converted values.

**Notes:**

| Parameter                 | In Model          |
| -----------               | -----------       |
| $\mathrm{{CO}}_2$         | None          |
| $v_\mathrm{{c}}$          | None  |
| $\mathrm{{C_i}}$          | None          |
| $H_\mathrm{{s}}^{{cp}}$   | None              |
| $\Gamma ^*$               | None              |
| $R_\mathrm{{light}}$      | None        |
| $A$                       | None            |


</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>PAM Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_pam.svg' alt='PAM Simulation' width='600'/>

Sample simulation of a common PAM protocol to show fluctuations of Flourescence and NPQ using saturating pulses. The simulation protocol is as follows: A dark adaptation period that simulates for 30 minutes at a dark light intensity (40 µmol m⁻² s⁻¹), then the actual protocol starts. The protocol consists of 22 periods with each being 2 minutes of length. That period consists of a specific light intensity of the respective type of period and ends with a saturating pulse with a length of 0.8 s and a light intensity of 3000 µmol m⁻² s⁻¹. First two dark periods with light intensity of 40 µmol m⁻² s⁻¹, followed by ten light periods with light intensity of 1000 µmol m⁻² s⁻¹, then ten dark periods again. The simulation is run using the default parameters and initial conditions of the model.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{{m}}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{{m}}$.
- If $F_\mathrm{{m}}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{{F_{{\mathrm{{m}}\vert t=0}} - F_{{\mathrm{{m}} \vert t}}}}{{F_{{\mathrm{{m}} \vert t}}}}$

**Notes:**

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Photosynthesis MCA</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_mca.svg' alt='Photosynthesis MCA' width='600'/>

A sample metabolic control analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent RuBisCO carboxylation rate ($v_\mathrm{{RuBisCO \vert C}}$), rate of photosystem II ($v_\mathrm{{PSII}}$), rate of photosystem I ($v_\mathrm{{PSI}}$), rate of cytochrome b<sub>6</sub>f ($v_\mathrm{{cytb6f}}$) and rate of ATP synthesis ($v_\mathrm{{ATPsynthase}}$). The variables chosen should represent CO<sub>2</sub> concentration ($\mathrm{{CO_2}}$), Ribulose-1,5-bisphosphate concentration ($\mathrm{{RUBP}}$), oxidised Plastoquinone ($\mathrm{{PQ_{{ox}}}}$), oxidised Plastocyanin ($\mathrm{{PC_{{ox}}}}$), adenosine triphosphate concentration ($\mathrm{{ATP}}$), and nicotinamide adenine dinucleotide phosphate concentration ($\mathrm{{NADPH}}$). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.0001$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{{p}}^{{x}} = \frac{{x_\mathrm{{upper}} - x_\mathrm{{lower}}}}{{2 \cdot \mathrm{{disp}} \cdot p}}$, where $C_{{p}}^{{x}}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{{disp}}$ is the displacement value. $x_\mathrm{{upper}}$ and $x_\mathrm{{lower}}$ are the steady-state result of $x$ at either $+\mathrm{{disp}}$ and $-\mathrm{{disp}}$ respectively.

**Assumptions:**

- Steady-State needs to be achievable for the model to perform the MCA.
- The parameters for each coefficient, rates, and variables chosen need to be representative of the respective process.
- If a parameter, rate, or variable is not present in the model, the respective coefficient will be greyed out in the Heatmap.

**Notes:**

| Coefficient                   | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | None|
| $\mathrm{{PSI}}$              | None |
| $\mathrm{{RuBisCO \vert C}}$  | None |
| $\mathrm{{cytb6f}}$           | None              |
| $\mathrm{{ATPsynthase}}$      | None              |

| Flux                          | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | None |
| $\mathrm{{PSI}}$              | None |
| $\mathrm{{RuBisCO \vert C}}$  | None |
| $\mathrm{{cytb6f}}$           | None              |
| $\mathrm{{ATPsynthase}}$      | None              |

| Variable                  | In Model      |
| -----------               | -----------   |
| $\mathrm{{CO_2}}$         | None       |
| $\mathrm{{RUBP}}$         | None      |
| $\mathrm{{PQ_{{ox}}}}$    | None          |
| $\mathrm{{PC_{{ox}}}}$    | None          |
| $\mathrm{{ATP}}$          | None    |
| $\mathrm{{NADPH}}$        | None  |

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>PAM Fitting</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_fitting.svg' alt='PAM Fitting' width='600'/>

Sample fitting to experimental NPQ data. The NPQ data used is taken from experimental work published in ([https://doi.org/10.1111/nph.18534](https://doi.org/10.1111/nph.18534)) and was aquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 ms at a light intensity of 5000 µmol m⁻² s⁻¹. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light (903 µmol m⁻² s⁻¹) for approximately 10 minutes, followed by a lower actinic light of (90 µmol m⁻² s⁻¹) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of 40 µmol m⁻² s⁻¹ is used to avoid numerical issues. The fitting is performed using the `lmfit`package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parmaters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{{m}}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{{m}}$.
- If $F_\mathrm{{m}}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{{F_{{\mathrm{{m}}\vert t=0}} - F_{{\mathrm{{m}} \vert t}}}}{{F_{{\mathrm{{m}} \vert t}}}}$

**Notes:**

</details>
""")

mdFile.create_md_file()
