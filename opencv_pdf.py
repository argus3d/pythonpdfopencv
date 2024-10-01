#adaptado do opencv_img que le a partir de imagens geradas pelo pdfextract.pdf

import cv2
import numpy as np
from PIL import Image  # For image processing
import os
import io
import fitz  # PyMuPDF

import tkinter as tk
from tkinter import filedialog, messagebox
import io  # Import io for handling byte conversion

def select_directory():
    """Prompt the user to select a directory and return the selected path."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Input Directory")
    return directory

# Load the icon you want to search for
# Load the icon you want to search for
icon_image = cv2.imread('icon2.png', cv2.IMREAD_UNCHANGED)

# Check if the icon image was loaded properly
if icon_image is None:
    raise ValueError("Could not load icon image. Check the file path.")

# Check if the image is already in grayscale
if len(icon_image.shape) == 2:
    # It's already a single-channel image
    icon_image_gray = icon_image
else:
    # Convert to grayscale
    icon_image_gray = cv2.cvtColor(icon_image, cv2.COLOR_BGR2GRAY)

# Set threshold for detection
threshold = 0.7

# Define the directory with images
input_directory = 'pdf'
output_directory = 'output_zapcodes'
   
# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
def processa_zapcodes(pdf_file, filename,output_directory,contagem):
    
     # Getting the user's desktop path 
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # For Windows
    
    doc = fitz.open(pdf_file)
    name_without_extension, _ = os.path.splitext(filename)
    output_directory = os.path.join(desktop_path, "zapcodes", filename)

     # Ensure output directory exists


    # Load icon image
    icon_image = cv2.imread('icon2.png', cv2.IMREAD_UNCHANGED)
    
    # Check if the icon image was loaded properly
    if icon_image is None:
        raise ValueError("Could not load icon image. Check the file path.")

    # Convert icon image to grayscale if it's in color
    if len(icon_image.shape) == 2:
        icon_image_gray = icon_image
    else:
        icon_image_gray = cv2.cvtColor(icon_image, cv2.COLOR_BGR2GRAY)
        
        
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        status_label.config(text=f"PDF: {pdf_file}")
        number_label.config(text=f"{page_num} de {doc.page_count} paginas")
        root.update()
        # Render page as image (pixmap)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        # Convert the PIL Image to a NumPy array
        page_image = np.array(img)

        # Convert RGB to BGR (OpenCV uses BGR format)
        page_image = cv2.cvtColor(page_image, cv2.COLOR_RGB2BGR)

        # Convert to grayscale for template matching
        page_image_gray = cv2.cvtColor(page_image, cv2.COLOR_BGR2GRAY)

        # Ensure both images are of the same type (CV_8U)
        page_image_gray = page_image_gray.astype(np.uint8)

        # Perform template matching
        result = cv2.matchTemplate(page_image_gray, icon_image_gray, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        # If matches are found, draw rectangles and save the image
        if locations[0].size > 0:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            output_file_path = os.path.join(output_directory, f"{name_without_extension}_page_{page_num + 1}.png")  # Ensuring the PNG extension

            # Save the image with a proper extension
            if cv2.imwrite(output_file_path, page_image):
                print(f"Processed and saved: {output_file_path}")
                found_label.config(text=f"Zapcode encontrado: {output_file_path}")
                root.update()
            else:
                print(f"Failed to save image: {output_file_path}")
        else:
            print(f"No icons found in: {filename}")
                   
def process_pdfs_in_folder(folder_path,output_directory):
    # Walk through the directory recursively to find all PDF files
    for dirpath, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_file_path = os.path.join(dirpath, file)
                print(f"Processing: {pdf_file_path}")
                
                # Extract QR codes from the PDF and save to the Excel file
                processa_zapcodes(pdf_file_path, os.path.splitext(file)[0], output_directory,files.count)
                
# Example usage


# Process all PDFs in the folder recursively
#process_pdfs_in_folder(input_directory)


def start_process():
    input_directory = select_directory()
    root.update() 
    #start_button = tk.Button(root, text="Iniciar Processo", command=start_process)
    #start_button.pack(pady=10)
    if input_directory:
        print(f"Selected directory: {input_directory}")
        output_directory = os.path.join(input_directory, "output")  # Example of setting an output directory
        start_button.pack_forget()
        
        
        # Now call your PDF processing function here, e.g.:
        process_pdfs_in_folder(input_directory, output_directory)
        
        # Notify user that processing has completed

        messagebox.showinfo("Process sucesso!\nConfirao completo a pasta", " 'zapProcessamentocodes' concluído na sua com sucesso Área de!\n Trabalho para os arquivosVerifique de saída a pasta.")
        start_button.pack(pady=10)
        close_button.pack(pady=10)
        root.update() 
    else:
        print("No directory selected.")
def close_application():
    root.quit()
       
root = tk.Tk()
root.title("Status do Processo")
status_label = tk.Label(root, text="Clique no botão para iniciar o processo.")
status_label.pack(pady=30)
number_label = tk.Label(root, text="...")
number_label.pack(pady=5)
found_label = tk.Label(root, text="...")
found_label.pack(pady=30)
start_button = tk.Button(root, text="Iniciar Processo", command=start_process)
start_button.pack(pady=10)

# Button to close the application
close_button = tk.Button(root, text="Fechar", command=close_application)
close_button.pack_forget()  # Initially hide the close button

# Bind the window close event to the close_application function
root.protocol("WM_DELETE_WINDOW", close_application)
root.mainloop()