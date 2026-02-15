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

model_title = "Matuszynska2016"
model_doi = "https://doi.org/10.1016/j.bbabio.2016.09.003"

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

PQH_2 = remove_math(comps_table, r"$\mathrm{PQH}_2$")
H_lu = remove_math(comps_table, r"$\mathrm{H}$")
ATPase_ac = remove_math(comps_table, r"$\mathrm{ATPase}^*$")
ATP_st = remove_math(comps_table, r"$\mathrm{ATP}$")
psbS = remove_math(comps_table, r"$\mathrm{PsbS}$")
Vx = remove_math(comps_table, r"$\mathrm{Vx}$")

# -- Derived Compounds --

pH_lu = remove_math(derived_comps_table, r"$\mathrm{pH}$")
PQ = remove_math(derived_comps_table, r"$\mathrm{PQ}$")
ADP_st = remove_math(derived_comps_table, r"$\mathrm{ADP}$")
PsbSP = remove_math(derived_comps_table, r"$\mathrm{PsbS^P}$")
Zx = remove_math(derived_comps_table, r"$\mathrm{Zx}$")
Q = remove_math(derived_comps_table, r"")
B0 = remove_math(derived_comps_table, r"$\mathrm{B_0}$")
B1 = remove_math(derived_comps_table, r"$\mathrm{B_1}$")
B2 = remove_math(derived_comps_table, r"$\mathrm{B_2}$")
B3 = remove_math(derived_comps_table, r"$\mathrm{B_3}$")
Fluo = remove_math(derived_comps_table, r"$\mathrm{Fluo}$")

# -- Rates --

v_PSII = remove_math(rates_table, r"$v_{\mathrm{PSII}}$")
v_PQ = remove_math(rates_table, r"$v_{\mathrm{PQ}_{\mathrm{ox}}}$")
v_ATPsynth = remove_math(rates_table, r"$v_{\mathrm{ATPsynthase}}$")
v_ATPact = remove_math(rates_table, r"$v_{\mathrm{ATPactivity}}$")
v_Leak = remove_math(rates_table, r"$v_{\mathrm{Leak}}$")
v_ATPcons = remove_math(rates_table, r"$v_{\mathrm{ATP}_{\mathrm{consumption}}}$")
v_Xcyc = remove_math(rates_table, r"$v_{\mathrm{Xcyc}}$")
v_PsbSP = remove_math(rates_table, r"$v_{\mathrm{Psbs^P}}$")

# -- Parameters --

PSII_tot = remove_math(params_table, r"$\mathrm{PSII^{tot}}$")
PQ_tot = remove_math(params_table, r"$\mathrm{PQ^{tot}}$")
AP_tot = remove_math(params_table, r"$\mathrm{AP^{tot}}$")
PsbS_tot = remove_math(params_table, r"$\mathrm{PsbS^{tot}}$")
X_tot = remove_math(params_table, r"$\mathrm{X^{tot}}$")
O2_ex = remove_math(params_table, r"$\mathrm{O_2^{ex}}$")
Pi = remove_math(params_table, r"$\mathrm{Pi^{mol}}$")
k_Cytb6f = remove_math(params_table, r"$k_{\mathrm{Cytb6f}}$")
k_ActATPase = remove_math(params_table, r"$k_{\mathrm{ActATPase}}$")
k_DeactATPase = remove_math(params_table, r"$k_{\mathrm{DeactATPase}}$")
k_ATPsynth = remove_math(params_table, r"$k_{\mathrm{ATPsynthase}}$")
k_ATPconsum = remove_math(params_table, r"$k_{\mathrm{ATPconsumption}}$")
k_PQH2 = remove_math(params_table, r"$k_{\mathrm{PQred}}$")
k_H = remove_math(params_table, r"$k_H$")
k_F = remove_math(params_table, r"$k_F$")
k_P = remove_math(params_table, r"$k_P$")
k_PTOX = remove_math(params_table, r"$k_\mathrm{PTOX}$")
pH_st = remove_math(params_table, r"$\mathrm{pH}_\mathrm{stroma}$")
k_leak = remove_math(params_table, r"$k_\mathrm{leak}$")
b_H = remove_math(params_table, r"$b_\mathrm{H}$")
hpr = remove_math(params_table, r"$\mathrm{HPR}$")
k_DV = remove_math(params_table, r"$k_\mathrm{DeepoxV}$")
k_EZ = remove_math(params_table, r"$k_\mathrm{EpoxZ}$")
K_pHSat = remove_math(params_table, r"$K_\mathrm{pHSat}$")
nhx = remove_math(params_table, r"$\mathrm{nH}_\mathrm{X}$")
K_ZSat = remove_math(params_table, r"$K_\mathrm{ZSat}$")
nhl = remove_math(params_table, r"$\mathrm{nH}_\mathrm{L}$")
k_deprot = remove_math(params_table, r"$k_\mathrm{Deprotonation}$")
k_prot = remove_math(params_table, r"$k_\mathrm{Protonation}$")
K_pHSatLHC = remove_math(params_table, r"$K_\mathrm{pHSatLHC}$")
gamma_0 = remove_math(params_table, r"$\gamma_0$")
gamma_1 = remove_math(params_table, r"$\gamma_1$")
gamma_2 = remove_math(params_table, r"$\gamma_2$")
gamma_3 = remove_math(params_table, r"$\gamma_3$")
F = remove_math(params_table, r"$F$")
R = remove_math(params_table, r"$R$")
T = remove_math(params_table, r"$T$")
E0_QA = remove_math(params_table, r"$E^0\mathrm{(QA/QA^-)}$")
E0_PQ = remove_math(params_table, r"$E^0\mathrm{(PQ/PQH_2)}$")
E0_PC = remove_math(params_table, r"$E^0\mathrm{(PC/PC^-)}$")
DG_ATP = remove_math(params_table, r"$\Delta G_{0_{\mathrm{ATP}}}$")
pfd = remove_math(params_table, r"$\mathrm{PFD}$")

# --- Derived Parameters ---

H_st = remove_math(derived_params_table, r"$\mathrm{H}_\mathrm{st}$")
K_pHSat_inv = remove_math(derived_params_table, r"$K_{\mathrm{pHSat}_\mathrm{inv}}$")
K_pHSatLHC_inv = remove_math(
    derived_params_table, r"$K_{\mathrm{pHSatLHC}_\mathrm{inv}}$"
)
K_QAPQ = remove_math(derived_params_table, r"$K_\mathrm{eq, QAPQ}$")
K_cytb6f = remove_math(derived_params_table, r"$K_\mathrm{eq, ATPsynthase}$")
K_ATPsynth = remove_math(derived_params_table, r"$K_\mathrm{eq, cytb6f}$")

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""The [{model_title}]({model_doi}) model, a small kinetic model, was developed to delve deeper into the effect of light memory caused by non-photochemical quenching. The systematic investigation of the Xanthophyll cycle, a combination of the pigments of violaxanthin, antheraxanthin, and zeaxanthin, sparked a series of experiments to determine whether plant light memory can be detected in a time-scale of minutes to hours through pulse amplitude modulated chlorophyll fluorescence. The model was then created based on these experimental results, providing a comprehensive description of NPQ dynamics and the short-term memory of the *Arabidopsis thaliana* plant.

To keep the model as simple as possible, several processes not directly linked to NPQ have been simplified to create a dynamic ODE system consisting only of 6 different compounds. With these simplifications, the authors could fulfil an additional goal: to make a general framework that is not specific to one model organism.

To demonstrate the adaptability of their model, the authors took their calibrated *Arabidopsis thaliana* model and successfully applied it to the non-model organism *Epipremnum aureum*. This adaptation allowed them to simulate realistic fluorescence measurements and replicate all the key features of chlorophyll induction, showcasing the model's versatility and potential for use in a variety of organisms.

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

mdFile.new_paragraph(rf"""
<details>
<summary>ODE System</summary>

```math 
{ode(PQH_2)} = {v_PSII} - {v_PQ}
```
```math 
{ode(H_lu)} = \frac{{2}}{{{b_H}}} \cdot {v_PSII} + \frac{{4}}{{{b_H}}} \cdot {v_PQ} + \frac{{-\left( \frac{{14}}{{3}} \right)}}{{{b_H}}} \cdot {v_ATPsynth} + \frac{{-1}}{{{b_H}}} \cdot {v_Leak}
```
```math 
{ode(ATP_st)} = {v_ATPsynth} - {v_ATPcons}
```
```math 
{ode(ATPase_ac)} = {v_ATPact}
```
```math 
{ode(Vx)} = - {v_Xcyc}
```
```math 
{ode(psbS)} = - {v_PsbSP}
```

</details>
                     """)

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(rf"""

<details>
<summary> Calculations </summary>

```math
{pH_lu} =  -\log_{{10}} \left( {H_lu} \cdot 0.00025 \right)
```
```math
{PQ} = {PQ_tot} - {PQH_2}
```
```math
{ADP_st} = {AP_tot} - {ATP_st}
```
```math
{PsbSP} = {PsbS_tot} - {psbS}
```
```math
{Zx} = {X_tot} - {Vx}
```
```math
{Q} =  {gamma_0} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) {psbS} + {gamma_1} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) {PsbSP} + {gamma_2} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbSP} + {gamma_3} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {psbS}
```
```math
{Fluo} =  \frac{{{k_F}}}{{{k_H} \cdot {Q} + {k_F} + {k_P}}} \cdot {B0} + \frac{{{k_F}}}{{{k_H} \cdot {Q} + {k_F}}} \cdot {B2}
```

<details>
<summary>Quasi steady-state approximation to calculate the rate of PSII</summary>

```math
    \begin{{align}}
        0 &= - \left( {pfd} + \frac{{{k_PQH2}}}{{{K_QAPQ}}} \cdot {PQ} \right) \cdot {B0} + \left( {k_H} \cdot Q + {k_F} \right) \cdot {B1} + {k_PQH2} \cdot {PQH_2} \cdot {B3} \\
        0 &= {pfd} \cdot {B0} - \left( {k_H} \cdot Q + {k_F} + {k_P} \right) \cdot {B1} \\
        0 &= {pfd} \cdot {B2} - \left( {k_H} \cdot Q + {k_F} \right) \cdot {B3} \\
        {PSII_tot} &= {B0} + {B1} + {B2} + {B3} 
    \end{{align}}
```
</details>
</details>

                     """)

mdFile.new_header(3, "Parameters")

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, "Derived Parameters")

mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

mdFile.new_paragraph(rf"""

<details>
<summary>Equations of derived parameters</summary>

```math
{H_st} =  32000.0 \cdot 10^{{-{pH_st}}}
```
```math
{K_pHSat_inv} =  32000.0 \cdot 10^{{-{K_pHSat}}}
```
```math
{K_pHSatLHC_inv} =  32000.0 \cdot 10^{{-{K_pHSatLHC}}}
```
```math
{K_QAPQ} =  \exp \left( \frac{{-\left( -2 \cdot -{F} \cdot {E0_QA} + -2 \cdot {F} \cdot {E0_PQ} + 2 \cdot {pH_st} \cdot \ln 10 \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_cytb6f} =  \exp \left( \frac{{-\left( -\left( -2 {F} \cdot {E0_PQ} + 2 \cdot {R} \cdot {T} \cdot \ln 10 \cdot {pH_lu} \right) + 2 \cdot -{F} \cdot {E0_PC} + 2 \cdot {R} \cdot {T} \cdot \ln 10 \cdot \left( {pH_st} - {pH_lu} \right) \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_ATPsynth} =  {Pi} \cdot \exp \left( \frac{{-\left( {DG_ATP} - \ln 10 \cdot \left( {pH_st} - {pH_lu} \right) \frac{{14}}{{3}} \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}} \right)
```

</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(rf"""

<details>
<summary>Rate equations</summary>

```math
{v_PSII} =  {k_P} \cdot 0.5 {B1}
```
```math
{v_PQ} =  \left( \frac{{{k_Cytb6f} \cdot {pfd} \cdot {K_cytb6f}}}{{{K_cytb6f} + 1}} + {k_PTOX} \cdot {O2_ex} \right) {PQH_2} - \frac{{{k_Cytb6f} \cdot {pfd}}}{{{K_cytb6f} + 1}} \cdot \left( {PQ_tot} - {PQH_2} \right)
```
```math
{v_ATPsynth} =  {ATPase_ac} \cdot {k_ATPsynth} \cdot \left( {AP_tot} - {ATP_st} - \frac{{{ATP_st}}}{{{K_ATPsynth}}} \right)
```
```math
{v_ATPact} =  {k_ActATPase} \cdot \left( {pfd} > 0 \right) \left( 1 - {ATPase_ac} \right) - {k_DeactATPase} \cdot \left( 1 - \left( {pfd} > 0 \right) \right) {ATPase_ac}
```
```math
{v_Leak} =  {k_leak} \cdot \left( {H_lu} - {H_st} \right)
```
```math
{v_ATPcons} =  {k_ATPconsum} \cdot {ATP_st}
```
```math
{v_Xcyc} =  {k_DV} \cdot \frac{{{H_lu}^{{{nhx}}}}}{{{H_lu}^{{{nhx}}} + {K_pHSat_inv}^{{{nhx}}}}} \cdot {Vx} - {k_EZ} \cdot \left( {X_tot} - {Vx} \right)
```
```math
{v_PsbSP} =  {k_prot} \cdot \frac{{{H_lu}^{{{nhl}}}}}{{{H_lu}^{{{nhl}}} + {K_pHSatLHC_inv}^{{{nhl}}}}} \cdot {psbS} - {k_deprot} \cdot \left( {PsbS_tot} - {psbS} \right)
```

</details>

                     """)

mdFile.new_header(3, "Figures")

mdFile.new_paragraph("""You can find the recreation of the figures from the original publication below. Due to differing copyright reasons the original figures cannot be included in this README file. Instead, the comparision has to be made using the original publication.""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 4</summary>
                     
<img style='float: center' src='figures/Matuszynska_fig4.svg'>
           
Pulse Amplitude Modulation (PAM) of wild type *Arabidopsis thaliana* experimentally obtained and simulated through the model for three different setups. The experimental data was collected through a series of 3 replications, where the plant was introduced to three phases. An initial light exposure, relaxation in the dark and a second light exposure. Several different types of data were collected through PAM, where the flourescence emission of a small area on the plant leaf has been monitored, during several applications of saturating pulses of light in increasing inter-pulse intervals. The experimental data shown in this figure are the maximal flourescence ($F_M$) and the ... flourescence ($F_S$), which were both normalized to the first point of the respective data. Several experiments were done, based on the duration of the relaxation phase and the light intensity of the light exposure phase. In this figure, the data for the 15 min, 30 min, 60 min and $100 \mathrm{{\mu E m^{{-2}}s^{{-1}}}}$, $300 \mathrm{{\mu E m^{{-2}}s^{{-1}}}}$, and $900 \mathrm{{\mu E m^{{-2}}s^{{-1}}}}$ light intensity, paired together, were used. This data was used as a comparision to the simulation strength of the model, where the internal parameter '${Fluo}$' was plotted against the time after simualting the model against the same PAM protocol used on the three different experiments. The results of the simulation was also normalized, however in this instance to the maximal value of the flourescence calcuated by the model. The top bar displays the three phases and the prior dark phase to adapt the plant to the dark.

This figure could easily be recreated using the given `modelbase2` version of this model. However, the experimental data plotted in this figure were set at the timepoints of each flourescence peak and do not follow the recorded timepoints in from eahc experiment. In this instance, it is acceptable, as the experimental timepoints are likely skewed due to device measurement uncertainty, which would blow up the information given in this figure and may make it less readable.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/Matuszynska_fig5.svg'>

Visualisation of lumenal pH (${pH_lu}$), protonated PsbP (${PsbSP}$), and Zeaxanthin (${Zx}$) of simulated pulse amplitude modulation (PAM) measurements of wild type *Arabidopsis thaliana* and a parameter phase projection of ${pH_lu}$ and the quencher activity (${Q}$) under different light intensities. The simulated PAM protocol included three phases: an initial light exposure, relaxation in the dark and a second light exposure. Both light exposures were done with $100\ \mathrm{{\mu E\ m^{{-2}}\ s^{{-1}}}}$, $300\ \mathrm{{\mu E\ m^{{-2}}\ s^{{-1}}}}$, and $900\ \mathrm{{\mu E\ m^{{-2}}\ s^{{-1}}}}$ and the duration of the phases were $14 min$, $16 min$, and $5 min$ respectively. In the parameter phase projection, the red line indicates steady-state simulation results under light intensities from zero to 1000 in steps of 10, where each big red circle indicates one fo the prior listed light intensities.

This figure recreation was not incredibly succesful. While both graphs represent the same broader structure as in the paper, there are still inconsisticies in the finer detail. For example, the location of the red markers in the phase projection or the general course of the concentration plots, especially at a light intensity of $300 \mathrm{{\mu E\ m^{{-2}}\ s^{{-1}}}}$. However, we still believe it was mildly succesful.

</details>
""")

mdFile.new_header(3, "Demonstrations")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle using real Photosynthetic Photon Flux Density (PPFD) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal and is used to create a protocol for the light intensity PPFD over the course of the day, in a minute interval. The data used is filtered to only show a PPFD that equals or is higher than $40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$. This threshold is chosen as it has shown to allow most models to still simulate the photosynthetic machinery, while still being a decent representation of the actual daylight conditions. The simulation is run using the default parameters and initial conditions of each model, and the RuBisCO carboxylation rate (vRuBisCO), Adenosine Triphosphate (ATP) and Nicotinamide Adenine Dinucleotide Phosphate (NADPH) ratio, and fluorescence (F) results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>FvCB Submodule</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_fvcb.svg' alt='FvCB Submodule' width='600'/>

Comparison of modelled carbon assimilation (A) and RuBisCO carboxylation rate (vRuBisCO) against the Farquhar, von Caemmerer, and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025). To be able to simulate A, there are two mandatory quantities that need to be present in the model: carbon dioxide (CO2) concentration and vRuBisCO. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The simulation is then run until steady-state, or quasi-steady-state if not otherwise possible, for different intercellular CO2 concentration (Ci) partial pressure. The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model.

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

Sample simulation of a common Pulse Amplitude Modulation (PAM) protocol to show fluctuations of fluorescence (F) and Non-Photochemical Quenching (NPQ) using saturating pulses. The simulation protocol is as follows: A dark adaptation period that simulates for 30 minutes at a dark light intensity ($40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$), then the actual protocol starts. The protocol consists of 22 periods with each being 2 minutes of length. That period consists of a specific light intensity of the respective type of period and ends with a saturating pulse with a length of 0.8 s and a light intensity of $3000 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$. First, two dark periods with light intensity of $40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$, followed by ten light periods with light intensity of 1000 µmol m−2 s−1, then ten dark periods again. The simulation is run using the default parameters and initial conditions of each model.

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

A sample Metabolic Control Analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent  RuBisCO carboxylation rate (vRuBisCO), PSII rate (vPSII), PSI rate (vPSI), Cytb6f rate (vb6f) and ATP synthase rate (vATPSynth). The variables chosen should represent  carbon dioxide (CO2) concentration, Ribulose-1,5-bisphosphate (RuBP), oxidised plastoquinone (PQox), oxidised plastocyanin (PCox), denosine Triphosphate (ATP), and Nicotinamide Adenine Dinucleotide Phosphate (NADPH). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.01\%$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{{p}}^{{x}} = \frac{{x_\mathrm{{upper}} - x_\mathrm{{lower}}}}{{2 \cdot \mathrm{{disp}} \cdot p}}$, where $C_{{p}}^{{x}}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{{disp}}$ is the displacement value. $x_\mathrm{{upper}}$ and $x_\mathrm{{lower}}$ are the steady-state result of $x$ at either $+\mathrm{{disp}}$ and $-\mathrm{{disp}}$ respectively. It has to be noted that the (MCA) results can be very dependent on the other values of the parameters in the model, therefore the results shown here are only representative of the default parameter set of the model.

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

Sample fitting to experimental Non-Photochemical Quenching (NPQ) data. The NPQ data used is taken from experimental work published in von Bismarck (2022) and was acquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana (A. thaliana) plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 µs at a light intensity of $5000 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light ($903 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$) for approximately 10 minutes, followed by a lower actinic light of ($90 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of $40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$ is used to avoid numerical issues. The fitting is performed using the lmfit package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help the fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parameters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{{m}}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{{m}}$.
- If $F_\mathrm{{m}}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{{F_{{\mathrm{{m}}\vert t=0}} - F_{{\mathrm{{m}} \vert t}}}}{{F_{{\mathrm{{m}} \vert t}}}}$

**Notes:**

</details>
""")

mdFile.create_md_file()
