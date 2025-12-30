# Instructions to Build Portable .exe on Windows (or Linux with Wine)

## Option 1: Build on Windows (Recommended)

1. Transfer the entire project folder to a Windows machine.
2. Install Python 3.11 on Windows.
3. Download FFmpeg for Windows from https://ffmpeg.org/download.html, extract `ffmpeg.exe`, and place it in the project root.
4. Create a virtual environment: `python -m venv venv && venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `python build_exe.py`
7. Find `OfflineConverter.exe` in `dist/`.

## Option 2: Build on Linux Mint using Wine

1. Install Wine on Linux Mint:
   ```
   sudo apt update
   sudo apt install wine
   ```

2. Download Python installer for Windows (python-3.11.x-amd64.exe) from https://www.python.org/downloads/windows/

3. Install Python in Wine:
   ```
   wine python-3.11.x-amd64.exe
   ```
   Follow the installer prompts.

4. Download FFmpeg for Windows, extract `ffmpeg.exe`, and place it in the project folder.

5. Install PyInstaller and dependencies in Wine's Python:
   ```
   wine python -m pip install pyinstaller
   wine python -m pip install -r requirements.txt
   ```

6. Run the build script under Wine:
   ```
   wine python build_exe.py
   ```

7. The `OfflineConverter.exe` will be in `dist/`.

Note: Wine builds may have compatibility issues. Test the .exe on a real Windows machine. If problems occur, use Option 1.