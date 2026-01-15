#!/usr/bin/env python3
"""
PDF Processor - Image to PDF & PDF Tools
========================================

Convert images to PDF, add page numbers, or create 2-up layouts.
Processes all subfolders in a given directory.

Usage:
    python pdf_processor.py
"""

import os
from PIL import Image

# ============================================================================
# UTILITIES
# ============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print formatted header."""
    clear_screen()
    print("=" * 60)
    print("📄 PDF PROCESSOR".center(60))
    print("=" * 60)
    print(title)
    print("-" * 60)

def get_folder_path():
    """Get and validate folder path."""
    while True:
        print("\nEnter folder path (drag & drop works):")
        path = input(">> ").strip()
        path = path.strip('"').strip("'")
        
        if os.path.isdir(path):
            return os.path.abspath(path)
        else:
            print(f"\n❌ '{path}' is not a valid folder")

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    
    # Check Pillow
    try:
        import PIL
    except ImportError:
        missing.append("pillow")
    
    # Check PyPDF2
    try:
        import PyPDF2
    except ImportError:
        missing.append("pypdf2")
    
    # Check reportlab
    try:
        import reportlab
    except ImportError:
        missing.append("reportlab")
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    
    return True

# ============================================================================
# TOOL 1: IMAGES TO PDF
# ============================================================================

def images_to_pdf():
    """Convert all images in subfolders to PDFs."""
    print_header("IMAGES TO PDF CONVERTER")
    
    try:
        from PIL import Image
    except ImportError:
        print("\n❌ Pillow is not installed!")
        print("Install with: pip install pillow")
        input("\nPress Enter to continue...")
        return
    
    root_path = get_folder_path()
    
    # Supported image formats
    image_exts = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".gif")
    
    print(f"\n📁 Processing folder: {os.path.basename(root_path)}")
    print(f"📁 Supported formats: {', '.join(image_exts)}")
    print("\n⏳ Converting images to PDF...")
    print("-" * 50)
    
    total_converted = 0
    
    # Process each subfolder
    for subfolder in os.listdir(root_path):
        subfolder_path = os.path.join(root_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            images = []
            
            # Collect images
            for file in sorted(os.listdir(subfolder_path)):
                if file.lower().endswith(image_exts):
                    img_path = os.path.join(subfolder_path, file)
                    try:
                        img = Image.open(img_path).convert("RGB")
                        images.append(img)
                    except Exception as e:
                        print(f"   ⚠️  Skipping {file}: {e}")
            
            # Create PDF if images found
            if images:
                pdf_path = os.path.join(subfolder_path, f"{subfolder}.pdf")
                images[0].save(
                    pdf_path,
                    save_all=True,
                    append_images=images[1:]
                )
                print(f"✅ Created: {subfolder}.pdf ({len(images)} images)")
                total_converted += 1
            else:
                print(f"📭 No images in: {subfolder}")
    
    print("-" * 50)
    print(f"\n✅ Conversion complete!")
    print(f"   Total PDFs created: {total_converted}")
    input("\nPress Enter to continue...")

# ============================================================================
# TOOL 2: ADD PAGE NUMBERS
# ============================================================================

def add_page_numbers():
    """Add page numbers to PDFs in subfolders."""
    print_header("ADD PAGE NUMBERS TO PDFS")
    
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from io import BytesIO
    except ImportError:
        print("\n❌ Required packages not installed!")
        print("Install with: pip install pypdf2 reportlab")
        input("\nPress Enter to continue...")
        return
    
    root_path = get_folder_path()
    
    def process_pdf(pdf_path):
        """Add page numbers to a single PDF."""
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            for i, page in enumerate(reader.pages):
                packet = BytesIO()
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Create canvas for page number
                c = canvas.Canvas(packet, pagesize=(page_width, page_height))
                c.setFont("Helvetica-Bold", 28)
                c.drawCentredString(
                    page_width / 2,
                    50,  # Position from bottom
                    str(i + 1)
                )
                c.save()
                
                # Merge page number
                packet.seek(0)
                overlay = PdfReader(packet)
                page.merge_page(overlay.pages[0])
                writer.add_page(page)
            
            # Save with numbers
            with open(pdf_path, "wb") as f:
                writer.write(f)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    print(f"\n📁 Processing folder: {os.path.basename(root_path)}")
    print("\n⏳ Adding page numbers...")
    print("-" * 50)
    
    total_numbered = 0
    total_failed = 0
    
    # Process each subfolder
    for subfolder in os.listdir(root_path):
        subfolder_path = os.path.join(root_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            pdfs = [f for f in os.listdir(subfolder_path) if f.lower().endswith(".pdf")]
            
            if pdfs:
                print(f"\n📂 Folder: {subfolder}")
                for pdf in pdfs:
                    pdf_path = os.path.join(subfolder_path, pdf)
                    success, error = process_pdf(pdf_path)
                    
                    if success:
                        print(f"   ✅ Numbered: {pdf}")
                        total_numbered += 1
                    else:
                        print(f"   ❌ Failed: {pdf} ({error})")
                        total_failed += 1
    
    print("-" * 50)
    print(f"\n✅ Page numbering complete!")
    print(f"   Successfully numbered: {total_numbered}")
    print(f"   Failed: {total_failed}")
    input("\nPress Enter to continue...")

# ============================================================================
# TOOL 3: CREATE 2-UP LAYOUT
# ============================================================================

def create_2up_pdfs():
    """Create 2-up layout PDFs (2 pages per sheet)."""
    print_header("CREATE 2-UP PDF LAYOUTS")
    
    try:
        from PyPDF2 import PdfReader, PdfWriter, PageObject
        from reportlab.lib.pagesizes import A4
    except ImportError:
        print("\n❌ Required packages not installed!")
        print("Install with: pip install pypdf2 reportlab")
        input("\nPress Enter to continue...")
        return
    
    root_path = get_folder_path()
    
    def make_2up(pdf_path):
        """Convert a PDF to 2-up layout."""
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            page_width, page_height = A4
            pages = reader.pages
            
            i = 0
            while i < len(pages):
                # Create new A4 page
                new_page = PageObject.create_blank_page(
                    width=page_width,
                    height=page_height
                )
                
                # First page (top half)
                p1 = pages[i]
                p1.scale_by(0.5)
                new_page.merge_translated_page(
                    p1,
                    0,
                    page_height / 2
                )
                
                # Second page (bottom half) if exists
                if i + 1 < len(pages):
                    p2 = pages[i + 1]
                    p2.scale_by(0.5)
                    new_page.merge_translated_page(
                        p2,
                        0,
                        0
                    )
                
                writer.add_page(new_page)
                i += 2
            
            # Save 2-up version
            out_path = pdf_path.replace(".pdf", "_2up.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    print(f"\n📁 Processing folder: {os.path.basename(root_path)}")
    print("\n⏳ Creating 2-up layouts...")
    print("-" * 50)
    
    total_converted = 0
    total_failed = 0
    
    # Process each subfolder
    for subfolder in os.listdir(root_path):
        subfolder_path = os.path.join(root_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            # Get PDFs that aren't already 2-up
            pdfs = [f for f in os.listdir(subfolder_path) 
                   if f.lower().endswith(".pdf") and not f.endswith("_2up.pdf")]
            
            if pdfs:
                print(f"\n📂 Folder: {subfolder}")
                for pdf in pdfs:
                    pdf_path = os.path.join(subfolder_path, pdf)
                    success, error = make_2up(pdf_path)
                    
                    if success:
                        print(f"   ✅ 2-up created: {pdf}")
                        total_converted += 1
                    else:
                        print(f"   ❌ Failed: {pdf} ({error})")
                        total_failed += 1
    
    print("-" * 50)
    print(f"\n✅ 2-up conversion complete!")
    print(f"   Successfully converted: {total_converted}")
    print(f"   Failed: {total_failed}")
    input("\nPress Enter to continue...")

# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main menu for PDF Processor."""
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    while True:
        clear_screen()
        print("=" * 60)
        print("📄 PDF PROCESSOR".center(60))
        print("=" * 60)
        print("\nProcess PDFs and images in folder structure")
        print("Tools process all subfolders in the selected directory")
        print()
        print("Choose a tool:")
        print()
        print("1. 🖼️  Images to PDF")
        print("   - Convert images in each subfolder to PDF")
        print("   - Supports: JPG, PNG, BMP, TIFF, WEBP, GIF")
        print()
        print("2. 🔢 Add Page Numbers")
        print("   - Add big page numbers to existing PDFs")
        print("   - Numbers appear at bottom center of each page")
        print()
        print("3. 📖 Create 2-up Layout")
        print("   - Combine 2 PDF pages onto single sheet")
        print("   - Creates new PDFs with '_2up' suffix")
        print()
        print("4. ℹ️  About / Dependencies")
        print()
        print("0. 🚪 Exit")
        print()
        
        choice = input("Choose (0-4): ").strip()
        
        if choice == '1':
            images_to_pdf()
        elif choice == '2':
            add_page_numbers()
        elif choice == '3':
            create_2up_pdfs()
        elif choice == '4':
            show_about()
        elif choice == '0':
            print("\n👋 Thank you for using PDF Processor!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def show_about():
    """Show information about the tool."""
    print_header("ABOUT PDF PROCESSOR")
    
    print("\n📋 What this tool does:")
    print("   • Converts images in subfolders to PDFs")
    print("   • Adds page numbers to existing PDFs")
    print("   • Creates 2-up layouts (2 pages per sheet)")
    print("   • Processes all subfolders automatically")
    print()
    
    print("📁 Folder Structure Example:")
    print("   MainFolder/")
    print("   ├── Project1/        → project1.pdf")
    print("   │   ├── image1.jpg")
    print("   │   ├── image2.png")
    print("   │   └── ...")
    print("   ├── Project2/        → project2.pdf")
    print("   │   ├── photo1.jpg")
    print("   │   └── ...")
    print()
    
    print("🔧 Required Packages:")
    print("   • Pillow - Image processing")
    print("   • PyPDF2 - PDF manipulation")
    print("   • ReportLab - PDF generation")
    print()
    print("   Install with: pip install pillow pypdf2 reportlab")
    print()
    
    input("Press Enter to continue...")

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")