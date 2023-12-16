from PIL import Image
import numpy as np


def convert_image_to_pixels(image_path):
    # Open the image
    img = Image.open(image_path)

    # Convert the image to grayscale
    img = img.convert('L')

    # Get the pixel data as a list of lists
    pixels = []
    for y in range(img.size[1]):
        row = []
        for x in range(img.size[0]):
            if img.getpixel((x, y)) >= 30:
                pixel_value = 1
            else:
                pixel_value = 0

            row.append(pixel_value)
        pixels.append(row)

    return pixels


# Replace 'paths.png' with the path to your image
image_path = r'paths.png'
pixels = convert_image_to_pixels(image_path)
np.savetxt('pixels.txt', pixels, fmt='%.f', delimiter='')

array = np.array(pixels, dtype=np.uint8) * 255
img = Image.fromarray(array, mode="L")
img.show()
