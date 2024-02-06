import sys
from display.interface import show_image
from dashboard import generate_image

def main(latitute, longitude):
    image = generate_image(latitute, longitude)

    show_image(image)

if __name__ == "__main__":
    latitute = sys.argv[1]
    longitude = sys.argv[2]
    main(latitute, longitude)