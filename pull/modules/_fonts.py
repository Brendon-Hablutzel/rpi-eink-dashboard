from PIL import ImageFont


def get_font(size: int) -> ImageFont.ImageFont:
    font_path = "assets/Font.ttc"
    return ImageFont.truetype(font_path, size)
