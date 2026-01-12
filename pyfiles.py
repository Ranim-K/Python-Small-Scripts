import os
from datetime import datetime

def extract_date_from_name(filename):
    """
    Tries to extract a date from filename.
    Expected examples:
    2024-01-15_script.py
    15-01-2024.py
    20240115_utils.py
    """
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y%m%d"):
        try:
            return datetime.strptime(filename[:10], fmt)
        except ValueError:
            pass
    return None


def main():
    folder_path = input("Enter folder path: ").strip()

    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path")
        return

    py_files = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".py"):
            full_path = os.path.join(folder_path, file)

            # 1️⃣ try date from filename
            date = extract_date_from_name(file)

            # 2️⃣ fallback to file modified time
            if date is None:
                date = datetime.fromtimestamp(os.path.getmtime(full_path))

            py_files.append((date, file, full_path))

    # sort by date
    py_files.sort(key=lambda x: x[0])

    output_path = os.path.join(folder_path, "merged_python_code.txt")

    with open(output_path, "w", encoding="utf-8") as out:
        for i, (_, file, path) in enumerate(py_files, start=1):
            out.write(f"{i:02d} - {file}\n")
            out.write("#" * 60 + "\n\n")

            with open(path, "r", encoding="utf-8") as f:
                out.write(f.read())

            out.write("\n\n\n")

    print(f"✅ Done! File created: {output_path}")


if __name__ == "__main__":
    main()
