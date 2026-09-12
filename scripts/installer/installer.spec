# -*- mode: python ; coding: utf-8 -*-


from pathlib import Path


PROJECT_ROOT = Path(SPECPATH).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src" / "nuoyanlib"
INSTALLER_DIRECTORY = PROJECT_ROOT / "scripts" / "installer"
ICON_PATH = PROJECT_ROOT / "img" / "installer_icon.ico"


a = Analysis(
    [str(INSTALLER_DIRECTORY / "main.py")],
    pathex=[str(INSTALLER_DIRECTORY)],
    binaries=[],
    datas=[
        (str(SOURCE_DIRECTORY), "nuoyanlib"),
        (str(ICON_PATH), "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name="nuoyanlib-installer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon=str(ICON_PATH),
)
