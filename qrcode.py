import fitz  # PyMuPDF
from pyzbar.pyzbar import decode  # For QR code detection
from PIL import Image  # For image processing
import io
import openpyxl  # For Excel file handling
import os

def extract_qrcodes_to_excel(pdf_file, output_excel, dpi=300):
    # Open the PDF
    doc = fitz.open(pdf_file)

    # Create a new Excel workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QR Code Data"
    
    # Write the header row
    ws.append(['Page', 'QR Code Data'])

    # Iterate through each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Increase DPI for better resolution
        zoom = dpi / 72  # Scale factor to increase resolution (72 is default DPI)
        mat = fitz.Matrix(zoom, zoom)

        # Render page to an image (as a pixmap) with higher DPI
        pix = page.get_pixmap(matrix=mat)

        # Convert pixmap to PIL image for QR code detection
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Detect QR codes using pyzbar
        qrcodes = decode(img)

        # If QR codes are found, log their data and page number
        if qrcodes:
            print(f"Page {page_num + 1}: Found {len(qrcodes)} QR codes")
            for qrcode in qrcodes:
                qr_data = qrcode.data.decode('utf-8')  # QR code data
                qr_rect = qrcode.rect  # QR code location (x, y, width, height)
                print(f"QR Code Data: {qr_data}")

                # Write the page number and QR code data to the Excel file
                ws.append([page_num + 1, qr_data])
        else:
            print(f"Page {page_num + 1}: No QR codes found")

    # Save the Excel file
    wb.save(output_excel)
    print(f"All QR code data saved to {output_excel}")

def process_pdfs_in_folder(folder_path, output_folder):
    # Walk through the directory recursively to find all PDF files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_file_path = os.path.join(root, file)
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # For Windows
                
                print(f"Processing: {pdf_file_path}")
                
                # Generate an output Excel file path for each PDF file
                output_excel_path = os.path.join(desktop_path, "qrcodes", f"{os.path.splitext(file)[0]}_qrcodes.xlsx")
                
                # Extract QR codes from the PDF and save to the Excel file
                extract_qrcodes_to_excel(pdf_file_path, output_excel_path, dpi=200)

# Example usage
folder_path = "pdf2"  # Replace with the folder you want to search
#output_folder = "excell"  # Replace with where you want to save the Excel files
output_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop',"qrcodes")
# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process all PDFs in the folder recursively
process_pdfs_in_folder(folder_path, output_folder)
