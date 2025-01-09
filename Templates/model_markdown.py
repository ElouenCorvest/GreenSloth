from mdutils.mdutils import MdUtils
from Templates.utils.glossary import *
from pathlib import Path

import os

print(os.path.realpath(__file__))

model_title = 'Ebenhoeh2011'
model_doi = 'https://doi.org/10.1016/j.biosystems.2010.10.011'
comp_glossary_path = Path('Templates/comp_glossary.csv')

model_compounds_dict = {
    'A1': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{A}_1$',
            glossary_path = comp_glossary_path
        ),
    'A2': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{A}_2$',
            glossary_path = comp_glossary_path
        ),
    'PQ_ox': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{P}$',
            glossary_path = comp_glossary_path
        ),
    'H_lu': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{H}$',
            glossary_path = comp_glossary_path
        ),
    'N': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{N}$',
            glossary_path = comp_glossary_path
        ),
    'ATP_st': extract_from_glossary(  # noqa: F405
            paper_abbr = r'$\mathrm{T}$',
            glossary_path = comp_glossary_path
        ),
}

compound_table_list_header = [
    'Name',
    'Paper Abbreviation',
    'Abbreviation Here',
    'Python Variable'
]

compound_table_list = [i for i in compound_table_list_header]

for var, comp_dict in model_compounds_dict.items():
    for column_name in compound_table_list_header:
        compound_table_list.append(comp_dict[column_name])

rates_glossary_path = Path('Templates/rates_glossary.csv')

rates_glossary = {
    'v1': extract_from_glossary(
        paper_abbr = r'$v_1$',
        glossary_path = rates_glossary_path
    ),
    'v2': extract_from_glossary(
        paper_abbr = r'$v_2$',
        glossary_path = rates_glossary_path
    ),
    'v3': extract_from_glossary(
        paper_abbr = r'$v_3$',
        glossary_path = rates_glossary_path
    ),
    'v4': extract_from_glossary(
        paper_abbr = r'$v_4$',
        glossary_path = rates_glossary_path
    ),
    'v4': extract_from_glossary(
        paper_abbr = r'$v_4$',
        glossary_path = rates_glossary_path
    ),
    'v5': extract_from_glossary(
        paper_abbr = r'$v_5$',
        glossary_path = rates_glossary_path
    ),
    'v6': extract_from_glossary(
        paper_abbr = r'$v_6$',
        glossary_path = rates_glossary_path
    ),
    'v7': extract_from_glossary(
        paper_abbr = r'$v_7$',
        glossary_path = rates_glossary_path
    ),
    'v8': extract_from_glossary(
        paper_abbr = r'$v_8$',
        glossary_path = rates_glossary_path
    ),
    'v9': extract_from_glossary(
        paper_abbr = r'$v_9$',
        glossary_path = rates_glossary_path
    ),
}

rates_table_list_header = [
    'Short Description',
    'Paper Abbreviation',
    'Abbreviation Here',
    'Python Variable'
]

rates_table_list = [i for i in rates_table_list_header]

for var, rates_dict in rates_glossary.items():
    for column_name in rates_table_list_header:
        rates_table_list.append(rates_dict[column_name])

mdFile = MdUtils(file_name='./models/Ebenhoeh2011/README_2.md')

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f'[here]({model_doi})')

mdFile.new_header(2, 'Installation')

mdFile.new_header(2, 'Summary')

mdFile.new_header(3, 'Compounds')

mdFile.new_table(columns = len(compound_table_list_header), rows = int(len(compound_table_list) / len(compound_table_list_header)), text = compound_table_list)

mdFile.new_header(3, 'Reaction Rates')

mdFile.new_table(columns = len(rates_table_list_header), rows = int(len(rates_table_list) / len(rates_table_list_header)), text = rates_table_list)

mdFile.create_md_file()