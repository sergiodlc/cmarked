# -*- mode: python -*-
import platform
import os

# Find PyQt5 directory
from inspect import getfile
import PyQt5
pyqt_dir = os.path.dirname(getfile(PyQt5))

print('PyQt5 Dir:', pyqt_dir)

block_cipher = None

added_files = [
	('../styles', 'styles'),
#	('C:\\develop\\cmark\\build\\src\\Release\\cmark.dll', '.'),
#	('C:\\Program Files (x86)\\Pandoc\\pandoc.exe', '.'),
	('C:\\projects\\cmark\\build\\windows\\bin\\cmark.dll', '.'),
	('C:\\Program Files (x86)\\Pandoc\\pandoc.exe', '.'),
]

added_binaries = [
#	('C:\\develop\\cmark\\build\\src\\Release\\cmark.dll', '.'),
#	('C:\\Program Files (x86)\\Pandoc\\pandoc.exe', '.'),
]

a = Analysis(['launch.py'],
#             pathex=['C:\\Users\\Sergio\\AppData\\Local\\Programs\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'c:\\develop\\cmarked\\src'],
#             pathex=['C:\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'c:\\projects\\cmarked\\src'],
             pathex=['C:\\projects\\cmarked\\src', pyqt_dir],
             binaries = added_binaries,
             datas = added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if platform.system() == 'Windows':
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='cmarked',
              debug=True,  # True
              strip=False,
              upx=False,
              console=False,  # True
              icon = 'ui\\img\\cmarked.ico'
    )
else:
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='cmarked',
              debug=False,  # True
              strip=False,
              upx=True,
              console=False  # True
    )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='cmarked')
