# -*- mode: python ; coding: utf-8 -*-
"""
HBS Carousel Windows PyInstaller Spec
Builds hbs-carousel.exe for Windows
"""
a = Analysis(
    ['../../../carousel.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../../../config.py', '.'),
        ('../../carousel_config.json.template', '.'),
    ],
    hiddenimports=['pyglet'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='hbs-carousel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)