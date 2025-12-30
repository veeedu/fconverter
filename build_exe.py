import subprocess
import sys
import os

def build_exe():
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Check for ffmpeg.exe
    if not os.path.exists("ffmpeg.exe"):
        print("ffmpeg.exe not found in project root.")
        print("Please download ffmpeg for Windows from https://ffmpeg.org/download.html")
        print("Extract ffmpeg.exe and place it in the project root folder.")
        sys.exit(1)

    # PyInstaller command - use full path
    pyinstaller_path = r"C:\users\vedu\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe"

    cmd = [
        pyinstaller_path,
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--name", "OfflineConverter",
        "--add-data", "converters;converters",  # Include converters folder (Windows separator)
        "--add-binary", "ffmpeg.exe;.",  # Bundle ffmpeg
        "--hidden-import", "PySide6.QtWidgets",
        "--hidden-import", "PySide6.QtCore",
        "--hidden-import", "PySide6.QtGui",
        "--hidden-import", "pydub",
        "--hidden-import", "PIL",
        "--hidden-import", "PyPDF2",
        "--hidden-import", "docx",
        "--hidden-import", "lxml",  # For docx
        "app.py"
    ]

    print("Building executable...")
    subprocess.check_call(cmd)
    print("Build complete. Check the 'dist' folder for OfflineConverter.exe")
    print("The .exe is now fully portable and includes FFmpeg.")

if __name__ == "__main__":
    build_exe()