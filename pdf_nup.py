import os
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.lib.pagesizes import A4

root_path = input("Enter folder path: ").strip()

def make_2up(pdf_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    page_width, page_height = A4
    pages = reader.pages
    i = 0

    while i < len(pages):
        new_page = PageObject.create_blank_page(
            width=page_width,
            height=page_height
        )

        # First page (top)
        p1 = pages[i]
        p1.scale_by(0.5)  # correct method in PyPDF2 3.x
        new_page.mergeTranslatedPage(
            p1,
            0,
            page_height / 2
        )

        # Second page (bottom) if exists
        if i + 1 < len(pages):
            p2 = pages[i + 1]
            p2.scale_by(0.5)
            new_page.mergeTranslatedPage(
                p2,
                0,
                0
            )

        writer.add_page(new_page)
        i += 2

    out_path = pdf_path.replace(".pdf", "_2up.pdf")
    with open(out_path, "wb") as f:
        writer.write(f)

    print(f"2-up created: {out_path}")

# Walk through folders
for subfolder in os.listdir(root_path):
    subfolder_path = os.path.join(root_path, subfolder)
    if os.path.isdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            if file.lower().endswith(".pdf") and not file.endswith("_2up.pdf"):
                make_2up(os.path.join(subfolder_path, file))
