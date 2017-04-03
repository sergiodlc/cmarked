# -*- mode: python -*-

block_cipher = None

added_files = [
	('../styles', 'styles'),
	('C:\\develop\\cmark\\build\\src\\Release\\cmark.dll', '.'),
	('C:\\Program Files (x86)\\Pandoc\\pandoc.exe', '.'),
]

added_binaries = [
#	('C:\\develop\\cmark\\build\\src\\Release\\cmark.dll', '.'),
#	('C:\\Program Files (x86)\\Pandoc\\pandoc.exe', '.'),
]

a = Analysis(['launch.py'],
             pathex=['C:\\Users\\Sergio\\AppData\\Local\\Programs\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'c:\\develop\\cmarked\\src'],
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
