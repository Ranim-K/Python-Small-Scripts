import os
import subprocess

# -------- SETTINGS --------
input_folder = "convert"  # folder with videos
output_root = "photos"    # main folder for frames
os.makedirs(output_root, exist_ok=True)

# supported video extensions
video_exts = (".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv")

# -------- PROCESS VIDEOS --------
for file in os.listdir(input_folder):
    if not file.lower().endswith(video_exts):
        continue

    input_path = os.path.join(input_folder, file)
    name, ext = os.path.splitext(file)

    print(f"\nProcessing video: {file}")

    # create folder for this video's frames
    out_folder = os.path.join(output_root, name)
    os.makedirs(out_folder, exist_ok=True)

    # extract frames
    # frames will be named: frame_0001.png, frame_0002.png, ...
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        os.path.join(out_folder, "frame_%04d.png")
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print(f"✅ Frames saved in {out_folder}")

print("\n🎉 All videos converted to frames!")
