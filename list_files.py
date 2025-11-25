import os

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))

folder = "."

for filename in os.listdir(folder):
    if is_image(filename):
        print("Image file:", filename)
    else:
        print("Not an image:", filename)
