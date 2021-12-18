from PIL import Image
import numpy as np
import math
import random

from numpy.lib.shape_base import column_stack

def editImage(image):
    pixels = np.array(image)
    common_divosor = math.gcd(image.height, image.width)
    COLUMN_LIMIT = image.width / common_divosor
    x = 0
    y = 0
    while y < image.height/common_divosor :
        rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        row = y * 120
        column = x * 120
        pixels[row: row + common_divosor, column : column + common_divosor] = rgb
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    
    showImage(pixels)


def showImage(image_pixels):
    newImage = Image.fromarray(image_pixels)
    newImage.show()


if __name__ == "__main__":
    main_image = Image.open("windows.jpg")
    print(f"Grandezza dell'immagine: {main_image.height} x {main_image.width}")    
    editImage(main_image)
    

