import display.epd3in52
from PIL import Image


def show_image(image: Image):
    """
    A high-level function that takes an image object and shows it
    on the E-ink display. This may need to be modified based on the
    user's physical setup.
    """

    # flip image because raspberry pi is upside down
    image = image.transpose(Image.ROTATE_180)

    # initialize screen
    epd = display.epd3in52.EPD()
    epd.init()
    epd.display_NUM(epd.WHITE)
    epd.lut_GC()
    epd.refresh()

    # ???
    epd.send_command(0x50)
    epd.send_data(0x17)

    # display image
    epd.display(epd.getbuffer(image))
    epd.lut_GC()
    epd.refresh()


def cleanup():
    # close screen resources
    epd = display.epd3in52.EPD()
    epd.sleep()
    display.epd3in52.epdconfig.module_exit(cleanup=True)
