import os
import subprocess

# ===== SETTINGS =====
input_folder = input(r"Enter the videos folder path: ")
output_folder = "cropped"

# crop values (from your points)
x = 502
y = 100
w = 345
h = 610
# ====================

os.makedirs(output_folder, exist_ok=True)

video_exts = (".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv")

for file in os.listdir(input_folder):
    if file.lower().endswith(video_exts):
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)

        print(f"Cropping: {file}")

        cmd = [
            "ffmpeg",
            "-y",
            "-i", in_path,
            "-vf", f"crop={w}:{h}:{x}:{y}",
            "-c:a", "copy",
            out_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print("✅ Done. All videos cropped.")
