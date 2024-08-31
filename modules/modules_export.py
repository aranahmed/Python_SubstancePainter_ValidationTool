# Substance Painter API import
import substance_painter

# Default utils imports
from math import log2
# from os import startfile


# From stackoverflow for os.startfile() on MacOS

import os, sys, subprocess

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# End Stackoverflow

def get_export_preset_from_shader_type(shader_type):
    custom_export_presets = {
         'Basic':'Custom_Basic',
         'Armament' : 'Custom_Armament',
         'Morph' : 'Custom_Morph'
         }
    
    export_preset_name = custom_export_presets.get(shader_type)
    if export_preset_name is None:
        substance_painter.logging.log(substance_painter.logging.ERROR, "custom_exporter", f'There is no export preset for specified {shader_type}')
    return export_preset_name

def build_export_config(texture_set_name, shader_type, export_path):
    texture_set = substance_painter.textureset.TextureSet.from_name(texture_set_name)
    texture_set_stack = texture_set.get_stack()

    export_preset_name = get_export_preset_from_shader_type(shader_type)

    export_preset_id = substance_painter.resource.ResourceID("custom_lib", export_preset_name )

    resolution = texture_set.get_resolution()
    resolution = [log2(resolution.width), log2(resolution.height)]

    export_config = {
    "exportShaderParams": False,
    "exportPath": export_path,
    "defaultExportPreset" : export_preset_id.url(),
    "exportList": [
        {
            "rootPath": str(texture_set_stack)
        }
       ],
    "exportParameters": [
        {
            "parameters": {
                "paddingAlgorithm": "infinite",
                "sizeLog2" : resolution
            }
        }]
    }
    return export_config

def open_export_at_given_path(path):
    open_file(path)
    # startfile(path)

def export_textures(texture_set_name, shader_type, export_path):
    if not substance_painter.project.is_open():
        return
    
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