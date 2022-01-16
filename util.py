import shutil
import sys
from setup import MAIN_PHOTO_FOLDER, INPUT_FOLDER, TEMP_FOLDER
import math

IMAGE_SIZES = [
    [256,144],
    [426,240],
    [640,360],
    [854,480],
    [1280,720],
    [1920,1080]
]

def getNewSize(img_size):
    img_width, img_height = img_size
    for size in reversed(IMAGE_SIZES):
        w,h = size
        if img_width == w and img_height == h:
            return None
        else:
            if img_width <= w and img_height <= h:
                return size

def getBlockSize(img_size):
    w,h = img_size
    common_divisors = []
    for i in range(1, min(w,h) + 1):
        if w%i==h%i==0:
            common_divisors.append(i)
    return common_divisors[ int( len(common_divisors)* 0.6 ) ]

def getMainImage():
    if any(MAIN_PHOTO_FOLDER.iterdir()):
        return next(MAIN_PHOTO_FOLDER.iterdir())
    else:
        print(f"Cannot find photo in {MAIN_PHOTO_FOLDER.resolve()}")
        sys.exit()

def getInputImages():
    if any(INPUT_FOLDER.iterdir()):
        return [file for file in INPUT_FOLDER.iterdir()]
    else:
        print(f"Cannot find photo in {INPUT_FOLDER.resolve()}")
        sys.exit()

def deleteTempImages():
    if TEMP_FOLDER.is_dir():
        shutil.rmtree(TEMP_FOLDER)
