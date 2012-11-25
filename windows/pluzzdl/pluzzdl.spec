# -*- mode: python -*-
a = Analysis(['C:\\pluzzdl\\mainGui.py'],
             pathex=['C:\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + [ ('pluzzdl.cfg', 'C:\pluzzdl\pluzzdl.cfg', 'DATA') ],
          name=os.path.join('dist', 'pluzzdl.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='C:\\pluzzdl\\tvdownloader.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'pluzzdl.exe.app'))
