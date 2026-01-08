import os
from datetime import datetime

def extract_date_from_name(filename):
    """
    Tries to extract a date from filename.
    Expected examples:
    2024-01-15_notes.txt
    15-01-2024.txt
    """
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y%m%d"):
        try:
            return datetime.strptime(filename[:10], fmt)
        except:
            pass
    return None

def main():
    folder_path = input("Enter folder path: ").strip()
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path")
        return

    txt_files = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".txt"):
            full_path = os.path.join(folder_path, file)

            # 1️⃣ try date from filename
            date = extract_date_from_name(file)

            # 2️⃣ fallback to metadata date
            if date is None:
                date = datetime.fromtimestamp(os.path.getmtime(full_path))

            txt_files.append((date, file, full_path))

    # sort by date
    txt_files.sort(key=lambda x: x[0])

    output_path = os.path.join(folder_path, "merged_output.txt")

    with open(output_path, "w", encoding="utf-8") as out:
        for i, (_, file, path) in enumerate(txt_files, start=1):
            out.write(f"{i:02d} - {file}\n")
            out.write("-" * 40 + "\n")

            with open(path, "r", encoding="utf-8") as f:
                out.write(f.read())

            out.write("\n\n")

    print(f"✅ Done! File created: {output_path}")

if __name__ == "__main__":
    main()
#i changed this code to the last puch a
#make sure to update it later

p = int(input("22"))