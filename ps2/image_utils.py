import os
from pathlib import Path
from PIL import Image


def count_fully_transparent_pixels(image_path):
    try:
        with Image.open(image_path) as img:
            # Ensure the image has an alpha channel
            if img.mode in ('RGBA', 'LA'):
                alpha = img.getchannel('A')
                # Count the number of fully transparent pixels (alpha = 0)
                transparent_pixels = sum(pixel == 0 for pixel in alpha.getdata())
                total_pixels = img.width * img.height
                return transparent_pixels / total_pixels
            else:
                print("Image does not have an alpha channel.")
                return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_image_properties(file_path):
    with Image.open(file_path) as img:
        dimensions = img.size
        color_count = len(img.getcolors(maxcolors=100000)) if img.getcolors(maxcolors=100000) else 0
    return dimensions, color_count
