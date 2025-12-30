import os
from pathlib import Path

def get_output_dir():
    desktop = Path.home() / "Desktop"
    output = desktop / "output"
    output.mkdir(exist_ok=True)
    return output
