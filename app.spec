# app.spec
from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, PYZ, EXE

datas = []
binaries = []
hiddenimports = []

# Collect everything needed for PySide6
pyside6 = collect_all("PySide6")
datas += pyside6.datas
binaries += pyside6.binaries
hiddenimports += pyside6.hiddenimports

a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="VeduConverter",
    windowed=True,
    console=False,
)
