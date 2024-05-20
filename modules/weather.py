import requests
from PIL import Image, ImageDraw, ImageFont
import datetime
from modules._config import parse_config


def parse_datetime_str(datetime_string):
    return datetime.datetime.strptime(
            datetime_string, "%Y-%m-%dT%H:%M")

def weather_code_to_text(wmo_code):
    '''
    Takes a WMO weather code and converts it to a human-readable string 
    weather type.
    '''
    if wmo_code == 0:
        return "Clear Sky"
    elif wmo_code == 1:
        return "Mainly Clear"
    elif wmo_code == 2:
        return "Partly Cloudy"
    elif wmo_code == 3:
        return "Overcast"
    elif wmo_code == 45 or wmo_code == 48:
        return "Foggy"
    elif wmo_code == 51:
        return "Light Drizzle"
    elif wmo_code == 53:
        return "Moderate Drizzle"
    elif wmo_code == 55:
        return "Dense Drizzle"
    elif wmo_code == 56 or wmo_code == 57:
        return "Freezing Drizzle"
    elif wmo_code == 61:
        return "Slight Rain"
    elif wmo_code == 63:
        return "Moderate Rain"
    elif wmo_code == 65:
        return "Heavy Rain"
    elif wmo_code == 66 or wmo_code == 67:
        return "Freezing Rain"
    elif wmo_code == 71:
        return "Slight Snow"
    elif wmo_code == 73:
        return "Moderate Snow"
    elif wmo_code == 75:
        return "Heavy Snow"
    elif wmo_code == 77:
        return "Snow Grains"
    elif wmo_code == 80:
        return "Slight Rain Showers"
    elif wmo_code == 81:
        return "Moderate Rain Showers"
    elif wmo_code == 82:
        return "Violent Rain Showers"
    elif wmo_code == 85:
        return "Slight Snow Showers"
    elif wmo_code == 86:
        return "Heavy Snow Showers"
    elif wmo_code >= 95 and wmo_code <= 99:
        return "Thunderstorm"
    else:
        return "Unknown"


def find_next_entry_index(datetimes):
    '''
    Takes a list of string datetimes and returns the index of the smallest 
    datetime greater than the current datetime.
    '''
    current_datetime = datetime.datetime.now()
    for (index, datetime_string) in enumerate(datetimes):
        datetime_parsed = parse_datetime_str(datetime_string)
        if datetime_parsed > current_datetime:
            return index


def temp_change_to_string(current_temp, next_temp):
    '''
    Takes a current temperature and a future temperature and returns
    a human-readable evaluation of how the temperature is changing.
    '''
    if next_temp > current_temp:
        return "increasing"
    elif next_temp < current_temp:
        return "decreasing"
    else:
        return "steady"


def get_weather_data(lat, long):
    '''
    Given a latitude and longitude, returns weather data for that location.
    '''
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,apparent_temperature,is_day,precipitation,weather_code,cloud_cover&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&forecast_days=3"
    data = requests.get(url).json()
    return data


def generate_image(screen_size, lat, long):
    '''
    Generates the image for the weather screen, given the screen size as a 
    tuple (height, width) and the latitude and longitude of the desired location.
    '''
    (screen_height, screen_width) = screen_size

    # weather data parsing
    data = get_weather_data(lat, long)

    current_data = data["current"]
    current_temp = current_data["temperature_2m"]
    current_time = datetime.datetime.now().isoformat("T", "seconds")
    weather_type = weather_code_to_text(current_data["weather_code"])

    daily_data = data["daily"]
    daily_min_temp = daily_data["temperature_2m_min"][0]
    daily_min_temp = daily_min_temp if daily_min_temp <= current_temp else current_temp
    daily_max_temp = daily_data["temperature_2m_max"][0]
    daily_max_temp = daily_max_temp if daily_max_temp >= current_temp else current_temp

    sunset_time = parse_datetime_str(daily_data["sunset"][0]).time()

    hourly_data = data["hourly"]
    forecast_datetimes = hourly_data["time"]
    next_record_index = find_next_entry_index(forecast_datetimes)
    next_temp = hourly_data["temperature_2m"][next_record_index]
    temp_change_status = temp_change_to_string(current_temp, next_temp)

    # image generation
    font18 = ImageFont.truetype("assets/Font.ttc", 18)
    font24 = ImageFont.truetype("assets/Font.ttc", 24)
    font32 = ImageFont.truetype("assets/Font.ttc", 32)
    font40 = ImageFont.truetype("assets/Font.ttc", 40)

    image = Image.new('1', (screen_height, screen_width),
                      255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # weather code
    weather_type_text_size = 32
    weather_type_text_x = 5
    weather_type_text_y = 0
    draw.text((weather_type_text_x, weather_type_text_y),
              weather_type, font=font32)

    # current temperature
    temp_text_size = 40
    temp_text_pos_x = weather_type_text_x
    temp_text_pos_y = weather_type_text_y + weather_type_text_size + 15
    draw.text((temp_text_pos_x, temp_text_pos_y),
              f"Temperature: {current_temp}°", font=font40, fill=0)

    # min - max temperature range
    # min temperature
    min_temp_text_size = 24
    min_temp_text_pos_x = temp_text_pos_x
    min_temp_text_pos_y = temp_text_pos_y + temp_text_size + 15
    draw.text((min_temp_text_pos_x, min_temp_text_pos_y),
              f"{daily_min_temp}°", font=font24)

    # max temperature
    max_temp_text_size = 24
    max_temp_text_pos_x = screen_height - (max_temp_text_size * 3 + 5)
    max_temp_text_pos_y = min_temp_text_pos_y
    draw.text((max_temp_text_pos_x, max_temp_text_pos_y),
              f"{daily_max_temp}°", font=font24)

    # temperature range bar outline
    rect_x0 = min_temp_text_pos_x + min_temp_text_size * 3  # top left distance right
    rect_y0 = min_temp_text_pos_y + 5  # top left distance down
    rect_x1 = max_temp_text_pos_x - 5  # bottom right distance right
    rect_y1 = max_temp_text_pos_y + max_temp_text_size  # bottom right distance down
    rect_shape = [
        (rect_x0, rect_y0),
        (rect_x1, rect_y1)
    ]
    draw.rectangle(rect_shape, fill=1, outline=0)

    # temp range bar fill
    outline_width = rect_x1 - rect_x0
    temp_range = daily_max_temp - daily_min_temp
    scale_factor = outline_width / temp_range
    current_temp_width = (current_temp - daily_min_temp) * scale_factor
    rect_shape = [
        (rect_x0, rect_y0),
        (rect_x0 + current_temp_width, rect_y1)
    ]
    draw.rectangle(rect_shape, fill=0, outline=0)

    # temperature change
    temp_change_text_size = 18
    temp_change_text_x = rect_x0
    temp_change_text_y = rect_y1 + 5
    draw.text((temp_change_text_x, temp_change_text_y),
              f"temperature {temp_change_status}", font=font18)

    sunset_text_size = 32
    sunset_text_x = min_temp_text_pos_x
    sunset_text_y = temp_change_text_y + temp_change_text_size + 10
    draw.text((sunset_text_x, sunset_text_y), f"Sunset is at {sunset_time}", font=font32)

    # current time
    draw.text((5, screen_width - (18 + 5)),
              f"On {current_time.split('T')[0]} at {current_time.split('T')[1]}", font=font18, fill=0)
    return image


def main(config_filename: str) -> Image.Image:
    '''
    The primary entry point for this dashboard. Takes a config filename, parses and
    validates it internaly, and returns an image with weather data.
    '''
    required_fields = {
        "latitude": float,
        "longitude": float
    }
    config = parse_config(config_filename, required_fields)

    screen_size = (config["screen"]["height"], config["screen"]["width"])
    latitude = config["latitude"]
    longitude = config["longitude"]

    image = generate_image(screen_size, latitude, longitude)
    return image
