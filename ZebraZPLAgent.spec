# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['agent/zpl_agent.py'],
    pathex=[],
    binaries=[],

    datas=[
        ('agent/printer.ico', 'agent'),
    ],

    hiddenimports=[
        # PyWin32
        'win32print',
        'win32api',
        'win32con',
        'win32file',
        'pywintypes',

        # PySide6
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',

        # pystray + PIL
        'pystray',
        'pystray._win32',
        'PIL',
        'PIL.Image',

        # Waitress
        'waitress',
        'waitress.server',
        'waitress.adjustments',
        'waitress.buffers',
        'waitress.channel',
        'waitress.task',
        'waitress.utilities',
    ],

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
    name='ZebraZPLAgent',
    icon='agent/printer.ico',
    debug=False,
    console=False,      # GUI mode
    strip=False,
    upx=True,
    upx_exclude=[],
)
