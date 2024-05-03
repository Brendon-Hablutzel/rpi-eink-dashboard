import json
from typing import Dict


def _base_validator(config_dict: dict):
    try:
        screen_data = config_dict["screen"]
    except KeyError:
        raise KeyError(
            f"missing screen config data, expected 'screen': {'height': _, 'width': _}")

    if screen_data.get("height") is None:
        raise KeyError(f"missing required screen data: height")

    if screen_data.get("width") is None:
        raise KeyError(f"missing required screen data: width")


def validate_required_fields(config_dict: dict, required_fields: Dict[str, type]):
    for field, field_type in required_fields.items():
        config_value = config_dict.get(field)
        if config_value is None:
            raise KeyError(f"missing required field: {field}")
        else:
            if not field_type.__instancecheck__(config_value):
                raise KeyError(
                    f"invalid type for {field}: expected: {field_type}, got {type(config_value)}")


def parse_config(config_filename: str, required_fields: Dict[str, type]) -> dict:
    with open(config_filename, "r") as f:
        config_dict = json.load(f)

    _base_validator(config_dict)
    validate_required_fields(config_dict, required_fields)

    return config_dict
