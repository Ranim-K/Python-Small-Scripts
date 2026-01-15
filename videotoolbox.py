#!/usr/bin/env python3
"""
Video Toolbox - Smart Video Processing Assistant
================================================

A guided tool for video processing with interactive workflows:
1. Find crop coordinates visually
2. Apply to single or multiple videos
3. Extract clips with precise timing

Usage:
    python videotoolbox.py
"""

import os
import sys
import subprocess
import cv2

# ============================================================================
# CONFIGURATION & UTILITIES
# ============================================================================

SUPPORTED_EXTENSIONS = (".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".MOV", ".MP4")
crop_settings = {"x": 0, "y": 0, "w": 0, "h": 0}  # Will be set by user

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header."""
    clear_screen()
    print("=" * 60)
    print("🎬 VIDEO TOOLBOX".center(60))
    print("=" * 60)
    print(f"{title}")
    print("-" * 60)

def show_progress(step, total, message):
    """Show progress in a nice format."""
    print(f"\n[{step}/{total}] {message}")
    print("-" * 40)

def wait_continue():
    """Wait for user to press Enter."""
    input("\n↵ Press Enter to continue...")

def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except:
        return False

def clean_path(path):
    """Clean up paths from drag-and-drop in Windows."""
    # Remove & ' prefix and ' suffix from Windows drag-and-drop
    path = path.strip()
    
    # Handle PowerShell drag-and-drop format
    if path.startswith("& '") and path.endswith("'"):
        path = path[3:-1]  # Remove & ' and '
    # Handle PowerShell drag-and-drop with just quotes
    elif path.startswith("'") and path.endswith("'"):
        path = path[1:-1]
    elif path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    
    return path.strip()

def get_folder_path(prompt):
    """Get and validate a folder path."""
    while True:
        print(f"\n{prompt}")
        print("Tip: You can type the path or drag and drop the folder here")
        path = input(">> ").strip()
        path = clean_path(path)
        
        if os.path.isdir(path):
            return os.path.abspath(path)
        else:
            print(f"\n❌ '{path}' is not a valid folder")
            print("Please make sure the folder exists and try again...")

def get_file_path(prompt):
    """Get and validate a file path."""
    while True:
        print(f"\n{prompt}")
        print("Tip: You can type the path or drag and drop the file here")
        path = input(">> ").strip()
        path = clean_path(path)
        
        if os.path.isfile(path):
            # Check if it's a supported video file
            if path.lower().endswith(SUPPORTED_EXTENSIONS):
                return os.path.abspath(path)
            else:
                print(f"\n❌ '{os.path.basename(path)}' is not a supported video file")
                print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
                print("Please select a video file...")
        else:
            print(f"\n❌ '{path}' is not a valid file")
            print("Please make sure the file exists and try again...")

def find_videos_in_folder(folder_path):
    """Find all video files in a folder."""
    videos = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(SUPPORTED_EXTENSIONS):
            videos.append(file)
    return sorted(videos)

# ============================================================================
# STEP 1: INTERACTIVE CROP COORDINATE FINDER
# ============================================================================

def find_crop_coordinates():
    """Interactive tool to visually find crop coordinates."""
    print_header("STEP 1: FIND CROP COORDINATES")
    
    if not check_ffmpeg():
        print("\n❌ FFmpeg is not installed!")
        print("Please install FFmpeg first: https://ffmpeg.org")
        wait_continue()
        return False
    
    print("\nI'll help you find the perfect crop area.")
    print("You'll select two points on the video to define a rectangle.")
    print()
    
    # Get video file
    video_file = get_file_path("Which video do you want to use as reference?")
    
    # Open video
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"\n❌ Could not open video: {os.path.basename(video_file)}")
        print("Please make sure it's a valid video file.")
        wait_continue()
        return False
    
    # Get video info
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"\n✅ Video loaded: {os.path.basename(video_file)}")
    print(f"   Resolution: {width} x {height}")
    print(f"   Full path: {video_file}")
    
    points = []
    
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            points.append((x, y))
            print(f"\n📍 Point {len(points)} selected: ({x}, {y})")
            
            if len(points) == 2:
                # Calculate rectangle
                x1, y1 = points[0]
                x2, y2 = points[1]
                left = min(x1, x2)
                top = min(y1, y2)
                right = max(x1, x2)
                bottom = max(y1, y2)
                width = right - left
                height = bottom - top
                
                print("\n" + "="*50)
                print("🎯 CROP AREA FOUND!")
                print(f"   Top-left corner:     ({left}, {top})")
                print(f"   Bottom-right corner: ({right}, {bottom})")
                print(f"   Dimensions:          {width} x {height} pixels")
                print("="*50)
    
    # Create window
    cv2.namedWindow("Video - Select Crop Area", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video - Select Crop Area", min(width, 1280), min(height, 720))
    cv2.setMouseCallback("Video - Select Crop Area", mouse_callback)
    
    print("\n" + "-"*50)
    print("INSTRUCTIONS:")
    print("1. Click to select FIRST point (top-left corner)")
    print("2. Click to select SECOND point (bottom-right corner)")
    print("3. Press SPACE to pause/resume")
    print("4. Press R to reset points")
    print("5. Press ESC when done")
    print("-"*50)
    print("\n⏳ Loading video...")
    
    paused = False
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
        
        display = frame.copy()
        
        # Draw rectangle if we have 2 points
        if len(points) == 2:
            cv2.rectangle(display, points[0], points[1], (0, 255, 0), 2)
            cv2.putText(display, "Crop Area Selected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw instructions on screen
        status = "PAUSED" if paused else "PLAYING"
        cv2.putText(display, f"Status: {status}", (10, height - 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if not paused else (0, 0, 255), 2)
        
        # Draw selected points count
        cv2.putText(display, f"Points: {len(points)}/2", (width - 150, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow("Video - Select Crop Area", display)
        
        key = cv2.waitKey(30 if not paused else 1) & 0xFF
        
        if key == 32:  # SPACE
            paused = not paused
            print(f"\n⏸️  Video {'paused' if paused else 'playing'}")
        elif key == ord('r'):  # R
            points = []
            print("\n🔄 Points reset")
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if len(points) == 2:
        # Save coordinates
        x1, y1 = points[0]
        x2, y2 = points[1]
        crop_settings['x'] = min(x1, x2)
        crop_settings['y'] = min(y1, y2)
        crop_settings['w'] = abs(x2 - x1)
        crop_settings['h'] = abs(y2 - y1)
        
        print("\n✅ Crop coordinates saved!")
        print(f"   x: {crop_settings['x']}")
        print(f"   y: {crop_settings['y']}")
        print(f"   w: {crop_settings['w']}")
        print(f"   h: {crop_settings['h']}")
        
        return True
    else:
        print("\n❌ No crop area selected")
        return False

# ============================================================================
# STEP 2: APPLY CROPPING
# ============================================================================

def apply_cropping():
    """Apply cropping to videos based on saved coordinates."""
    print_header("STEP 2: APPLY CROPPING")
    
    if crop_settings['w'] == 0 or crop_settings['h'] == 0:
        print("\n❌ No crop coordinates found!")
        print("Please run 'Find Crop Coordinates' first.")
        wait_continue()
        return
    
    print(f"\nCurrent crop settings:")
    print(f"   Position: ({crop_settings['x']}, {crop_settings['y']})")
    print(f"   Size:     {crop_settings['w']} x {crop_settings['h']} pixels")
    print()
    
    # Ask what to crop
    print("What would you like to crop?")
    print("1. A single video")
    print("2. All videos in a folder")
    print("3. Go back")
    
    choice = input("\nChoose (1-3): ").strip()
    
    if choice == '1':
        crop_single_video()
    elif choice == '2':
        crop_folder_videos()
    elif choice == '3':
        return

def crop_single_video():
    """Crop a single video."""
    show_progress(1, 2, "Select video to crop")
    
    video_file = get_file_path("Which video do you want to crop?")
    
    # Create output filename
    base_name = os.path.basename(video_file)
    name, ext = os.path.splitext(base_name)
    output_file = f"{name}_cropped{ext}"
    output_path = os.path.join(os.path.dirname(video_file), output_file)
    
    print(f"\n📁 Input:  {base_name}")
    print(f"📁 Output: {output_file}")
    
    confirm = input("\nProceed with cropping? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation cancelled")
        wait_continue()
        return
    
    show_progress(2, 2, "Cropping video...")
    
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-vf", f"crop={crop_settings['w']}:{crop_settings['h']}:{crop_settings['x']}:{crop_settings['y']}",
        "-c:a", "copy",
        output_path
    ]
    
    try:
        print(f"\n⏳ Processing...")
        result = subprocess.run(cmd, 
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Success! Cropped video saved as:")
            print(f"   {output_path}")
        else:
            print(f"\n❌ Error cropping video:")
            print(result.stderr[:500])
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    wait_continue()

def crop_folder_videos():
    """Crop all videos in a folder."""
    show_progress(1, 3, "Select folder with videos")
    
    folder_path = get_folder_path("Which folder contains the videos?")
    
    # Find videos
    videos = find_videos_in_folder(folder_path)
    
    if not videos:
        print(f"\n❌ No video files found in folder")
        wait_continue()
        return
    
    print(f"\n📁 Found {len(videos)} video(s):")
    for i, video in enumerate(videos[:10], 1):
        print(f"   {i:2d}. {video}")
    if len(videos) > 10:
        print(f"   ... and {len(videos) - 10} more")
    
    # Create output folder
    output_folder = os.path.join(folder_path, "cropped_videos")
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\n📁 Output folder: {output_folder}")
    
    confirm = input("\nCrop all these videos? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation cancelled")
        wait_continue()
        return
    
    show_progress(2, 3, "Cropping videos...")
    
    success_count = 0
    for i, video in enumerate(videos, 1):
        input_path = os.path.join(folder_path, video)
        output_path = os.path.join(output_folder, video)
        
        print(f"\n[{i}/{len(videos)}] Processing: {video}")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vf", f"crop={crop_settings['w']}:{crop_settings['h']}:{crop_settings['x']}:{crop_settings['y']}",
            "-c:a", "copy",
            output_path
        ]
        
        try:
            subprocess.run(cmd, 
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         check=True)
            print(f"   ✅ Success")
            success_count += 1
        except:
            print(f"   ❌ Failed")
    
    show_progress(3, 3, "Complete!")
    
    print(f"\n✅ Cropping complete!")
    print(f"   Successful: {success_count}/{len(videos)}")
    print(f"   Output folder: {output_folder}")
    wait_continue()

# ============================================================================
# STEP 3: VIDEO CLIPPING
# ============================================================================

def clip_videos():
    """Extract clips from videos."""
    print_header("VIDEO CLIPPING")
    
    if not check_ffmpeg():
        print("\n❌ FFmpeg is not installed!")
        wait_continue()
        return
    
    print("\nI'll help you extract specific clips from videos.")
    print("You can extract multiple clips from each video.")
    print()
    
    folder_path = get_folder_path("Which folder contains the videos?")
    
    videos = find_videos_in_folder(folder_path)
    
    if not videos:
        print(f"\n❌ No video files found")
        wait_continue()
        return
    
    output_folder = os.path.join(folder_path, "clips")
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\n📁 Found {len(videos)} video(s)")
    print(f"📁 Clips will be saved to: {output_folder}")
    
    for video in videos:
        print(f"\n{'='*50}")
        print(f"Processing: {video}")
        print(f"{'='*50}")
        
        input_path = os.path.join(folder_path, video)
        name, ext = os.path.splitext(video)
        
        clip_count = 1
        
        while True:
            print(f"\n--- Clip {clip_count} from '{video}' ---")
            print("Enter timing in MINUTES and SECONDS")
            print("(Press Enter to skip this video)")
            
            start_min = input("Start minute: ").strip()
            if start_min == "":
                print(f"Skipping {video}")
                break
            
            try:
                start_min = int(start_min)
                start_sec = int(input("Start second: "))
                end_min = int(input("End minute: "))
                end_sec = int(input("End second: "))
                
                start_time = start_min * 60 + start_sec
                end_time = end_min * 60 + end_sec
                duration = end_time - start_time
                
                if duration <= 0:
                    print("❌ End time must be after start time")
                    continue
                
                output_name = f"{name}_clip{clip_count}{ext}"
                output_path = os.path.join(output_folder, output_name)
                
                print(f"\n⏳ Extracting clip {clip_count}...")
                
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-ss", str(start_time),
                    "-i", input_path,
                    "-t", str(duration),
                    "-c", "copy",
                    output_path
                ]
                
                subprocess.run(cmd, 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
                
                print(f"✅ Saved: {output_name}")
                clip_count += 1
                
                another = input("\nExtract another clip from this video? (y/n): ").strip().lower()
                if another != 'y':
                    break
                    
            except ValueError:
                print("❌ Please enter valid numbers")
                continue
    
    print(f"\n{'='*50}")
    print("✅ Clipping complete!")
    print(f"Clips saved to: {output_folder}")
    print(f"{'='*50}")
    wait_continue()

# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def guided_workflow():
    """Main guided workflow."""
    while True:
        clear_screen()
        print("=" * 60)
        print("🎬 VIDEO TOOLBOX - MAIN WORKFLOW".center(60))
        print("=" * 60)
        print("\nI'll guide you through the process step by step.")
        print("\nChoose your starting point:")
        print()
        print("1. 🎯 Find crop coordinates (First time)")
        print("   - Visually select area to crop from a video")
        print()
        print("2. ✂️  Apply cropping to videos")
        print("   - Use saved coordinates to crop videos")
        print()
        print("3. ⏱️  Extract video clips")
        print("   - Cut specific sections from videos")
        print()
        print("4. 📊 View current settings")
        print()
        print("0. ↩️  Back to main menu")
        print()
        
        choice = input("Choose (0-4): ").strip()
        
        if choice == '1':
            if find_crop_coordinates():
                print("\n✅ Great! Now you can apply these coordinates.")
                print("   Go to 'Apply cropping to videos' next.")
                wait_continue()
        elif choice == '2':
            apply_cropping()
        elif choice == '3':
            clip_videos()
        elif choice == '4':
            view_settings()
        elif choice == '0':
            break

def view_settings():
    """View current crop settings."""
    print_header("CURRENT SETTINGS")
    
    if crop_settings['w'] > 0:
        print(f"\n📐 Crop Area:")
        print(f"   X Position: {crop_settings['x']} pixels")
        print(f"   Y Position: {crop_settings['y']} pixels")
        print(f"   Width:      {crop_settings['w']} pixels")
        print(f"   Height:     {crop_settings['h']} pixels")
        print(f"\n   Area Size: {crop_settings['w']} × {crop_settings['h']}")
    else:
        print("\n📭 No crop coordinates saved yet")
        print("   Run 'Find crop coordinates' first")
    
    print(f"\n🔧 Tools Available:")
    print("   ✓ FFmpeg: " + ("Installed" if check_ffmpeg() else "Not found"))
    print(f"   ✓ Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
    
    wait_continue()

# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main entry point."""
    
    # Check requirements
    if not check_ffmpeg():
        print("\n" + "="*60)
        print("⚠️  IMPORTANT: FFmpeg is not installed!")
        print("="*60)
        print("\nThis tool requires FFmpeg to process videos.")
        print("Please install FFmpeg first:")
        print("\nWindows: Download from https://ffmpeg.org")
        print("         Or install via Chocolatey: choco install ffmpeg")
        print("macOS:   brew install ffmpeg")
        print("Linux:   sudo apt install ffmpeg")
        print("\n" + "="*60)
        input("\nPress Enter to exit...")
        return
    
    while True:
        clear_screen()
        print("=" * 60)
        print("🎬 VIDEO TOOLBOX".center(60))
        print("Your Complete Video Processing Assistant".center(60))
        print("=" * 60)
        
        if crop_settings['w'] > 0:
            print(f"\n📐 Ready to crop: {crop_settings['w']}×{crop_settings['h']}")
        
        print("\nChoose an option:")
        print()
        print("1. 🚀 Start Guided Workflow")
        print("   (Recommended - I'll walk you through everything)")
        print()
        print("2. 🎯 Find Crop Coordinates")
        print("   - Visually select area to crop")
        print()
        print("3. ✂️  Apply Cropping")
        print("   - Crop videos with saved coordinates")
        print()
        print("4. ⏱️  Extract Clips")
        print("   - Cut specific sections from videos")
        print()
        print("5. 📊 View Settings")
        print("   - Check current crop coordinates")
        print()
        print("0. 🚪 Exit")
        print()
        
        choice = input("Choose (0-5): ").strip()
        
        if choice == '1':
            guided_workflow()
        elif choice == '2':
            find_crop_coordinates()
        elif choice == '3':
            apply_cropping()
        elif choice == '4':
            clip_videos()
        elif choice == '5':
            view_settings()
        elif choice == '0':
            print("\n👋 Thank you for using Video Toolbox!")
            print("Have a great day!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
            wait_continue()

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        input("\nPress Enter to exit...")