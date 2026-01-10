import os
from PIL import Image

# Get root folder path
path = input("Enter folder path: ").strip()

# Supported image extensions
image_exts = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

for subfolder in os.listdir(path):
    subfolder_path = os.path.join(path, subfolder)

    if os.path.isdir(subfolder_path):
        images = []

        # Collect images in subfolder
        for file in sorted(os.listdir(subfolder_path)):
            if file.lower().endswith(image_exts):
                img_path = os.path.join(subfolder_path, file)
                img = Image.open(img_path).convert("RGB")
                images.append(img)

        # Create PDF if images exist
        if images:
            pdf_path = os.path.join(subfolder_path, f"{subfolder}.pdf")
            images[0].save(
                pdf_path,
                save_all=True,
                append_images=images[1:]
            )
            print(f"Created: {pdf_path}")
        else:
            print(f"No images in: {subfolder_path}")
