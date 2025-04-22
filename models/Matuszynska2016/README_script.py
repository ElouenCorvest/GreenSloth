import os
from pathlib import Path

from greensloth_utils import gloss_fromCSV, remove_math
from mdutils.mdutils import MdUtils

###### Util Functions ######


def ode(first_var: str, second_var: str = "t"):
    for i in [first_var, second_var]:
        if "$" in i:
            raise ValueError(f"Your given variable '{i}' has a '$' in it")

    return rf"\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}"


###### Model Infos ######

model_title = "Matuszynska2016"
model_doi = "https://doi.org/10.1016/j.bbabio.2016.09.003"

###### Glossaries ######

cite_dict = dict()

model_info = Path(__file__).parent / "model_info"
python_written = model_info / "python_written"
main_gloss = Path(__file__).parents[2] / "Templates"

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / "comps.csv", omit_col="Glossary ID"
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = (
    gloss_fromCSV(path=model_info / "derived_comps.csv", omit_col="Glossary ID")
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / "rates.csv", omit_col="Glossary ID"
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / "params.csv", cite_dict=cite_dict
)

derived_params_table, derived_params_table_tolist, derived_params_table_list = (
    gloss_fromCSV(model_info / "derived_params.csv")
)

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

mdFile = MdUtils(file_name=f"{os.path.dirname(__file__)}/README.md")

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""The [Matuszynska2016]({model_doi}) model, a small kinetic model, was developed to delve deeper into the effect of light memory caused by non-photochemical quenching. The systematic investigation of the Xanthophyll cycle, a combination of the pigments of violaxanthin, antheraxanthin, and zeaxanthin, sparked a series of experiments to determine whether plant light memory can be detected in a time-scale of minutes to hours through pulse amplitude modulated chlorophyll fluorescence. The model was then created based on these experimental results, providing a comprehensive description of NPQ dynamics and the short-term memory of the *Arabidopsis thaliana* plant.

To keep the model as simple as possible, several processes not directly linked to NPQ have been simplified to create a dynamic ODE system consisting only of 6 different compounds. With these simplifications, the authors could fulfil an additional goal: to make a general framework that is not specific to one model organism.

To demonstrate the adaptability of their model, the authors took their calibrated *Arabidopsis thaliana* model and successfully applied it to the non-model organism *Epipremnum aureum*. This adaptation allowed them to simulate realistic fluorescence measurements and replicate all the key features of chlorophyll induction, showcasing the model's versatility and potential for use in a variety of organisms.

                     """)

mdFile.new_header(2, "Installation")

mdFile.new_header(2, "Summary")

mdFile.new_header(3, "Compounds")

mdFile.new_header(4, "Part of ODE system")

mdFile.new_table(
    columns=len(comps_table.columns),
    rows=len(comps_table_tolist),
    text=comps_table_list,
)

mdFile.new_paragraph(rf"""
<details>
<summary>ODE System</summary>

```math 
{ode(PQH_2)} = {v_PSII} - {v_PQ}
```
```math 
{ode(H_lu)} = \frac{{1}}{{{b_H}}} \cdot \left( 2 \cdot {v_PSII} + 4 \cdot {v_PQ} - {hpr} \cdot {v_ATPsynth} - {v_Leak} \right)
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

mdFile.new_table(
    columns=len(derived_comps_table.columns),
    rows=len(derived_comps_table_tolist),
    text=derived_comps_table_list,
)

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

mdFile.new_table(
    columns=len(params_table.columns),
    rows=len(params_table_tolist),
    text=params_table_list,
)

mdFile.new_header(4, "Derived Parameters")

mdFile.new_table(
    columns=len(derived_params_table.columns),
    rows=len(derived_params_table_tolist),
    text=derived_params_table_list,
)

mdFile.new_paragraph(rf"""

<details>
<summary>Equations of derived parameters</summary>

```math
{H_st} =  32000.0 \cdot 10^{{-{pH_st}}}
```
```math
{K_pHSat_inv} =  4000.0 \cdot 10^{{-{K_pHSat}}}
```
```math
{K_pHSatLHC_inv} =  4000.0 \cdot 10^{{-{K_pHSatLHC}}}
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

mdFile.new_table(
    columns=len(rates_table.columns),
    rows=len(rates_table_tolist),
    text=rates_table_list,
)

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

mdFile.create_md_file()
