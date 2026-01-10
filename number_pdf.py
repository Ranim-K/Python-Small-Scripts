import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

root_path = input("Enter folder path: ").strip()

def add_page_numbers(pdf_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        packet = BytesIO()
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # BIG and visible page number
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(
            page_width / 2,
            50,          # higher from bottom
            str(i + 1)
        )

        c.save()
        packet.seek(0)

        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(pdf_path, "wb") as f:
        writer.write(f)

    print(f"Numbered: {pdf_path}")

for subfolder in os.listdir(root_path):
    subfolder_path = os.path.join(root_path, subfolder)

    if os.path.isdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            if file.lower().endswith(".pdf"):
                add_page_numbers(os.path.join(subfolder_path, file))
