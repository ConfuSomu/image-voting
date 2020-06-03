# This Python program is based on features added in Python 3.5. Python 3.7 is recommanded.
# Requires Pillow >= 6.0.0 for ImageOps.exif_transpose() in utils.py
from PIL import Image
import math
from os import walk, listdir
from os.path import isfile, join
from utils import is_animated, rotate, combineImages, animate, getFps, avgFps

ROOT_DIR = 'images' # Directory containing subdirectories with images
#FILE_FMT = '{root}/{subdir} - {frame}.png' # Format string for output image
FILE_FMT = '/tmp/{root}/{subdir} - {frame}.png' # Format string for output image
TEXT_OVERLAY = ['Love', 'Like', 'Dislike', 'Haha', '!!', '?'] # Overlays to apply on the images, in this case: iMessage reactions

# Canvas parameters
CANVAS_ATT = {}
CANVAS_ATT["FONT"] = {}

CANVAS_ATT["MODE"]     = 'RGB'
CANVAS_ATT["COLOR"]    = 0
CANVAS_ATT["COLS"]     = 3    # Number of colums
CANVAS_ATT["WIDTH"]    = 500  # Total width
CANVAS_ATT["C_HEIGHT"] = 200  # Cell height

CANVAS_ATT["FONT"]["FILE"] = 'Jost-Regular.ttf' # TrueType/OpenType font
CANVAS_ATT["FONT"]["SIZE"] = 13 # Size in points, this should be set in proportion to the cell size
CANVAS_ATT["FONT"]["COLOR"] = 255 # Fill color of the font
CANVAS_ATT["FONT"]["S_COLOR"] = 0 # Color of the text stroke
CANVAS_ATT["FONT"]["S_WIDTH"] = 1 # Width of the text stroke

CANVAS_ATT["ROWS"] = None
CANVAS_ATT["HEIGHT"] = None
CANVAS_ATT["C_WIDTH"] = CANVAS_ATT["WIDTH"]/CANVAS_ATT["COLS"]

# FFmpeg parameters
FFMPEG = {}
FFMPEG["FFMPEG"] = 'ffmpeg' # Location of the ffmpeg binary
FFMPEG["CODEC"] = 'ffv1' # Codec to use for the generated video, prefer a lossless one for better fidelity
#FFMPEG["FILENAME"] = '{root}/{subdir}.avi' # Filename format string
FFMPEG["FILENAME"] = '/tmp/{root}/{subdir}.avi' # Filename format string
FFMPEG["FPS"] = '30' # FPS of the resulting video file

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
            try:
                images.append(Image.open(file))
            except OSError:
                # Ignore non image files
                pass
        
        CANVAS_ATT["ROWS"] = math.ceil(len(images)/CANVAS_ATT["COLS"])
        CANVAS_ATT["HEIGHT"] = CANVAS_ATT["ROWS"]*CANVAS_ATT["C_HEIGHT"]
        print(CANVAS_ATT) # Debug
        
        # Rotate non-animated images and add attribute to tell if animated
        taggedImages = []
        for image in images:
            if not is_animated(image):
                taggedImages.append([rotate(image), False, None]) # Append rotated image
            else:
                taggedImages.append([image, True, getFps(image)]) # Append original image
        del images # Unused
        
        # Create a canvas image that will contain the other images
        canvas = Image.new(CANVAS_ATT["MODE"], (CANVAS_ATT["WIDTH"], CANVAS_ATT["HEIGHT"]), CANVAS_ATT["COLOR"])
        
        frames = combineImages(canvas, taggedImages, CANVAS_ATT, TEXT_OVERLAY, [FILE_FMT, [root, subdir]])
        
        # If multiple frames have been created,
        # Than create a video file…
        if frames > 1:
            fps = avgFps(taggedImages)
            animate(frames, fps, FFMPEG, CANVAS_ATT, [FILE_FMT, [root, subdir]])
