# -*- mode: python ; coding: utf-8 -*-
"""
HBS Windows PyInstaller Spec
Builds hbs.exe for Windows
"""
a = Analysis(
    ['../../../hbs.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../../../config.py', '.'),
        ('../../../config.json', '.'),
        ('../../../launcher.sh', '.'),
        ('../../../routes', 'routes'),
    ],
    hiddenimports=[],
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
    name='hbs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)