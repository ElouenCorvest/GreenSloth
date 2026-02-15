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

model_title = "Li2021"
model_doi = "https://doi.org/10.1038/s41477-021-00947-5"

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

QA_red = remove_math(comps_table, r'$\mathrm{Q_{A}}^{-}$')
PQH_2 = remove_math(comps_table, r'$\mathrm{PQH_2}$')
pH_lumen = remove_math(comps_table, r'$\mathrm{pH_{lumen}}$')
Dpsi = remove_math(comps_table, r'$\Delta \Psi$')
K_lu = remove_math(comps_table, r'$\mathrm{K}^{+}_{\mathrm{lumen}}$')
PC_ox = remove_math(comps_table, r'$\mathrm{PC}^+$')
Y2 = remove_math(comps_table, r'$\mathrm{P_{700}}^+$')
Zx = remove_math(comps_table, r'$\mathrm{Zx}$')
singO2 = remove_math(comps_table, r'$\mathrm{sing}^{O2}$')
Fd_red = remove_math(comps_table, r'$\mathrm{Fd_{red}}$')
NADPH_st = remove_math(comps_table, r'$\mathrm{NADPH}$')
Cl_lu = remove_math(comps_table, r'$\mathrm{Cl}^{-}_{\mathrm{lumen}}$')
Cl_st = remove_math(comps_table, r'$\mathrm{Cl}^{-}_{\mathrm{stroma}}$')

# -- Derived Compounds --

QA = remove_math(derived_comps_table, r'$qL$')
Y0 = remove_math(derived_comps_table, r'$P700$')
PQ = remove_math(derived_comps_table, r'$\mathrm{PQ}$')
PC_red = remove_math(derived_comps_table, r'$\mathrm{PC}$')
Fd_ox = remove_math(derived_comps_table, r'$\mathrm{Fd_{ox}}$')
NADP_st = remove_math(derived_comps_table, r'$\mathrm{NADP}^+$')
Vx = remove_math(derived_comps_table, r'$\mathrm{Vx}$')
PsbSP = remove_math(derived_comps_table, r'$PsbS\_H$')
NPQ = remove_math(derived_comps_table, r'$NPQ$')
PhiPSII = remove_math(derived_comps_table, r'$\Phi \mathrm{PSII}$')
H_lumen = remove_math(derived_comps_table, r'$H_{lumen}$')
pmf = remove_math(derived_comps_table, r'$pmf$')
H_st = remove_math(derived_comps_table, r'$H_{stroma}$')

# -- Rates --

vPSII_recomb = remove_math(rates_table, r'$PSII_{recom}$')
vPSII_ChSep = remove_math(rates_table, r'$PSII_{charge}$')
v_PSII = remove_math(rates_table, r'$v_{PSII}$')
v_PQ = remove_math(rates_table, r'$v_{PQ}$')
v_b6f = remove_math(rates_table, r'$v_{b6f}$')
v_NDH = remove_math(rates_table, r'$v_{NDH}$')
v_PGR = remove_math(rates_table, r'$v_{PGR}$')
PSI_ChSep = remove_math(rates_table, r'$PSI_{charge}$')
v_PSI_PCoxid = remove_math(rates_table, r'$PSI_{PC\_oxidiation}$')
v_FNR = remove_math(rates_table, r'')
v_Mehler = remove_math(rates_table, r'$v_{Mehler}$')
v_CBB = remove_math(rates_table, r'$v_{CBB}$')
v_KEA3 = remove_math(rates_table, r'$v_{KEA3}$')
v_VKC = remove_math(rates_table, r'$v_{K\_channel}$')
v_VCCN1 = remove_math(rates_table, r'$v_{VCCN1}$')
v_ClCe = remove_math(rates_table, r'$v_{ClCe}$')
v_Leak = remove_math(rates_table, r'$v_{leak}$')
v_pmf_protons_activity = remove_math(rates_table, r'$v_{pmf}$')
v_Epox = remove_math(rates_table, r'$v_{ZE}$')
v_Deepox = remove_math(rates_table, r'$v_{VDE}$')

# -- Parameters --

PPFD = remove_math(params_table, r'$\mathrm{PAR}$')
k_recomb = remove_math(params_table, r'$k_{recomb}$')
phi_triplet = remove_math(params_table, r'$\Phi _{triplet}$')
phi_1O2 = remove_math(params_table, r'$\Phi _{O_2}^1$')
sigma0_II = remove_math(params_table, r'$\mathrm{PSII_{antenna_size}}$')
c_b6f = remove_math(params_table, r'$\mathrm{cytochrome b_6f content}$')
pKa_reg = remove_math(params_table, r'$\mathrm{pK_{reg}}$')
Em_PC_pH7 = remove_math(params_table, r'$Em_\mathrm{PC\_pH7}$')
Em_PQH2_pH7 = remove_math(params_table, r'$Em_\mathrm{PQH2\_pH7}$')
Vmax_b6f = remove_math(params_table, r'$V_{max}\left( \mathrm{b6f} \right)$')
pKa_PsbS = remove_math(params_table, r'$\mathrm{pK_{PsbS}}$')
NPQ_max = remove_math(params_table, r'$NPQ_{max}$')
pH_st = remove_math(params_table, r'$\mathrm{pH_{stroma}}$')
Em_Fd = remove_math(params_table, r'$Em_{Fd}$')
k_NDH1 = remove_math(params_table, r'$k_\mathrm{{NDH}}$')
Vmax_PGR = remove_math(params_table, r'$V_{max}\left( \mathrm{PGR} \right)$')
sigma0_I = remove_math(params_table, r'$\mathrm{PSI_{antenna_size}}$')
k_QA = remove_math(params_table, r'$k_\mathrm{{QA}}$')
Keq_QA = remove_math(params_table, r'$Keq_{QA \rightarrow PQ}$S')
k_PCtoP700 = remove_math(params_table, r'$k_{PC\_to\_P700}$')
k_FdtoNADP = remove_math(params_table, r'$k_\mathrm{Fd\_to\_NADP}$')
K_st = remove_math(params_table, r'$\mathrm{K}^{+}_{\mathrm{stroma}}$')
k_KEA3 = remove_math(params_table, r'$k_{KEA3}$')
P_K = remove_math(params_table, r'$\mathrm{Perm_K}$')
ipt_lu = remove_math(params_table, r'$\mathrm{lumen\_protons\_per\_turnover}$')
k_VCCN1 = remove_math(params_table, r'$k_{VCCN1}$')
k_ClCe = remove_math(params_table, r'$k_{CLCE}$')
HPR = remove_math(params_table, r'$\mathrm{HPR}$')
Vmax_ATPsynth = remove_math(params_table, r'$V_\mathrm{max|ATPsynth}$')
b_H = remove_math(params_table, r'$\mathrm{Buffering\ capacity}$')
vpc = remove_math(params_table, r'$\mathrm{Volts\_per\_charge}$')
k_EZ = remove_math(params_table, r'$k_\mathrm{ZE}')
nh_VDE = remove_math(params_table, r'$\mathrm{Hill_{VDE}}$')
pKa_VDE = remove_math(params_table, r'$\mathrm{pK_{VDE}}$')
Vmax_VDE = remove_math(params_table, r'$V_{max}\left( \mathrm{VDE} \right)$')
k_leak = remove_math(params_table, r'$k_{leak}$')
QA_total = remove_math(params_table, r'$\mathrm{QA}^{\mathrm{tot}}$')
PQ_tot = remove_math(params_table, r'$\mathrm{PQ}^{\mathrm{tot}}$')
P700_total = remove_math(params_table, r'$\mathrm{P700}^{\mathrm{tot}}$')
PC_tot = remove_math(params_table, r'$\mathrm{PC}^{\mathrm{tot}}$')
Fd_tot = remove_math(params_table, r'$\mathrm{Fd}^{\mathrm{tot}}$')
NADP_tot = remove_math(params_table, r'$\mathrm{NADP}^{\mathrm{tot}}$')
Carotenoids_tot = remove_math(params_table, r'$\mathrm{X}^{\mathrm{tot}}$')
time = "t"

# --- Derived Parameters ---

light_per_L = remove_math(derived_params_table, r'$\mathrm{light\_per\_L}$')
kCBB = remove_math(derived_params_table, r'$k_{CBC}$')
driving_force_Cl = remove_math(derived_params_table, r'$v$')
delta_pH = remove_math(derived_params_table, r'$\mathrm{\Delta pH}$')
delta_pH_inVolts = remove_math(derived_params_table, r'$\mathrm{\Delta pH / V}$')
qL_act = remove_math(derived_params_table, r'$qL_{act}$')
pH_act = remove_math(derived_params_table, r'$pH_{act}$')

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_header(2, "Summary")

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

The [{model_title}]({model_doi}) model is a kinetic model of photosynthesis that focuses more on the ion fluxes across the thylakoid membrane and their effect on the proton motive force (PMF). It was built on the Davis2017 model, focuses more on the photosynthetic reactions that are directly linked to the PMF, such as the water splitting at PSII, the plastoquinone oxidation at the Cytochrome b6f complex (Cyt b6f) complex, and more. Other photosynthetic reactions are kept as simple as possible. The Li2021 model adds two potassium ion (K+) and two chloride ion (Cl<sup>-</sup>) ion transport channels to the thylakoid membrane, to investigate their effects on the PMF. To validate the model, the authors compare their simulated results to experimental data from several different experiments. They show that the model can reproduce not only wild type (WT) behavior, but also the behavior of several knockout mutants. The mutants chosen, were the VCCN1, Cl<sup>-</sup> channel (CLCE) and K<sup>+</sup>/H+ antiporter 3 (KEA3) knockouts and any combination thereof. After the validation, the model is then used to investigate the impact these ion channels have on the PMF and the resulting photosynthetic efficiency. Several interesting simulation protocols are used, to showcase the model’s capabilities, such as a light oscillation protocol, a scan of enzyme abundance and more. Overall, this model was created to answer an already existing question in the field of photosynthesis, which is the role of ion fluxes across the thylakoid membrane.

The model itself is not well presented in the publication, but the authors do provide a link to a public GitHub repository where the model is available. It is written in Python, with many comments added to the code. The script includes many different parts of the model and simulation protocols, therefore it is not clear, what is part of the model used in the publication. The script was summarized as much as possible, to only include the parts relevant to the model, but it is not clear if this interpretation is that of the publication. Between the code and the minimal information given in the publication and its supplementary materials, there are still discrepancies, which makes it hard to fully establish the model and its parameters. However, the model shows a good example of why models of photosynthesis are important and versatile, which is why it was included in GreenSloth.

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
{ode(singO2)} = {phi_triplet} {phi_1O2} \cdot {vPSII_recomb}
```
```math 
{ode(QA_red)} = - {vPSII_recomb} + {vPSII_ChSep} - {v_PSII} + {v_PQ}
```
```math 
{ode(pH_lumen)} = \frac{{{ipt_lu}}}{{{b_H}}} \cdot {vPSII_recomb} + \frac{{-{ipt_lu}}}{{{b_H}}} \cdot {vPSII_ChSep} + \frac{{-2 {ipt_lu}}}{{{b_H}}} \cdot {v_b6f} + \frac{{-2 {ipt_lu}}}{{{b_H}}} \cdot {v_NDH} + \frac{{{ipt_lu}}}{{{b_H}}} \cdot {v_KEA3} + \frac{{{ipt_lu}}}{{{b_H}}} \cdot {v_ClCe} + \frac{{{ipt_lu}}}{{{b_H}}} \cdot {v_Leak} + \frac{{{ipt_lu}}}{{{b_H}}} \cdot {v_pmf_protons_activity}
```
```math 
{ode(Dpsi)} = - {vpc} \cdot {vPSII_recomb} + {vpc} \cdot {vPSII_ChSep} + {vpc} \cdot {v_b6f} + {vpc} \cdot 2 \cdot {v_NDH} + {vpc} \cdot -3 \cdot {v_ClCe} - {vpc} \cdot {v_Leak} - {vpc} \cdot {v_pmf_protons_activity} + {vpc} \cdot {PSI_ChSep} - {vpc} \cdot {v_VKC} - {vpc} \cdot {v_VCCN1}
```
```math 
{ode(PQH_2)} = 0.5 \cdot {v_PSII} - 0.5 \cdot {v_PQ} - 0.5 \cdot {v_b6f} + 0.5 \cdot {v_NDH} + 0.5 \cdot {v_PGR}
```
```math 
{ode(PC_ox)} = - {v_b6f} + {v_PSI_PCoxid}
```
```math 
{ode(Fd_red)} = - {v_NDH} + {PSI_ChSep} - {v_PGR} - {v_FNR} - {v_Mehler}
```
```math 
{ode(Y2)} = {PSI_ChSep} - {v_PSI_PCoxid}
```
```math 
{ode(NADPH_st)} = 0.5 \cdot {v_FNR} - {v_CBB}
```
```math 
{ode(K_lu)} = {ipt_lu} \cdot {v_KEA3} - {ipt_lu} \cdot {v_VKC}
```
```math 
{ode(Cl_lu)} = {ipt_lu} \cdot 2 \cdot {v_ClCe} + {ipt_lu} \cdot {v_VCCN1}
```
```math 
{ode(Cl_st)} = - 0.2 {ipt_lu} \cdot {v_ClCe} - 0.1 {ipt_lu} \cdot {v_VCCN1}
```
```math 
{ode(Zx)} = - {v_Epox} + {v_Deepox}
```

</details>
                     """)

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
{QA} =  {QA_total} - {QA_red}
```
```math
{Y0} =  {P700_total} - {Y2}
```
```math
{PQ} =  {PQ_tot} - {PQH_2}
```
```math
{PC_red} =  {PC_tot} - {PC_ox}
```
```math
{Fd_ox} =  {Fd_tot} - {Fd_red}
```
```math
{NADP_st} =  {NADP_tot} - {NADPH_st}
```
```math
{Vx} =  {Carotenoids_tot} - {Zx}
```
```math
{PsbSP} =  \frac{{1}}{{10^{{3 \left( {pH_lumen} - {pKa_PsbS} \right)}} + 1}}
```
```math
{NPQ} =  0.4 {NPQ_max} \cdot {PsbSP} {Zx} + 0.5 {NPQ_max} \cdot {PsbSP} + 0.1 {NPQ_max} {Zx}
```
```math
{PhiPSII} =  \frac{{1}}{{1 + \frac{{1 + {NPQ}}}{{4.88 {QA}}}}}
```
```math
{H_lumen} =  10^{{-1 {pH_lumen}}}
```
```math
{pmf} =  {Dpsi} + 0.06 \left( {pH_st} - {pH_lumen} \right)
```
```math
{H_st} =  10^{{-1 {pH_st}}}
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
{light_per_L} =  \frac{{0.84 {PPFD}}}{{0.7}}
```
```math
{kCBB} =  60 \frac{{{PPFD}}}{{{PPFD} + 250}}
```
```math
{driving_force_Cl} =  0.06 \log_{{10}} \left( \frac{{{Cl_st}}}{{{Cl_lu}}} \right) + {Dpsi}
```
```math
{delta_pH} =  {pH_st} - {pH_lumen}
```
```math
{delta_pH_inVolts} =  0.06 {delta_pH}
```
```math
{qL_act} =  \frac{{{QA}^{{3}}}}{{{QA}^{{3}} + 0.15^{{3}}}}
```
```math
{pH_act} =  \frac{{1}}{{10^{{1 \left( {pH_lumen} - 6.0 \right)}} + 1}}
```

</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
{vPSII_recomb} =  {k_recomb} \cdot {QA_red} \cdot 10^{{\frac{{{Dpsi} + 0.06 \left( 7.0 - {pH_lumen} \right)}}{{0.06}}}}
```
```math
{vPSII_ChSep} =  {sigma0_II} \cdot {light_per_L} \cdot {PhiPSII}
```
```math
{v_PSII} =  {QA_red} \cdot {PQ} \cdot {k_QA}
```
```math
{v_PQ} =  \frac{{{PQH_2} \cdot {QA} \cdot {k_QA}}}{{{Keq_QA}}}
```
```math
{v_b6f} =  \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \cdot {PC_ox} \cdot \left( 1 - \frac{{1}}{{10^{{{pH_lumen} - {pKa_reg}}} + 1}} \right) {c_b6f} \cdot {Vmax_b6f} - \left( 1 - \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \right) {PC_red} \frac{{\left( 1 - \frac{{1}}{{10^{{{pH_lumen} - {pKa_reg}}} + 1}} \right) {c_b6f} \cdot {Vmax_b6f}}}{{10^{{\frac{{{Em_PC_pH7} - \left( {Em_PQH2_pH7} - 0.06 \left( {pH_lumen} - 7.0 \right) \right) - {pmf}}}{{0.06}}}}}}
```
```math
{v_NDH} =  {k_NDH1} \cdot {Fd_red} \cdot {PQ} - \frac{{{k_NDH1}}}{{10^{{\frac{{{Em_PQH2_pH7} - 0.06 \left( {pH_st} - 7.0 \right) - {Em_Fd} - {pmf} \cdot 2}}{{0.06}}}}}} \cdot {Fd_ox} \cdot {PQH_2}
```
```math
{v_PGR} =  \frac{{{Vmax_PGR} \cdot \frac{{{Fd_red}^{{4}}}}{{{Fd_red}^{{4}} + 0.1^{{4}}}} \cdot {PQ}}}{{{PQ} + {PQH_2}}}
```
```math
{PSI_ChSep} =  {Y0} \cdot {light_per_L} \cdot {sigma0_I} \cdot {Fd_ox}
```
```math
{v_PSI_PCoxid} =  {PC_red} \cdot {k_PCtoP700} \cdot {Y2}
```
```math
{v_FNR} =  {k_FdtoNADP} \cdot {NADP_st} \cdot {Fd_red}
```
```math
{v_Mehler} =  \frac{{4 \cdot 0.000265 {Fd_red}}}{{{Fd_red} + {Fd_ox}}}
```
```math
{v_CBB} =  \frac{{\mathrm{{kCBB}} \cdot \left( 1.0 - \exp \left( \frac{{-{time}}}{{600}} \right) \right) \left( \log \left( \frac{{{NADPH_st}}}{{{NADP_st}}} \right) - \log 1.25 \right) }}{{\log \left( \frac{{3.5}}{{1.25}} \right) }}
```
```math
{v_KEA3} =  {k_KEA3} \cdot \left( {H_lumen} \cdot {K_st} - {H_st} \cdot {K_lu} \right) {qL_act} \cdot {pH_act}
```
```math
{v_VKC} =  \frac{{{P_K} \cdot \left( -0.06 \log_{{10}} \left( \frac{{{K_st}}}{{{K_lu}}} \right) + {Dpsi} \right) \left( {K_lu} + {K_st} \right)}}{{2}}
```
```math
{v_VCCN1} =  \frac{{{k_VCCN1} \cdot \left( 332 {driving_force_Cl}^{{3}} + 30.8 {driving_force_Cl}^{{2}} + 3.6 {driving_force_Cl} \right) \left( {Cl_st} + {Cl_lu} \right)}}{{2}}
```
```math
{v_ClCe} =  \frac{{{k_ClCe} \cdot \left( {driving_force_Cl} \cdot 2 + {pmf} \right) \left( {Cl_st} + {Cl_lu} \right) \left( {H_lumen} + {H_st} \right)}}{{4}}
```
```math
{v_Leak} =  {pmf} \cdot {k_leak} \cdot {H_lumen}
```
```math
{v_pmf_protons_activity} = ERROR because of function "_v_pmf_protons_activity"
```
```math
{v_Epox} =  {Zx} \cdot \mathrm{{k\_E{Zx}}}
```
```math
{v_Deepox} =  {Vx} \cdot \mathrm{{{Vx}max\_{Vx}DE}} \frac{{1}}{{10^{{\mathrm{{nh\_{Vx}DE}} \cdot \left( {pH_lumen} - \mathrm{{pKa\_{Vx}DE}} \right)}} + 1}}
```

</details>

                     """)

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
