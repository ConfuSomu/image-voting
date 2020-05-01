from PIL import Image
import os

# Walk in subdirectories (jour 1, jour 2, ...)
    # For each subdir
        # Read all the image files in the dir
        # Create an image that has the [height of the biggest image in the dir] and the [width of all of the images combined in the dir]
        # If there is an animated image (GIF):
            # For each frame of the GIF:
                # Place in the created image each of the dir's images and the current frame of the GIF
                # Overlay the images with the text (black with 0.5 alpha) "HaHa" for the first image, "Yes" for the second, "No" for the third... (iMessage reactions)
                # Save the image as a TIFF with the dir's name and current frame number
        # Else:
            # Place in the created image each of the dir's images
            # Overlay the images with the text (black with 0.5 alpha) "HaHa" for the first image, "Yes" for the second, "No" for the third... (iMessage reactions for voting)
            # Save the image as a TIFF with the dir's name