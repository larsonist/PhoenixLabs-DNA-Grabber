# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  
    pathex=[],
    binaries=[],
    datas=[
        # openocd
        ('openocd.exe', '.'),
        ('openocd-347.exe', '.'),
        
        # cfg
        ('xilinx-dna.cfg', '.'),
        ('xilinx-dna-347.cfg', '.'),
        ('xilinx-xc7.cfg', '.'),
        ('jtagspi.cfg', '.'),
        ('init_232_35t.cfg', '.'),
        ('init_232_75t.cfg', '.'),
        ('init_347_35t.cfg', '.'),
        ('init_347_75t.cfg', '.'),
        
        # dlls
        ('cygusb-1.0.dll', '.'),
        ('cygwin1.dll', '.'),
        ('libhidapi-0.dll', '.'),
        ('libusb-1.0.dll', '.'),
        
        # app
        ('phoenix.ico', '.'),
        ('gui', 'gui'),
        ('core', 'core')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PhoenixLabsDNAGrabber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='phoenix.ico'
)