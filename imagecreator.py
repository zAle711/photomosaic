from email.mime import image
from setup import MAIN_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER
import util
import numpy as np
from PIL import Image
from scipy.spatial import distance

main_image_path = util.getMainImage()
input_images_path = util.getInputImages()

images_average = {}


def createImage():
    
    #open and resize main image
    main_image = Image.open(main_image_path)
    new_size = util.getNewSize(main_image.size)
    if new_size:
        main_image = main_image.resize(new_size)
    
    #get width and height of a block of pixels
    block_size = util.getBlockSize(main_image.size)
    
    #resize input images and place them in a folder
    resizeInputImage(block_size)
    averageInputImages()
    transformImage(main_image, block_size)
    print("Image Created!")
    util.deleteTempImages()

""" Loop throught every block of pixels and replace it with the matching image  """
def transformImage(main_image, block_size):
    main_image_pixels = np.array(main_image)
    COLUMN_LIMIT = (main_image.width / block_size) - 1
    ROW_LIMIT = (main_image.height / block_size)
    column = 0
    row = 0
    count = 0

    while row < ROW_LIMIT:

        block = main_image_pixels[row * block_size: row * block_size + block_size, column * block_size: column * block_size + block_size]
        block_average = computeAverage(block)
        getMatchingImage(block_average)
        main_image_pixels[row * block_size: row * block_size + block_size, column * block_size: column * block_size + block_size] = getMatchingImage(block_average)

        if column < COLUMN_LIMIT:
            column += 1
        else:
            column = 0
            row += 1

    saveImage(main_image_pixels)

""" Given the average of a block of pixels finds the best match in the given images """
def getMatchingImage(block_average):

    min_distance = float("inf")
    best_match = ""

    for image_name, image_average in images_average.items():
        euclian_distance = distance.euclidean(block_average, image_average)
        if euclian_distance < min_distance:
            min_distance = euclian_distance
            best_match = image_name
    image_path = TEMP_FOLDER.joinpath(best_match)
    return np.array(Image.open(image_path))
    
""" Resize every input image, new size depends on the main image """
def resizeInputImage(block_size):
    block_size = (block_size, block_size)
    for image_path in input_images_path:
        resized_image_path = TEMP_FOLDER.joinpath(image_path.name)
        input_image = Image.open(image_path)
        resized_image = input_image.resize(block_size)
        resized_image.save(resized_image_path)

"""Calculates the average of every input images and saves it in a dictionary  """
def averageInputImages():   
    for img in TEMP_FOLDER.iterdir():
        pixels = np.array(Image.open(img))
        images_average[img.name] = computeAverage(pixels)

"""Calculates the average of a chunk of pixels"""
def computeAverage(pixels):
    average = np.zeros(3)
    for row in pixels:
        for p in row:
            average += p
    average /= pixels.size / 3
    return average.astype(np.uint8)

""" Create and save image from pixels """
def saveImage(pixels):
    new_image = Image.fromarray(pixels) 
    new_image.save(OUTPUT_FOLDER.joinpath('photomosaic.jpg'))