from PIL import Image
import numpy as np
import random
import os
import pathlib
import scipy
from scipy.spatial import distance

def getBlockPixels(image, size, photos_average):
    """Calculates the average of every block

    Args:   
        image (PIL.Image): main image used to calculate the average
        size (int): size of every block ( 30x30 )
        
    Returns: 
        np.array : reeturn an array that contains the average of every block
    
    """
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
        #avg_blocks[y,x] = computeAvergage(block)
        average = computeAvergage(block)
        image = getMatchingImage(photos_average, average)
        block = np.array(Image.open(image))
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    #print(f"x:{x} y:{y} COLUMN_LIMIT: {COLUMN_LIMIT} ROW_LIMIT: {ROW_LIMIT} count: {count}")
    #return(avg_blocks)
    Image.fromarray(pixels).show()
def getMatchingImage(photos_average, block_average):
    """Returns the matching photo to a given block of pixels

    Args:   
        photos_average (dict) : Dictionary with name of every photo as key and average as value
        average (np.array): average we want to be matched
    Returns:
        (str): Returns the name of the image matched
    """
    
    min_distance = float("inf")
    path = str(pathlib.Path().parent.resolve()) + f"\\foto\\"
    photo = ""
    
    for photo_name, photo_average in photos_average.items():
        #I use the euclidean distance to find the best match for a given block
        euclidean_distance = distance.euclidean(block_average,photo_average)
        if euclidean_distance < min_distance:
            min_distance = euclidean_distance
            photo = photo_name
    return path + photo    
def showImage(image_pixels):
    """ Given an array of pixels shows the image """
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
    """ Finds the best match according to the average of a block 

    Args:
        photos_average (dict): Dictionary with the name of a photo as a key and the averaga of his pixels as value
        main_photo_average (np.array): Numpy Array with average of every block of pixels

    Returns:
        np.array: returns a photo for each block of pixels
    """
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
                #I use the euclidean distance to find the best match for a given block
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

def joinImgs(image, img_match, size) :
    """Combine photos to recreate the main image and shows it

    Args:
        image (PIL.Image): original image where i replace blocks of pixels with one of the photos
        img_match (np.array): array with photo name for every block
        size (int): size of a block (30x30) 
    """
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
        path = str(pathlib.Path().parent.resolve())
        path += f"\\foto\\{img_match[y,x]}"
        pixels[row: (row + size) , column : (column + size) ] = np.array(Image.open(path).resize( (size,size) ))
        if x < COLUMN_LIMIT:
            x += 1
        else:
            x = 0
            y += 1
    showImage(pixels)
    
def createNewImage(image, size=20):
    photos_average = avgPixelsPhoto(size)
    main_photo_average = getBlockPixels(image ,size, photos_average)
    
if __name__ == "__main__":
    main_image = Image.open("windows.jpg")
    print(f"Grandezza dell'immagine: {main_image.height} x {main_image.width}")    
    createNewImage(main_image)

