import os
import subprocess

input_folder = "recut"
output_folder = "cut"

os.makedirs(output_folder, exist_ok=True)

video_exts = (".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv")

for file in os.listdir(input_folder):
    if not file.lower().endswith(video_exts):
        continue

    print("\n==============================")
    print(f"Video: {file}")

    input_path = os.path.join(input_folder, file)
    name, ext = os.path.splitext(file)

    clip_index = 1

    while True:
        start_min = input("Start minute (Enter to skip video): ")
        if start_min == "":
            break

        start_min = int(start_min)
        start_sec = int(input("Start second: "))

        end_min = int(input("End minute: "))
        end_sec = int(input("End second: "))

        start_time = start_min * 60 + start_sec
        end_time = end_min * 60 + end_sec
        duration = end_time - start_time

        if duration <= 0:
            print("❌ Invalid time range. Try again.")
            continue

        output_path = os.path.join(
            output_folder,
            f"{name}_clip{clip_index}{ext}"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", input_path,
            "-t", str(duration),
            "-c", "copy",
            output_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        print(f"✅ Saved: {output_path}")
        clip_index += 1

        more = input("Add another clip from this video? (y/n): ").lower()
        if more != "y":
            break

print("\n🎉 All videos processed.")
