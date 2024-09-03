"""
    Module to validate texture set names.

    Rules:
    Names need to be split with _
    Name must consist of Acronyms specified in documentation: AssetType_AssetDeatil1_AssetDetail2_AssetID

    For Props, details are Prop type and Size/Scale:
        Prop Type could be: "CHR" (Chair), "TBL" (Table), "LMP" (Lamp), or "WIN" (Window)
        Prop Size/Scale could be: "S" (Small), "M" (Medium), or "L" (Large)
        Valid Texture Set names for Props:
            PROP_CHR_S_01 
            PROP_TBL_M_41
    
    For Weapons, details are Prop type and Size/Scale:
    Weapon Type could be: "SWD" (Sword), "BOW" (Bow), "RFL" (Rifle), or "EXP" (Explosive)
    Weapon Size/Scale could be: "COM" (Common), "RAR" (Rare), or "EPC" (Epic)
    Valid Texture Set names for Weapons:
        WPN_SWD_RAR_03 
        WPN_BOW_EPC_98

    For Characters, details are Prop type and Size/Scale:
        Character Type could be: "PLR" (Player), "ENM" (Enemy), "CIV" (Civilization)
        Character Size/Scale could be: "ML" (Male), "FL" (Female), or "NB" (Non-Binary)
        Valid Texture Set names for Characters:
            CHAR_SWD_RAR_03
            CHAR_BOW_EPC_98

    Content:
        - validate_name
        - validate_name_props
        - validate_name_weapon
        - validate_name_characters

    Contributors
        - Aran Ahmed, aranahmed1@live.co.uk
"""
# Default Utils imports
from typing import Tuple

import substance_painter

# Utility Lib
# used to reload imported modulees : importlib.reload()
import importlib
import module_import_data_from_json

asset_dict = module_import_data_from_json.list_of_asset_dicts

# props_asset_detail_1_list = ['CHR', 'TBL', 'LMP', 'WIN']
# props_asset_detail_2_list = ['S', 'M', 'L']

# weapons_asset_detail_1_list = ['SWD', 'BOW', 'RFL', 'EXP']
# weapons_asset_detail_2_list = ['COM', 'RAR', 'EPC']

# characters_asset_detail_1_list = ['PLR', 'ENM', 'CIV']
# characters_asset_detail_2_list = ['ML', 'FL', 'NB']


# def validate_name_props(asset_type_acronym: str, asset_type_detail_1: str, asset_type_detail_2: str) -> Tuple[bool, str]:
#     """ 
#     Sub-validation function used for specific rules check.
#     Applied for Props asset type. 
#     """
#     is_validation_pass = None
#     validate_details = None
#     if asset_type_acronym != asset_dict[0]['asset_type']:
#         is_validation_pass = False
#         # substance_painter.logging.log(substance_painter.logging.ERROR, "custom_exporter", " Validation Failed: asset type not set to PROP")
#         validate_details = f"First acronym is for asset type \
#                             \nFor asset type: 'Props', valid option is: {asset_dict[0]['asset_type']}. \
#                             \nCurrent Acronym: {asset_type_acronym}" 
#     elif asset_type_detail_1 not in asset_dict[0]['asset_details_01']:
#         is_validation_pass = False
#         validate_details = f"Second acronym is for Asset Detail #1 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[0]['asset_details_01']}. \
#                             \nCurrent Acronym: {asset_type_detail_1}" 

#     elif asset_type_detail_2 not in asset_dict[0]['asset_details_02']:
#         is_validation_pass = False
#         validate_details = f"Third acronym is for Asset Detail #2 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[0]['asset_details_02']}. \
#                             \nCurrent Acronym: {asset_type_detail_2}" 

#     else: 
#         is_validation_pass = True
#         validate_details = "Validation Passed!"

#     return is_validation_pass, validate_details

# def validate_name_weapons(asset_type_acronym: str, asset_type_detail_1: str, asset_type_detail_2: str) -> Tuple[bool, str]:
#     """ 
#     Sub-validation function used for specific rules check.
#     Applied for Weapons asset type. 
#     """
#     is_validation_pass = None
#     if asset_type_acronym != asset_dict[1]['asset_type']:
#         is_validation_pass = False
#         validate_details = f"First acronym is for asset type \
#                             \nFor asset type: 'Weapons', valid option is: {asset_dict[1]['asset_type']}. \
#                             \nCurrent Acronym: {asset_type_acronym}" 

#     elif asset_type_detail_1 not in asset_dict[1]['asset_details_01']:
#         is_validation_pass = False
#         validate_details = f"Second acronym is for Asset Detail #1 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[1]['asset_details_01']}. \
#                             \nCurrent Acronym: {asset_type_detail_1}" 

#     elif asset_type_detail_2 not in asset_dict[1]['asset_details_02']:
#         is_validation_pass = False
#         validate_details = f"Third acronym is for Asset Detail #2 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[1]['asset_details_02']}. \
#                             \nCurrent Acronym: {asset_type_detail_2}" 
#     else: 
#         is_validation_pass = True
#         validate_details = "Validation Passed!"


#     return is_validation_pass, validate_details

# def validate_name_characters(asset_type_acronym: str, asset_type_detail_1: str, asset_type_detail_2: str) -> Tuple[bool, str]:
#     """ 
#     Sub-validation function used for specific rules check.
#     Applied for Characters asset type. 
#     """
#     is_validation_pass = None
#     if asset_type_acronym != asset_dict[2]['asset_type']:
#         is_validation_pass = False
#         validate_details = f"First acronym is for asset type \
#                             \nFor asset type: 'Characters', valid option is: {asset_dict[2]['asset_type']}. \
#                             \nCurrent Acronym: {asset_type_acronym}" 

#     elif asset_type_detail_1 not in asset_dict[2]['asset_details_01']:
#         is_validation_pass = False
#         validate_details = f"Second acronym is for Asset Detail #1 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[2]['asset_details_01']}. \
#                             \nCurrent Acronym: {asset_type_detail_1}" 

#     elif asset_type_detail_2 not in asset_dict[2]['asset_details_02']:
#         is_validation_pass = False
#         validate_details = f"Third acronym is for Asset Detail #2 \
#                             \nFor asset detail 1, valid acronyms are: {asset_dict[2]['asset_details_02']}. \
#                             \nCurrent Acronym: {asset_type_detail_2}" 

#     else: 
#         is_validation_pass = True        
#         validate_details = "Validation Passed!"

#     return is_validation_pass, validate_details

def validate_name_generic(asset_i :str,asset_type_acronym: str, asset_type_detail_1: str, asset_type_detail_2: str) -> Tuple[bool, str]:
    """ 
    Sub-validation function used for specific rules check.
    Applied for Props asset type. 
    """
    is_validation_pass = None
    validate_details = None

    if not asset_type_acronym or not asset_type_detail_1 or not asset_type_detail_2:
        return False

    
    if asset_type_acronym != asset_i['asset_type']:
        is_validation_pass = False
        #substance_painter.logging.log(substance_painter.logging.ERROR, "custom_exporter", f" Validation Failed: asset type not set to {asset_i['asset_type']}")
        validate_details = f"First acronym is for asset type \
                            \nFor asset type: 'Props', valid option is: {asset_i['asset_type']}. \
                            \nCurrent Acronym: {asset_type_acronym}" 
    elif asset_type_detail_1 not in asset_i['asset_details_01']:
        is_validation_pass = False
        validate_details = f"Second acronym is for Asset Detail #1 \
                            \nFor asset detail 1, valid acronyms are: {asset_i['asset_details_01']}. \
                            \nCurrent Acronym: {asset_type_detail_1}" 

    elif asset_type_detail_2 not in asset_i['asset_details_02']:
        is_validation_pass = False
        validate_details = f"Third acronym is for Asset Detail #2 \
                            \nFor asset detail 1, valid acronyms are: {asset_i['asset_details_02']}. \
                            \nCurrent Acronym: {asset_type_detail_2}" 

    else: 
        is_validation_pass = True
        validate_details = "Validation Passed!"

    return is_validation_pass, validate_details

def validate_name(asset_type: str, texture_set_name: str) -> Tuple[bool,str]:
    """
    Core function to validate texture set name.
    Preforms general rule validation and if they pass,
    trigger sub-validation functions for specific asset type.
    """
    # Needs asset types, 
    texture_set_name_acronyms = texture_set_name.split("_") # Returns list of strings seprated by "_" so USER_I_AM_LEGEND will return a list of 4

    # Template validation # 
    if len(texture_set_name_acronyms) != 4: # here we check that there is 4 words in the string spereated by _
        return False, f"Texture set name should consist of 4 acronyms seperated by underscore symbol : _ \
                        \nValid Structure: AssetType_AssetDetail1_AssetDetail2_AssetID \
                        \nCurrent Number of acronyms: {len(texture_set_name_acronyms)}"
    # All code after this is validated
   
    # PROP _ CHR _ S _ 01 these are are seperated based on the split function then sepereated to their own string vars below
    asset_type_acronym, asset_type_detail_1, asset_type_detail_2, asset_id = texture_set_name_acronyms

    # UDIM Validation
    

    # Asset ID validation
    if (len(asset_id) != 2) or (not asset_id.isdigit()):
        substance_painter.logging.log(substance_painter.logging.ERROR, "custom_exporter", "asset_id needs to be a 2 digit number e.g. 02, 03, 99")
        return False, f"Asset ID needs to contain only 2 digits, e.g. 02, 99, 42, 03 etc \
                        \nValid Values: any number from range 00 to 99 \
                        \nCurrent ID: {asset_id}" 
                        # fails validation if asset id is not explicitly 2 digits, and if its not a digit
    
    for asset_i in asset_dict:
        if asset_type == asset_i['asset_name']:
            return validate_name_generic(asset_i,asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    
    # Changed this long if else to a loop that matches the Dictionary so updates with spreadsheet/JSON
    # if asset_type == asset_dict[0]['asset_name']:
    #     return validate_name_props(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    # elif asset_type == asset_dict[1]['asset_name']:
    #     return validate_name_weapons(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    # elif asset_type == asset_dict[2]['asset_name']:
    #     return validate_name_characters(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    
    return False,"General Validation Error: Asset Type is not valid \
                    \nThere is a mismatch between asset type from the dropdown of the widget with strings in validate function \
                    \n Suggestion: Please Contact Support Team for Tools" 