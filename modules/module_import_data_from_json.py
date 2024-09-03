"""
This script processes the data taken from a JSON file provided, 
and processes it to dictionaries sorted into the texture naming convention:
    -   asset_type
    -   asset_detail_01
    -   asset_detail_02
    -   max_res

It's in a seperate script to avoid needing to import JSON into main scripts.

If it can't find a JSON file it will take some default data based on original Texture Set Name data

"""
import json
import os

json_path = "/Users/aranazadahmed/Documents/Adobe/Adobe Substance 3D Painter/python/texture_set_name_data.json"

default_data=[
            {"asset_name": "Props", "asset_types": "PROP", "asset_detail_01": "CHR,TBL,LMP,WIN", "asset_detail_02": "S,M,L", "max_res": "1024,1024"},
               {"asset_name": "Weapons", "asset_types": "WPN", "asset_detail_01": "SWD,BOW,RFL,EXP", "asset_detail_02": "COM,RAR,EPC", "max_res": "2048,2048"},
                 {"asset_name": "Characters", "asset_types": "CHAR", "asset_detail_01": "PLR,ENM,CIV", "asset_detail_02": "ML,FL,NB", "max_res": "4096,4096"},
                   {"asset_name": "Shaders", "asset_types": "SHDR", "asset_detail_01": "UNL,LIT", "asset_detail_02": "HRS,LRS", "max_res": "512,512"}
                   ]

loaded_data = default_data  # Start with default data

try:
    if os.path.exists(json_path):
             
        # Load JSON data
        with open(json_path, 'r') as f:
            data = json.load(f)

    else:
        print("JSON not found, using default data")
except Exception as e:
    print(f"Error loading JSON file: {e}, using default data.")


# Iterate through each dictionary in the JSON list
for item in data:
    # Split the 'asset_detail_01' and 'asset_detail_02' values by commas
    item['asset_detail_01'] = item['asset_detail_01'].split(',')
    item['asset_detail_02'] = item['asset_detail_02'].split(',')
    # Split the 'max_res' value by commas or 'x' depending on the format

# Print the modified JSON data
list_of_asset_dicts =[]
for item in data:

    asset_name = item['asset_name']
    asset_type = item['asset_types']
    asset_detail_01 = item['asset_detail_01']
    asset_detail_02 = item['asset_detail_02']
    #asset_max_res = item['max_res']
    width_str, height_str = item['max_res'].split(',')

    # Extract the max_res string
    # resolution_str = item['max_res']
    
    # Split the string by comma
    # width_str, height_str = resolution_str.split(',')
    
    # Convert the width and height to integers
    width = int(width_str)
    height = int(height_str)
    
    # Store the integers back into the dictionary with new keys
    item['width'] = width
    item['height'] = height
    
    asset_dictionary = {
        "asset_name" : asset_name,
        "asset_type": asset_type,
        "asset_details_01": asset_detail_01,
        "asset_details_02": asset_detail_02,
        #"asset_id" : "00",
        "width" : width,
        "height" : height
        # "asset_resolution": asset_max_res
    }

    # print(f"{asset_dictionary}\n")

    list_of_asset_dicts.append(asset_dictionary)
    # print(type(list_of_asset_dicts[0]['width']))
    # print(list_of_asset_dicts)


# for i in list_of_asset_dicts:
     
#     print(f"{list_of_asset_dicts}")

# if list_of_asset_dicts[0]['asset_detail_01'] == "PROP":
#     print("Yes")  
# else:
#     print("No")

# if "Props" in list_of_asset_dicts[0]['asset_name']:
#     print("Yes")  
# else:
#     print("No")