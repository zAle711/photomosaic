import pathlib

MAIN_FOLDER = pathlib.Path().parent.resolve().joinpath('photo')

INPUT_FOLDER = MAIN_FOLDER.joinpath('input')
OUTPUT_FOLDER = MAIN_FOLDER.joinpath('output')
MAIN_PHOTO_FOLDER = MAIN_FOLDER.joinpath('main_photo')
TEMP_FOLDER = MAIN_FOLDER.joinpath('temp_folder')

#Create folders if not exists
MAIN_FOLDER.mkdir(parents=True, exist_ok= True)
INPUT_FOLDER.mkdir(parents=True, exist_ok= True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok= True)
MAIN_PHOTO_FOLDER.mkdir(parents=True, exist_ok= True)
TEMP_FOLDER.mkdir(parents=True, exist_ok= True)