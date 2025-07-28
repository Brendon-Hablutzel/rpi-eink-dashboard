import requests
from typing import Union, Literal, Tuple
from dataclasses import dataclass
import datetime
from PIL import Image, ImageDraw, ImageFont
from modules._config import parse_config
from modules._fonts import get_font

HILL_API_URL = (
    "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=264&library=hill"
)

HUNT_API_URL = (
    "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=1356&library=hunt"
)


@dataclass
class LibraryBusyness:
    name: str
    count: int
    percentage: float
    timestamp: datetime.datetime
    active: bool


def get_busyness(
    library_name: Union[Literal["hill"], Literal["hunt"]],
) -> LibraryBusyness:
    if library_name == "hill":
        res = requests.get(HILL_API_URL)
    elif library_name == "hunt":
        res = requests.get(HUNT_API_URL)
    else:
        raise ValueError(f"'{library_name}' is not a valid library")

    data = res.json()

    str_timestamp = data["timestamp"]
    native_timestamp = datetime.datetime.strptime(
        str_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    return LibraryBusyness(
        name=data["name"],
        count=data["count"],
        percentage=data["percentage"],
        timestamp=native_timestamp,
        active=data["isActive"],
    )


def generate_image(screen: Tuple[float, float]):
    (screen_height, screen_width) = screen

    current_time = datetime.datetime.now().isoformat("T", "seconds")

    hill_data = get_busyness("hill")
    hunt_data = get_busyness("hunt")

    image = Image.new("1", screen, 255)
    draw = ImageDraw.Draw(image)

    font18 = get_font(18)
    font30 = get_font(30)
    font40 = get_font(40)

    draw.text((5, 5), hill_data.name, font=font40, fill=0)
    draw.text(
        (5, 50),
        f"{hill_data.count} people ({round(hill_data.percentage * 100)}% filled)",
        font=font30,
        fill=0,
    )

    rect_width = screen_height - 10
    rect_shape = [
        # (x0, y0)
        (5, 90),
        # (x1, y1)
        (5 + rect_width, 105),
    ]
    draw.rectangle(rect_shape, fill=1, outline=0)

    rect_shape = [(5, 90), (5 + rect_width * hill_data.percentage, 105)]
    draw.rectangle(rect_shape, fill=0, outline=0)

    draw.text((5, 110), hunt_data.name, font=font40, fill=0)
    draw.text(
        (5, 155),
        f"{hunt_data.count} people ({round(hunt_data.percentage * 100)}% filled)",
        font=font30,
        fill=0,
    )

    rect_width = screen_height - 10
    rect_shape = [
        # (x0, y0)
        (5, 195),
        # (x1, y1)
        (5 + rect_width, 210),
    ]
    draw.rectangle(rect_shape, fill=1, outline=0)

    rect_shape = [(5, 195), (5 + rect_width * hunt_data.percentage, 210)]
    draw.rectangle(rect_shape, fill=0, outline=0)

    draw.text(
        (5, screen_width - (20 + 5)),
        f"On {current_time.split('T')[0]} at {current_time.split('T')[1]}",
        font=font18,
        fill=0,
    )

    return image


def main(config_filename: str) -> Image.Image:
    config = parse_config(config_filename, {})

    screen_size = (config["screen"]["height"], config["screen"]["width"])

    image = generate_image(screen_size)
    return image
