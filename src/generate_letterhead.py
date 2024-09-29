from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Function to add text to PDF
def add_text_to_pdf(address, subject, body, input_pdf="./letterhead/base.pdf", output_pdf="./letterhead/populated.pdf"):
    # Read the existing PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Create a new PDF to overlay the text
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Set font and text properties
    can.setFont("Times-Bold", 14)  # Bold font for the subject

    # Calculate the width of the subject string
    subject_width = can.stringWidth(subject, "Times-Bold", 14)
    
    # Center the subject text (x position is half the page width minus half the text width)
    page_width, page_height = letter[0], letter[1]  # Letter page width
    # print(page_width, page_height)
    x_subject = (page_width - subject_width) / 2  # Centered position

    # Draw the centered subject
    can.drawString(x_subject, 550, f"{subject}")
    
    # Set font for normal text (address and body)
    can.setFont("Times-Roman", 12)
    
    # Right-align the address
    address_width = can.stringWidth(address, "Times-Roman", 12)
    # print(address_width)
    can.drawString(page_width - address_width - 65, 650, address)  # Adjust x position for right-align
    
    # Add the body text
    can.drawString(65, 520, body)
    
    # Save the overlay PDF
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    
    # Read the overlay PDF
    overlay = PdfReader(packet)
    overlay_page = overlay.pages[0]
    
    # Merge the overlay with the original PDF (on the first page only)
    first_page = reader.pages[0]
    first_page.merge_page(overlay_page)
    writer.add_page(first_page)
    
    # If there are multiple pages in the input, add the remaining pages
    for page_num in range(1, len(reader.pages)):
        writer.add_page(reader.pages[page_num])
    
    # Save the result to a new PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)