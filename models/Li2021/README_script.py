from mdutils.mdutils import MdUtils  # noqa: E402
from glossary_utils import gloss_fromCSV
from pathlib import Path
# from models import get_model

import os

###### Util Functions ######


def remove_math_mode(dic: dict, k: str, column_name: str = "Abbreviation Here"):
    s = dic[k][column_name]

    for i in range(dic[k][column_name].count("$")):
        s = s.replace("$", "")

    return s


def ode(first_var: str, second_var: str = "t"):
    for i in [first_var, second_var]:
        if "$" in i:
            raise ValueError(f"Your given variable '{i}' has a '$' in it")

    return rf"\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}"


###### Model Infos ######

model_title = "Li2021"
model_doi = "ENTER HERE"

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


def remove_math(
    df, query_result, query_column="Paper Abbr.", answer_column="Common Abbr."
):
    res = df[df[query_column] == query_result][answer_column].values[0]

    for i in range(
        df.loc[df[query_column] == query_result, answer_column].iloc[0].count("$")
    ):
        res = res.replace("$", "")

    return res


# -- Compounds --

Vx = remove_math(comps_table, r"$\mathrm{Vx}$")
Zx = remove_math(comps_table, r"$\mathrm{Zx}$")
ATP_st = remove_math(comps_table, r"$\mathrm{ATP}$")
ADP_st = remove_math(comps_table, r"$\mathrm{ADP}$")
K_lu = remove_math(comps_table, r"$\mathrm{K}^{+}_{\mathrm{lumen}$")
K_st = remove_math(comps_table, r"$\mathrm{K}^{+}_{\mathrm{stroma}$")
Cl_lu = remove_math(comps_table, r"$\mathrm{Cl}^{-}_{\mathrm{lumen}$")
Cl_st = remove_math(comps_table, r"$\mathrm{Cl}^{-}_{\mathrm{stroma}$")
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
K_QA = remove_math(params_table, r"$Keq_{QA \rightarrow PQ}")
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
pH_st = remove_math(params_table, r"$\mathrm{pH_{stroma}}")
time = "t"

# --- Derived Parameters ---

ppPSII = remove_math(derived_params_table, r"$\mathrm{light\_per\_L}$")
K_b6f = remove_math(derived_params_table, r"$Keq_{b6f}")
k_b6f = remove_math(derived_params_table, r"$k_{b6f}$")
K_NDH1 = remove_math(derived_params_table, r"$Keq_{NDH}")
Act_ATPsynth = remove_math(derived_params_table, r"$\mathrm{ATP\_synthase\_actvt}$")
PSII_ChSep = remove_math(derived_params_table, r"$PSII_{charge}$")
PSII_recomb = remove_math(derived_params_table, r"$PSII_{recom}$")
Cl_df = remove_math(derived_params_table, r"$\mathrm{driving\_force\_Cl}$")


###### Making README File ######

mdFile = MdUtils(file_name=f"{os.path.dirname(__file__)}/README.md")

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
{ode(PC_red)} = 1.0 \cdot {v_b6f} - 1.0 \cdot {v_PSI_PCoxid} 
```
```math 
{ode(PC_ox)} = -1.0 \cdot {v_b6f} + 1.0 \cdot {v_PSI_PCoxid} 
```
```math 
{ode(PQH_2)} = -0.5 \cdot {v_b6f} + 0.5 \cdot {v_NDH} + 0.5 \cdot {v_PGR} + 0.5 \cdot {v_PSII} 
```
```math 
{ode(PQ)} = 0.5 \cdot {v_b6f} - 0.5 \cdot {v_NDH} - 0.5 \cdot {v_PGR} - 0.5 \cdot {v_PSII} 
```
```math 
{ode(pH_lu)} = -0.08385714285714285 \cdot {v_b6f} - 0.08385714285714285 \cdot {v_NDH} + 0.19566666666666666 \cdot {v_ATPsynth} + 0.041928571428571426 \cdot {v_ClCe} + 0.041928571428571426 \cdot {v_KEA3} - 0.041928571428571426 \cdot {vPSII_ChSep} + 0.041928571428571426 \cdot {vPSII_recomb} 
```
```math 
{ode(Dpsi)} = 0.047 \cdot {v_b6f} + 0.094 \cdot {v_NDH} - 0.21933333333333335 \cdot {v_ATPsynth} - 0.047 \cdot {v_ClCe} + 0.047 \cdot {vPSII_ChSep} - 0.047 \cdot {vPSII_recomb} - 0.047 \cdot {v_VCCN1} - 0.047 \cdot {v_VKC} + 0.047 \cdot {PSI_ChSep} 
```
```math 
{ode(Fd_red)} = -1.0 \cdot {v_NDH} - 1.0 \cdot {v_PGR} + 1.0 \cdot {PSI_ChSep} - 1.0 \cdot {v_FNR} - 1.0 \cdot {v_Mehler} 
```
```math 
{ode(Fd_ox)} = 1.0 \cdot {v_NDH} + 1.0 \cdot {v_PGR} - 1.0 \cdot {PSI_ChSep} + 1.0 \cdot {v_FNR} + 1.0 \cdot {v_Mehler} 
```
```math 
{ode(Vx)} = -1.0 \cdot {v_Deepox} 
```
```math 
{ode(Zx)} = 1.0 \cdot {v_Deepox} 
```
```math 
{ode(Cl_lu)} = 0.001174 \cdot {v_ClCe} + 0.000587 \cdot {v_VCCN1} 
```
```math 
{ode(Cl_st)} = -0.0001174 \cdot {v_ClCe} - 5.87e-05 \cdot {v_VCCN1} 
```
```math 
{ode(K_lu)} = 0.000587 \cdot {v_KEA3} - 0.000587 \cdot {v_VKC} 
```
```math 
{ode(K_st)} = -5.87e-05 \cdot {v_KEA3} + 5.87e-05 \cdot {v_VKC} 
```
```math 
{ode(QA_red)} = -1.0 \cdot {v_PSII} + 1.0 \cdot {vPSII_ChSep} - 1.0 \cdot {vPSII_recomb} 
```
```math 
{ode(QA_ox)} = 1.0 \cdot {v_PSII} - 1.0 \cdot {vPSII_ChSep} + 1.0 \cdot {vPSII_recomb} 
```
```math 
{ode(Y2)} = -1.0 \cdot {v_PSI_PCoxid} + 1.0 \cdot {PSI_ChSep} 
```
```math 
{ode(Y0)} = 1.0 \cdot {v_PSI_PCoxid} - 1.0 \cdot {PSI_ChSep} 
```
```math 
{ode(NADPH_st)} = 0.5 \cdot {v_FNR} - 0.5 \cdot {v_CBB} 
```
```math 
{ode(NADP_st)} = -0.5 \cdot {v_FNR} + 0.5 \cdot {v_CBB} 
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
{H_lu} =  10^{{-1 {pH_lu}}}
```
```math
{PMF} =  {Dpsi} + 0.06 \left( {pH_st} - {pH_lu} \right)
```
```math
{PsbSP} =  \frac{{1}}{{10^{{3 \left( {pH_lu} - {pKa_PsbS} \right)}} + 1}}
```
```math
{NPQ} =  0.4 {NPQ_max} \cdot {PsbSP} \cdot {Zx} + 0.5 {NPQ_max} \cdot {PsbSP} + 0.1 {NPQ_max} \cdot {Zx}
```
```math
{Prot_ATPsynth} =  {Act_ATPsynth} \cdot \left( 1 - \frac{{1}}{{10^{{\frac{{\left( {PMF} - 0.132 \right) \cdot 1.5}}{{0.06}}}} + 1}} \right) {HPR} \cdot {Vmax_ATPsynth} + \left( 1 - {Act_ATPsynth} \right) \left( 1 - \frac{{1}}{{10^{{\frac{{\left( {PMF} - 0.204 \right) \cdot 1.5}}{{0.06}}}} + 1}} \right) {HPR} \cdot {Vmax_ATPsynth}
```
```math
{PhiPSII} =  \frac{{1}}{{1 + \frac{{1 + {NPQ}}}{{4.88 {QA_ox}}}}}
```
```math
{singO2} =  {PSII_recomb} \cdot {phi_triplet} \cdot {phi_1O2}
```
```math
{H_st} =  10^{{-1 {pH_st}}}
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
{ppPSII} =  0.84 \frac{{{PAR}}}{{0.7}}
```
```math
{K_b6f} =  10^{{\frac{{{Em_PC_pH7} - \left( {Em_PQH2_pH7} - 0.06 \left( {pH_lu} - 7.0 \right) \right) - {PMF}}}{{0.06}}}}
```
```math
{k_b6f} =  \left( 1 - \frac{{1}}{{10^{{{pH_lu} - {pKa_reg}}} + 1}} \right) {c_b6f} \cdot {Vmax_b6f}
```
```math
{K_NDH1} =  10^{{\frac{{{Em_PQH2_pH7} - 0.06 \left( {pH_st} - 7.0 \right) - {Em_Fd} - {PMF} \cdot 2}}{{0.06}}}}
```
```math
{Act_ATPsynth} =  0.2 + 0.8 \frac{{\left( \frac{{{time}}}{{165}} \right)^{{4}}}}{{\left( \frac{{{time}}}{{165}} \right)^{{4}} + 1}}
```
```math
{PSII_ChSep} =  {sigma0_II} \cdot {ppPSII} \cdot {PhiPSII}
```
```math
{PSII_recomb} =  {k_recomb} \cdot {QA_red} \cdot 10^{{\frac{{{Dpsi} + 0.06 \left( 7.0 - {pH_lu} \right)}}{{0.06}}}}
```
```math
{Cl_df} =  0.06 \log_{{10}} \left( \frac{{{Cl_st}}}{{{Cl_lu}}} \right) + {Dpsi}
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
{v_b6f} =  \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \cdot {PC_ox} \cdot {k_b6f} - \left( 1 - \frac{{{PQH_2}}}{{{PQH_2} + {PQ}}} \right) {PC_red} \frac{{{k_b6f}}}{{{K_b6f}}}
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
    {Prot_ATPsynth} + {PMF} * {k_Leak} * {H_lu} & \quad \textrm{{if }} {ppPSII} > 0 \\
    {PMF} * {k_Leak} * {H_lu} & \quad \textrm{{else}}
  \end{{array}}
\right.
```
```math
{v_VCCN1} =  \frac{{{k_VCCN1} \cdot \left( 332 {Cl_df}^{{3}} + 30.8 {Cl_df}^{{2}} + 3.6 {Cl_df} \right) \left( {Cl_st} + {Cl_lu} \right)}}{{2}}
```
```math
{v_ClCe} =  \frac{{{k_ClCe} \cdot \left( {Cl_df} \cdot 2 + {PMF} \right) \left( {Cl_st} + {Cl_lu} \right) \left( {H_lu} + {H_st} \right)}}{{4}}
```
```math
{v_KEA3} =  {k_KEA3} \cdot \left( {H_lu} \cdot {K_st} - {H_st} \cdot {K_lu} \right) \frac{{\left( 1 - {QA_red} \right)^{{3}}}}{{\left( 1 - {QA_red} \right)^{{3}} + 0.15^{{3}}}} \frac{{1}}{{10^{{1 \left( {pH_lu} - 6.0 \right)}} + 1}}
```
```math
{v_VKC} =  \frac{{{P_K} \cdot \left( -0.06 \log_{{10}} \left( \frac{{{K_st}}}{{{K_lu}}} \right) + {Dpsi} \right) \left( {K_lu} + {K_st} \right)}}{{2}}
```
```math
{vPSII_ChSep} =  {PSII_ChSep}
```
```math
{vPSII_recomb} =  {PSII_recomb}
```
```math
{v_PSII} =  {QA_red} \cdot {PQ} \cdot {k_QA} - {PQH_2} \cdot {QA_ox} \frac{{{k_QA}}}{{{K_QA}}}
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
{v_CBB} =  \frac{{{k_CBB} \cdot \left( 1 - \exp \left( \frac{{-{time}}}{{600}} \right) \right) \left( \log \left( \frac{{{NADPH_st}}}{{{NADP_st}}} \right) - \log 1.25 \right)}}{{\log \left( \frac{{3.5}}{{1.25}} \right)}}
```
```math
{v_Mehler} =  \frac{{4 \cdot 0.000265 {Fd_red}}}{{{Fd_red} + {Fd_ox}}}
```

</details>

                     """)

mdFile.create_md_file()
