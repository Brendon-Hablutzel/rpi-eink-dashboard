import requests
from PIL import Image, ImageDraw, ImageFont
import datetime
from modules._config import parse_config
from modules._fonts import get_font


def generate_image(screen_size, devices):
    """
    Generates an image showing system resource usage for a list of devices.
    Each device is queried at http://<ip>:8080 for JSON system stats.
    """
    (screen_height, screen_width) = screen_size
    image = Image.new("1", (screen_height, screen_width), 255)
    draw = ImageDraw.Draw(image)

    # Layout settings
    margin = 10
    row_height = 90
    font_title = get_font(28)
    font_label = get_font(18)
    font_value = get_font(22)

    for idx, ip in enumerate(devices):
        try:
            url = f"http://{ip}:8080"
            resp = requests.get(url, timeout=2)
            data = resp.json()
        except Exception:
            data = None

        y_offset = margin + idx * row_height
        x_offset = margin

        # Device title
        title = data.get("host_name") if data and data.get("host_name") else ip
        draw.text((x_offset, y_offset), title, font=font_title, fill=0)

        if not data:
            draw.text((x_offset, y_offset + 32), "No data", font=font_label, fill=0)
            continue

        # CPU usage
        cpu_usage = data.get("global_cpu_usage", 0)
        draw.text(
            (x_offset, y_offset + 32), f"CPU: {cpu_usage:.1f}%", font=font_value, fill=0
        )

        # Memory usage
        used_mem = data.get("used_memory", 0)
        total_mem = data.get("total_memory", 1)
        mem_percent = (used_mem / total_mem * 100) if total_mem else 0
        draw.text(
            (x_offset + 160, y_offset + 32),
            f"Mem: {used_mem // 1024 // 1024}MB / {total_mem // 1024 // 1024}MB ({mem_percent:.1f}%)",
            font=font_value,
            fill=0,
        )

        # Uptime
        uptime_sec = data.get("uptime_seconds", 0)
        uptime_hr = uptime_sec // 3600
        draw.text(
            (x_offset, y_offset + 60), f"Uptime: {uptime_hr}h", font=font_label, fill=0
        )

        # Load averages
        la1 = data.get("load_average_one", 0)
        la5 = data.get("load_average_five", 0)
        la15 = data.get("load_average_fifteen", 0)
        draw.text(
            (x_offset + 160, y_offset + 60),
            f"Load: {la1:.2f}, {la5:.2f}, {la15:.2f}",
            font=font_label,
            fill=0,
        )

    return image


def main(config_filename: str) -> Image.Image:
    """
    The primary entry point for this dashboard. Takes a config filename, parses and
    validates it internally, and returns an image with system resource data.
    """
    required_fields = {"devices": list[str]}
    config = parse_config(config_filename, required_fields)

    screen_size = (config["screen"]["height"], config["screen"]["width"])
    devices = config["devices"]

    image = generate_image(screen_size, devices)
    return image
