import subprocess
import sys
import os

# Get ffmpeg path
if hasattr(sys, '_MEIPASS'):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_path):
        ffmpeg_path = "ffmpeg"  # Fallback
else:
    ffmpeg_path = "ffmpeg"

def convert(input_path, output_path):
    subprocess.run([ffmpeg_path, "-y", "-i", input_path, output_path])
