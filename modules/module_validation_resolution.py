"""
    Module to validate texture set resolution.

    Rules:
    Props can only have a texture resolution of up to 1024x1024
    Weapons can only have a texture resolution of up to 2048x2048
    Characters can only have a texture resolution of up to 4096x4096

    Content:
        - get_required_res_from_asset_type
        - validate_res
    
    Contributors
        - Aran Ahmed, aranahmed1@live.co.uk
"""
# Sub P API import
import substance_painter.logging
import module_import_data_from_json

asset_dict = module_import_data_from_json.list_of_asset_dicts

res_requirements = {
    # asset_dict[0]['asset_name']: [asset_dict[0]['width'], asset_dict[0]['height']],
    # asset_dict[1]['asset_name']: [asset_dict[1]['width'], asset_dict[1]['height']],
    # asset_dict[2]['asset_name']: [asset_dict[2]['width'], asset_dict[2]['height']],
    # asset_dict[3]['asset_name']: [asset_dict[3]['width'], asset_dict[3]['height']],

    # for i in range(asset_dict)):
    #     asset_dict[i]['asset_name']: [asset_dict[i]['width'], asset_dict[i]['height']]
}

# for i in range(asset_dict):
    # res_requirements[f'{asset_dict[i]['asset_name']}'] = [asset_dict[i]['width'], asset_dict[i]['height']]
    
for asset in asset_dict:
    res_requirements[asset['asset_name']] = [asset['width'], asset['height']]

def get_required_res_from_asset_type(asset_type: str)-> tuple[int, int]:

    required_res = res_requirements.get(asset_type)

    if required_res is None:
        strict_res_values = min(res_requirements.values(), key=sum) # Moves through all the dictionary values, adding all the sums together, compares and finds the lowest value, essentially giving a fallback value
        required_res_width, required_res_height = strict_res_values
        substance_painter.logging.log(severity=substance_painter.logging.WARNING, 
                                      channel="custom_exporter", 
                                      message=f"There is no resolution budget for: {asset_type}\
                                      \nFallback to the default: {required_res_width} x {required_res_height}")
    else:
        required_res_width, required_res_height = required_res
    return required_res_width, required_res_height

def validate_res(asset_type: str, current_texset_res: substance_painter.textureset.Resolution)-> tuple[bool, str]:
    is_validation_passed = None
    validation_details = None

    required_res_width, required_res_height = get_required_res_from_asset_type(asset_type)

    if current_texset_res.width > required_res_width or current_texset_res.height > required_res_height:
        is_validation_passed = False
        validation_details = f"Current Resolution for texture set: {current_texset_res.width} x {current_texset_res.height}, \
                            \nwhich is higher than the max allowed for current Asset Type: {asset_type}:\
                            \n{current_texset_res.width} x {current_texset_res.height}"
    else:
        is_validation_passed = True
        validation_details = "Validation Passed!"

    return is_validation_passed, validation_details

def validate_res_udim(asset_type: str, current_uv_tile_res: substance_painter.textureset.UVTile)-> tuple[bool, str]:
    is_validation_passed = None
    validation_details = None

    required_res_width, required_res_height = get_required_res_from_asset_type(asset_type)
    # for uv_tile in (substance_painter.textureset.TextureSet.all_uv_tiles(self)):

    # uv_tile = substance_painter.textureset.TextureSet.get_uvtiles_resolution(texture_set)
    # uv_tile_dict= []
    # uv_tile_dict.append(substance_painter.textureset.TextureSet.get_uvtiles_resolution(self))
    
    current_uv_tile_res_width = current_uv_tile_res.width
    current_uv_tile_res_height = current_uv_tile_res.height

    if current_uv_tile_res_width > required_res_width or current_uv_tile_res_height > required_res_height:
            is_validation_passed = False
            validation_details = f"Current Resolution for uv tile: {current_uv_tile_res_width} x {current_uv_tile_res_height}, \
                                \nwhich is higher than the max allowed for current Asset Type: {asset_type}:\
                                \n{current_uv_tile_res_width} x {current_uv_tile_res_width}"

    else:
        is_validation_passed = True
        validation_details = "Validation Passed!"

    return is_validation_passed, validation_details
