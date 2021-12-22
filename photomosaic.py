from PIL import Image
import numpy as np
import random
import os
import pathlib
import scipy
from scipy.spatial import distance
from scipy.spatial.kdtree import distance_matrix

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
    ROW_LIMIT = (image.height / size)
    x = 0
    y = 0
    count = 0
    avg_blocks = np.zeros( (int(ROW_LIMIT), int(COLUMN_LIMIT + 1), 3)).astype(int)
    while y < ROW_LIMIT :
        count += 1
        pixels_average = np.zeros(3)
        row = y * size
        column = x * size
        block = pixels[row: (row + size) , column : (column + size) ]
        #block = pixels[row: (row + size) , column : (column + size) ] = pixels_average.astype(int)
        avg_blocks[y,x] = computeAvergage(block)
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    print(f"x:{x} y:{y} COLUMN_LIMIT: {COLUMN_LIMIT} ROW_LIMIT: {ROW_LIMIT} count: {count}")
    return(avg_blocks)


def showImage(image_pixels):
    newImage = Image.fromarray(image_pixels)
    newImage.show()

def computeAvergage (pixels):
    """Calculates the average of a chunk of pixels"""
    average = np.zeros(3)
    for row in pixels:
        for p in row:
            average += p
    average /= pixels.size
    return average.astype(np.uint8)

def avgPixelsPhoto(size):
    """ Convert the photo to the given size and then calculates the average of his pixels  """
    path = str(pathlib.Path().parent.resolve()) + r"\foto"
    files = os.listdir(path)
    all_photo_average = {}
    for image in files:
        img = Image.open(f"{path}//{image}").resize( (size,size) )
        all_photo_average[image] = computeAvergage(np.array(img))
    
    return all_photo_average

def findBestMatchOfPixels(photos_average, main_photo_average):
    [row, column, dim] = main_photo_average.shape
    pixelMatch = np.empty( (row,column) ).astype(object)
    x = 0
    y = 0
    for blocks in main_photo_average:
        for p in blocks:
            min_distance = float("inf")
            average = None
            photos = ""
            for photo, avg in photos_average.items():
                euclidean_distance = distance.euclidean(p,avg)
                if euclidean_distance < min_distance:
                    min_distance = euclidean_distance
                    average = avg
                    photos = photo
            pixelMatch[y,x] = photos
            x += 1
        y += 1
        x = 0
    return pixelMatch

def joinImgs(image, img_match, size):
    #print(img_match)
    pixels = np.array(image)
    COLUMN_LIMIT = (image.width / size) - 1
    ROW_LIMIT = (image.height / size)
    x = 0
    y = 0
    count = 0
    while y < ROW_LIMIT :
        count += 1
        pixels_average = np.zeros(3)
        row = y * size
        column = x * size
        path = str(pathlib.Path().parent.resolve()) + r"\foto"
        pixels[row: (row + size) , column : (column + size) ] = np.array(Image.open(f"{path}\\{img_match[y,x]}").resize( (size,size) ))
        #block = pixels[row: (row + size) , column : (column + size) ] = pixels_average.astype(int)
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    showImage(pixels)
def createNewImage(image):
    #calculate pixels average of all photos
    photos_average = avgPixelsPhoto(30)
    main_photo_average = getBlockPixels(image ,30)
    img_match = findBestMatchOfPixels(photos_average, main_photo_average)
    joinImgs(image, img_match, 30)
if __name__ == "__main__":
    main_image = Image.open("windows1.jpg")
    print(f"Grandezza dell'immagine: {main_image.height} x {main_image.width}")    
    createNewImage(main_image)
    #randomPixels(main_image, 30)
    #print(getBlockPixels(main_image, 30))

