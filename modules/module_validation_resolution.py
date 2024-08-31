# Sub P API import
import substance_painter.logging

res_requirements = {
    'Props': [1024, 1024],
    'Weapons' : [2048, 2048],
    'Characters' : [4096, 4096]
}

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
