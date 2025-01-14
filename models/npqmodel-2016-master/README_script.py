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
model_info = os.path.dirname(__file__) + '/model_info'

comps_table = pd.read_csv(model_info + '/comps.csv', sep = ';')

comps_table_tolist = [comps_table.columns.values.tolist()] + comps_table.values.tolist()

comps_table_list = []

for lst in comps_table_tolist:
    for i in lst:
        comps_table_list.append(i)

# conserved_quantities = {
#     'D': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{D}$',
#             glossary_path = comp_glossary_path
#         ),
#     'X': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{X}$',
#             glossary_path = comp_glossary_path
#         ),
#     'Atot': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{A}^{\mathrm{tot}}$',
#             glossary_path = comp_glossary_path
#         ),
# }

# derived_comps = {
#     'A3': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{A}_3$',
#             glossary_path = comp_glossary_path
#         ),
#     'Q': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{Q}$',
#             glossary_path = comp_glossary_path
#         ),
#     'S': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{S}$',
#             glossary_path = comp_glossary_path
#         ),
#     'N0': extract_from_glossary(  # noqa: F405
#             paper_abbr = r'$\mathrm{N}^0$',
#             glossary_path = comp_glossary_path
#         ),
# }

# rates_glossary_path = Path('Templates/rates_glossary.csv')

# rates_glossary = {
#     'v1': extract_from_glossary(
#         paper_abbr = r'$v_1$',
#         glossary_path = rates_glossary_path
#     ),
#     'v2': extract_from_glossary(
#         paper_abbr = r'$v_2$',
#         glossary_path = rates_glossary_path
#     ),
#     'v3': extract_from_glossary(
#         paper_abbr = r'$v_3$',
#         glossary_path = rates_glossary_path
#     ),
#     'v4': extract_from_glossary(
#         paper_abbr = r'$v_4$',
#         glossary_path = rates_glossary_path
#     ),
#     'v5': extract_from_glossary(
#         paper_abbr = r'$v_5$',
#         glossary_path = rates_glossary_path
#     ),
#     'v6': extract_from_glossary(
#         paper_abbr = r'$v_6$',
#         glossary_path = rates_glossary_path
#     ),
#     'v7': extract_from_glossary(
#         paper_abbr = r'$v_7$',
#         glossary_path = rates_glossary_path
#     ),
#     'v8': extract_from_glossary(
#         paper_abbr = r'$v_8$',
#         glossary_path = rates_glossary_path
#     ),
#     'v9': extract_from_glossary(
#         paper_abbr = r'$v_9$',
#         glossary_path = rates_glossary_path
#     ),
# }

###### Glossary generated tables ######

# compound_table_list_header = [
#     'Name',
#     'Paper Abbreviation',
#     'Abbreviation Here',
#     'Python Variable'
# ]

# compound_table_list = [i for i in compound_table_list_header]

# for var, comp_dict in ode_dict.items():
#     for column_name in compound_table_list_header:
#         compound_table_list.append(comp_dict[column_name])
        
# conserved_quantities_list_header = [
#     'Name',
#     'Paper Abbreviation',
#     'Abbreviation Here',
#     'Python Variable'
# ]

# conserved_quantities_list = [i for i in conserved_quantities_list_header]

# for var, comp_dict in conserved_quantities.items():
#     for column_name in conserved_quantities_list_header:
#         conserved_quantities_list.append(comp_dict[column_name])
        
# derived_comps_list_header = [
#     'Name',
#     'Paper Abbreviation',
#     'Abbreviation Here',
#     'Python Variable'
# ]

# derived_comps_list = [i for i in derived_comps_list_header]

# for var, comp_dict in derived_comps.items():
#     for column_name in derived_comps_list_header:
#         derived_comps_list.append(comp_dict[column_name])

# rates_table_list_header = [
#     'Short Description',
#     'Paper Abbreviation',
#     'Abbreviation Here',
#     'Python Variable'
# ]

# rates_table_list = [i for i in rates_table_list_header]

# for var, rates_dict in rates_glossary.items():
#     for column_name in rates_table_list_header:
#         rates_table_list.append(rates_dict[column_name])

###### Variables for ease of access ######

def remove_math(
    df,
    query_result,
    query_column = 'Python Var',
    answer_column = 'Common Abbr.'
):
    res = df.loc[df[query_column] == query_result, answer_column].iloc[0]
    
    for i in range(df.loc[df[query_column] == query_result, answer_column].iloc[0].count('$')):
        res = res.replace('$', '')
        
    return res



PQH_2 = remove_math(comps_table, 'PQH_2')
ATP = remove_math(comps_table, 'ATP_st')
H = remove_math(comps_table, 'H_lu')
PsbS = remove_math(comps_table, 'psbS')
Vx = remove_math(comps_table, 'Vx')
ATPase = remove_math(comps_table, 'ATPase_ac')

# D = remove_math_mode(conserved_quantities, 'D')
# X = remove_math_mode(conserved_quantities, 'X')
# Atot = remove_math_mode(conserved_quantities, 'Atot')

# A3 = remove_math_mode(derived_comps, 'A3')
# Q = remove_math_mode(derived_comps, 'Q')
# S = remove_math_mode(derived_comps, 'S')
# N0 = remove_math_mode(derived_comps, 'N0')

# v1 = remove_math_mode(rates_glossary, 'v1')
# v2 = remove_math_mode(rates_glossary, 'v2')
# v3 = remove_math_mode(rates_glossary, 'v3')
# v4 = remove_math_mode(rates_glossary, 'v4')
# v5 = remove_math_mode(rates_glossary, 'v5')
# v6 = remove_math_mode(rates_glossary, 'v6')
# v7 = remove_math_mode(rates_glossary, 'v7')
# v8 = remove_math_mode(rates_glossary, 'v8')
# v9 = remove_math_mode(rates_glossary, 'v9')

###### Making README File ######

mdFile = MdUtils(file_name=f'{os.path.dirname(__file__)}/README.md')

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f'[here]({model_doi})')

mdFile.new_header(2, 'Installation')

mdFile.new_header(2, 'Summary')

mdFile.new_header(3, 'Compounds')

mdFile.new_header(4, 'Part of ODE system')

mdFile.new_table(columns = len(comps_table.columns), rows = len(comps_table_tolist), text = comps_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Open me for the ODE system!</summary>

# $$    
#     \begin{{align}}
#         {ode(PQH_2)} &= {v_} - {v1} \\
#         {ode(A2)} &= {v1} - {v2} \\
#         {ode(P)} &= {v3} - {v4} \\
#         {ode(H)} &= b_{{{H}}} \cdot \left( 2 \cdot {v2} + {v4} - \frac{{14}}{{3}} \cdot {v5} - {v8} \right) \\
#         {ode(N)} &= {v6} - {v7}  \\
#         {ode(T)} &= {v5} - {v9}
#     \end{{align}}
# $$

# </details>

#                      """)

# mdFile.new_header(4, 'Conserved quantities')

# mdFile.new_table(columns = len(conserved_quantities_list_header), rows = int(len(conserved_quantities_list) / len(conserved_quantities_list_header)), text = conserved_quantities_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Open me for the calculations of the conserved quantities!</summary>

# $$    
#     \begin{{align}}
#         {D} &= {A1} + {A2} + {A3} \\
#         {X} &= {P} + {Q} \\
#         {Atot} &= {S} + {T} \\
#         1 &= {N0} + {N}
#     \end{{align}}
# $$

# </details>

#                      """)

# mdFile.new_header(4, 'Derived from conserved quantities')

# mdFile.new_table(columns = len(derived_comps_list_header), rows = int(len(derived_comps_list) / len(derived_comps_list_header)), text = derived_comps_list)

# mdFile.new_header(3, 'Parameters')



# mdFile.new_header(3, 'Reaction Rates')

# mdFile.new_table(columns = len(rates_table_list_header), rows = int(len(rates_table_list) / len(rates_table_list_header)), text = rates_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Open me for the rates!</summary>

# $$    
#     \begin{{align}}
#         {v1} &= {N0} \cdot k_1 \cdot {A1} \\
#         {v2} &= k_2 \cdot {A2} \\
#         {v3} &= k⁺_3 \cdot {A3} \cdot {P} - k⁻_3 \cdot {A1} \cdot {Q} \\
#         {v4} &= k_4 \cdot {Q} \\
#         {v5} &= k_5 \cdot \left({Atot} - {T} \cdot \left(1 + \frac{{1}}{{K_{{eq}}({H})}}\right)\right)  \\ \notag
#         \mathrm{{with}} \ K_{{\mathrm{{eq}}}}({H}) &= \sqrt[RT]{{e^{{\Delta G^0 - \mathrm{{ln}}\ 10 \cdot \Delta \mathrm{{pH}} \cdot \frac{{14}}{{3}} \cdot RT}}}}\\
#         {v6} &= k6 \cdot {N0} \cdot \frac{{{H}^n}}{{{H}^n \cdot K_{{Q}}^n}} \\
#         {v7} &= k7 \cdot {N} \\
#         {v8} &= k8 \cdot \left( {H} - \mathrm{{H}}_{{\mathrm{{st}}}} \right) \\
#         {v9} &= k9 \cdot {T}
#     \end{{align}}
# $$

# </details>
#                      """)

mdFile.create_md_file()