#!/usr/bin/env python3
"""
Interactive Video Crop Selector
================================

A tool to visually select rectangular cropping regions from videos.
Useful for extracting consistent regions of interest from screen recordings.

Usage:
    python interactive_crop_selector.py <video_file>

Controls:
    MOUSE:
        - Left-click: Set two points to define cropping rectangle
          (first click = top-left, second click = bottom-right)
    
    KEYBOARD:
        - SPACE: Pause/Resume video playback
        - R: Reset selected points
        - ESC: Exit the application

Output:
    Prints coordinates in format: CROP -> x:10, y:20, w:300, h:200
    Where (x,y) is top-left corner, (w,h) are width and height
"""

import cv2
import sys
import os


class VideoCropSelector:
    def __init__(self, video_path):
        """Initialize video capture and window settings."""
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open video file '{video_path}'")
            sys.exit(1)
            
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        self.paused = False
        self.points = []  # Stores [(x1, y1), (x2, y2)]
        
        self.setup_window()
        
    def setup_window(self):
        """Create and configure the display window."""
        cv2.namedWindow("Video Crop Selector", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Video Crop Selector", 
                         min(self.video_width, 1280), 
                         min(self.video_height, 720))
        
        # Set mouse callback for point selection
        cv2.setMouseCallback("Video Crop Selector", self.mouse_callback)
        
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for point selection."""
        if event == cv2.EVENT_LBUTTONDOWN and len(self.points) < 2:
            self.points.append((x, y))
            print(f"Point {len(self.points)} selected: ({x}, {y})")
            
            if len(self.points) == 2:
                self.print_crop_coordinates()
                
    def print_crop_coordinates(self):
        """Print cropping coordinates in user-friendly format."""
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        
        # Ensure x1 < x2 and y1 < y2 for standard rectangle format
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)
        
        width = right - left
        height = bottom - top
        
        print("\n" + "="*50)
        print("CROP COORDINATES:")
        print(f"  Top-left:      ({left}, {top})")
        print(f"  Bottom-right:  ({right}, {bottom})")
        print(f"  Dimensions:    {width} x {height} pixels")
        print(f"  Format:        x:{left}, y:{top}, w:{width}, h:{height}")
        print("="*50 + "\n")
        
        return left, top, width, height
        
    def draw_overlay(self, frame):
        """Draw cropping rectangle and instructions on the frame."""
        display = frame.copy()
        
        # Draw cropping rectangle if points are selected
        if len(self.points) == 2:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw crosshairs at the selected points
            cv2.drawMarker(display, (x1, y1), (0, 0, 255), 
                          cv2.MARKER_CROSS, 20, 2)
            cv2.drawMarker(display, (x2, y2), (0, 0, 255), 
                          cv2.MARKER_CROSS, 20, 2)
        
        # Draw status overlay
        status = "PAUSED" if self.paused else "PLAYING"
        color = (0, 0, 255) if self.paused else (0, 255, 0)
        
        # Add status text
        cv2.putText(display, f"Status: {status}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Add instructions
        instructions = [
            "CONTROLS:",
            "SPACE: Pause/Resume",
            "R: Reset points",
            "ESC: Exit",
            "Click: Set crop points (2 needed)"
        ]
        
        y_offset = 60
        for line in instructions:
            cv2.putText(display, line, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
            
        return display
        
    def handle_keyboard(self):
        """Process keyboard inputs."""
        key = cv2.waitKey(30 if not self.paused else 1) & 0xFF
        
        if key == 32:  # SPACE - Toggle pause
            self.paused = not self.paused
            print(f"Video {'paused' if self.paused else 'resumed'}")
            
        elif key == ord('r'):  # R - Reset points
            if self.points:
                print("Points reset")
                self.points = []
                
        elif key == 27:  # ESC - Exit
            return False
            
        return True
        
    def run(self):
        """Main loop to process video and handle interactions."""
        print(f"\nVideo loaded: {os.path.basename(self.video_path)}")
        print(f"Resolution: {self.video_width} x {self.video_height}")
        print(f"FPS: {self.video_fps}, Frames: {self.total_frames}")
        print("\n" + "-"*50)
        print("Click to set two points for cropping rectangle")
        print("First click: Top-left corner")
        print("Second click: Bottom-right corner")
        print("-"*50 + "\n")
        
        while self.cap.isOpened():
            if not self.paused:
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                current_time = current_frame / self.video_fps if self.video_fps > 0 else 0
                
                # Display progress in console
                if current_frame % 30 == 0:  # Update every ~1 second at 30fps
                    print(f"Progress: {current_frame}/{self.total_frames} frames "
                          f"({current_time:.1f}s)", end='\r')
            else:
                # Keep displaying the same frame when paused
                current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                current_time = current_frame / self.video_fps if self.video_fps > 0 else 0
            
            # Draw overlay and display
            display = self.draw_overlay(frame)
            cv2.imshow("Video Crop Selector", display)
            
            # Handle keyboard input
            if not self.handle_keyboard():
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        print("\n" + "="*50)
        print("Application closed")
        if self.points == 2:
            print("Final crop coordinates printed above")
        print("="*50)


def main():
    """Main entry point with command line argument handling."""
    if len(sys.argv) != 2:
        print(__doc__)
        print(f"\nError: Please provide a video file.")
        print(f"Usage: python {os.path.basename(__file__)} <video_file>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    
    if not os.path.exists(video_file):
        print(f"Error: File '{video_file}' not found")
        sys.exit(1)
    
    # Run the crop selector
    selector = VideoCropSelector(video_file)
    selector.run()


if __name__ == "__main__":
    main()