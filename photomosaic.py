from PIL import Image



if __name__ == "__main__":
    inputImage = Image.open("windows.jpg")
    print(f"Grandezza dell'immagine: {inputImage.height} x {inputImage.width}")