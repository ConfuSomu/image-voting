from PIL import ImageOps, ImageDraw, ImageFont

def is_animated(im):
    try:
        im.seek(1)
        im.seek(0) # Rewind
        return True
    except EOFError:
        return False

def rotate(im):
    # Rotate the image using the EXIF data.
    
    # The following lines are used to bypass a bug in the Pillow library.
    # This fixes:
    #    [...]
    #    File "/home/pi/.local/lib/python3.7/site-packages/PIL/TiffImagePlugin.py", line 808, in tobytes
    #    data = self._write_dispatch[typ](self, *values)
    #    TypeError: write_undefined() takes 2 positional arguments but 5 were given
    # See https://github.com/python-pillow/Pillow/issues/4346#issuecomment-575049324
    # for more information.
    
    exif = im.getexif()
    # Remove all exif tags
    for k in exif.keys():
        if k != 0x0112:
            exif[k] = None # If I don't set it to None first (or print it) the del fails for some reason. 
            del exif[k]
    # Put the new exif object in the original image
    new_exif = exif.tobytes()
    im.info["exif"] = new_exif
    
    return ImageOps.exif_transpose(im)

def resize(im, CANVAS_ATT):
    # Resize using the ratio between the image and grid cell
    ratioW = im.width / CANVAS_ATT["C_WIDTH"]
    ratioH = im.height / CANVAS_ATT["C_HEIGHT"]
    
    if (ratioW > ratioH):
        height = im.height/ratioW
        width = CANVAS_ATT["C_WIDTH"]
    else:
        width = im.width/ratioH
        height = CANVAS_ATT["C_HEIGHT"]
    
    height = int(round(height))
    width = int(round(width))
    return im.resize((width, height))

def center(im, CANVAS_ATT, dx, dy):
    # Delta from top-left corner is required to correctly position image.
    return (int(round((CANVAS_ATT["C_WIDTH"]/2)-(im.width/2)+dx)),int(round((CANVAS_ATT["C_HEIGHT"]/2)-(im.height/2)+dy)))

def textOverlay(draw, CANVAS_ATT, font, dx, dy, text):
    x = dx+2
    y = dy+2
    
    return draw.text((x, y), text, fill=CANVAS_ATT["FONT"]["COLOR"], font=font, stroke_width=CANVAS_ATT["FONT"]["S_WIDTH"], stroke_fill=CANVAS_ATT["FONT"]["S_COLOR"])

def save(im, file, frame):
    FILE_FMT = file[0]
    DIRS = file[1]
    frame = str(frame).zfill(4)
    
    print("Saving frame {}...".format(frame))
    im.save(FILE_FMT.format(root=DIRS[0], subdir=DIRS[1], frame=frame))

def combineImages(canvas, images, CANVAS_ATT, TEXT_OVERLAY, SAVING):
    # Combine images on the canvas
    i = EOFCount = maxEOF = 0
    for image in images:
        if image[1]: # is_animated attribut
            maxEOF += 1
    
    # Do not allow EOF when no animated images are present
    if maxEOF == 0:
        EOFCount = -1
    
    # Load font
    font = ImageFont.truetype(CANVAS_ATT["FONT"]["FILE"], CANVAS_ATT["FONT"]["SIZE"])
    
    # While there are frames left to draw…
    while not EOFCount >= maxEOF:
        generated = canvas.copy()
        draw = ImageDraw.Draw(generated)
        
        EOFCount = j = 0
        for row in range(0, CANVAS_ATT["ROWS"]):
            for col in range(0, CANVAS_ATT["COLS"]):         
                dx = col*CANVAS_ATT["C_WIDTH"]
                dy = row*CANVAS_ATT["C_HEIGHT"]
                try:
                    image = images[j]
                    if image[1]: # is_animated attribut
                        try:
                            # Try to seek each animated image
                            image[0].seek(i)
                        except EOFError:
                            image[0].seek(0)
                            EOFCount += 1
                            print("EOFError, count={}, maxEOF={}, len(images)={}".format(str(EOFCount),str(maxEOF),str(len(images))))
                    
                    toPaste = image[0]
                    toPaste = resize(toPaste, CANVAS_ATT) # Resize image for it to be able to fit in a cell
                    generated.paste(toPaste, center(toPaste, CANVAS_ATT, dx, dy)) # Paste the image in the center of the cell
                    try:
                        textOverlay(draw, CANVAS_ATT, font, dx, dy, TEXT_OVERLAY[j])
                    except IndexError:
                        # No text to overlay…
                        pass
                except IndexError:
                    # No images left to draw…
                    pass
                
                j += 1
        
        # Save frames here to avoid possible memory exhaustion
        # No need to combine draw and generated, as ImageDraw modifies the image inplace
        save(generated, SAVING, i)
        
        x = 0
        i += 1
        
        # To avoid waiting for an eternity… (dev)
        if i > 10:
            break
        
    return i # Total frames (with 0 as the first frame)
