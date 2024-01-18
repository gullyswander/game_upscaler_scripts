
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from pathlib import Path

def count_fully_transparent_pixels(image_path):
    try:
        with Image.open(image_path) as img:
            # Ensure the image has an alpha channel
            if img.mode in ('RGBA', 'LA'):
                alpha = img.getchannel('A')
                # Count the number of fully transparent pixels (alpha = 0)
                transparent_pixels = sum(pixel == 0 for pixel in alpha.getdata())
                total_pixels = img.width * img.height
                return transparent_pixels/total_pixels
            else:
                print("Image does not have an alpha channel.")
                return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def calculate_alpha_percentage(image_path):
    with Image.open(image_path) as img:
        if img.mode != 'RGBA':
            return 0
        print("*"*80)
        alpha = img.split()[-1]
        transparent_pixels = sum(pixel < 255 for pixel in alpha.getdata())
        print(f"t:{transparent_pixels}")
        total_pixels = img.width * img.height
        print(total_pixels)
        percentage = (transparent_pixels / total_pixels) * 100
        color_count = len(img.getcolors(maxcolors=100000)) if img.getcolors(maxcolors=100000) else 0
        print(color_count)

        return percentage, color_count

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        alpha_percentage, color_count = calculate_alpha_percentage(file_path)
        full_alpha_percentage = count_fully_transparent_pixels(file_path)
        result_label.config(text=f"Alpha Trans.: {alpha_percentage:.2f}% | Full Trans: {full_alpha_percentage}| Color Count: {color_count} ")

# Set up the tkinter GUI
root = tk.Tk()
root.title("Alpha Transparency Checker")
open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack()

result_label = tk.Label(root, text="Alpha Transparency: ")
result_label.pack()

root.mainloop()
