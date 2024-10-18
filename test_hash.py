from imagehash import average_hash
from PIL import Image
from imagehash import phash

def image_hash(image_path):
    image = Image.open(image_path)
    return phash(image)

def image_hash2(image_path):
    image = Image.open(image_path)
    return average_hash(image)



