from pathlib import Path
from xml.parsers.expat import model

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

model_title = "Bellasio2019"
model_doi = "https://doi.org/10.1007/s11120-018-0601-1"

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

CO2 = remove_math(comps_table, r'$\left[\mathrm{CO_2}\right]$')
HCO3 = remove_math(comps_table, r'$\left[\mathrm{HCO_3^-}\right]$')
RUBP = remove_math(comps_table, r'$\left[\mathrm{RuBP}\right]$')
PGA = remove_math(comps_table, r'$\left[\mathrm{PGA}\right]$')
DHAP = remove_math(comps_table, r'$\left[\mathrm{DHAP}\right]$')
ATP_st = remove_math(comps_table, r'$\left[\mathrm{ATP}\right]$')
NADPH_st = remove_math(comps_table, r'$\left[\mathrm{NADPH}\right]$')
RU5P = remove_math(comps_table, r'$\left[\mathrm{RuP}\right]$')
Ract = remove_math(comps_table, r'$R_{\mathrm{act}}$')
J_NADPH = remove_math(comps_table, r'$J_\mathrm{NADPH}$')
J_ATP = remove_math(comps_table, r'$J_\mathrm{ATP}$')
Ci = remove_math(comps_table, r'$C_\mathrm{i}$')
gs = remove_math(comps_table, r'$g_\mathrm{S}$')

# -- Derived Compounds --

ADP_st = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
NADP_st = remove_math(derived_comps_table, r'$\mathrm{NADP}$')
Pi_st = remove_math(derived_comps_table, r'$\mathrm{P_i}$')
PhiPSII = remove_math(derived_comps_table, r'$Y\mathrm{(II)}$')
A = remove_math(derived_comps_table, r'$A$')
O2 = remove_math(derived_comps_table, r'$O_2$')

# -- Rates --

Ract_rate = remove_math(rates_table, r'$R_{\mathrm{act}\ t+\mathrm{d}t}$')
v_J_NADPH = remove_math(rates_table, r'$J_{\mathrm{NADPH}\ t+\mathrm{d}t}$')
v_J_ATP = remove_math(rates_table, r'$J_{\mathrm{ATP}\ t+\mathrm{d}t}$')
v_gs = remove_math(rates_table, r'$g_{\mathrm{S}\ t+\mathrm{d}t}$')
v_RuBisCO_c = remove_math(rates_table, r'$V_C$')
rubisco_oxygenase = remove_math(rates_table, r'$V_O$')
glycine_decarboxylase = remove_math(rates_table, r'$\mathrm{GDC}$')
v_PRKase = remove_math(rates_table, r'$\mathrm{RuP_{Phosp}}$')
v_pgareduction = remove_math(rates_table, r'$\mathrm{PR}$')
v_carbohydrate_synthesis = remove_math(rates_table, r'$\mathrm{CS}$')
v_rpp = remove_math(rates_table, r'$\mathrm{RPP}$')
v_co2_hydration = remove_math(rates_table, r'$\mathrm{CA}$')
v_RLight = remove_math(rates_table, r'$R_\mathrm{LIGHT}$')
v_FNR = remove_math(rates_table, r'$v_\mathrm{NADPH}$')
v_ATPsynth = remove_math(rates_table, r'$v_\mathrm{ATP}$')
CO2_dissolution = remove_math(rates_table, r'$\mathrm{CO_2 dissolution}$')
CO2_stomatal_diffusion = remove_math(rates_table, r'$\mathrm{CO_2 stomatal diffusion}$')

# -- Parameters --

AP_tot = remove_math(params_table, r'$A_\mathrm{Tot}$')
Pi_tot = remove_math(params_table, r'$[P_\mathrm{i}]$')
p_o2 = remove_math(params_table, r'$\mathrm{p\ O_2}$')
Kh_o2 = remove_math(params_table, r'$K_\mathrm{h}\ \mathrm{O_2}$')
V_m = remove_math(params_table, r'Volume M')
PPFD = remove_math(params_table, r'$I_\mathrm{inc}$')
RLight = remove_math(params_table, r'$R_\mathrm{LIGHT}$')
s = remove_math(params_table, r'$s$')
PhiPSII_LL = remove_math(params_table, r'$Y(II)_\mathrm{LL}$')
PhiPSI_LL = remove_math(params_table, r'$Y(I)_\mathrm{LL}$')
alpha_ppfd_PhiPSII = remove_math(params_table, r'$\alpha_{Y(II)}$')
V0_ppfd_PhiPSII = remove_math(params_table, r'$V_{0Y(II)}$')
theta_ppfd_PhiPSII = remove_math(params_table, r'$\theta_{Y(II)}$')
f_pseudocycNR = remove_math(params_table, r'$f_\mathrm{PSEUDO\ NR}$')
fq = remove_math(params_table, r'$f_\mathrm{Q}$')
f_ndh = remove_math(params_table, r'$f_\mathrm{NDH}$')
h = remove_math(params_table, r'$h$')
Ca = remove_math(params_table, r'$C_\mathrm{a}$')
alpha_ppfd_rub = remove_math(params_table, r'$\alpha_\mathrm{V}$')
V0_ppfd_rub = remove_math(params_table, r'$V_{0}$')
theta_ppfd_rub = remove_math(params_table, r'$\theta_\mathrm{V}$')
alpha_co2 = remove_math(params_table, r'$\alpha_\mathrm{C}$')
V0_co2 = remove_math(params_table, r'$V_{0C}$')
theta_co2 = remove_math(params_table, r'$\theta_\mathrm{C}$')
tau_i = remove_math(params_table, r'$\tau_\mathrm{i}$')
tau_d = remove_math(params_table, r'$\tau_\mathrm{d}$')
km_v_RuBisCO_c_CO2 = remove_math(params_table, r'$K_\mathrm{C}$')
km_v_RuBisCO_c_RUBP = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{RuBP}$')
km_v_RuBisCO_c_O2 = remove_math(params_table, r'$K_\mathrm{O}$')
ki_v_RuBisCO_c_PGA = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{PGA}$')
ki_v_RuBisCO_c_NADP_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{NADP}$')
ki_v_RuBisCO_c_ADP_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{ADP}$')
ki_v_RuBisCO_c_Pi_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{P_i}$')
vmax_v_RuBisCO_c = remove_math(params_table, r'$V_\mathrm{cmax}$')
kcat_v_RuBisCO_c = remove_math(params_table, r'Cat n°')
S_co_gas = remove_math(params_table, r'$S_\mathrm{C/O}$')
vmax_v_PRKase = remove_math(params_table, r'$V_\mathrm{max}\ \mathrm{RuP_{Phosp}}$')
keq_v_PRKase = remove_math(params_table, r'$K_\mathrm{e}\ \mathrm{RuP_{Phosp}}$')
km_v_PRKase_ATP_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{ATP}$')
ki_v_PRKase_ADP_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{ADP}$')
km_v_PRKase_RU5P = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{RuP}$')
ki_v_PRKase_PGA = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{PGA}$')
ki_v_PRKase_RUBP = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{RuBP}$')
ki_v_PRKase_Pi_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{P_i}$')
vmax_v_pgareduction = remove_math(params_table, r'$V_\mathrm{max}\ \mathrm{PR}$')
km_v_pgareduction_ATP_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{ATP}$')
km_v_pgareduction_PGA = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{PGA}$')
km_v_pgareduction_NADPH_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{NADPH}$')
ki_v_pgareduction_ADP_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{ADP}$')
vmax_v_carbohydrate_synthesis = remove_math(params_table, r'$V_\mathrm{max}\ \mathrm{CA}$')
keq_v_carbohydrate_synthesis = remove_math(params_table, r'$K_\mathrm{e}\ \mathrm{CA}$')
km_v_carbohydrate_synthesis_DHAP = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{DHAP}$')
ki_v_carbohydrate_synthesis_ADP_st = remove_math(params_table, r'$K_\mathrm{i}\ \mathrm{ADP}$')
vmax_v_rpp = remove_math(params_table, r'$V_\mathrm{max}\ \mathrm{RPP}$')
keq_v_rpp = remove_math(params_table, r'$K_\mathrm{e}\ \mathrm{RPP}$')
km_v_rpp_DHAP = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{DHAP}$')
H = remove_math(params_table, r'$[H^+]$')
vmax_v_co2_hydration = remove_math(params_table, r'$V_\mathrm{max}\ \mathrm{CA}$')
keq_v_co2_hydration = remove_math(params_table, r'$K_\mathrm{e}\ \mathrm{CA}$')
km_v_co2_hydration_CO2 = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{CO_2}$')
km_v_co2_hydration_HCO3 = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{HCO_3}$')
keq_v_FNR = remove_math(params_table, r'$K_\mathrm{e}\ \mathrm{NADPH}$')
km_v_FNR_NADP_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{NADP}$')
km_v_FNR_NADPH_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{NADPH}$')
Kj_NADPH = remove_math(params_table, r'$K_\mathrm{J}\ \mathrm{NADPH}$')
keq_v_ATPsynth = remove_math(params_table, r'$K_\mathrm{e}$')
km_v_ATPsynth_ADP_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{ADP}$')
km_v_ATPsynth_Pi_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{P_i}$')
km_v_ATPsynth_ATP_st = remove_math(params_table, r'$K_\mathrm{m}\ \mathrm{ATP}$')
Kj_ATP = remove_math(params_table, r'$K_\mathrm{J}\ \mathrm{ATP}$')
gm = remove_math(params_table, r'$g_\mathrm{M}$')
Kh_co2 = remove_math(params_table, r'$K_\mathrm{h}\ \mathrm{CO_2}$')
Kd = remove_math(params_table, r'$K_\mathrm{d}$')
Ki = remove_math(params_table, r'$K_\mathrm{i}$')
tau0 = remove_math(params_table, r'$\tau_0$')
chi_beta = remove_math(params_table, r'$\chi \beta$')
phi = remove_math(params_table, r'$\Phi_\mathrm{soil}$')
pi_e = remove_math(params_table, r'$\pi _\mathrm{e}$')
Kh = remove_math(params_table, r'$K_\mathrm{h}$')
Ds = remove_math(params_table, r'$D_\mathrm{S}$')
gs0 = remove_math(params_table, r'$g_\mathrm{s0}$')
NADP_tot = remove_math(params_table, r'$NAD_\mathrm{Tot}$')

# --- Derived Parameters ---

Et = remove_math(derived_params_table, r'$E_\mathrm{T}$')
I2_0 = remove_math(derived_params_table, r'$I_\mathrm{2,0}$')
I1_0 = remove_math(derived_params_table, r'$I_\mathrm{1,0}$')
km_v_RuBisCO_c_RUBP_extra = remove_math(derived_params_table, r'$K_{\mathrm{m\ RuBP}}^\prime$')
f_rubp = remove_math(derived_params_table, r'$f\left(\mathrm{RuBP}\right)$')
Ract_eq = remove_math(derived_params_table, r'$R_\mathrm{act\ eq}$')
chi = remove_math(derived_params_table, r'$\chi$')
I1 = remove_math(derived_params_table, r'$I_1$')
f_cyc = remove_math(derived_params_table, r'$f_\mathrm{Cyc}$')
I2 = remove_math(derived_params_table, r'$I_2$')
J2 = remove_math(derived_params_table, r'$J_2$')
J1 = remove_math(derived_params_table, r'$J_1$')
f_pseudocyc = remove_math(derived_params_table, r'$f_\mathrm{Pseudocyc}$')
J_NADPH_steady = remove_math(derived_params_table, r'$J_\mathrm{NADPH}$')
J_ATP_steady = remove_math(derived_params_table, r'$J_\mathrm{ATP}$')
gs_steady = remove_math(derived_params_table, r'$g_\mathrm{S}$')

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_header(2, "Summary")

mdFile.new_paragraph(f"""The [{model_title}]({model_doi}) model is a generalized C3 leaf-photosynthesis model, that includes simplified representations of the light and dark reactions and a stomatal behavior submodule. A lot of its implementation is based on past work by the same author and is mainly inspired by the common Farquhar-von Caemmerer-Berry model. The light reactions are modified from Yin et al. (2004) and include the potential rates of ATP and NADPH production based on light intensity. This model has been created with the simple user in mind, and the author has made an effort to show its simplicity, by giving access to a Microsoft Excel Workbook containing the entire model. To showcase the model's capabilities, the author creates common steady-state carbon assimilation curves, against intercellular CO2 concentration and light intensity, and compares them to experimental data from the literature. As many models of photosynthesis rely on purely stead-state assumptions, this model is also validated in dynamic conditions, showing for example the response of the model to a fluctuation of ambient oxygen concentration.

This model was created to stay as simple as possible, while still being able to accurately represent the main features of C<sub>3</sub> photosynthesis. As such, it can be used as a base for more complex models, or as a starting block in larger models of plant physiology. While giving access to the entire model in an Excel Workbook format is transparent and great, the execution of said practice has been inefficient in this instance. The entire mathematical description of the model is also given in the Appendix of the publication, however there are missing or different equations between the publication and the Excel Workbook, which can lead to confusion. On top of that, the simulation protocols used for each figure are only given in small details, which leads to further confusion when trying to reproduce the results and see which equations are correct or not.
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
{ode(Ract)} = {Ract_rate}
```
```math 
{ode(J_NADPH)} = {v_J_NADPH}
```
```math 
{ode(J_ATP)} = {v_J_ATP}
```
```math 
{ode(gs)} = {v_gs}
```
```math 
{ode(CO2)} = \frac{{-1.0}}{{{V_m}}} \cdot {v_RuBisCO_c} + \frac{{0.5}}{{{V_m}}} \cdot {glycine_decarboxylase} + \frac{{-1.0}}{{{V_m}}} \cdot {v_co2_hydration} + \frac{{1.0}}{{{V_m}}} \cdot {v_RLight} + \frac{{1.0}}{{{V_m}}} \cdot {CO2_dissolution}
```
```math 
{ode(RUBP)} = \frac{{-1.0}}{{{V_m}}} \cdot {v_RuBisCO_c} + \frac{{-1.0}}{{{V_m}}} \cdot {rubisco_oxygenase} + \frac{{1.0}}{{{V_m}}} \cdot {v_PRKase}
```
```math 
{ode(PGA)} = \frac{{2.0}}{{{V_m}}} \cdot {v_RuBisCO_c} + \frac{{0.5}}{{{V_m}}} \cdot {glycine_decarboxylase} - \left( \frac{{1}}{{3}} \right) \frac{{1}}{{{V_m}}} \cdot {v_RLight} + \frac{{1.0}}{{{V_m}}} \cdot {rubisco_oxygenase} + \frac{{-1.0}}{{{V_m}}} \cdot {v_pgareduction}
```
```math 
{ode(ATP_st)} = \frac{{-1.0}}{{{V_m}}} \cdot {rubisco_oxygenase} + \frac{{-1.0}}{{{V_m}}} \cdot {v_PRKase} + \frac{{-1.0}}{{{V_m}}} \cdot {v_pgareduction} + \frac{{-0.5}}{{{V_m}}} \cdot {v_carbohydrate_synthesis} + \frac{{1.0}}{{{V_m}}} \cdot {v_ATPsynth}
```
```math 
{ode(NADPH_st)} = \frac{{-0.5}}{{{V_m}}} \cdot {rubisco_oxygenase} + \frac{{-1.0}}{{{V_m}}} \cdot {v_pgareduction} + \frac{{1.0}}{{{V_m}}} \cdot {v_FNR}
```
```math 
{ode(DHAP)} = - \left( \frac{{5}}{{3}} \right) \frac{{1}}{{{V_m}}} \cdot {v_PRKase} + \frac{{1.0}}{{{V_m}}} \cdot {v_pgareduction} + \frac{{-1.0}}{{{V_m}}} \cdot {v_carbohydrate_synthesis}
```
```math 
{ode(RU5P)} = \frac{{-1.0}}{{{V_m}}} \cdot {v_PRKase} + \frac{{1.0}}{{{V_m}}} \cdot {v_rpp}
```
```math 
{ode(HCO3)} = \frac{{1.0}}{{{V_m}}} \cdot {v_co2_hydration}
```
```math 
{ode(Ci)} = - {CO2_dissolution} + {CO2_stomatal_diffusion}
```

</details>
                     """)

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
{ADP_st} =  {AP_tot} - {ATP_st}
```
```math
{NADP_st} =  {NADP_tot} - {NADPH_st}
```
```math
{Pi_st} =  {Pi_tot} - {PGA} - {DHAP} - {RU5P} - 2 {RUBP} - {ATP_st}
```
```math
{PhiPSII} =  {PhiPSII_LL} \cdot \frac{{{v_ATPsynth}}}{{{J_ATP}}} \frac{{{v_FNR}}}{{{J_NADPH}}} \cdot \left( 1 - \mathrm{{max}} \left( 0, \mathrm{{non\_rect\_hyperbole}} \left( {PPFD}, {alpha_ppfd_PhiPSII}, {V0_ppfd_PhiPSII}, {theta_ppfd_PhiPSII} \right) \right) \right)
```
```math
{A} =  {v_RuBisCO_c} - 0.5 {rubisco_oxygenase} - {RLight}
```
```math
{O2} =  \frac{{{p_o2}}}{{{Kh_o2}}}
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
{Et} =  \frac{{\frac{{{vmax_v_RuBisCO_c}}}{{{kcat_v_RuBisCO_c}}}}}{{{V_m}}}
```
```math
{I2_0} =  {PPFD} \cdot {s}
```
```math
{I1_0} =  \frac{{{I2_0} \cdot {PhiPSII_LL}}}{{{PhiPSI_LL}}}
```
```math
{km_v_RuBisCO_c_RUBP_extra} =  {km_v_RuBisCO_c_RUBP} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_RuBisCO_c_PGA}}} + \frac{{{NADP_st}}}{{{ki_v_RuBisCO_c_NADP_st}}} + \frac{{{ADP_st}}}{{{ki_v_RuBisCO_c_ADP_st}}} + \frac{{{Pi_st}}}{{{ki_v_RuBisCO_c_Pi_st}}} \right)
```
```math
{f_rubp} =  \frac{{{Et} + {km_v_RuBisCO_c_RUBP_extra} + {RUBP} - \sqrt{{ \left( {Et} + {km_v_RuBisCO_c_RUBP_extra} + {RUBP} \right)^{{2}} - 4 {RUBP} \cdot {Et} }}}}{{2 {Et}}}
```
```math
{Ract_eq} =  \mathrm{{non\_rect\_hyperbole}} \left( {PPFD}, {alpha_ppfd_rub}, {V0_ppfd_rub}, {theta_ppfd_rub} \right) \cdot \mathrm{{non\_rect\_hyperbole}} \left( {CO2}, {alpha_co2}, {V0_co2}, {theta_co2} \right)
```
```math
{chi} =  \frac{{{f_cyc}}}{{1 + {f_cyc} + {PhiPSII_LL}}}
```
```math
{I1} =  \left( 1 + {chi} \right) {I1_0}
```
```math
{f_cyc} =  \mathrm{{max}} \left( 0, -1 + 15^{{\frac{{{v_ATPsynth}}}{{{J_ATP}}} - \frac{{{v_FNR}}}{{{J_NADPH}}}}} \right)
```
```math
{I2} =  \left( \frac{{1}}{{{PhiPSII_LL}}} - {chi} \right) {I2_0} \cdot {PhiPSII_LL}
```
```math
{J2} =  {I2} \cdot {PhiPSII}
```
```math
{J1} =  \frac{{{J2}}}{{1}} - {f_cyc}
```
```math
{f_pseudocyc} =  {f_pseudocycNR} + 4 {O2} \cdot \left( 1 - \frac{{{v_FNR}}}{{{J_NADPH}}} \right)
```
```math
{J_NADPH_steady} =  \frac{{\frac{{{J1} \cdot \left( 1 - {f_cyc} - {f_pseudocyc} \right)}}{{2}}}}{{1000}}
```
```math
{J_ATP_steady} =  \frac{{\frac{{{J2} + \left( 1 - {fq} \rig{h}t) {J1} + 2 {fq} \cdot {J1} + 2 {f_cyc} \cdot {f_ndh} \cdot {J1}}}{{{h}}}}}{{1000}}
```
```math
{gs_steady} =  \mathrm{{max}} \left( {gs0}, \frac{{{chi_beta} \cdot \left( {tau0} + {f_rubp} \right) \left( {phi} + {pi_e} \right)}}{{1 + {chi_beta} \cdot \left( {tau0} + {f_rubp} \right) \frac{{1}}{{{Kh}}} \cdot {Ds}}} \right)
```

</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
{Ract_rate} = \left\{"{"} \begin{{array}}{{cl}} \frac{{{Ract_eq} - {Ract}}}{{{tau_d}}} & : \ {Ract} \geq {Ract_eq} \\ \frac{{{Ract_eq} - {Ract}}}{{{tau_i}}} & : \ {Ract} < {Ract_eq} \end{{array}} \right.
```
```math
{v_J_NADPH} = \left\{"{"} \begin{{array}}{{cl}} \frac{{{J_NADPH_steady} - {J_NADPH}}}{{0.1 \cdot {Kj_NADPH}}} & : \ {J_NADPH} \geq {J_NADPH_steady} \\ \frac{{{J_NADPH_steady} - {J_NADPH}}}{{{Kj_NADPH}}} & : \ {J_NADPH} < {J_NADPH_steady} \end{{array}} \right.
```
```math
{v_J_NADPH} = \left\{"{"} \begin{{array}}{{cl}} \frac{{{J_ATP_steady} - {J_ATP}}}{{0.1 \cdot {Kj_ATP}}} & : \ {J_ATP} \geq {J_ATP_steady} \\ \frac{{{J_ATP_steady} - {J_ATP}}}{{{Kj_ATP}}} & : \ {J_ATP} < {J_NADPH_steady} \end{{array}} \right.
```
```math
{v_gs} = \left\{"{"} \begin{{array}}{{cl}} \frac{{{gs_steady} - {gs}}}{{{Kd}}} & : \ {gs} \geq {gs_steady} \\ \frac{{{gs_steady} - {gs}}}{{{Ki}}} & : \ {gs} < {gs_steady} \end{{array}} \right.
```
```math
{v_RuBisCO_c} =  \frac{{{vmax_v_RuBisCO_c} \cdot {Ract} \cdot {f_rubp} \cdot {RUBP} \cdot {CO2}}}{{\left( {km_v_RuBisCO_c_CO2} \cdot \left( 1 + \frac{{{O2}}}{{{km_v_RuBisCO_c_O2}}} \right) + {CO2} \right) \left( {km_v_RuBisCO_c_RUBP_extra} + {RUBP} \right)}}
```
```math
{rubisco_oxygenase} =  \frac{{{v_RuBisCO_c} \cdot 2 \frac{{1}}{{2 \frac{{{S_co_gas}}}{{{Kh_o2}}} \cdot {Kh_co2}}} \cdot {O2}}}{{{CO2}}}
```
```math
{glycine_decarboxylase} =  {rubisco_oxygenase}
```
```math
{v_PRKase} =  \frac{{{vmax_v_PRKase} \cdot \left( {ATP_st} \cdot {RU5P} - \frac{{{ADP_st} \cdot {RUBP}}}{{{keq_v_PRKase}}} \right)}}{{\left( {ATP_st} + {km_v_PRKase_ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_PRKase_ADP_st}}} \right) \right) \left( {RU5P} + {km_v_PRKase_RU5P} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_PRKase_PGA}}} + \frac{{{RUBP}}}{{{ki_v_PRKase_RUBP}}} + \frac{{{Pi_st}}}{{{ki_v_PRKase_Pi_st}}} \right) \right)}}
```
```math
{v_pgareduction} =  \frac{{{vmax_v_pgareduction} \cdot {ATP_st} \cdot {PGA} \cdot {NADPH_st}}}{{\left( {PGA} + {km_v_pgareduction_PGA} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_pgareduction_ADP_st}}} \right) \right) \left( {ATP_st} + {km_v_pgareduction_ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_pgareduction_ADP_st}}} \right) \right) \left( {NADPH_st} + {km_v_pgareduction_NADPH_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_pgareduction_ADP_st}}} \right) \right)}}
```
```math
{v_carbohydrate_synthesis} =  \frac{{{vmax_v_carbohydrate_synthesis} \cdot \left( {DHAP} - 0.4 \right) \left( 1 - \frac{{\left| {v_pgareduction} \right| \cdot {Pi_st}}}{{{keq_v_carbohydrate_synthesis}}} \right)}}{{{DHAP} + {km_v_carbohydrate_synthesis_DHAP} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_carbohydrate_synthesis_ADP_st}}} \right)}}
```
```math
{v_rpp} =  \frac{{{vmax_v_rpp} \cdot \left( {DHAP} - \frac{{{RU5P}}}{{{keq_v_rpp}}} \right)}}{{{DHAP} + {km_v_rpp_DHAP}}}
```
```math
{v_co2_hydration} =  \frac{{{vmax_v_co2_hydration} \cdot \left( {CO2} - \frac{{{HCO3} \cdot {H}}}{{{keq_v_co2_hydration}}} \right)}}{{{km_v_co2_hydration_CO2} \cdot \left( 1 + \frac{{{CO2}}}{{{km_v_co2_hydration_CO2}}} + \frac{{{HCO3}}}{{{km_v_co2_hydration_HCO3}}} \right)}}
```
```math
{v_RLight} =  {RLight}
```
```math
{v_FNR} =  \frac{{{J_NADPH} \cdot \left( {NADP_st} - \frac{{{NADPH_st}}}{{{keq_v_FNR}}} \right)}}{{{km_v_FNR_NADP_st} \cdot \left( 1 + \frac{{{NADP_st}}}{{{km_v_FNR_NADP_st}}} + \frac{{{NADPH_st}}}{{{km_v_FNR_NADPH_st}}} \right)}}
```
```math
{v_ATPsynth} =  \frac{{{J_ATP} \cdot \left( {ADP_st} \cdot {Pi_st} - \frac{{{ATP_st}}}{{{keq_v_ATPsynth}}} \right)}}{{{km_v_ATPsynth_ADP_st} \cdot {km_v_ATPsynth_Pi_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{km_v_ATPsynth_ADP_st}}} + \frac{{{ATP_st}}}{{{km_v_ATPsynth_ATP_st}}} + \frac{{{Pi_st}}}{{{km_v_ATPsynth_Pi_st}}} + \frac{{{ADP_st} \cdot {Pi_st}}}{{{km_v_ATPsynth_ADP_st} \cdot {km_v_ATPsynth_Pi_st}}} \right)}}
```
```math
{CO2_dissolution} =  \frac{{{gm} \cdot \left( {Ci} - {CO2} \cdot {Kh_co2} \right)}}{{1000}}
```
```math
{CO2_stomatal_diffusion} =  \frac{{{gs} \cdot \left( {Ca} - {Ci} \right)}}{{1000}}
```

</details>

                     """)

mdFile.new_header(3, "Figures")

mdFile.new_paragraph("""You can find the recreation of the figures from the original publication below. Due to differing copyright reasons the original figures cannot be included in this README file. Instead, the comparision has to be made using the original publication.""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 3</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_fig3.svg' alt='Figure 3' width='600'/>

Simulated ${A}$- ${PPFD}$ (left) and ${A}$- ${Ca}$ (right) response curves under two different oxygen partial pressures (${O2}$ = 210000, orange, and = 20000, blue). The simulation was run to a quasi steady-state (1800 s) at each value of ${Ca}$ or ${PPFD}$. The ${Ca}$ response curve was simulated at a ${PPFD}$ of 1500 µmol m⁻² s⁻¹, while the ${PPFD}$ response curve was simulated at a ${Ca}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$, the middle row the stomatal conductance (${gs}$), and the bottom row the ${NADPH_st}$ production rate ${v_FNR}$.

The recreation of this figure was done effortlessly with only a few issues. The original figure does not specify how long the simulations were run; therefore, it was assumed to follow the length of simulation detailed in Figure 4. Additionally, the original figure shows an ${A}$-${Ci}$ response curve on the right; it could be inferred that they either meant ${A}$-${Ca}$ or assumed ${Ci}$ to be equal to ${Ca}$. In this recreation, ${A}$-${Ca}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 4</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_fig4.svg' alt='Figure 4' width='600'/>

Simulated ${A}$-${PPFD}$ (left) and  ${A}$-${Ca}$ (right) response curves under two different oxygen partial pressures (${p_o2} = 210000 \mathrm{{\mu bar}}$, orange, and ${p_o2} = 20000 \mathrm{{\mu bar}}$, blue). The simulation was run to a quasi steady-state (1800 s) at each value of ${Ca}$ or ${PPFD}$. The ${Ca}$ response curve was simulated at a ${PPFD}$ of 1500 µmol m⁻² s⁻¹, while the ${PPFD}$ response curve was simulated at a ${Ca}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top and middle row show the concentrations of ${RUBP}$ and ${PGA}$, respectively. These concentrations were given in µmol m⁻² by multiplying their volumetric concentrations by the chloroplast volume per leaf area (${V_m}$). The bottom row shows the relative RuBisCO activity by multiplying ${Ract}$ and ${f_rubp}$.


The recreation of this figure was done effortlessly with only a few issues. The original figure shows an ${A}$-${Ci}$ response curve on the right; it could be inferred that they either meant ${A}$-${Ca}$ or assumed ${Ci}$ to be equal to ${Ca}$. In this recreation, ${A}$-${Ca}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_fig5.svg' alt='Figure 5' width='600'/>

Response curves to a transition from low to high light (left) and from high to low light (right). The low light intensity was 50 µmol m⁻² s⁻¹, while the high light intensity was 1500 µmol m⁻² s⁻¹. Acclimation was simulated for 400s at the respective light intensities before switching to the other light intensity. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: ${Ca} = 350 \mathrm{{\mu mol\ mol^{{-1}}}}$, ${vmax_v_RuBisCO_c} = 0.18 \mathrm{{mmol\ m^{{-2}}\ s^{{-1}}}}$, ${chi_beta} = 0.8 \mathrm{{mol\ air\ MPa^{{-1}}}}$, ${tau0} = -0.12$, ${Ki} = 3600 \mathrm{{s}}$, and ${Kd} = 1200 \mathrm{{s}}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$ and the rate of {ATP_st} and {NADPH_st} synthesis (${v_ATPsynth}$ and ${v_FNR}$ respectively). The middle shows row the stomatal conductance (${gs}$), the RuBisCO activation state (${Ract}), and ${f_rubp}$. Lastly, the bottom row shows the ratio of ${ATP_st}$ and ${NADPH_st}$ to their respective totals.

The recreation of this figure was only partly achieved. Both upper rows show trends very similar to the original figure; however, the right plots show a gradual but stark decrease in the recreation, whereas in the original figure, it is a sudden drop immediately after the light switch. The other four plots show distinct differences in values and trends, especially in the concentrations of ${Pi_st}$ and ${PGA}$, as well as in the ratio of ${NADPH_st}$. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results. Even though the recreation is not perfect, it still captures the same information as the original figure; this recreation is still valid.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 6</summary>
                     
<img style='float: center' src='paper_figures/{model_title.lower()}_fig6.svg' alt='Figure 6' width='600'/>

Response curves to a transition from low to high atmospheric $\mathrm{{CO_2}}$ concentration ${Ca}$ (left) and from high to low atmospheric ${Ca}$ (right). The low concentration was 350 µmol mol⁻¹, while the high concentration was 1500 µmol mol⁻¹. Acclimation was simulated for $100000\ \mathrm{{s}}$ at the respective concentration before switching to the other concentration. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: ${PPFD} = 1500 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$, ${vmax_v_RuBisCO_c} = 0.18 \mathrm{{mmol\ m^{{-2}}\ s^{{-1}}}}$, ${chi_beta} = 0.8 \mathrm{{mol\ air\ MPa^{{-1}}}}$, ${tau0} = -0.12$, ${Ki} = 3600 \mathrm{{s}}$, and ${Kd} = 1200 \mathrm{{s}}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$ and the rate of {ATP_st} and {NADPH_st} synthesis (${v_ATPsynth}$ and ${v_FNR}$ respectively). The middle shows row the stomatal conductance (${gs}$), the RuBisCO activation state (${Ract}$), and ${f_rubp}$. Lastly, the bottom row shows the ratio of ${ATP_st}$ and ${NADPH_st}$ to their respective totals.

The recreation of this figure could be achieved. While the acclimation follows the trends and approximate values of the original figure, there are vast differences in the phase after acclimation. In the recreation, the values remain relatively steady after the switch. In contrast, in the original figure, there is a gradual increase or decrease after the switch. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 7</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_fig7.svg' alt='Figure 7' width='600'/>

Response to a transition from ambient (${p_o2} = 210000 \mathrm{{\mu bar}}$) to low oxygen partial pressure (${p_o2} = 20000 \mathrm{{\mu bar}}$). The simulation uses the default parameter values, except for ${Ca} = 200 \mathrm{{\mu mol\ mol^{{-1}}}}$ and ${PPFD} = 300 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. Ambient oxygen was simulated until steady-state was reached. From the zero point on the x-axis only $250\ \mathrm{{{s}}}$ of the atmospheric pressure is shown, then the simulation is run at low pressure for the rest of the plot. The switch point is also indicated by the two different bars at the top of the figure. The two shown lines are the assimilation rate ${A}$ (green solid) and the efficiency of PSII ${PhiPSII}$ (grey dotted).

</details>
""")

mdFile.new_header(3, "Demonstrations")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle (06:00 to 20:00) using real Photosynthetically active radiation (PAR) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal ([https://doi.org/10.48443/vzfh-7675])(https://doi.org/10.48443/vzfh-7675) and is used to create a protocol for the light intensity (${PPFD}$) over the course of the day, in a minute interval. The simulation is run using the default parameters and initial conditions of the model, and the RuBisCO carboxylation rate (${v_RuBisCO_c}$), ${ATP_st}$ and ${NADPH_st}$ ratio, and Flourescence results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

As this model does not contain a representation of Flourescence output, this can not be shown. However, both the RuBisCO carboxylation rate and ATP and NADPH ratio follow the trend of the light intensity over the course of the day.

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
| $\mathrm{{CO}}_2$         | ${CO2}$           |
| $v_\mathrm{{c}}$          | ${v_RuBisCO_c}$ but unit conversion to $\mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$  |
| $\mathrm{{C_i}}$          | ${Ci}$ but calculated through ${Ca}$          |
| $H_\mathrm{{s}}^{{cp}}$   | None              |
| $\Gamma ^*$               | None              |
| $R_\mathrm{{light}}$      | ${RLight}$        |
| $A$                       | ${A}$ but unit conversion to $\mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$            |

To be able to create this figure, three things had to be added to the model: ${Ci}_\mathrm{{new}}$ as a parameter to use it as input that calculates ${Ca}$, and ${A}$ and  ${v_RuBisCO_c}$ converted in $\mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. As the model does not always reach true steady-state, a quasi-steady-state is used where the model is simulated to $1800\ \mathrm{{s}}$ if not otherwise possible. The recreated figure shows the same trends as the original FvCB model, especially follwing the Rubisco-limited and light-limited regimes. Some discrepancies can be seen in lower ${Ci}$ values and in the general shape of the curve; however, the recreation is still valid.

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

As this model does not contain a representation of Flourescence or NPQ output, this can not be shown.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Photosynthesis MCA</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_mca.svg' alt='Photosynthesis MCA' width='600'/>

A sample metabolic control analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent RuBisCO carboxylation rate ($v_\mathrm{{RuBisCO \vert C}}$), rate of photosystem II ($v_\mathrm{{PSII}}$), rate of photosystem I ($v_\mathrm{{PSI}}$), rate of cytochrome b<sub>6</sub>f ($v_\mathrm{{cytb6f}}$) and rate of ATP synthesis ($v_\mathrm{{ATPsynthase}}$). The variables chosen should represent CO<sub>2</sub> concentration ($\mathrm{{CO_2}}$), Ribulose-1,5-bisphosphate concentration ($\mathrm{{RUBP}}$), oxidised Plastoquinone ($\mathrm{{PQ_{{ox}}}}$), oxidised Plastocyanin ($\mathrm{{PC_{{ox}}}}$), adenosine triphosphate concentration ($\mathrm{{ATP}}$), and nicotinamide adenine dinucleotide phosphate concentration ($\mathrm{{NADPH}}$). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.0001$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{{p}}^{{x}} = \frac{{x_\mathrm{{upper}} - x_\mathrm{{lower}}}}{{2 \cdot \mathrm{{disp}} \cdot p}}$, where $C_{{p}}^{{x}}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{{disp}}$ is the displacement value. $x_\mathrm{{upper}}$ and $x_\mathrm{{lower}}$ are the steady-state result of $x$ at either $+\mathrm{{disp}}$ and $-\mathrm{{disp}}$ respectively. It has to be noted that the MCA results a very specific on the other values of the parameters in the model, therefore the results shown here are only representative of the default parameter set of the model.

**Assumptions:**

- Steady-State needs to be achievable for the model to perform the MCA.
- The parameters for each coefficient, rates, and variables chosen need to be representative of the respective process.
- If a parameter, rate, or variable is not present in the model, the respective coefficient will be greyed out in the Heatmap.

**Notes:**

| Coefficient                   | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | ${PPFD}$ |
| $\mathrm{{PSI}}$              | None |
| $\mathrm{{RuBisCO \vert C}}$  | ${kcat_v_RuBisCO_c}$ |
| $\mathrm{{cytb6f}}$           | None              |
| $\mathrm{{ATPsynthase}}$      | None              |

| Flux                          | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | None |
| $\mathrm{{PSI}}$              | None |
| $\mathrm{{RuBisCO \vert C}}$  | ${v_RuBisCO_c}$ |
| $\mathrm{{cytb6f}}$           | None              |
| $\mathrm{{ATPsynthase}}$      | ${v_ATPsynth}$              |

| Variable                  | In Model      |
| -----------               | -----------   |
| $\mathrm{{CO_2}}$         | ${CO2}$       |
| $\mathrm{{RUBP}}$         | ${RUBP}$      |
| $\mathrm{{PQ_{{ox}}}}$    | None          |
| $\mathrm{{PC_{{ox}}}}$    | None          |
| $\mathrm{{ATP}}$          | ${ATP_st}$    |
| $\mathrm{{NADPH}}$        | ${NADPH_st}$  |

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

As this model does not contain a representation of Flourescence or NPQ output, the model cannot be fitted to the data.

</details>
""")

mdFile.create_md_file()
