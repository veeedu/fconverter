from pydub import AudioSegment
from pathlib import Path
import sys
import os

# Set ffmpeg path for bundled executable
if hasattr(sys, '_MEIPASS'):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
    if os.path.exists(ffmpeg_path):
        AudioSegment.converter = ffmpeg_path

def convert(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format=Path(output_path).suffix[1:])
