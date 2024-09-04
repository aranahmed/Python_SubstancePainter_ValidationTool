"""
    Module to export all validated textures.

    Rules:
    
    Content:
        - open_file - Opens file on Explorer / Finder depending on platform
        - get_export_preset_from_shader_type
        - build_export_config - returns a dictionary of export parameters
        - open_export_at_given_path
        - export_textures
    
    Contributors
        - Aran Ahmed, aranahmed1@live.co.uk
"""
# Substance Painter API import
import substance_painter

# Default utils imports
from math import log2
# from os import startfile

# From stackoverflow for os.startfile() on MacOS

import os, sys, subprocess

def open_file(filename :str):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# End Stackoverflow

def get_export_preset_from_shader_type(shader_type : str) -> str:
    custom_export_presets = {
         'Basic':'Custom_Basic',
         'Armament' : 'Custom_Armament',
         'Morph' : 'Custom_Morph',
         'UDIM' : 'Custom_UDIM'
         }
    
    export_preset_name = custom_export_presets.get(shader_type)
    if export_preset_name is None:
        substance_painter.logging.log(substance_painter.logging.ERROR, "custom_exporter", f'There is no export preset for specified {shader_type}')
    return export_preset_name

# Function to generate export paths based on amount of UV Tiles found during UDIM workflow
def create_new_export_paths(export_path: str):
    original_export_path = export_path

    for uv_tile in len(substance_painter.textureset.TextureSet.all_uv_tiles):
        new_path = f"{export_path}/{uv_tile}"
        return new_path

def build_export_config(texture_set_name: str, shader_type: str, export_path: str):
    texture_set = substance_painter.textureset.TextureSet.from_name(texture_set_name)
    texture_set_stack = texture_set.get_stack()

    export_preset_name = get_export_preset_from_shader_type(shader_type)

    export_preset_id = substance_painter.resource.ResourceID("custom_lib", export_preset_name )

    uv_tile_list = substance_painter.textureset.TextureSet.all_uv_tiles(texture_set)

    if substance_painter.textureset.TextureSet.has_uv_tiles(texture_set):
        export_configs=[]
        for i, uv_tile in enumerate(substance_painter.textureset.TextureSet.all_uv_tiles(texture_set),0):
            resolution = substance_painter.textureset.UVTile.get_resolution(uv_tile)
            resolution = [log2(resolution.width), log2(resolution.height)]
            formatted_uv_tile = [uv_tile.u,uv_tile.v]
            
            # Doesnt look like this works:
            export_config = {
            "exportShaderParams": False,
            "exportPath": export_path,
            "defaultExportPreset" : export_preset_id.url(),
            # "exportPresets" : [{
            #     "name" : export_preset_name,
            #     "maps" : [{
            #         "fileName"  : "$textureSet_$udim"
            #     }]
            # }],
            "exportList": [
                {
                    "rootPath": str(texture_set_stack),
                    
                    # Chooses which UV tiles to export 
                    "filter" : {

                        "uvTiles" : [formatted_uv_tile]
                    }
                }
            ],
            "exportParameters": [
                {

                    # "filter" :  {
                    #     "uvTiles" : [[0,0],[1,0],[2,0]]
                    # },
                    "parameters": {
                        "paddingAlgorithm": "infinite",
                        "sizeLog2" : resolution
                    }
                }]
            }
            export_configs.append(export_config)
        return export_configs
        # print(f"Export configs: {len(export_configs)}")
    else:
        resolution = texture_set.get_resolution()
        resolution = [log2(resolution.width), log2(resolution.height)]

        export_config = {
        "exportShaderParams": False,
        "exportPath": export_path,
        "defaultExportPreset" : export_preset_id.url(),
        # "exportPresets" : [{
        #     "name" : export_preset_name,
        #     "maps" : [{
        #         "fileName"  : "$textureSet_$udim"
        #     }]
        # }],
        "exportList": [
            {
                "rootPath": str(texture_set_stack),
                
                # Chooses which UV tiles to export 
                # "filter" : {

                #     "uvTiles" : [[0,0],[1,0] ]
                # }
            }
        ],
        "exportParameters": [
            {

                # "filter" :  {
                #     "uvTiles" : [[0,0], [1,0]]
                # },
                "parameters": {
                    "paddingAlgorithm": "infinite",
                    "sizeLog2" : resolution
                }
            }]
        }
        return export_config

def open_export_at_given_path(path: str):
    open_file(path)
    # startfile(path)

def export_textures(texture_set_name: str,uv_tile_name: str, shader_type : str, export_path : str):
    if not substance_painter.project.is_open():
        return
    
    texture_set = substance_painter.textureset.TextureSet.from_name(texture_set_name)
    if substance_painter.textureset.TextureSet.has_uv_tiles(texture_set):
        
        export_configs = build_export_config(texture_set_name, shader_type, export_path)
        print(len(export_configs))

        # for i,uv_tile in enumerate(substance_painter.textureset.TextureSet.all_uv_tiles(texture_set),0):
        for export_config in export_configs:

    
            # export_config, uv_tile = build_export_config(texture_set_name, uv_tile, shader_type, export_path)
            
            # Actual export operation:
            substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", "Going to preform Texture Exporting")

            export_result = substance_painter.export.export_project_textures(export_config)

            # In case of error, display a human readable message:
            if export_result.status == substance_painter.export.ExportStatus.Success:
                open_export_at_given_path(export_path)
            else:
                substance_painter.logging.log(substance_painter.logging.WARNING, "custom_exporter", export_result.message)

            # Display the details of what was exported:
            for k,v in export_result.textures.items():
                substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", f"Stack {k}:")
                for exported in v:
                    substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", exported)
    
    else:
        export_config = build_export_config(texture_set_name, shader_type, export_path)
        
        # Actual export operation:
        substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", "Going to preform Texture Exporting")

        export_result = substance_painter.export.export_project_textures(export_config)

        # In case of error, display a human readable message:
        if export_result.status == substance_painter.export.ExportStatus.Success:
            open_export_at_given_path(export_path)
        else:
            substance_painter.logging.log(substance_painter.logging.WARNING, "custom_exporter", export_result.message)

        # Display the details of what was exported:
        for k,v in export_result.textures.items():
            substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", f"Stack {k}:")
            for exported in v:
                substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", exported)