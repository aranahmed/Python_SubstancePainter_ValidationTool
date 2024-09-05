"""
Module to import data from spreadsheet file.

Extension : 
    - read excel document from given path

"""
import pandas as pd
import json

# url = "https://docs.google.com/spreadsheets/d/1wT5ecdxHLwECxJSBGp27qBcw6God1qa0/edit?usp=sharing&ouid=107471557719184358220&rtpof=true&sd=true"

# Load the spreadsheet
df = pd.read_excel('/Users/aranazadahmed/Documents/Adobe/Adobe Substance 3D Painter/python/modules/subp_data.xlsx', engine='openpyxl')
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
