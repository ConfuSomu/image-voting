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
    conf = {}
    conf["ROOT_DIR"] = args.directory # Directory containing subdirectories with images
    conf["FILE_FMT"] = '{root}/{subdir} - {frame}.png' # Format string for output image
    conf["TEXT_OVERLAY"] = ['Love', 'Like', 'Dislike', 'Haha', '!!', '?'] # Overlays to apply on the images, in this case: iMessage reactions
    
    try:
        return {**conf, **userconf['general']}
    except KeyError:
        return conf

def canvas(args, userconf):
    conf = {}
    conf["FONT"] = {}

    conf["MODE"]     = 'RGB'
    conf["COLOR"]    = 0
    conf["COLS"]     = 3    # Number of colums
    conf["WIDTH"]    = 500  # Total width
    conf["C_HEIGHT"] = 200  # Cell height

    conf["FONT"]["FILE"] = 'Jost-Regular.ttf' # TrueType/OpenType font
    conf["FONT"]["SIZE"] = 13 # Size in points, this should be set in proportion to the cell size
    conf["FONT"]["COLOR"] = 255 # Fill color of the font
    conf["FONT"]["S_COLOR"] = 0 # Color of the text stroke
    conf["FONT"]["S_WIDTH"] = 1 # Width of the text stroke

    conf["ROWS"] = None
    conf["HEIGHT"] = None
    conf["C_WIDTH"] = conf["WIDTH"]/conf["COLS"]
    
    try:
        return {**conf, **userconf['canvas']}
    except KeyError:
        return conf

def ffmpeg(args, userconf):
    conf = {}
    conf["FFMPEG"] = 'ffmpeg' # Location of the ffmpeg binary
    conf["CODEC"] = 'ffv1' # Codec to use for the generated video, prefer a lossless one for better fidelity
    conf["FILENAME"] = '{root}/{subdir}.avi' # Filename format string
    conf["FPS"] = '30' # FPS of the resulting video file
    
    try:
        return {**conf, **userconf['ffmpeg']}
    except KeyError:
        return conf
