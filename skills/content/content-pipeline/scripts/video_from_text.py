#!/usr/bin/env python3
"""Create a simple video from text + background image.

Usage: python video_from_text.py --text "Hello World" --bg background.png --output video.mp4
       python video_from_text.py --script script.json --output video.mp4

Script JSON format:
{
  "slides": [
    {"text": "Slide 1 text", "duration": 3, "bg": "optional_bg.png"},
    {"text": "Slide 2 text", "duration": 4}
  ],
  "voiceover": "path/to/audio.wav",
  "subtitles": "path/to/subs.srt"
}
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FFMPEG = "/home/dima/bin/ffmpeg"

def create_slides_video(slides, output, fps=1):
    """Create video from text slides using ffmpeg."""
    with tempfile.TemporaryDirectory() as tmpdir:
        from PIL import Image, ImageDraw, ImageFont

        for i, slide in enumerate(slides):
            img = Image.new("1080x1920", color=(15, 15, 25))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            except OSError:
                font = ImageFont.load_default()

            # Center text
            text = slide.get("text", "")
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1080 - text_width) // 2
            draw.text((x, 800), text, fill="white", font=font)

            slide_path = Path(tmpdir) / f"slide_{i:04d}.png"
            img.save(slide_path)

            # Each slide shown for duration seconds
            duration = slide.get("duration", 3)

            # Create video for this slide
            slide_video = Path(tmpdir) / f"slide_{i:04d}.mp4"
            subprocess.run([
                FFMPEG, "-y",
                "-loop", "1",
                "-i", str(slide_path),
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1080:1920",
                str(slide_video)
            ], capture_output=True)

        # Concatenate all slides
        concat_file = Path(tmpdir) / "concat.txt"
        with open(concat_file, "w") as f:
            for i in range(len(slides)):
                f.write(f"file '{tmpdir}/slide_{i:04d}.mp4'\n")

        subprocess.run([
            FFMPEG, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output)
        ], capture_output=True)

        print(f"Video created: {output}")

def add_audio(video_path, audio_path, output_path):
    """Merge audio track with video."""
    subprocess.run([
        FFMPEG, "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path)
    ], capture_output=True)

def add_subtitles(video_path, subs_path, output_path):
    """Burn subtitles into video."""
    subprocess.run([
        FFMPEG, "-y",
        "-i", video_path,
        "-vf", f"subtitles={subs_path}:force_style='FontSize=22,MarginV=80'",
        "-c:a", "copy",
        str(output_path)
    ], capture_output=True)

def main():
    parser = argparse.ArgumentParser(description="Create video from text")
    parser.add_argument("--text", help="Single slide text")
    parser.add_argument("--script", help="JSON script file")
    parser.add_argument("--output", default="output.mp4", help="Output path")
    parser.add_argument("--voiceover", help="Audio file to overlay")
    parser.add_argument("--subtitles", help="SRT subtitle file")
    args = parser.parse_args()

    if args.script:
        with open(args.script) as f:
            data = json.load(f)
        slides = data.get("slides", [{"text": args.text or "", "duration": 3}])
    elif args.text:
        slides = [{"text": args.text, "duration": max(3, len(args.text) // 15)}]
    else:
        print("Provide --text or --script", file=sys.stderr)
        sys.exit(1)

    create_slides_video(slides, args.output)

    if args.voiceover:
        temp_out = args.output + ".tmp.mp4"
        add_audio(args.output, args.voiceover, temp_out)
        Path(temp_out).rename(args.output)

    if args.subtitles:
        temp_out = args.output + ".tmp.mp4"
        add_subtitles(args.output, args.subtitles, temp_out)
        Path(temp_out).rename(args.output)

if __name__ == "__main__":
    main()
