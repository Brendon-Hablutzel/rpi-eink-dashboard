import sys
import os
from modules import weather, library_busyness
from display.interface import show_image

# a dictionary where each key is the name of a module
# and each corresponding item is a function that takes a
# config file and returns the image for that module
module_entrypoints = {
    "weather": weather.main,
    "busyness": library_busyness.main
}

# EXAMPLE USAGE: python main.py weather weather_config.json
if __name__ == "__main__":
    args = sys.argv
    if len(args) - 1 != 2:
        # this takes two arguments, the first being the name of the
        # module to render (as provided in module_entrypoints), and
        # the second being the path to the config file
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
