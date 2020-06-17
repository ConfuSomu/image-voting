import argparse, json

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default="images",
                        help="Directory containing images")
    parser.add_argument('-c', '--config',
                        help="Configuration file")
    return parser.parse_args()

def user(filename):
    if filename is None:
        return {}
    
    try:
        return json.load(open(filename))
    except OSError:
        print("Warning: No configuration file called {}".format(filename))
        return {}

def general(args, userconf):
    default = {}
    default["ROOT_DIR"] = args.directory # Directory containing subdirectories with images
    default["FILE_FMT"] = '{root}/{subdir} - {frame}.png' # Format string for output image
    default["TEXT_OVERLAY"] = ['Love', 'Like', 'Dislike', 'Haha', '!!', '?'] # Overlays to apply on the images, in this case: iMessage reactions
    
    try:
        return {**default, **userconf['general']}
    except KeyError:
        return default

def canvas(args, userconf):
    default = {}
    default["FONT"] = {}

    default["MODE"]     = 'RGB'
    default["COLOR"]    = 0
    default["COLS"]     = 3    # Number of colums
    default["WIDTH"]    = 500  # Total width
    default["C_HEIGHT"] = 200  # Cell height

    default["FONT"]["FILE"] = 'Jost-Regular.ttf' # TrueType/OpenType font
    default["FONT"]["SIZE"] = 13 # Size in points, this should be set in proportion to the cell size
    default["FONT"]["COLOR"] = 255 # Fill color of the font
    default["FONT"]["S_COLOR"] = 0 # Color of the text stroke
    default["FONT"]["S_WIDTH"] = 1 # Width of the text stroke

    default["ROWS"] = None
    default["HEIGHT"] = None
    
    try:
        conf = {**default, **userconf['canvas']}
        
        try:
            conf["FONT"] = {**default["FONT"], **userconf['canvas']["FONT"]}
        except KeyError:
            # No font config has been defined in the config file, use the default.
            conf["FONT"] = default["FONT"]
        
        conf["C_WIDTH"] = conf["WIDTH"]/conf["COLS"]
        return conf
        
    except KeyError:
        default["C_WIDTH"] = default["WIDTH"]/default["COLS"]
        return default

def ffmpeg(args, userconf):
    default = {}
    default["FFMPEG"] = 'ffmpeg' # Location of the ffmpeg binary
    default["CODEC"] = 'ffv1' # Codec to use for the generated video, prefer a lossless one for better fidelity
    default["FILENAME"] = '{root}/{subdir}.avi' # Filename format string
    default["FPS"] = '30' # FPS of the resulting video file
    
    try:
        return {**default, **userconf['ffmpeg']}
    except KeyError:
        return default
