import display.epd3in52
from PIL import Image

def show_image(image):
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
 
    # close screen resources
    epd.sleep()
    display.epd3in52.epdconfig.module_exit(cleanup=True)