from mdutils.mdutils import MdUtils  # noqa: E402
from glossary_utils.glossary import update_from_main_gloss, gloss_fromCSV, write_python_from_gloss, write_odes_from_model, extract_params_from_model
from pathlib import Path
import pandas as pd
from models import get_model

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

model_title = 'Saadat2021'
model_doi = 'https://doi.org/10.3389/fpls.2021.750580'

###### Glossaries ######

cite_dict = dict()

model_info = Path(__file__).parent / 'model_info'
main_gloss = Path(__file__).parents[2] / 'Templates'

update_from_main_gloss(
    main_gloss_path=main_gloss / 'comp_glossary.csv',
    gloss_path=model_info / 'comps.csv',
    add_to_main=True,
    model_title=model_title
)

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / 'comps.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=Path(__file__).parent / 'model_info/comps.txt',
    gloss=comps_table,
    var_list_name='comps_table'
)

update_from_main_gloss(
    main_gloss_path=main_gloss / 'comp_glossary.csv',
    gloss_path=model_info / 'derived_comps.csv',
    add_to_main=True,
    model_title=model_title
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(
    path=model_info / 'derived_comps.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=Path(__file__).parent / 'model_info/derived_comps.txt',
    gloss=derived_comps_table,
    var_list_name='derived_comps_table'
)

update_from_main_gloss(
    main_gloss_path=main_gloss / 'rates_glossary.csv',
    gloss_path=model_info / 'rates.csv',
    add_to_main=True,
    model_title=model_title
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / 'rates.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=Path(__file__).parent / 'model_info/rates.txt',
    gloss=rates_table,
    var_list_name='rates_table'
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / 'params.csv',
    cite_dict=cite_dict
)

# extract_params_from_model(
#     model=get_model(),
#     path_to_write=model_info / 'test.csv'
# )



derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info / 'derived_params.csv')

write_odes_from_model(
    path_to_write=model_info / 'odes.txt',
    model=get_model(),
)

###### Variables for ease of access ######

def remove_math(
    df,
    query_result,
    query_column = 'Paper Abbr.',
    answer_column = 'Common Abbr.'
):
    res = df[df[query_column] == query_result][answer_column].values[0]

    for i in range(df.loc[df[query_column] == query_result, answer_column].iloc[0].count('$')):
        res = res.replace('$', '')

    return res

# -- Compounds --

PQ = remove_math(comps_table, r'$\mathrm{PQ}_\mathrm{ox}$')
PC_ox = remove_math(comps_table, r'$\mathrm{PC}_\mathrm{ox}$')
Fd_ox = remove_math(comps_table, r'$\mathrm{Fd}_\mathrm{ox}$')
ATP_st = remove_math(comps_table, r'$\mathrm{ATP}$')
NADPH_st = remove_math(comps_table, r'$\mathrm{NADPH}$')
H_lu = remove_math(comps_table, r'$\mathrm{H}^+$')
LHC = remove_math(comps_table, r'$\mathrm{LHC}$')
psbS = remove_math(comps_table, r'$\mathrm{Psbs}$')
Vx = remove_math(comps_table, r'$\mathrm{Vx}$')
PGA = remove_math(comps_table, r'$\mathrm{PGA}$')
BPGA = remove_math(comps_table, r'$\mathrm{BPGA}$')
GAP = remove_math(comps_table, r'$\mathrm{GAP}$')
DHAP = remove_math(comps_table, r'$\mathrm{DHAP}$')
FBP = remove_math(comps_table, r'$\mathrm{FBP}$')
F6P = remove_math(comps_table, r'$\mathrm{F6P}$')
G6P = remove_math(comps_table, r'$\mathrm{G6P}$')
G1P = remove_math(comps_table, r'$\mathrm{G1P}$')
SBP = remove_math(comps_table, r'$\mathrm{SBP}$')
S7P = remove_math(comps_table, r'$\mathrm{S7P}$')
E4P = remove_math(comps_table, r'$\mathrm{E4P}$')
X5P = remove_math(comps_table, r'$\mathrm{X5P}$')
R5P = remove_math(comps_table, r'$\mathrm{R5P}$')
RUBP = remove_math(comps_table, r'$\mathrm{RUBP}$')
RU5P = remove_math(comps_table, r'$\mathrm{RU5P}$')
MDA = remove_math(comps_table, r'$\mathrm{MDA}$')
H2O2 = remove_math(comps_table, r'$\mathrm{H_2O_2}$')
DHA = remove_math(comps_table, r'$\mathrm{DHA}$')
GSSG = remove_math(comps_table, r'$\mathrm{GSSG}$')
Trx_ox = remove_math(comps_table, r'$\mathrm{Trx_{ox}}$')
E_CBB_inactive = remove_math(comps_table, r'$\mathrm{E}_\mathrm{inactive}$')

# -- Derived Compounds --

PQH_2 = remove_math(derived_comps_table, r'$\mathrm{PQH}_2$')
PC_red = remove_math(derived_comps_table, r'$\mathrm{PC}^-$')
Fd_red = remove_math(derived_comps_table, r'$\mathrm{Fd}^-$')
ADP_st = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
NADP = remove_math(derived_comps_table, r'$\mathrm{NADP}^+$')
Pi_st = remove_math(derived_comps_table, r'$\mathrm{P}_\mathrm{i}$')
IF_3P = remove_math(derived_comps_table, r'$\mathrm{N}$')
Zx = remove_math(derived_comps_table, r'$\mathrm{Zx}$')
PsbSP = remove_math(derived_comps_table, r'$\mathrm{PsbS^P}$')

# -- Rates --

v_PSII = remove_math(rates_table, r'$v_{\mathrm{PSII}}$')
v_b6f = remove_math(rates_table, r'$v_{\mathrm{b6f}}$')
v_FNR = remove_math(rates_table, r'$v_{\mathrm{FNR}}$')
v_FQR = remove_math(rates_table, r'$v_{\mathrm{FQR}}$')
v_ATPsynth = remove_math(rates_table, r'$v_{\mathrm{ATPsynthase}}$')
v_Leak = remove_math(rates_table, r'$v_{\mathrm{Leak}}$')
v_PQ = remove_math(rates_table, r'$v_{\mathrm{PTOX}}$')
v_NDH = remove_math(rates_table, r'$v_{\mathrm{NDH}}$')
v_Cyc = remove_math(rates_table, r'$v_{\mathrm{Cyc}}$')
v_St21 = remove_math(rates_table, r'$v_{\mathrm{St12}}$')
v_St12 = remove_math(rates_table, r'$v_{\mathrm{St21}}$')
v_Deepox = remove_math(rates_table, r'$v_{\mathrm{Deepox}}$')
v_Epox = remove_math(rates_table, r'$v_{\mathrm{Epox}}$')
v_PsbSP = remove_math(rates_table, r'$v_{\mathrm{LHCprotonation}}$')
v_psbSD = remove_math(rates_table, r'$v_{\mathrm{LHCdeprotonation}}$')
v_rubisco = remove_math(rates_table, r'$v_{\mathrm{RuBisCo}}$')
v_FBPase = remove_math(rates_table, r'$v_{\mathrm{FBPase}}$')
v_SBPase = remove_math(rates_table, r'$v_9$')
v_PRKase = remove_math(rates_table, r'$v_{13}$')
v_pga_ex = remove_math(rates_table, r'$v_{pga}$')
v_dhap_ex = remove_math(rates_table, r'$v_{DHAP}$')
v_gap_ex = remove_math(rates_table, r'$v_{gap}$')
v_starch = remove_math(rates_table, r'$v_{\mathrm{Starch}}$')
v_PGK1ase = remove_math(rates_table, r'$v_{\mathrm{PGA\_kinase}}$')
v_BPGAdehynase = remove_math(rates_table, r'$v_{\mathrm{BPGA\_dehydrogenase}}$')
v_TPIase = remove_math(rates_table, r'$v_{\mathrm{TPI}}$')
v_Aldolase_FBP = remove_math(rates_table, r'$v_{\mathrm{Aldolase}}$')
v_TKase_E4P = remove_math(rates_table, r'$v_{\mathrm{F6P\_ Transketolase}}$')
v_Aldolase_SBP = remove_math(rates_table, r'$v_{8}$')
v_TKase_R5P = remove_math(rates_table, r'$v_{10}$')
v_Rpiase = remove_math(rates_table, r'$v_{11}$')
v_RPEase = remove_math(rates_table, r'$v_{12}$')
v_PGIase = remove_math(rates_table, r'$v_{G6P\_ isomerase}$')
v_PGMase = remove_math(rates_table, r'$v_{\mathrm{Phosphoglucomutase}}$')
v_PSI = remove_math(rates_table, r'$v_{\mathrm{PSI}}$')
v_ATPcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ ATP}}$')
v_NADPHcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ NADPH}}$')
v_Fdred = remove_math(rates_table, r'$v_{\mathrm{Fd,\ red}}$')
v_FdTrReduc = remove_math(rates_table, r'$v_{\mathrm{FdTrReductase}}$')
v_MDAreduc = remove_math(rates_table, r'$v_{\mathrm{MDAreduct}}$')
v_GR = remove_math(rates_table, r'$v_{\mathrm{GR}}$')
v_RuBisCO = remove_math(rates_table, r'$v_{\mathrm{RuBisCO}}$')
v_APXase = remove_math(rates_table, r'$v_{\mathrm{Ascorbate}}$')
v_Mehler = remove_math(rates_table, r'$v_{\mathrm{Mehler}}$')
v_DHAR = remove_math(rates_table, r'$v_{\mathrm{DHAR}}$')
v_3ASC = remove_math(rates_table, r'$v_{\mathrm{3ASC}}$')
v_Eact = remove_math(rates_table, r'$v_{\mathrm{Eact}}$')
v_Einact = remove_math(rates_table, r'$v_{\mathrm{Einact}}$')

###### Making README File ######

mdFile = MdUtils(file_name=f'{os.path.dirname(__file__)}/README.md')

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

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
      {ode(PQ)} &= -{v_PSII} + {v_PQ} - {v_NDH} + {v_b6f} - {v_Cyc} \\
      {ode(H_lu)} &= 0.02 \cdot {v_PSII} + 0.04 \cdot {v_b6f} - 0.0{v_Leak} - 0.04666666666666667 \cdot {v_ATPsynth} \\
      {ode(Fd_ox)} &= 2 \cdot {v_Cyc} + 2 \cdot {v_FNR} - {v_Fdred} + {v_FdTrReduc} \\
      {ode(PC_ox)} &= -2 \cdot {v_b6f} + {v_PSI} \\
      {ode(NADPH_st)} &= 0.032 \cdot {v_FNR} - {v_BPGAdehynase} - {v_MDAreduc} - {v_GR} - {v_NADPHcons} \\
      {ode(LHC)} &= -{v_St21} + {v_St12} \\
      {ode(ATP_st)} &= 0.032 \cdot {v_ATPsynth} - {v_PGK1ase} - {v_PRKase} - {v_starch} - {v_ATPcons} \\
      {ode(Vx)} &= -{v_Deepox} + {v_Epox} \\
      {ode(psbS)} &= -{v_PsbSP} + {v_psbSD} \\
      {ode(RUBP)} &= -{v_RuBisCO} + {v_PRKase} \\
      {ode(PGA)} &= 2 \cdot {v_RuBisCO} - {v_PGK1ase} - {v_pga_ex} \\
      {ode(BPGA)} &= {v_PGK1ase} - {v_BPGAdehynase} \\
      {ode(GAP)} &= {v_BPGAdehynase} - {v_TPIase} - {v_Aldolase_FBP} - {v_TKase_E4P} - {v_TKase_R5P} - {v_gap_ex} \\
      {ode(DHAP)} &= {v_TPIase} - {v_Aldolase_FBP} - {v_Aldolase_SBP} - {v_dhap_ex} \\
      {ode(FBP)} &= {v_Aldolase_FBP} - {v_FBPase} \\
      {ode(F6P)} &= {v_FBPase} - {v_TKase_E4P} - {v_PGIase} \\
      {ode(X5P)} &= {v_TKase_E4P} + {v_TKase_R5P} - {v_RPEase} \\
      {ode(E4P)} &= {v_TKase_E4P} - {v_Aldolase_SBP} \\
      {ode(SBP)} &= {v_Aldolase_SBP} - {v_SBPase} \\
      {ode(S7P)} &= {v_SBPase} - {v_TKase_R5P} \\
      {ode(R5P)} &= {v_TKase_R5P} - {v_Rpiase} \\
      {ode(RU5P)} &= {v_Rpiase} + {v_RPEase} - {v_PRKase} \\
      {ode(G6P)} &= {v_PGIase} - {v_PGMase} \\
      {ode(G1P)} &= {v_PGMase} - {v_starch} \\
      {ode(H2O2)} &= -{v_APXase} + 0.032 \cdot {v_Mehler} \\
      {ode(MDA)} &= 2 \cdot {v_APXase} - 2 \cdot {v_MDAreduc} - 2 \cdot {v_3ASC} \\
      {ode(GSSG)} &= -{v_GR} + {v_DHAR} \\
      {ode(DHA)} &= -{v_DHAR} + {v_3ASC} \\
      {ode(Trx_ox)} &= -{v_FdTrReduc} + 5 \cdot {v_Eact} \\
      {ode(E_CBB_inactive)} &= -5 \cdot {v_Eact} + 5 \cdot {v_Einact} \\
   \end{{align}}
```

</details>
                     """)

mdFile.new_header(4, 'Conserved quantities')

# mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Open me for the calculations of the conserved quantities!</summary>

# ```math
#     \begin{{align}}
#         {PSII_tot} &= {B_0} + {B_1} + {B_2} + {B_3} \\
#         {PQ_tot} &= {PQ} + {PQH_2} \\
#         {AP_tot} &= {ATP} + {ADP} \\
#         {PsbS_tot} &= {PsbS} + {PsbSP} \\
#         {X_tot} &= {Vx} + {Zx} \\
#         {pH_lu} &= - \mathrm{{log}}_{{10}}\left( {H} \cdot 2.5 \times 10^{{-4}} \right)
#     \end{{align}}
# ```

# <details>
# <summary>Calculation of Quencher</summary>

# ```math
#     \begin{{align}}
#         Q &= {gamma_0} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {PsbS} + {gamma_1} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {PsbSP} + {gamma_2} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbSP} + {gamma_3} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbS} \\
#     \end{{align}}
# ```

# </details>

# <details>
# <summary>Quasi steady-state approximation to calculate the rate of PSII</summary>

# ```math
#     \begin{{align}}
#         0 &= - \left( {pfd} + \frac{{{k_PQred}}}{{{K_eqQAPQ}}} \cdot {PQ} \right) \cdot {B_0} + \left( {k_H} \cdot Q + {k_F} \right) \cdot {B_1} + {k_PQred} \cdot {PQH_2} \cdot {B_3} \\
#         0 &= {pfd} \cdot {B_0} - \left( {k_H} \cdot Q + {k_F} + {k_P} \right) \cdot {B_1} \\
#         0 &= {pfd} \cdot {B_2} - \left( {k_H} \cdot Q + {k_F} \right) \cdot {B_3}
#     \end{{align}}
# ```

# </details>

# </details>

#                      """)

mdFile.new_header(3, 'Parameters')

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, 'Derived Parameters')

# mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Equations of derived parameters</summary>

# ```math
#     \begin{{align}}
#         {K_eqQAPQ} &= e^{{\frac{{-\left( -2 \cdot {E_QA} \cdot {F} - 2 \cdot {E_PQ} \cdot {F} + 2 \cdot {pH_st} \cdot \mathrm{{ln}}(10) \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}}}} \\
#         {K_eqATPsynthase} &= {Pi} \cdot e^{{\frac{{-{DG_ATP} - \mathrm{{ln}}\left( 10 \right) \cdot {hpr} \cdot \left( {pH_st} - {pH_lu} \right)}}{{{R} \cdot {T}}}}} \\
#         {K_eqcytb6f} &= e^{{\frac{{-\left( \left( 2 \cdot {F} \cdot {E_PQ} - 2 \cdot \mathrm{{ln}}\left( 10 \right) \cdot {R} \cdot {T} \cdot {pH_lu} \right) - 2 \cdot {F} \cdot {E_PC} + 2 \cdot \mathrm{{ln}}\left( 10 \right) \cdot {R} \cdot {T} \cdot \left( {pH_st} - {pH_lu} \right) \right)}}{{{R} \cdot {T}}}}} \\
#         {H_st} &= 4 \times 10^3 \cdot 10^{{{pH_st}}}
#     \end{{align}}
# ```

# </details>

#                      """)

mdFile.new_header(3, 'Reaction Rates')

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Rate equations</summary>

# ```math
#     \begin{{align}}
#         {v_PSII} &= {k_P} \cdot 0.5 \cdot {B_1} \\
#         {v_PQ} &= \left( \frac{{{k_Cytb6f} \cdot {pfd} \cdot {K_eqcytb6f}}}{{{K_eqcytb6f} + 1}} + {k_PTOX} \right) \cdot {PQH_2} - \frac{{{k_Cytb6f} \cdot {pfd}}}{{{K_eqcytb6f} + 1}} \cdot {PQ} \\
#         {v_ATPsynth} &= {ATPase} \cdot {k_ATPsynth} \cdot \left( {AP_tot} - {ATP} - \frac{{{ATP}}}{{{K_eqATPsynthase}}} \right) \\
#         {v_ATPact} &= {k_ActATPase} \cdot {pfd} \cdot {ATPase_inac} - {k_DeactATPase} \cdot \left( 1 - {pfd} \right) \cdot {ATPase} \\
#         {v_Leak} &= {k_leak} \cdot \left( {H} - {H_st} \right) \\
#         {v_ATPcons} &= {k_ATPconsum} \cdot {ATP} \\
#         {v_Xcyc} &= {k_DV} \cdot \frac{{{H}^{{{nhx}}}}}{{{H}^{{{nhx}}} + \left( 4 \times 10^3 \cdot 10^{K_pHSat} \right)^{{{nhx}}}}} \cdot {Vx} - {k_EZ} \cdot \left( {X_tot} - {Vx} \right) \\
#         {v_PsbSP} &= {k_prot} \cdot \frac{{{H}^{{{nhl}}}}}{{{H}^{{{nhl}}} + \left( 4 \times 10^3 \cdot 10^{K_pHSatLHC} \right)^{{{nhl}}}}} \cdot {PsbS} - {k_deprot} \cdot {PsbSP}
#     \end{{align}}
# ```

# </details>

#                      """)

mdFile.new_header(3, 'Tags')

# mdFile.write(rf'''

# ```mermaid
# flowchart LR;
#     H("$${H}$$") -->|"$${v_PSII}$$"| P("$${PQH_2}$$");
#     P -->|"$${v_PQ}$$"| H;
#     H -->|"$${v_ATPsynth}$$"| A("$${ATP}$$");
#     A -->|"$${v_ATPcons}$$"| empty:::hidden;
#     H -->|"$${v_Leak}$$"| empty1:::hidden;
#     PS("$${PsbS}$$") -->|"$${v_PsbSP}$$"| e1:::hidden;
#     Vx("$${Vx}$$") -->|"$${v_Xcyc}$$"| e2:::hidden;
#     e3:::hidden -->|"$${v_ATPact}$$"| ATP("$${ATPase}$$")


#     classDef hidden display: none;
# ```

#              ''')

mdFile.create_md_file()
