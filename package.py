import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--add-data=ffmpeg.exe;.',
    '--icon=icons/icon.ico',
    '--name=Youtube Downloader'
])