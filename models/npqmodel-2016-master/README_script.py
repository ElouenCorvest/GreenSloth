from mdutils.mdutils import MdUtils  # noqa: E402
from glossary_utils.glossary import extract_from_glossary
from pathlib import Path
import pandas as pd

import os

###### Util Functions ######

def remove_math_mode(
    dic: dict,
    k: str,
    column_name: str = 'Abbreviation Here'
):
    s = dic[k][column_name]

    for i in range(dic[k][column_name].count('$')):
        s = s.replace('$', '')

    return s

def ode(
    first_var: str,
    second_var: str = 't'
):
    for i in [first_var, second_var]:
        if '$' in i:
            raise ValueError(f"Your given variable '{i}' has a '$' in it")

    return rf'\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}'

###### Model Infos ######

model_title = 'Matuszynska2016'
model_doi = 'https://doi.org/10.1016/j.bbabio.2016.09.003'

###### Glossaries ######
cite_dict = dict()
def cite(
    cit: str,
    cite_dict = cite_dict
):
    if cit == '':
        return ''
    elif cit in cite_dict.keys():
        return f'[[{cite_dict[cit]}]]({cit})'
    else:
        num_cites_stored = len(cite_dict.keys())
        cite_dict[cit] = num_cites_stored + 1
        return f'[[{cite_dict[cit]}]]({cit})'

def gloss_fromCSV(
    path,
    cite_flag: bool = False,
    reference_col: str = 'Reference'
):
    table_df = pd.read_csv(path, keep_default_na=False)

    if cite_flag:
        table_df[reference_col] = table_df[reference_col].apply(cite)

    table_tolist = [table_df.columns.values.tolist()] + table_df.values.tolist()

    table_list = [i for k in table_tolist for i in k]

    return table_df, table_tolist, table_list

model_info = os.path.dirname(__file__) + '/model_info'

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(model_info + '/comps.csv')

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(model_info + '/rates.csv')

params_table, params_table_tolist, params_table_list = gloss_fromCSV(model_info + '/params.csv', cite_flag=True)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(model_info + '/derived_comps.csv')

derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info + '/derived_params.csv')

###### Variables for ease of access ######

def remove_math(
    df,
    query_result,
    query_column = 'Paper Abbr.',
    answer_column = 'Common Abbr.'
):
    res = df.loc[df[query_column] == query_result, answer_column].iloc[0]

    for i in range(df.loc[df[query_column] == query_result, answer_column].iloc[0].count('$')):
        res = res.replace('$', '')

    return res

PQH_2 = remove_math(comps_table, r'$\mathrm{PQH}_2$')
ATP = remove_math(comps_table, r'$\mathrm{ATP}$')
H = remove_math(comps_table, r'$\mathrm{H}$')
PsbS = remove_math(comps_table, r'$\mathrm{PsbS}$')
Vx = remove_math(comps_table, r'$\mathrm{Vx}$')
ATPase = remove_math(comps_table, r'$\mathrm{ATPase}^*$')

v_PSII = remove_math(rates_table, r'$v_{\mathrm{PSII}}$')
v_PQ = remove_math(rates_table, r'$v_{\mathrm{PQ}_{\mathrm{ox}}}$')
v_ATPsynth = remove_math(rates_table, r'$v_{\mathrm{ATPsynthase}}$')
v_ATPact = remove_math(rates_table, r'$v_{\mathrm{ATPactivity}}$')
v_Leak = remove_math(rates_table, r'$v_{\mathrm{Leak}}$')
v_ATPcons = remove_math(rates_table, r'$v_{\mathrm{ATP}_{\mathrm{consumption}}}$')
v_Xcyc = remove_math(rates_table, r'$v_{\mathrm{Xcyc}}$')
v_PsbSP = remove_math(rates_table, r'$v_{\mathrm{Psbs^P}}$')

PQ = remove_math(derived_comps_table, r'$\mathrm{PQ}$')
ADP = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
PsbSP = remove_math(derived_comps_table, r'$\mathrm{PsbS^P}$')
Zx = remove_math(derived_comps_table, r'$\mathrm{Zx}$')
B_0 = remove_math(derived_comps_table, r'$\mathrm{B_0}$')
B_1 = remove_math(derived_comps_table, r'$\mathrm{B_1}$')
B_2 = remove_math(derived_comps_table, r'$\mathrm{B_2}$')
B_3 = remove_math(derived_comps_table, r'$\mathrm{B_3}$')
pH_lu = remove_math(derived_comps_table, r'$\mathrm{pH}$')
ATPase_inac = remove_math(derived_comps_table, r'$\mathrm{ATPase}$')

PSII_tot = remove_math(params_table, r'$\mathrm{PSII^{tot}}$')
PQ_tot = remove_math(params_table, r'$\mathrm{PQ^{tot}}$')
AP_tot = remove_math(params_table, r'$\mathrm{AP^{tot}}$')
PsbS_tot = remove_math(params_table, r'$\mathrm{PsbS^{tot}}$')
X_tot = remove_math(params_table, r'$\mathrm{X^{tot}}$')
gamma_0 = remove_math(params_table, r'$\gamma_0$')
K_ZSat = remove_math(params_table, r'$K_\mathrm{ZSat}$')
gamma_1 = remove_math(params_table, r'$\gamma_1$')
gamma_2 = remove_math(params_table, r'$\gamma_2$')
gamma_3 = remove_math(params_table, r'$\gamma_3$')
pfd = remove_math(params_table, r'$\mathrm{PFD}$')
k_PQred = remove_math(params_table, r'$k_{\mathrm{PQred}}$')
E_QA = remove_math(params_table, r'$E^0\mathrm{(QA/QA^-)}$')
E_PQ = remove_math(params_table, r'$E^0\mathrm{(PQ/PQH_2)}$')
E_PC = remove_math(params_table, r'$E^0\mathrm{(PC/PC^-)}$')
pH_st = remove_math(params_table, r'$\mathrm{pH}_\mathrm{stroma}$')
R = remove_math(params_table, r'$R$')
T = remove_math(params_table, r'$T$')
F = remove_math(params_table, r'$F$')
k_H = remove_math(params_table, r'$k_H$')
k_F = remove_math(params_table, r'$k_F$')
k_P = remove_math(params_table, r'$k_P$')
k_ATPconsum = remove_math(params_table, r'$k_{\mathrm{ATPconsumption}}$')
Pi = remove_math(params_table, r'$\mathrm{Pi^{mol}}$')
DG_ATP = remove_math(params_table, r'$\Delta G_{0_{\mathrm{ATP}}}$')
hpr = remove_math(params_table, r'$\mathrm{HPR}$')
k_Cytb6f = remove_math(params_table, r'$k_{\mathrm{Cytb6f}}$')
k_PTOX = remove_math(params_table, r'$k_\mathrm{PTOX}$')
k_ATPsynth = remove_math(params_table, r'$k_{\mathrm{ATPsynthase}}$')
k_ActATPase = remove_math(params_table, r'$k_{\mathrm{ActATPase}}$')
k_DeactATPase = remove_math(params_table, r'$k_{\mathrm{DeactATPase}}$')
k_leak = remove_math(params_table, r'$k_\mathrm{leak}$')
k_DV = remove_math(params_table, r'$k_\mathrm{DeepoxV}$')
nhx = remove_math(params_table, r'$\mathrm{nH}_\mathrm{X}$')
K_pHSat = remove_math(params_table, r'$K_\mathrm{pHSat}$')
k_EZ = remove_math(params_table, r'$k_\mathrm{EpoxZ}$')
k_prot = remove_math(params_table, r'$k_\mathrm{Protonation}$')
k_deprot = remove_math(params_table, r'$k_\mathrm{Deprotonation}$')
K_pHSatLHC = remove_math(params_table, r'$K_\mathrm{pHSatLHC}$')
nhl = remove_math(params_table, r'$\mathrm{nH}_\mathrm{L}$')

K_eqQAPQ = remove_math(derived_params_table, r'$K_\mathrm{eq, QAPQ}$')
K_eqATPsynthase = remove_math(derived_params_table, r'$K_\mathrm{eq, ATPsynthase}$')
K_eqcytb6f = remove_math(derived_params_table, r'$K_\mathrm{eq, cytb6f}$')
H_st = remove_math(derived_params_table, r'$\mathrm{H}_\mathrm{st}$')

###### Making README File ######

mdFile = MdUtils(file_name=f'{os.path.dirname(__file__)}/README.md')

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""The [Matuszynska2016]({model_doi}) model, a small kinetic model, was developed to delve deeper into the effect of light memory caused by non-photochemical quenching. The systematic investigation of the Xanthophyll cycle, a combination of the pigments of violaxanthin, antheraxanthin, and zeaxanthin, sparked a series of experiments to determine whether plant light memory can be detected in a time-scale of minutes to hours through pulse amplitude modulated chlorophyll fluorescence. The model was then created based on these experimental results, providing a comprehensive description of NPQ dynamics and the short-term memory of the *Arabidopsis thaliana* plant.
                     
To keep the model as simple as possible, several processes not directly linked to NPQ have been simplified to create a dynamic ODE system consisting only of 6 different compounds. With these simplifications, the authors could fulfil an additional goal: to make a general framework that is not specific to one model organism.

To demonstrate the adaptability of their model, the authors took their calibrated *Arabidopsis thaliana* model and successfully applied it to the non-model organism *Epipremnum aureum*. This adaptation allowed them to simulate realistic fluorescence measurements and replicate all the key features of chlorophyll induction, showcasing the model's versatility and potential for use in a variety of organisms.

                     """)

mdFile.new_header(2, 'Installation')

mdFile.new_header(2, 'Summary')

mdFile.new_header(3, 'Compounds')

mdFile.new_header(4, 'Part of ODE system')

mdFile.new_table(columns = len(comps_table.columns), rows = len(comps_table_tolist), text = comps_table_list)

mdFile.new_paragraph(fr"""
<details>
<summary>ODE System</summary>

```math
    \begin{{align}}
        {ode(PQH_2)} &= {v_PSII} - {v_PQ}\\
        {ode(ATP)} &= {v_ATPsynth} - {v_ATPcons}\\
        {ode(H)} &= \frac{{1}}{{b_{{\mathrm{{H}}}}}} \cdot \left( 2 \cdot {v_PSII} + 4 \cdot {v_PQ} - \frac{{14}}{{3}} \cdot {v_ATPsynth} - {v_Leak} \right) \\
        {ode(PsbS)} &= -{v_PsbSP}\\
        {ode(Vx)} &= - {v_Xcyc}\\
        {ode(ATPase)} &= {v_ATPact}
    \end{{align}}
```

</details>
                     """)

mdFile.new_header(4, 'Conserved quantities')

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Open me for the calculations of the conserved quantities!</summary>

```math
    \begin{{align}}
        {PSII_tot} &= {B_0} + {B_1} + {B_2} + {B_3} \\
        {PQ_tot} &= {PQ} + {PQH_2} \\
        {AP_tot} &= {ATP} + {ADP} \\
        {PsbS_tot} &= {PsbS} + {PsbSP} \\
        {X_tot} &= {Vx} + {Zx} \\
        {pH_lu} &= - \mathrm{{log}}_{{10}}\left( {H} \cdot 2.5 \times 10^{{-4}} \right)
    \end{{align}}
```

<details>
<summary>Calculation of Quencher</summary>

```math
    \begin{{align}}
        Q &= {gamma_0} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {PsbS} + {gamma_1} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {PsbSP} + {gamma_2} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbSP} + {gamma_3} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbS} \\
    \end{{align}}
```

</details>

<details>
<summary>Quasi steady-state approximation to calculate the rate of PSII</summary>

```math
    \begin{{align}}
        0 &= - \left( {pfd} + \frac{{{k_PQred}}}{{{K_eqQAPQ}}} \cdot {PQ} \right) \cdot {B_0} + \left( {k_H} \cdot Q + {k_F} \right) \cdot {B_1} + {k_PQred} \cdot {PQH_2} \cdot {B_3} \\
        0 &= {pfd} \cdot {B_0} - \left( {k_H} \cdot Q + {k_F} + {k_P} \right) \cdot {B_1} \\
        0 &= {pfd} \cdot {B_2} - \left( {k_H} \cdot Q + {k_F} \right) \cdot {B_3}
    \end{{align}}
```

</details>

</details>

                     """)

mdFile.new_header(3, 'Parameters')

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, 'Derived Parameters')

mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Equations of derived parameters</summary>

```math
    \begin{{align}}
        {K_eqQAPQ} &= e^{{\frac{{-\left( -2 \cdot {E_QA} \cdot {F} - 2 \cdot {E_PQ} \cdot {F} + 2 \cdot {pH_st} \cdot \mathrm{{ln}}(10) \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}}}} \\
        {K_eqATPsynthase} &= {Pi} \cdot e^{{\frac{{-{DG_ATP} - \mathrm{{ln}}\left( 10 \right) \cdot {hpr} \cdot \left( {pH_st} - {pH_lu} \right)}}{{{R} \cdot {T}}}}} \\
        {K_eqcytb6f} &= e^{{\frac{{-\left( \left( 2 \cdot {F} \cdot {E_PQ} - 2 \cdot \mathrm{{ln}}\left( 10 \right) \cdot {R} \cdot {T} \cdot {pH_lu} \right) - 2 \cdot {F} \cdot {E_PC} + 2 \cdot \mathrm{{ln}}\left( 10 \right) \cdot {R} \cdot {T} \cdot \left( {pH_st} - {pH_lu} \right) \right)}}{{{R} \cdot {T}}}}} \\
        {H_st} &= 4 \times 10^3 \cdot 10^{pH_st}
    \end{{align}}
```

</details>

                     """)

mdFile.new_header(3, 'Reaction Rates')

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
    \begin{{align}}
        {v_PSII} &= {k_P} \cdot 0.5 \cdot {B_1} \\
        {v_PQ} &= \left( \frac{{{k_Cytb6f} \cdot {pfd} \cdot {K_eqcytb6f}}}{{{K_eqcytb6f} + 1}} + {k_PTOX} \right) \cdot {PQH_2} - \frac{{{k_Cytb6f} \cdot {pfd}}}{{{K_eqcytb6f} + 1}} \cdot {PQ} \\
        {v_ATPsynth} &= {ATPase} \cdot {k_ATPsynth} \cdot \left( {AP_tot} - {ATP} - \frac{{{ATP}}}{{{K_eqATPsynthase}}} \right) \\
        {v_ATPact} &= {k_ActATPase} \cdot {pfd} \cdot {ATPase_inac} - {k_DeactATPase} \cdot \left( 1 - {pfd} \right) \cdot {ATPase} \\
        {v_Leak} &= {k_leak} \cdot \left( {H} - {H_st} \right) \\
        {v_ATPcons} &= {k_ATPconsum} \cdot {ATP} \\
        {v_Xcyc} &= {k_DV} \cdot \frac{{{H}^{{{nhx}}}}}{{{H}^{{{nhx}}} + \left( 4 \times 10^3 \cdot 10^{K_pHSat} \right)^{{{nhx}}}}} \cdot {Vx} - {k_EZ} \cdot \left( {X_tot} - {Vx} \right) \\
        {v_PsbSP} &= {k_prot} \cdot \frac{{{H}^{{{nhl}}}}}{{{H}^{{{nhl}}} + \left( 4 \times 10^3 \cdot 10^{K_pHSatLHC} \right)^{{{nhl}}}}} \cdot {PsbS} - {k_deprot} \cdot {PsbSP}
    \end{{align}}
```

</details>

                     """)

mdFile.create_md_file()
