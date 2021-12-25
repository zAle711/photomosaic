from PIL import Image
import numpy as np
import os
import pathlib
from scipy.spatial import distance
import shutil

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
        block_average = computeAvergage(block)
        image = getMatchingImage(photos_average, block_average)
        img_pixels = np.array(Image.open(image))
        print(f"x:{x} y:{y} row:{row} column:{column} blockShape:{block.shape} imgShape: {img_pixels.shape}")
        pixels[row: (row + size) , column : (column + size) ] = img_pixels
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
    path = pathlib.Path().parent.resolve()
    photo = ""
    
    for photo_name, photo_average in photos_average.items():
        #I use the euclidean distance to find the best match for a given block
        euclidean_distance = distance.euclidean(block_average,photo_average)
        if euclidean_distance < min_distance:
            min_distance = euclidean_distance
            photo = photo_name
    return os.path.join(path,"temp" ,photo)   
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
    
def resizeImagesAndCalculateAverage(size):
    """ Resize all the images to the given size
    
    """
    parent_path = pathlib.Path().parent.resolve()
    photos_folder_path = os.path.join(parent_path, "foto")
    temp_folder_path = os.path.join(parent_path, "temp")

    if not os.path.isdir(temp_folder_path):
        os.mkdir(temp_folder_path)
    
    all_photos = os.listdir(photos_folder_path) 
    all_photo_average = {}
    for photo in all_photos:
        img = Image.open(os.path.join(photos_folder_path, photo))
        img = img.resize( (size, size) )
        all_photo_average[photo] = computeAvergage(np.array(img))
        img.save(os.path.join(temp_folder_path, photo))
    return all_photo_average
    
def deleteTempImages():
    temp_folder_path = os.path.join(pathlib.Path().parent.resolve(), "temp")
    if os.path.isdir(temp_folder_path):
        shutil.rmtree(temp_folder_path)

def createNewImage(image, size=30):
    photos_average = resizeImagesAndCalculateAverage(size)
    getBlockPixels(image, size, photos_average)
    deleteTempImages()
    
if __name__ == "__main__":
    main_image = Image.open("windows.jpg")
    print(f"Grandezza dell'immagine: {main_image.height} x {main_image.width}")    
    createNewImage(main_image)

