import pandas as pd
import os

def df_to_dict(
    df: pd.DataFrame,
    keep_index: bool = False,
):
    if len(df) == 0:
        raise ValueError('The df "{df}" is empty. It cannot be translated to a dict.')
    elif len(df) > 1:
        raise ValueError('The df "{df}" contains more than one row. The dict will not be appropriate.')
    else:
        result_dict = {}
        
        tmp_dict = df.to_dict()
        
        if keep_index:
            return tmp_dict
        else:    
            for key, value in tmp_dict.items():
                result_dict[key] = list(value.values())[0]

            return result_dict
    

def extract_from_glossary(
    paper_abbr: str,
    glossary_path: os.PathLike[str]
):
    glossary_df = pd.read_csv(glossary_path)

    result_dict = {}
    
    cor_row = glossary_df.loc[glossary_df['Paper Abbreviation'] == paper_abbr]
    
    if not cor_row.empty:
        
        result_dict = df_to_dict(cor_row)
        
        return result_dict
    
    else:
        print()
        print(f'"{paper_abbr}" is not found in the glossary')
        add_to_gloss = input('Do you wish to include it in the existing glossary? - Type "Yes" or "No": \n')
        
        if add_to_gloss in ['Yes', 'yes', 'y']:
            
            insert_to_glossary(
                paper_abbr,
                glossary_df,
                glossary_path=glossary_path,
            )
            
            return extract_from_glossary(
                paper_abbr=paper_abbr,
                glossary_path=glossary_path
            )
            
        else:
            
            print('Abbreviation cannot be found in glossary')
            
            return None
        
def insert_to_glossary(
    paper_abbr: str,
    glossary: pd.DataFrame,
    glossary_path: os.PathLike[str],
):
    header = glossary.columns
    
    dict_to_add = {}
    
    for column_name in header:
        
        if column_name == 'Paper Abbreviation':
            tmp_input = paper_abbr
        else:
            tmp_input = input(f'Type in the information that corresponds to the "{column_name}": \n')
            print()
        
        if not (glossary.loc[glossary[column_name] == tmp_input].empty) and 'Reference' not in column_name:
            
            print('We have found an entry corresponding to your input.')
            print()
            print(glossary.loc[glossary[column_name] == tmp_input])
            print()
            override_input = input(f'Do you wish to take these settings and add the new "{paper_abbr}"')
            
            if override_input in ['Yes', 'yes', 'y']:
                dict_to_add = df_to_dict(glossary.loc[glossary[column_name] == tmp_input], keep_index=True)
                
                dict_to_add['Paper Abbreviation'] = paper_abbr
                
                dict_to_add['Reference Paper'] = input('What is the reference of the new glossary entry?: \n')
            
                break
        
        else:
            dict_to_add[column_name] = [tmp_input]
    
    df_to_add = pd.DataFrame.from_dict(dict_to_add)
    df_combined = pd.concat([glossary, df_to_add], ignore_index = True)
    
    df_combined.to_csv(glossary_path, index=False)
    
def change_item(
    glossary_path: os.PathLike[str],
    glossary_column: str,
    old_item: str,
    new_item: str,
):
    glossary_df = pd.read_csv(glossary_path)
    
    glossary_df[[glossary_column]] = glossary_df[[glossary_column]].replace(
        to_replace=old_item,
        value=new_item,
    )
    
    glossary_df.to_csv(glossary_path, index = False)
