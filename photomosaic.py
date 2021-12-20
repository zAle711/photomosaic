from PIL import Image
import numpy as np
import math
import random



def randomPixels(image, size):
    """Replace square of pixels with sixe x size area with a radom color

    Args:
        image (PIL.Image): original image
        size (int): size of every random color
    """
    
    pixels = np.array(image)
    COLUMN_LIMIT = (image.width / size) - 1
    ROW_LIMIT = image.height / size
    x = 0
    y = 0
    while y < ROW_LIMIT :
        rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        row = y * size
        column = x * size
        pixels[row: row + size, column : column + size] = rgb
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    showImage(pixels)

def getBlockPixels(image, size):
    pixels = np.array(image)
    COLUMN_LIMIT = (image.width / size) - 1
    ROW_LIMIT = image.height / size
    x = 0
    y = 0
    avg_blocks = np.array([])
    while y < ROW_LIMIT :
        pixels_average = np.zeros(3)
        rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        row = y * size
        column = x * size
        block = pixels[row: (row + size) , column : (column + size) ]
        for b in block:
           for p in b:
               pixels_average += p
        pixels_average /= block.size
        block = pixels[row: (row + size) , column : (column + size) ] = pixels_average.astype(int)
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    showImage(pixels)
    return(avg_blocks)


def showImage(image_pixels):
    newImage = Image.fromarray(image_pixels)
    newImage.show()


if __name__ == "__main__":
    main_image = Image.open("windows.jpg")
    print(f"Grandezza dell'immagine: {main_image.height} x {main_image.width}")    
    randomPixels(main_image, 30)
    print(getBlockPixels(main_image, 30))

