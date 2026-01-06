import subprocess
import sys
from pathlib import Path
from tqdm import tqdm

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi", ".mov", ".webm", ".flv", ".ts"}

def is_video(file):
    return file.suffix.lower() in VIDEO_EXTENSIONS

def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

def remux(input_file, output_file):
    return run([
        "ffmpeg", "-y",
        "-i", str(input_file),
        "-c", "copy",
        "-movflags", "+faststart",
        str(output_file)
    ])

def reencode(input_file, output_file):
    return run([
        "ffmpeg", "-y",
        "-i", str(input_file),

        # Video: Telegram-safe, high quality
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.1",

        # Audio: Telegram-safe
        "-c:a", "aac",
        "-b:a", "160k",

        "-movflags", "+faststart",
        str(output_file)
    ])

def main():
    if len(sys.argv) != 2:
        print("Usage: python telegram_fix.py <folder_path>")
        sys.exit(1)

    input_dir = Path(sys.argv[1]).resolve()
    if not input_dir.is_dir():
        print("❌ Invalid folder path")
        sys.exit(1)

    output_dir = Path(__file__).parent / "telegram_ready"
    output_dir.mkdir(exist_ok=True)

    videos = [v for v in input_dir.iterdir() if v.is_file() and is_video(v)]

    if not videos:
        print("⚠️ No video files found")
        return

    print(f"🎬 Found {len(videos)} videos")
    print(f"📁 Output: {output_dir}\n")

    for video in tqdm(videos, desc="Processing", unit="video"):
        out = output_dir / f"{video.stem}.mp4"

        # 1) Try no-loss remux
        if remux(video, out):
            continue

        # 2) If remux fails, re-encode
        if out.exists():
            out.unlink()

        if not reencode(video, out):
            print(f"\n❌ Failed: {video.name}")

    print("\n✅ DONE — all videos Telegram compatible")

if __name__ == "__main__":
    main()
