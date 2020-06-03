import subprocess

def getFps(im):
    # Based on https://stackoverflow.com/a/53365469
    im.seek(0)
    frames = duration = 0
    
    while True:
        try:
            frames += 1
            duration += im.info['duration']
            im.seek(frames)
        except EOFError:
            im.seek(0)
            return frames/duration*1000

def avgFps(images):
    numAnim = total = 0
    
    for image in images:
        if image[1] and image[2] is not None: # is_animated and fps attribute
            numAnim += 1
            total += image[2]
    
    return total/numAnim

def animate(frames, fps, FFMPEG, CANVAS_ATT, SAVING):
    IMAGE_FILE_FMT = SAVING[0]
    DIRS = SAVING[1]
    
    inputImages = IMAGE_FILE_FMT.format(root=DIRS[0], subdir=DIRS[1], frame='%04d')
    resolution = '{}x{}'.format(CANVAS_ATT["WIDTH"], CANVAS_ATT["HEIGHT"])
    outputFile = FFMPEG["FILENAME"].format(root=DIRS[0], subdir=DIRS[1])
    startFrame = 0
    
    args = [FFMPEG["FFMPEG"], '-nostdin', '-y',
            '-framerate', str(fps), '-i', inputImages,
            '-start_number', str(startFrame), '-vframes', str(frames),
            '-s', resolution, '-r', FFMPEG["FPS"],
            '-vcodec', FFMPEG["CODEC"], outputFile]
    
    proc = subprocess.run(args, capture_output=True, check = True)
    print(proc) # Debug