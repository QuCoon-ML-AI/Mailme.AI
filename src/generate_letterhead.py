from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import textwrap

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
    subject_width = can.stringWidth(subject.upper(), "Times-Bold", 14)
    
    # Center the subject text (x position is half the page width minus half the text width)
    page_width, page_height = letter[0], letter[1]  # Letter page width
    # print(page_width, page_height)
    x_subject = (page_width - subject_width) / 2  # Centered position

    # Draw the centered subject
    can.drawString(x_subject, 550, subject.upper())
    
    # Set font for normal text (address and body)
    can.setFont("Times-Roman", 12)
    

    # print(address_width)
    address_group = address.split("\n")

    # Right-align the address
    address_width = can.stringWidth(max(address_group, key=len), "Times-Roman", 12)

    address_start = 650
    for address_line in address_group:
        can.drawString(65, address_start, address_line)  # Adjust x position for right-align
        address_start -= 15
    
    # Add the body text
    body_group = body.split("\n")
    start = 520
    for line in body_group:
        # print(textwrap.fill(line, width=100))
        separate_parts = textwrap.fill(line, width=100).split("\n")
        for section in separate_parts:
            can.drawString(65, start, section)
            start -= 15
    
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
