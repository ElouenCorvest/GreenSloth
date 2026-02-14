from pathlib import Path

from mdutils.mdutils import MdUtils  # noqa: E402

from GreenSlothUtils import gloss_fromCSV, remove_math

###### Util Functions ######


def ode(first_var: str, second_var: str = "t") -> str:
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

Vx = remove_math(comps_table, r"$\mathrm{Vx}$")
Zx = remove_math(comps_table, r"$\mathrm{Zx}$")
ATP_st = remove_math(comps_table, r"$\mathrm{ATP}$")
ADP_st = remove_math(comps_table, r"$\mathrm{ADP}$")
K_lu = remove_math(comps_table, r"$\mathrm{K}^{+}_{\mathrm{lumen}}$")
K_st = remove_math(comps_table, r"$\mathrm{K}^{+}_{\mathrm{stroma}}$")
Cl_lu = remove_math(comps_table, r"$\mathrm{Cl}^{-}_{\mathrm{lumen}}$")
Cl_st = remove_math(comps_table, r"$\mathrm{Cl}^{-}_{\mathrm{stroma}}$")
Dpsi = remove_math(comps_table, r"$\Delta \Psi$")
QA_ox = remove_math(comps_table, r"$\mathrm{Q_{A}}$")
QA_red = remove_math(comps_table, r"$\mathrm{Q_{A}}^{-}$")
PQH_2 = remove_math(comps_table, r"$\mathrm{PQH_2}$")
PQ = remove_math(comps_table, r"$\mathrm{PQ}$")
PC_red = remove_math(comps_table, r"$\mathrm{PC}$")
PC_ox = remove_math(comps_table, r"$\mathrm{PC}^+$")
Fd_ox = remove_math(comps_table, r"$\mathrm{Fd_{ox}}$")
Fd_red = remove_math(comps_table, r"$\mathrm{Fd_{red}}$")
pH_lu = remove_math(comps_table, r"$\mathrm{pH_{lumen}}")
NADPH_st = remove_math(comps_table, r"$\mathrm{NADPH}$")
NADP_st = remove_math(comps_table, r"$\mathrm{NADP}^+$")
Y0 = remove_math(comps_table, r"$\mathrm{P_{700}}$")
Y2 = remove_math(comps_table, r"$\mathrm{P_{700}}^+$")

# -- Derived Compounds --

H_lu = remove_math(derived_comps_table, r"$H_{lumen}$")
PMF = remove_math(derived_comps_table, r"$pmf$")
PsbSP = remove_math(derived_comps_table, r"$PsbS\_H$")
NPQ = remove_math(derived_comps_table, r"$NPQ$")
Prot_ATPsynth = remove_math(derived_comps_table, r"$\mathrm{d\_protons\_to\_ATP}$")
PhiPSII = remove_math(derived_comps_table, r"$\Phi \mathrm{PSII}$")
singO2 = remove_math(derived_comps_table, r"$^1\mathrm{O_2}$")
H_st = remove_math(derived_comps_table, r"$H_{stroma}$")

# -- Rates --

v_b6f = remove_math(rates_table, r"$v_{b6f}$")
v_NDH = remove_math(rates_table, r"$v_{NDH}$")
v_PGR = remove_math(rates_table, r"$v_{PGR}$")
v_Deepox = remove_math(rates_table, r"$v_{VDE}$")
v_ATPsynth = remove_math(rates_table, r"$v_{ATPsynthase}$")
v_VCCN1 = remove_math(rates_table, r"$v_{VCCN1}$")
v_ClCe = remove_math(rates_table, r"$v_{ClCe}$")
v_KEA3 = remove_math(rates_table, r"$v_{KEA3}$")
v_VKC = remove_math(rates_table, r"$v_{K\_channel}$")
vPSII_ChSep = remove_math(rates_table, r"$PSII_{charge}$")
vPSII_recomb = remove_math(rates_table, r"$PSII_{recom}$")
v_PSII = remove_math(rates_table, r"$v_{PSII}$")
PSI_ChSep = remove_math(rates_table, r"$PSI_{charge}$")
v_PSI_PCoxid = remove_math(rates_table, r"$PSI_{PC\_oxidiation}$")
v_FNR = remove_math(rates_table, r"$v_{FNR}$")
v_CBB = remove_math(rates_table, r"$v_{CBB}$")
v_Mehler = remove_math(rates_table, r"$v_{Mehler}$")

# -- Parameters --

Pi_st = remove_math(params_table, r"$\mathrm{P}_\mathrm{i}$")
Vmax_b6f = remove_math(params_table, r"$V_{max}\left( \mathrm{b6f} \right)$")
c_b6f = remove_math(params_table, r"$\mathrm{cytochrome b_6f content}$")
pKa_reg = remove_math(params_table, r"$\mathrm{pK_{reg}}$")
Em_PC_pH7 = remove_math(params_table, r"$Em_\mathrm{PC\_pH7}$")
Em_PQH2_pH7 = remove_math(params_table, r"$Em_\mathrm{PQH2\_pH7}$")
Em_Fd = remove_math(params_table, r"$Em_{Fd}$")
k_NDH1 = remove_math(params_table, r"$k_\mathrm{{NDH}}$")
Vmax_PGR = remove_math(params_table, r"$V_{max}\left( \mathrm{PGR} \right)$")
Vmax_VDE = remove_math(params_table, r"$V_{max}\left( \mathrm{VDE} \right)$")
pKa_VDE = remove_math(params_table, r"$\mathrm{pK_{VDE}}$")
nh_VDE = remove_math(params_table, r"$\mathrm{Hill_{VDE}}$")
k_EZ = remove_math(params_table, r"$k_\mathrm{ZE}")
pKa_PsbS = remove_math(params_table, r"$\mathrm{pK_{PsbS}}$")
DeltaG0_ATP = remove_math(params_table, r"$\Delta G_{\mathrm{ATP}}$")
HPR = remove_math(params_table, r"$\mathrm{HPR}$")
Vmax_ATPsynth = remove_math(params_table, r"$V_\mathrm{max|ATPsynth}$")
F = remove_math(params_table, r"$F$")
NPQ_max = remove_math(params_table, r"$NPQ_{max}$")
k_recomb = remove_math(params_table, r"$k_{recomb}$")
phi_triplet = remove_math(params_table, r"$\Phi _{triplet}$")
phi_1O2 = remove_math(params_table, r"$\Phi _{O_2}^1$")
PAR = remove_math(params_table, r"$\mathrm{PAR}$")
PSII_max = remove_math(params_table, r"")
sigma0_II = remove_math(params_table, r"$\mathrm{PSII_{antenna_size}}$")
k_QA = remove_math(params_table, r"$k_\mathrm{{QA}}$")
K_QA = remove_math(params_table, r"$Keq_{QA \rightarrow PQ}$S")
vpc = remove_math(params_table, r"$\mathrm{Volts\_per\_charge}$")
sigma0_I = remove_math(params_table, r"$\mathrm{PSI_{antenna_size}}$")
ipt_lu = remove_math(params_table, r"$\mathrm{lumen\_protons\_per\_turnover}$")
b_H = remove_math(params_table, r"$\mathrm{Buffering\ capacity}$")
ipt_st = remove_math(params_table, r"$\mathrm{stroma\_protons\_per\_turnover}$")
P_K = remove_math(params_table, r"$\mathrm{Perm_K}$")
k_VCCN1 = remove_math(params_table, r"$k_{VCCN1}$")
k_ClCe = remove_math(params_table, r"$k_{CLCE}$")
k_PCtoP700 = remove_math(params_table, r"$k_{PC\_to\_P700}$")
k_KEA3 = remove_math(params_table, r"$k_{KEA3}$")
k_FdtoNADP = remove_math(params_table, r"$k_\mathrm{Fd\_to\_NADP}$")
k_CBB = remove_math(params_table, r"$k_{CBC}$")
k_Leak = remove_math(params_table, r"$k_{leak}$")
pH_st = remove_math(params_table, r"$\mathrm{pH_{stroma}}$")
time = "t"

# --- Derived Parameters ---

ppPSII = remove_math(derived_params_table, r"$\mathrm{light\_per\_L}$")
K_b6f = remove_math(derived_params_table, r"$Keq_{b6f}$")
k_b6f = remove_math(derived_params_table, r"$k_{b6f}$")
K_NDH1 = remove_math(derived_params_table, r"$Keq_{NDH}$")
Act_ATPsynth = remove_math(derived_params_table, r"$\mathrm{ATP\_synthase\_actvt}$")
PSII_ChSep = remove_math(derived_params_table, r"$PSII_{charge}$")
PSII_recomb = remove_math(derived_params_table, r"$PSII_{recom}$")
Cl_df = remove_math(derived_params_table, r"$\mathrm{driving\_force\_Cl}$")

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

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
{ode(PC_red)} = {v_b6f} - {v_PSI_PCoxid}
```
```math 
{ode(PC_ox)} = - {v_b6f} + {v_PSI_PCoxid}
```
```math 
{ode(PQH_2)} = - 0.5 \cdot {v_b6f} + 0.5 \cdot {v_NDH} + 0.5 \cdot {v_PGR} + 0.5 \cdot {v_PSII}
```
```math 
{ode(PQ)} = 0.5 \cdot {v_b6f} - 0.5 \cdot {v_NDH} - 0.5 \cdot {v_PGR} - 0.5 \cdot {v_PSII}
```
```math 
{ode(pH_lu)} = \frac{{{ipt_lu}}}{{{b_H}}} \cdot \left( -2 \cdot {v_b6f} - 2 \cdot {v_NDH} + \frac{{14}}{{3}} \cdot {v_ATPsynth} + {v_ClCe} + {v_KEA3} - {vPSII_ChSep} + {vPSII_recomb} \right)
```
```math 
{ode(Dpsi)} = {vpc} \cdot \left( {v_b6f} + 2 \cdot {v_NDH} - \frac{{14}}{{3}} \cdot {v_ATPsynth} - {v_ClCe} + {vPSII_ChSep} - {vPSII_recomb} - {v_VCCN1} - {v_VKC} + {PSI_ChSep} \right)
```
```math 
{ode(Fd_red)} = - {v_NDH} - {v_PGR} + {PSI_ChSep} - {v_FNR} - {v_Mehler}
```
```math 
{ode(Fd_ox)} = {v_NDH} + {v_PGR} - {PSI_ChSep} + {v_FNR} + {v_Mehler}
```
```math 
{ode(Vx)} = - {v_Deepox}
```
```math 
{ode(Zx)} = {v_Deepox}
```
```math 
{ode(Cl_lu)} = 2 {ipt_lu} \cdot {v_ClCe} + {ipt_lu} \cdot {v_VCCN1}
```
```math 
{ode(Cl_st)} = - 2 {ipt_st} \cdot {v_ClCe} - 1 {ipt_st} \cdot {v_VCCN1}
```
```math 
{ode(K_lu)} = {ipt_lu} \cdot {v_KEA3} - 1 {ipt_lu} \cdot {v_VKC}
```
```math 
{ode(K_st)} = - 1 {ipt_st} \cdot {v_KEA3} + {ipt_st} \cdot {v_VKC}
```
```math 
{ode(QA_red)} = - {v_PSII} + {vPSII_ChSep} - {vPSII_recomb}
```
```math 
{ode(QA_ox)} = {v_PSII} - {vPSII_ChSep} + {vPSII_recomb}
```
```math 
{ode(Y2)} = - {v_PSI_PCoxid} + {PSI_ChSep}
```
```math 
{ode(Y0)} = {v_PSI_PCoxid} - {PSI_ChSep}
```
```math 
{ode(NADPH_st)} = 0.5 \cdot {v_FNR} - 0.5 \cdot {v_CBB}
```
```math 
{ode(NADP_st)} = - 0.5 \cdot {v_FNR} + 0.5 \cdot {v_CBB}
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
{H_lu} =  10^{{-{pH_lu}}}
```
```math
{PMF} =  {Dpsi} + 0.06 \cdot \left( {pH_st} - {pH_lu} \right)
```
```math
{PsbSP} =  \frac{{1}}{{10^{{3 \cdot \left( {pH_lu} - {pKa_PsbS} \right)}} + 1}}
```
```math
{NPQ} =  0.4 \cdot {NPQ_max} \cdot {PsbSP} \cdot {Zx} + 0.5 \cdot {NPQ_max} \cdot {PsbSP} + 0.1 \cdot {NPQ_max} \cdot {Zx}
```
```math
{Prot_ATPsynth} =  {Act_ATPsynth} \cdot \left( 1 - \frac{{1}}{{10^{{\frac{{\left( {PMF} - 0.132 \right) \cdot 1.5}}{{0.06}}}} + 1}} \right) {HPR} \cdot {Vmax_ATPsynth} + \left( 1 - {Act_ATPsynth} \right) \left( 1 - \frac{{1}}{{10^{{\frac{{\left( {PMF} - 0.204 \right) \cdot 1.5}}{{0.06}}}} + 1}} \right) {HPR} \cdot {Vmax_ATPsynth}
```
```math
{PhiPSII} =  \frac{{1}}{{1 + \frac{{1 + {NPQ}}}{{4.88 \cdot {QA_ox}}}}}
```
```math
{singO2} =  {PSII_recomb} \cdot {phi_triplet} \cdot {phi_1O2}
```
```math
{H_st} =  10^{{-{pH_st}}}
```

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
{ppPSII} =  0.84 \cdot \frac{{{PAR}}}{{0.7}}
```
```math
{K_b6f} =  10^{{\frac{{{Em_PC_pH7} - \left( {Em_PQH2_pH7} - 0.06 \cdot \left( {pH_lu} - 7.0 \right) \right) - {PMF}}}{{0.06}}}}
```
```math
{k_b6f} =  \left( 1 - \frac{{1}}{{10^{{{pH_lu} - {pKa_reg}}} + 1}} \right) {c_b6f} \cdot {Vmax_b6f}
```
```math
{K_NDH1} =  10^{{\frac{{{Em_PQH2_pH7} - 0.06 \cdot \left( {pH_st} - 7.0 \right) - {Em_Fd} - {PMF} \cdot 2}}{{0.06}}}}
```
```math
{Act_ATPsynth} =  0.2 + 0.8 \cdot \frac{{\left( \frac{{{time}}}{{165}} \right)^{{4}}}}{{\left( \frac{{{time}}}{{165}} \right)^{{4}} + 1}}
```
```math
{PSII_ChSep} =  {sigma0_II} \cdot {ppPSII} \cdot {PhiPSII}
```
```math
{PSII_recomb} =  {k_recomb} \cdot {QA_red} \cdot 10^{{\frac{{{Dpsi} + 0.06 \cdot \left( 7.0 - {pH_lu} \right)}}{{0.06}}}}
```
```math
{Cl_df} =  0.06 \cdot \log_{{10}} \left( \frac{{{Cl_st}}}{{{Cl_lu}}} \right) + {Dpsi}
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
{v_b6f} =  \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \cdot {PC_ox} \cdot {k_b6f} - \left( 1 - \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \right) \cdot {PC_red} \cdot \frac{{{k_b6f}}}{{{K_b6f}}}
```
```math
{v_NDH} =  {k_NDH1} \cdot {Fd_red} \cdot {PQ} - \frac{{{k_NDH1}}}{{{K_NDH1}}} \cdot {Fd_ox} \cdot {PQH_2}
```
```math
{v_PGR} =  \frac{{{Vmax_PGR} \cdot \frac{{{Fd_red}^{{4}}}}{{{Fd_red}^{{4}} + 0.1^{{4}}}} \cdot {PQ}}}{{{PQ} + {PQH_2}}}
```
```math
{v_Deepox} =  {Vx} \cdot {Vmax_VDE} \frac{{1}}{{10^{{{nh_VDE} \cdot \left( {pH_lu} - {pKa_VDE} \right)}} + 1}} - {Zx} \cdot {k_EZ}
```
```math
{v_ATPsynth} = \left\{{ 
  \begin{{array}}{{ c l }}
    {Prot_ATPsynth} + {PMF} \cdot {k_Leak} \cdot {H_lu} & \quad \textrm{{if }} {ppPSII} > 0 \\
    {PMF} \cdot {k_Leak} \cdot {H_lu} & \quad \textrm{{else}}
  \end{{array}}
\right.
```
```math
{v_VCCN1} =  \frac{{{k_VCCN1} \cdot \left( 332 \cdot {Cl_df}^{{3}} + 30.8 \cdot {Cl_df}^{{2}} + 3.6 \cdot {Cl_df} \right) \cdot \left( {Cl_st} + {Cl_lu} \right)}}{{2}}
```
```math
{v_ClCe} =  \frac{{{k_ClCe} \cdot \left( {Cl_df} \cdot 2 + {PMF} \right) \cdot \left( {Cl_st} + {Cl_lu} \right) \cdot \left( {H_lu} + {H_st} \right)}}{{4}}
```
```math
{v_KEA3} =  {k_KEA3} \cdot \left( {H_lu} \cdot {K_st} - {H_st} \cdot {K_lu} \right) \frac{{\left( 1 - {QA_red} \right)^{{3}}}}{{\left( 1 - {QA_red} \right)^{{3}} + 0.15^{{3}}}} \cdot \frac{{1}}{{10^{{\left( {pH_lu} - 6.0 \right)}} + 1}}
```
```math
{v_VKC} =  \frac{{{P_K} \cdot \left( -0.06 \cdot \log_{{10}} \left( \frac{{{K_st}}}{{{K_lu}}} \right) + {Dpsi} \right) \cdot \left( {K_lu} + {K_st} \right)}}{{2}}
```
```math
{vPSII_ChSep} =  {PSII_ChSep}
```
```math
{vPSII_recomb} =  {PSII_recomb}
```
```math
{v_PSII} =  {QA_red} \cdot {PQ} \cdot {k_QA} - {PQH_2} \cdot {QA_ox} \cdot \frac{{{k_QA}}}{{{K_QA}}}
```
```math
{PSI_ChSep} =  {Y0} \cdot {ppPSII} \cdot {sigma0_I} \cdot {Fd_ox}
```
```math
{v_PSI_PCoxid} =  {PC_red} \cdot {k_PCtoP700} \cdot {Y2}
```
```math
{v_FNR} =  {k_FdtoNADP} \cdot {NADP_st} \cdot {Fd_red}
```
```math
{v_CBB} =  \frac{{{k_CBB} \cdot \left( 1 - \exp \left( \frac{{-{time}}}{{600}} \right) \right) \left( \ln \left( \frac{{{NADPH_st}}}{{{NADP_st}}} \right) - \ln 1.25 \right)}}{{\ln \left( \frac{{3.5}}{{1.25}} \right)}}
```
```math
{v_Mehler} =  \frac{{4 \cdot 0.000265 \cdot {Fd_red}}}{{{Fd_red} + {Fd_ox}}}
```

</details>

                     """)

mdFile.new_header(3, "Figures")

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
