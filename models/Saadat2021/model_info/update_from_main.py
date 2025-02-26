import pandas as pd
from pathlib import Path

def update_from_main_gloss(
    main_gloss_path,
    gloss_path,
    model_title,
    add_to_main = False,
):

    main_gloss = pd.read_csv(main_gloss_path, keep_default_na=False, dtype={'Glossary ID': 'Int64'})
    gloss = pd.read_csv(gloss_path, keep_default_na=False, converters={'Glossary ID': lambda i: int(i) if i != '' else ''})

    gloss_ids = gloss['Glossary ID']

    main_to_gloss_col_match = [i for i in main_gloss.columns if i in gloss.columns]

    for index, gloss_id in gloss_ids.items():
        main_ids = main_gloss['Glossary ID']

        if gloss_id == '':
            if add_to_main:
                try:
                    new_id = max(main_ids) + 1
                except:
                    new_id = 1

                gloss.loc[index, 'Glossary ID'] = new_id

                main_gloss_dic = {}

                for col_name in main_gloss.columns:
                    if col_name in gloss.columns:
                        new_val = gloss.loc[gloss['Glossary ID'] == new_id, col_name].values[0]

                    elif col_name == 'Reference':
                        new_val = f'{model_title}'

                    main_gloss_dic[col_name] = [new_val]

                new_df = pd.DataFrame(main_gloss_dic)

                main_gloss = pd.concat([main_gloss, new_df], join='inner')

        else:
            for i in main_to_gloss_col_match:
                new_val = main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, i].values[0]
                gloss.loc[index, i] = new_val

            main_refs = main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, 'Reference'].values[0]

            if model_title not in main_refs:
                main_refs += f', {model_title}'

            main_gloss.loc[main_gloss['Glossary ID'] == gloss_id, 'Reference'] = main_refs

    gloss.to_csv(gloss_path, na_rep = '', index=False)
    if add_to_main:
        inp = input('Are you sure you want to update the main gloss? y/[n] > ')
        if inp.upper() in ['Y', 'YES']:
            print('Main Gloss CHnaged')
            main_gloss.to_csv(main_gloss_path, na_rep = '', index=False)

    return

update_from_main_gloss(
        main_gloss_path=Path(__file__).parents[3] / 'Templates' / 'comps_glossary.csv',
        gloss_path=Path(__file__).parent / 'comps.csv',
        add_to_main=False,
        model_title='Saadat2021'
    )

update_from_main_gloss(
        main_gloss_path=Path(__file__).parents[3] / 'Templates' / 'comps_glossary.csv',
        gloss_path=Path(__file__).parent / 'derived_comps.csv',
        add_to_main=False,
        model_title='Saadat2021'
    )

update_from_main_gloss(
        main_gloss_path=Path(__file__).parents[3] / 'Templates' / 'rates_glossary.csv',
        gloss_path=Path(__file__).parent / 'rates.csv',
        add_to_main=False,
        model_title='Saadat2021'
    )
