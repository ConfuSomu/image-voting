# Requires Pillow >= 6.0.0 for ImageOps.exif_transpose() in utils.py
from PIL import Image
from os import walk, listdir
from os.path import isfile, join
from utils import is_animated, rotate, combineImages

ROOT_DIR = 'images' # Directory containing subdirectories with images
TEXT_OVERLAY = ['Love', 'Like', 'Dislike', 'Haha', '!!', '?'] # iMessage reactions

IMAGE_MODE = 'RGB'
IMAGE_COLOR = 0

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
                print("-- Not image") # Debug
                pass # Ignore non image files
        
        # Rotate images based on EXIF data and add attribute to tell if animated
        rimages = []
        taggedImages = []
        for image in images:
            rotated = rotate(image)
            rimages.append(rotated)
            if not is_animated(image):
                taggedImages.append([rotated, False]) # Append rotated image
            else:
                taggedImages.append([image, True]) # Append original
        del images # Stops being used from the point on
        
        #rimages = [rotate(image) for image in images]
        
        # Find the biggest height and total width
        height = width = 0
        for image in rimages:
            width += image.width
            if image.height > height:
                height = image.height
        print("biggest height: {}, total width: {}".format(height, width))
        
        # Create a canvas image that will contain the other images
        canvas = Image.new(IMAGE_MODE, (width, height), IMAGE_COLOR)
        
        # Create an image that has the [height of the biggest image in the dir] and the [width of all of the images combined in the dir]
        # If there is an animated image (GIF):
        
        combineImages(canvas, taggedImages)
        
            # For each frame of the GIF:
                # Place in the created image each of the dir's images and the current frame of the GIF
                # Overlay the images with the text (black with 0.5 alpha) "HaHa" for the first image, "Yes" for the second, "No" for the third... (iMessage reactions)
                # Save the image as a TIFF with the dir's name and current frame number
                
        # Else:
            # Place in the created image each of the dir's images
            # Overlay the images with the text (black with 0.5 alpha) "HaHa" for the first image, "Yes" for the second, "No" for the third... (iMessage reactions for voting)
            # Save the image as a TIFF with the dir's name