#!/usr/bin/env python3
"""
File Merger - Combine multiple files into one
=============================================

Merge Python (.py) or Text (.txt) files from a folder
into a single organized file, sorted by date.

Usage:
    python file_merger.py
"""

import os
import sys
from datetime import datetime

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print formatted header."""
    clear_screen()
    print("=" * 60)
    print("📂 FILE MERGER".center(60))
    print("=" * 60)
    print(title)
    print("-" * 60)

def get_folder_path():
    """Get and validate folder path from user."""
    while True:
        print("\nEnter folder path (or drag & drop folder):")
        path = input(">> ").strip()
        
        # Clean up drag-and-drop paths
        path = path.strip('"').strip("'")
        
        if os.path.isdir(path):
            return os.path.abspath(path)
        else:
            print(f"\n❌ '{path}' is not a valid folder")
            print("Please try again...")

def extract_date_from_filename(filename):
    """
    Extract date from filename.
    Supports formats: 2024-01-15, 15-01-2024, 20240115
    """
    date_str = filename[:10]  # Try first 10 characters
    
    # Try different date formats
    formats = [
        "%Y-%m-%d",  # 2024-01-15
        "%d-%m-%Y",  # 15-01-2024
        "%Y%m%d",    # 20240115
        "%m-%d-%Y",  # 01-15-2024 (US format)
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

# ============================================================================
# MERGING FUNCTIONS
# ============================================================================

def merge_python_files():
    """Merge all Python files in a folder."""
    print_header("MERGE PYTHON FILES")
    
    folder = get_folder_path()
    
    # Find all Python files
    py_files = []
    for file in os.listdir(folder):
        if file.lower().endswith(".py"):
            file_path = os.path.join(folder, file)
            
            # Try to extract date from filename
            date = extract_date_from_filename(file)
            
            # If no date in filename, use modification date
            if not date:
                mod_time = os.path.getmtime(file_path)
                date = datetime.fromtimestamp(mod_time)
            
            py_files.append((date, file, file_path))
    
    if not py_files:
        print(f"\n❌ No Python files (.py) found in folder")
        input("\nPress Enter to continue...")
        return
    
    # Sort by date (oldest first)
    py_files.sort(key=lambda x: x[0])
    
    # Create output file
    output_file = os.path.join(folder, "merged_python_code.txt")
    
    print(f"\n📁 Found {len(py_files)} Python file(s):")
    for date, file, _ in py_files:
        print(f"   • {file} ({date.strftime('%Y-%m-%d')})")
    
    print(f"\n📄 Output will be saved as: {os.path.basename(output_file)}")
    
    confirm = input("\nMerge these files? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation cancelled")
        input("\nPress Enter to continue...")
        return
    
    # Merge files
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("PYTHON CODE MERGER\n")
        outfile.write("=" * 60 + "\n\n")
        
        for i, (date, file, file_path) in enumerate(py_files, 1):
            outfile.write(f"File {i:02d}: {file}\n")
            outfile.write(f"Date: {date.strftime('%Y-%m-%d')}\n")
            outfile.write("=" * 60 + "\n\n")
            
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content)
            except UnicodeDecodeError:
                outfile.write(f"[Error: Could not read {file} as UTF-8]\n")
            except Exception as e:
                outfile.write(f"[Error reading {file}: {str(e)}]\n")
            
            outfile.write("\n\n" + "=" * 60 + "\n\n")
    
    print(f"\n✅ Successfully merged {len(py_files)} Python files!")
    print(f"📄 Output file: {output_file}")
    input("\nPress Enter to continue...")

def merge_text_files():
    """Merge all text files in a folder."""
    print_header("MERGE TEXT FILES")
    
    folder = get_folder_path()
    
    # Find all text files
    txt_files = []
    for file in os.listdir(folder):
        if file.lower().endswith(".txt"):
            file_path = os.path.join(folder, file)
            
            # Try to extract date from filename
            date = extract_date_from_filename(file)
            
            # If no date in filename, use modification date
            if not date:
                mod_time = os.path.getmtime(file_path)
                date = datetime.fromtimestamp(mod_time)
            
            txt_files.append((date, file, file_path))
    
    if not txt_files:
        print(f"\n❌ No text files (.txt) found in folder")
        input("\nPress Enter to continue...")
        return
    
    # Sort by date (oldest first)
    txt_files.sort(key=lambda x: x[0])
    
    # Create output file
    output_file = os.path.join(folder, "merged_text_files.txt")
    
    print(f"\n📁 Found {len(txt_files)} text file(s):")
    for date, file, _ in txt_files:
        print(f"   • {file} ({date.strftime('%Y-%m-%d')})")
    
    print(f"\n📄 Output will be saved as: {os.path.basename(output_file)}")
    
    confirm = input("\nMerge these files? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation cancelled")
        input("\nPress Enter to continue...")
        return
    
    # Merge files
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("TEXT FILES MERGER\n")
        outfile.write("=" * 60 + "\n\n")
        
        for i, (date, file, file_path) in enumerate(txt_files, 1):
            outfile.write(f"File {i:02d}: {file}\n")
            outfile.write(f"Date: {date.strftime('%Y-%m-%d')}\n")
            outfile.write("-" * 40 + "\n\n")
            
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content)
            except UnicodeDecodeError:
                outfile.write(f"[Error: Could not read {file} as UTF-8]\n")
            except Exception as e:
                outfile.write(f"[Error reading {file}: {str(e)}]\n")
            
            outfile.write("\n\n" + "-" * 40 + "\n\n")
    
    print(f"\n✅ Successfully merged {len(txt_files)} text files!")
    print(f"📄 Output file: {output_file}")
    input("\nPress Enter to continue...")

def merge_custom_files():
    """Merge files with custom extension."""
    print_header("MERGE CUSTOM FILES")
    
    folder = get_folder_path()
    
    print("\nEnter file extension to merge (without dot):")
    print("Examples: py, txt, md, js, html, csv")
    
    extension = input("Extension: ").strip().lower()
    if not extension:
        print("\n❌ No extension provided")
        input("\nPress Enter to continue...")
        return
    
    # Find files with given extension
    custom_files = []
    for file in os.listdir(folder):
        if file.lower().endswith(f".{extension}"):
            file_path = os.path.join(folder, file)
            
            # Try to extract date from filename
            date = extract_date_from_filename(file)
            
            # If no date in filename, use modification date
            if not date:
                mod_time = os.path.getmtime(file_path)
                date = datetime.fromtimestamp(mod_time)
            
            custom_files.append((date, file, file_path))
    
    if not custom_files:
        print(f"\n❌ No .{extension} files found in folder")
        input("\nPress Enter to continue...")
        return
    
    # Sort by date (oldest first)
    custom_files.sort(key=lambda x: x[0])
    
    # Create output file
    output_file = os.path.join(folder, f"merged_{extension}_files.txt")
    
    print(f"\n📁 Found {len(custom_files)} .{extension} file(s):")
    for date, file, _ in custom_files:
        print(f"   • {file} ({date.strftime('%Y-%m-%d')})")
    
    print(f"\n📄 Output will be saved as: {os.path.basename(output_file)}")
    
    confirm = input("\nMerge these files? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation cancelled")
        input("\nPress Enter to continue...")
        return
    
    # Merge files
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(f"{extension.upper()} FILES MERGER\n")
        outfile.write("=" * 60 + "\n\n")
        
        for i, (date, file, file_path) in enumerate(custom_files, 1):
            outfile.write(f"File {i:02d}: {file}\n")
            outfile.write(f"Date: {date.strftime('%Y-%m-%d')}\n")
            outfile.write("-" * 40 + "\n\n")
            
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content)
            except UnicodeDecodeError:
                outfile.write(f"[Error: Could not read {file} as UTF-8]\n")
            except Exception as e:
                outfile.write(f"[Error reading {file}: {str(e)}]\n")
            
            outfile.write("\n\n" + "-" * 40 + "\n\n")
    
    print(f"\n✅ Successfully merged {len(custom_files)} .{extension} files!")
    print(f"📄 Output file: {output_file}")
    input("\nPress Enter to continue...")

# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main menu for file merger."""
    
    while True:
        clear_screen()
        print("=" * 60)
        print("📂 FILE MERGER".center(60))
        print("=" * 60)
        print("\nCombine multiple files into a single organized file")
        print("Files are sorted by date (from filename or file metadata)")
        print()
        print("Choose what to merge:")
        print()
        print("1. 🐍 Python Files (.py)")
        print("   - Merge all Python scripts in a folder")
        print()
        print("2. 📝 Text Files (.txt)")
        print("   - Merge all text files in a folder")
        print()
        print("3. 🔧 Custom Files")
        print("   - Merge files with any extension")
        print()
        print("4. ℹ️  About")
        print()
        print("0. 🚪 Exit")
        print()
        
        choice = input("Choose (0-4): ").strip()
        
        if choice == '1':
            merge_python_files()
        elif choice == '2':
            merge_text_files()
        elif choice == '3':
            merge_custom_files()
        elif choice == '4':
            show_about()
        elif choice == '0':
            print("\n👋 Thank you for using File Merger!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def show_about():
    """Show information about the tool."""
    print_header("ABOUT FILE MERGER")
    
    print("\n📋 What this tool does:")
    print("   • Merges multiple files into one organized file")
    print("   • Sorts files by date automatically")
    print("   • Extracts dates from filenames or uses file metadata")
    print("   • Creates clean, readable output with separators")
    print()
    
    print("📅 Supported date formats in filenames:")
    print("   • YYYY-MM-DD (e.g., 2024-01-15_script.py)")
    print("   • DD-MM-YYYY (e.g., 15-01-2024_notes.txt)")
    print("   • YYYYMMDD   (e.g., 20240115_log.md)")
    print("   • MM-DD-YYYY (e.g., 01-15-2024_data.csv)")
    print()
    
    print("📂 How to use:")
    print("   1. Select file type to merge")
    print("   2. Enter folder path (drag & drop works)")
    print("   3. Confirm the files found")
    print("   4. Get merged output in same folder")
    print()
    
    input("Press Enter to continue...")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")