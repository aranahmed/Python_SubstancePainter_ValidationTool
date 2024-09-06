"""
Module to import data from spreadsheet file.

Extension : 
    - read excel document from given path
    - convert the Excel data to JSON
"""
import pandas as pd
import json
import os

def save_excel_to_json():

    script_dir = os.path.dirname(os.path.abspath(__file__))

    excel_path = os.path.join(script_dir, 'subp_data.xlsx')
    # Load the spreadsheet
    df = pd.read_excel(excel_path, engine='openpyxl')
    # df = pd.read_excel(url, engine='openpyxl')

    #Drop rows where elements are NaN
    df = df.dropna(how='all')

    #Drop columns where elements are NaN
    df = df.dropna(how='all', axis=1)

    print(df)

    # Convert to JSON
    data = df.to_dict(orient='records')

    # Save to a JSON file
    with open('texture_set_name_data.json', 'w') as f:
        json.dump(data, f)

save_excel_to_json()