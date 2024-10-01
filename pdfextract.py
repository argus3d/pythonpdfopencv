import fitz  # PyMuPDF
import os

output_directory = 'output_paginas'

input_directory = 'pdf'

# Create output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)



# Iterate through pages
for filename in os.listdir(input_directory):
    if filename.endswith('.pdf'):
        print(f"PDF: {filename}")
        input_file_path = os.path.join(input_directory, filename)  # Construct full file path
        doc = fitz.open(input_file_path)
        name_without_extension, _ = os.path.splitext(filename)
        if not os.path.exists(os.path.join(output_directory, name_without_extension)):
            os.makedirs(os.path.join(output_directory, name_without_extension))
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
    
            # Render page as image (pixmap)
            pix = page.get_pixmap()
    
            # Save or process the image
            output_file_path = os.path.join(os.path.join(output_directory, name_without_extension), f"page_{page_num}.png")
            pix.save(output_file_path)
