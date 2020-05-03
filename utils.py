from PIL import Image, ImageOps

def is_animated(im):
    try:
        im.seek(1)
        im.seek(0) # Rewind
        return True
    except EOFError:
        return False

def rotate(im):
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

def combineImages(canvas, images):    
    # Place in the created image each of the dir's images and the current frame of the GIF
    x = 0
    i = 0
    EOFCount = 0
    maxEOF = 0
    for image in images:
        if image[1]: # is_animated attribut
            maxEOF += 1
    while not EOFCount >= maxEOF:
        generated = canvas.copy()
        
        for image in images:
            if image[1]: # is_animated attribut
                try:
                    # Try to seek each animated image
                    image[0].seek(i)
                except EOFError:
                    image[0].seek(0)
                    exceptCount += 1
                    print("EOFError, count={}, maxEOF={}, len(images)={}".format(str(exceptCount),str(maxEOF),str(len(images))))
            
            print("Paste image")
            
            # Only rotate animated images, as non animated have been rotated
#             if image[1]:
#                 toPaste = rotate(image[0])
#             else:
#                 toPaste = image[0]
            toPaste = image[0]
            generated.paste(toPaste, (x,0))
            x += toPaste.width
        
        # Save frames here to avoid memory exhaustion
        print("Saving frame {}...".format(str(i)))
        generated.save('/tmp/{},{}.png'.format(str(x),str(i)))
        
        EOFCount = 0
        x = 0
        i += 1
        
        # To avoid waiting for an eternity... (dev)
        if i > 10:
            break
    # Overlay the images with the text (black with 0.5 alpha) "HaHa" for the first image, "Yes" for the second, "No" for the third... (iMessage reactions)
    # Save the image as a TIFF with the dir's name and current frame number