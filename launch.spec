# -*- mode: python -*-

block_cipher = None

added_files = [('pics', 'pics'),
               ('stimuli', 'stimuli')
               ]

a = Analysis(['launch.py'],
             pathex=['/home/ivanvoronin/P-files/2018-09-04-RT_grant/RT_tests'],
             binaries=[],
             datas=added_files,
             hiddenimports=['UserList', 'UserString', 'psychopy.iohub.devices.display', 'msgpack_numpy'],
             hookspath=[],
             runtime_hooks=['gtk_rthook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='launch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

base_dir = '.'
gtks = ['loaders.cache']
data_files = [(x, os.path.join(base_dir, x), 'DATA') for x in gtks]

more_binaries = []
pixbuf_dir = '/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders'
for pixbuf_type in os.listdir(pixbuf_dir):
    if pixbuf_type.endswith('.so'):
        more_binaries.append((pixbuf_type, os.path.join(pixbuf_dir, pixbuf_type), 'BINARY'))

coll = COLLECT(exe, data_files,
               a.binaries + more_binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launch')
