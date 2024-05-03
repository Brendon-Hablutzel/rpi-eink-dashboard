import sys
import os
from modules import weather
from display.interface import show_image

module_entrypoints = {
    "weather": weather.main
}

if __name__ == "__main__":
    args = sys.argv
    if len(args) - 1 != 2:
        raise IndexError(
            f"invalid number of arguments: expected 2, got {len(args) - 1}")

    module_name = args[1]
    config_filepath = args[2]

    if module_name not in module_entrypoints:
        raise ValueError(f"module not found: {module_name}")

    if not os.path.exists(config_filepath):
        raise ValueError(f"config file not found: {config_filepath}")

    entrypoint = module_entrypoints[module_name]
    image = entrypoint(config_filepath)
    show_image(image)
