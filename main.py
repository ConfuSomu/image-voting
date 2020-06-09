# This Python program is based on features added in Python 3.5. Python 3.7 is recommanded.
# Requires Pillow >= 6.0.0 for ImageOps.exif_transpose() in utils.py
from PIL import Image
import math
from os import walk, listdir
from os.path import isfile, join
import config
from image import is_animated, rotate, combineImages
from video import animate, getFps, avgFps

# Load configuration
args = config.args()
userconf = config.user(args.config)
CONFIG = config.general(args, userconf)
CANVAS_ATT = config.canvas(args, userconf)
FFMPEG = config.ffmpeg(args, userconf)

# Walk in subdirectories (jour 1, jour 2, ...)
for root, dirs, _ in walk(CONFIG["ROOT_DIR"]):
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
        
        frames = combineImages(canvas, taggedImages, CANVAS_ATT, CONFIG["TEXT_OVERLAY"], [CONFIG["FILE_FMT"], [root, subdir]])
        
        # If multiple frames have been created,
        # Than create a video file…
        if frames > 1:
            fps = avgFps(taggedImages)
            animate(frames, fps, FFMPEG, CANVAS_ATT, [CONFIG["FILE_FMT"], [root, subdir]])
