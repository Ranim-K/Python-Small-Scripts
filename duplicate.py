import os
import hashlib
import shutil

# Paths - update these to your actual folders
folder1 = input(r"Path\To\Folder1: ")  # folder with subfolders
folder2 = input(r"Path\To\Folder2: ")  # flat folder
output_folder = input(r"Path\To\Unique_Folder2: ")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def hash_file(path):
    """Return SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

# Step 1: Scan Folder1 recursively and hash all files
folder1_hashes = {}
for root, dirs, files in os.walk(folder1):
    for file in files:
        full_path = os.path.join(root, file)
        file_hash = hash_file(full_path)
        folder1_hashes[file_hash] = full_path

# Step 2: Scan Folder2 and check for duplicates
duplicates = []
unique_count = 0

for file in os.listdir(folder2):
    full_path = os.path.join(folder2, file)
    if os.path.isfile(full_path):
        file_hash = hash_file(full_path)
        if file_hash in folder1_hashes:
            duplicates.append(file)
        else:
            # Copy unique files to output folder
            shutil.copy2(full_path, os.path.join(output_folder, file))
            unique_count += 1

# Step 3: Print results
if duplicates:
    print("Duplicates found in Folder2 that exist in Folder1:")
    for d in duplicates:
        print(d)
else:
    print("No duplicates found. All files in Folder2 are unique.")

print(f"\nUnique files from Folder2 copied to: {output_folder}")
print(f"Total unique files: {unique_count}")
