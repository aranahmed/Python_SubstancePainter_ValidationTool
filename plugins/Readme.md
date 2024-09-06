# Substance Painter Custom Exporter

## Goal: 
- Automated way of exporting texture sets with consideration of Project requirements.
- Create a systemic naming system.
- Data that can be updated by developers who are not programmers.

## Key Features:
- Generate export path
- Validate Texture set Name and Resolution
- Support Multiple Asset Types and Export Presets
- Import Data from Spreadsheet data directly to painter for texture validation
- Generate Texture Set Name strings using the naming convention provided, leaving minimal room for error

## Future Goals:
- [ ] Support Material Layering 
- [ ] Add Path to Excel File / JSON 

## Updates:

[01.09.24] - Text Set Name string generator added. You can simply right click , select rename on any of the Textset names and select from a dynamic list of options that change based on Asset_Type.

[02.09.24] - Spreadsheet data is available for import. The data will be converted from .xlsx file to JSON automatically. If it doesn’t detect a JSON file it will throw up a warning and set some defaults.

[03.09.24] - Tool fully supports UDIMs and different texture resolutions for each map. Will need to use a UDIM specified shader from the list.

[04.09.24] - Tool now supports uneven textures and validates correctly. Aspect ratio is not maintained for textures when correcting the texture sizes at the moment.

## Known Issues:
- Tool does not currently support material layering workflows.
- Aspect ratio is not automatically maintained for textures when correcting the texture sizes for uneven textures at the moment.

# UI overview

## Main Widget Window

![png](https://i.imgur.com/XKuRdzv.png)

1. Using UDIMs workflow. This will dictate whether will suggest using UDIM based custom shaders.
2. Personal Export. Checkbox to specify either the Export Path should be generated in Official project path (unchecked) or Personal (checked)
3. Asset Type. Dropbox to specify Asset Type. It affects the Export Path generation process as well as Naming and Resolution validation.
4. Help button. Used to open this help menu. Shortcut for this is Ctrl/Cmnd F1.
5. Refresh button. Used to refresh the Table widget below.
5. Export button. Used to trigger exporting selected texture sets.
6. Table widget has 6 columns that contains information about texture sets currently present in the opened .spp project. One row per one texture set.
- 6.1 Export checkbox. Used to specify either the texture set in that row should be exported (checked) or ignored (unchecked). When validation is OK, the user can change the state of this checkbox. When validation is Failed, this checkbox becomes disabled and unchecked automatically to prevent export until validation is OK.
- 6.2 Texture Set Name. Name of the texture set, driven from the values specified in the Texture Set List tab. Not allowed for direct users edit.
- 6.3. Shader Type. Dropdown list to specify which shader (export preset) should be used during the export for texture set in that row. User can always modify it.
- 6.4. Resolution.Resolution of the texture set, driven from the values specified in the Texture Set Settings tab. Not allowed for direct users edit.
- 6.5 Export Path. Shows path in which textures of the texture set in that row will be exported to. Generated automatically based on the Asset Type, Shader Type and Texture Set name.
- 6.6. Validation. Shows status of Name and Resolution validations. Green checkmark icon represents Passed status, Red X – Failed.


## Pop-up Texture Set rename string generator
To access the menu, simply right click any of the texture set names in the table and select 'Rename'
![png](https://i.imgur.com/iX2ZJll.png)

1. Dropdown select Asset Acronyms
2. Read-Only String - avoids user from typing in incorrect naming convention
3. Copy to Clipboard - Copies the string to users Ctrl/Cmnd + C 
- Extras:
- Context sensitive details: Asset_Detail_01, 02 change depending on which Asset_Type has been chosen. e.g. CHR is selected, so ML, FL, NB would be the only selectable options
- Exists to avoid user choosing the incorrect Asset Details for the Asset Type.


## Resolution over budget Dialog Window

That Dialog Window appears if there is at least one texture set in the opened .spp project that exceeds the specified Resolution limitations.
1. Allows the tool to apply max required resolution for all texture sets listed in the opened .spp file.
2. Skips the automated resolution adjustment.
3. Checkbox to not show this dialog window further on even if there is resolution validation failed.

# How to edit data using Excel File

## Sample Excel Data
![png](https://i.imgur.com/1gS759t.png)

### Excel Information
1. Keys : (Not chaneable at this time)
- Asset_Types
- Asset_Detail_01
- Asset_Detail_02
- Max_Resolution
2. Values: (Fully modular)
- Addition Asset Types will appear in both the Texset Renamer tool and in the main widget window.
- You can add as many Asset_Types, Details and Maximum Resolutions as you want.
- Make sure Values are input as Text and not Numbers or other Cell data types.

## Hotkeys
- Alt + F1 – Open Help Menu.
- Alt + R – Refresh Table widget.
- Alt + E – Export selected Texture Sets. 

## Default Supported Asset Types
- Props;
- Weapons;
- Characters.
- Shaders
- Can be extended with subp_data.xlsx spreadsheet

## Supported Export Presets (Shader Types)

- Basic
- Originally intended for asset type Props.
- Channels:
- Albedo (RGB)
- Normal (RBG)
- Roughness (Grayscale)
- Metallic (Grayscale)
- Format: .png, 8 bits
- Output Template: Custom_Basic.spexp 
## Armament
 - Originally intended for asset type Weapons.
### Channels:
- Albedo (RGBA)
- Normal (RBG)
- Roughness (Grayscale)
- Metallic (Grayscale)
- Height (Grayscale)
- Format: .tga, 8 bits
- Output Template: Custom_Armament.spexp


## Morph
- Originally intended for asset type Characters.
### Channels:
- Albedo (RGBA)
- Normal (RBG)
- Roughness (Grayscale)
- Metallic (Grayscale)
- Height (Grayscale)
- User0 (Grayscale). Custom channel for Details.
- Format: .png, 8 bits
- Output Template used: Custom_Characters.spexp


# Validation rules

## Texture Set Naming rules

## General rules
- Name should consist of 4 Acronyms separated by underscore (“_”).
- IF using UDIM workflow, the output will consist of 5 Acronyms separated by underscore (“_”).
- Order of Acronyms is constant and important: AssetType_AssetDetail1_AssetDetail2_AssetID
- IF using UDIMs you do not need to add the Acronym for UVTile
- AssetID has the same rules for all asset types and are the following: 2 numbers from 0 to 9 representing values from 00 to 99.


**The Following is the default settings the tool will revert to if no Excel/JSON file is supplied**

## Naming rules for Props
- Asset Type is “PROP”
### AssetDetail1 describes the type of the prop. Valid options are:
- “CHR” for Chair;
- “TBL” for Table;
- “LMP” for Lamp;
- “WIN” for Window.
### AssetDetail2 describes the size of the prop. Valid options are:
- “S” for Small;
- “M” for Medium;
- “L” for Large.
### Valid examples of Texture Set name for Props:
- PROP_CHR_S_01
- PROP_TBL_M_02

## Naming rules for Weapons
## Asset Type is “WPN”
### AssetDetail1 describes the type of the weapon. Valid options are:
   - “SWD” for Sword;
   - “BOW” for Bow;
   - “RFL” for Rifle;
   - “EXP” for Explosive.
### AssetDetail2 describes the rarity of the weapon. Valid options are:
    - “COM” for Common;
    - “RAR” for Rare;
    - “EPC” for Epic.
### Valid examples of Texture Set name for Weapons:
    - WPN_BOW_COM_01
    - WPN_RLF_EPC_04

## Naming rules for Characters
 - Asset Type is “CHAR”
### AssetDetail1 describes the type of the character. Valid options are:
   - “PLR” for Player;
   - “ENM” for Enemy;
   - “CIV” for Civilian.
### AssetDetail2 describes the Gender of the character. Valid options are:
   - “ML” for Male;
   - “FL” for Female.
   - "NB" for Non-Binary
### Valid examples of Texture Set name for Weapons:
   - CHAR_PLR_ML_01
   - CHAR_CIV_FM_05


## Texture Set Resolution rules
==Subject to Change, based on the Spreadsheet Rules provided, will default to :==
### Max allowed resolution for each asset type:
- Props: 1024 x 1024
- Weapons: 2048 x 2048
- Characters: 4096 x 4096
- Lower resolution is allowed.

==Uneven texture sets are allowed, but will not maintain their asepct ratio at the moment.==

Contact point 
Aran Ahmed -  aranahmed1@live.co.uk

Work based off tutorial from : Viacheslav Makhynko
