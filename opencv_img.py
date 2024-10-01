import cv2
import numpy as np
import os

# Load the icon you want to search for
icon_image = cv2.imread('icon2.png', 0)

# Set threshold for detection
threshold = 0.7

# Define the directory with images
input_directory = 'output_paginas'
output_directory = 'output_zapcodes'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through all files in the directory and subdirectories
for dirpath, dirnames, filenames in os.walk(input_directory):
    for filename in filenames:
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            # Load the PDF page (now rendered as image)
            page_image = cv2.imread(os.path.join(dirpath, filename), 0)

            # Perform template matching
            result = cv2.matchTemplate(page_image, icon_image, cv2.TM_CCOEFF_NORMED)

            # Check for matches
            locations = np.where(result >= threshold)

            # If matches are found, draw rectangles and save the image
            if locations[0].size > 0:
                #desenha retangulo na imagem:
                #for pt in zip(*locations[::-1]):
                    #cv2.rectangle(page_image, pt, (pt[0] + icon_image.shape[1], pt[1] + icon_image.shape[0]), (0, 255, 255), 2)

                # Save the resulting image in the output folder
                # Change output path to maintain folder structure
                output_file_path = os.path.join(output_directory, os.path.relpath(os.path.join(dirpath, filename), input_directory))
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                cv2.imwrite(output_file_path, page_image)
                print(f"Processed and saved: {output_file_path}")
            else:
                print(f"No icons found in: {filename}")