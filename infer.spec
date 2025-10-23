# infer.spec – Build configuration for AI Crop Doctor

# -----------------------------
# Import build modules
# -----------------------------
# PyInstaller uses these to pack files into a single .exe
# Keep this structure exactly the same

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['infer.py'],               # main entry file
    pathex=['.'],               # current directory
    binaries=[],                # no extra binary libs
    datas=[
        ('models/*', 'models'),             # include model files
        ('resources/*', 'resources'),       # include JSON, images, tips
        ('logs/*', 'logs'),                 # optional: log folder
        ('tts_engine.py', '.'),             # include TTS engine
        ('utils.py', '.'),                  # include utils
        ('colors.py', '.'),                 # include color/animation helpers
    ],
    hiddenimports=[
        'tensorflow', 'keras', 'numpy', 'PIL', 'argparse',
        'time', 'os', 'json', 'random', 'logging', 'sys'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# -----------------------------
# Executable Build Section
# -----------------------------

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_Crop_Doctor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # set False if you want no terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/leaf.ico'  # optional app icon
)
