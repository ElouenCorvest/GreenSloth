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
Kh_o2 = remove_math(params_table, r'$K_\mathrm{h}\ \mathrm{O_2}')
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
Kh_co2 = remove_math(params_table, r'$K_\mathrm{h}\ \mathrm{CO_2}')
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
km_v_RuBisCO_c_RUBP_extra = remove_math(derived_params_table, r'$K_{\mathrm{m\ RuBP}}^\'$')
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

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

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

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 3</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig3.svg' alt='Figure 3' width='600'/>

Simulated ${A}$-${PPFD}$ (left) and  ${A}$-${Ca}$ (right) response curves under two different oxygen partial pressures (${O2}$ = 210000, orange, and = 20000, blue). The simulation was run to a quasi steady-state (1800 s) at each value of ${Ca}$ or ${PPFD}$. The ${Ca}$ response curve was simulated at a ${PPFD}$ of 1500 µmol m⁻² s⁻¹, while the ${PPFD}$ response curve was simulated at a ${Ca}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$, the middle row the stomatal conductance (${gs}$), and the bottom row the ${NADPH_st}$ production rate ${v_FNR}$.

The recreation of this figure was done effortlessly with only a few issues. The original figure does not specify how long the simulations were run; therefore, it was assumed to follow the length of simulation detailed in Figure 4. Additionally, the original figure shows an ${A}$-${Ci}$ response curve on the right; it could be inferred that they either meant ${A}$-${Ca}$ or assumed ${Ci}$ to be equal to ${Ca}$. In this recreation, ${A}$-${Ca}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 4</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig4.svg' alt='Figure 4' width='600'/>

Simulated ${A}$-${PPFD}$ (left) and  ${A}$-${Ca}$ (right) response curves under two different oxygen partial pressures (${p_o2} = 210000 \mathrm{{\mu bar}}$, orange, and ${p_o2} = 20000 \mathrm{{\mu bar}}$, blue). The simulation was run to a quasi steady-state (1800 s) at each value of ${Ca}$ or ${PPFD}$. The ${Ca}$ response curve was simulated at a ${PPFD}$ of 1500 µmol m⁻² s⁻¹, while the ${PPFD}$ response curve was simulated at a ${Ca}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top and middle row show the concentrations of ${RUBP}$ and ${PGA}$, respectively. These concentrations were given in µmol m⁻² by multiplying their volumetric concentrations by the chloroplast volume per leaf area ({V_m}). The bottom row shows the relative RuBisCO activity by multiplying ${Ract}$ and ${f_rubp}$.


The recreation of this figure was done effortlessly with only a few issues. The original figure shows an ${A}$-${Ci}$ response curve on the right; it could be inferred that they either meant ${A}$-${Ca}$ or assumed ${Ci}$ to be equal to ${Ca}$. In this recreation, ${A}$-${Ca}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig5.svg' alt='Figure 5' width='600'/>

Response curves to a transition from low to high light (left) and from high to low light (right). The low light intensity was 50 µmol m⁻² s⁻¹, while the high light intensity was 1500 µmol m⁻² s⁻¹. Acclimation was simulated for 400s at the respective light intensities before switching to the other light intensity. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: ${Ca} = 350 \mathrm{{\mu mol\ mol^{{-1}}}}$, ${vmax_v_RuBisCO_c} = 0.18 \mathrm{{mmol\ m^{{-2}}\ s^{{-1}}}}$, ${chi_beta} = 0.8 \mathrm{{mol\ air\ MPa^{{-1}}}}$, ${tau0} = -0.12$, ${Ki} = 3600 \mathrm{{s}}$, and ${Kd} = 1200 \mathrm{{s}}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$ and the rate of {ATP_st} and {NADPH_st} synthesis (${v_ATPsynth}$ and ${v_FNR}$ respectively). The middle shows row the stomatal conductance (${gs}$), the RuBisCO activation state (${Ract}), and ${f_rubp}$. Lastly, the bottom row shows the ratio of ${ATP_st}$ and ${NADPH_st}$ to their respective totals.

The recreation of this figure was only partly achieved. Both upper rows show trends very similar to the original figure; however, the right plots show a gradual but stark decrease in the recreation, whereas in the original figure, it is a sudden drop immediately after the light switch. The other four plots show distinct differences in values and trends, especially in the concentrations of ${Pi_st}$ and ${PGA}$, as well as in the ratio of ${NADPH_st}$. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results. Even though the recreation is not perfect, it still captures the same information as the original figure; this recreation is still valid.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig5.svg' alt='Figure 5' width='600'/>

Response curves to a transition from low to high light (left) and from high to low light (right). The low light intensity was 50 µmol m⁻² s⁻¹, while the high light intensity was 1500 µmol m⁻² s⁻¹. Acclimation was simulated for $1000 \mathrm{s}$ at the respective light intensities before switching to the other light intensity. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: ${Ca} = 350 \mathrm{{\mu mol\ mol^{{-1}}}}$, ${vmax_v_RuBisCO_c} = 0.18 \mathrm{{mmol\ m^{{-2}}\ s^{{-1}}}}$, ${chi_beta} = 0.8 \mathrm{{mol\ air\ MPa^{{-1}}}}$, ${tau0} = -0.12$, ${Ki} = 3600 \mathrm{{s}}$, and ${Kd} = 1200 \mathrm{{s}}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$ and the rate of {ATP_st} and {NADPH_st} synthesis (${v_ATPsynth}$ and ${v_FNR}$ respectively). The middle shows row the stomatal conductance (${gs}$), the RuBisCO activation state (${Ract}), and ${f_rubp}$. Lastly, the bottom row shows the ratio of ${ATP_st}$ and ${NADPH_st}$ to their respective totals.

The recreation of this figure was only partly achieved. Both upper rows show trends very similar to the original figure; however, the right plots show a gradual but stark decrease in the recreation, whereas in the original figure, it is a sudden drop immediately after the light switch. The other four plots show distinct differences in values and trends, especially in the concentrations of ${Pi_st}$ and ${PGA}$, as well as in the ratio of ${NADPH_st}$. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results. Furthermore, true steady-state can not be achieved with the recreated version of the model, and so the shortest duration that shows least of change at the end is used. Even though the recreation is not perfect, it still captures the same information as the original figure and therefore is still deemed valid.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 6</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig6.svg' alt='Figure 6' width='600'/>

Response curves to a transition from low to high atmospheric $\mathrm{{CO_2}}$ concentration ${Ca}$ (left) and from high to low atmospheric ${Ca}$ (right). The low concentration was 350 µmol mol⁻¹, while the high concentration was 1500 µmol mol⁻¹. Acclimation was simulated for $100000\ \mathrm{{s}}$ at the respective concentration before switching to the other concentration. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: ${PPFD} = 1500 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$, ${vmax_v_RuBisCO_c} = 0.18 \mathrm{{mmol\ m^{{-2}}\ s^{{-1}}}}$, ${chi_beta} = 0.8 \mathrm{{mol\ air\ MPa^{{-1}}}}$, ${tau0} = -0.12$, ${Ki} = 3600 \mathrm{{s}}$, and ${Kd} = 1200 \mathrm{{s}}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate ${A}$ and the rate of {ATP_st} and {NADPH_st} synthesis (${v_ATPsynth}$ and ${v_FNR}$ respectively). The middle shows row the stomatal conductance (${gs}$), the RuBisCO activation state (${Ract}), and ${f_rubp}$. Lastly, the bottom row shows the ratio of ${ATP_st}$ and ${NADPH_st}$ to their respective totals.

The recreation of this figure could be achieved. While the acclimation follows the trends and approximate values of the original figure, there are vast differences in the phase after acclimation. In the recreation, the values remain relatively steady after the switch. In contrast, in the original figure, there is a gradual increase or decrease after the switch. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 7</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig7.svg' alt='Figure 7' width='600'/>

Response to a transition from ambient (${p_o2} = 210000 \mathrm{{\mu bar}}$) to low oxygen partial pressure (${p_o2} = 20000 \mathrm{{\mu bar}}$). The simulation uses the default parameter values, except for ${Ca} = 200 \mathrm{{\mu mol\ mol^{{-1}}}}$ and ${PPFD} = 300 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. Ambient oxygen was simulated until steady-state was reached. From the zero point on the x-axis only $250\ \mathrm{{{s}}}$ of the atmospheric pressure is shown, then the simulation is run at low pressure for the rest of the plot. The switch point is also indicated by the two different bars at the top of the figure. The two shown lines are the assimilation rate ${A}$ (green solid) and the efficiency of PSII ${PhiPSII}$ (grey dotted).

</details>
""")

mdFile.create_md_file()
