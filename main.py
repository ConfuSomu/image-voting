# Requires Pillow >= 6.0.0 for ImageOps.exif_transpose() in utils.py
from PIL import Image
from os import walk, listdir
from os.path import isfile, join
from utils import is_animated, rotate, combineImages

ROOT_DIR = 'images' # Directory containing subdirectories with images
TEXT_OVERLAY = ['Love', 'Like', 'Dislike', 'Haha', '!!', '?'] # iMessage reactions

# Canvas parameters
CANVAS_MODE = 'RGB'
CANVAS_COLOR = 0

# Walk in subdirectories (jour 1, jour 2, ...)
for root, dirs, _ in walk(ROOT_DIR):
    print("dirs in root: "+str(dirs)) # Debug
    
    # For each subdir
    for subdir in dirs:
        dir = join(root, subdir)
        print("current subdir: "+str(dir)) # Debug
        
        # Read all the files in the dir & keep only images
        images = []
        for file in listdir(dir):
            file = join(dir, file)
            print("current file: "+str(file)) # Debug
            try:
                images.append(Image.open(file))
            except OSError:
                # Ignore non image files
                print("-- Not image") # Debug
                pass
        
        # Rotate images based on EXIF data and add attribute to tell if animated
        rimages = [] # This line and the line below can't be put on one line, as this causes a strange bug
        taggedImages = []
        for image in images:
            rotated = rotate(image)
            rimages.append(rotated)
            if not is_animated(image):
                taggedImages.append([rotated, False]) # Append rotated image
            else:
                taggedImages.append([image, True]) # Append original image
        del images # Unused
        
        # Find the biggest height and total width
        height = width = 0
        for image in rimages:
            width += image.width
            if image.height > height:
                height = image.height
        print("biggest height: {}, total width: {}".format(height, width))
        
        # Create a canvas image that will contain the other images
        canvas = Image.new(CANVAS_MODE, (width, height), CANVAS_COLOR)
        
        combineImages(canvas, taggedImages)