from pytube import YouTube
from pytube.cli import on_progress
import shutil
import ffmpeg
import os
import sys

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

link = str(input("Video Link: "))
yt = YouTube(link, on_progress_callback=on_progress)
ytname=yt.title.replace('.', '')
streams = str(yt.streams)
with open("streams.tmp", "w") as f:
    f.write(str(streams).replace(', ',',\n').replace('[', '\n').replace(']', '\n'))
    f.close()
streams = []
[streams.append(line) for line in open('streams.tmp') if 'Stream' in line]
print("\n".join(streams))
itag = input("Enter itag number of stream to download: ")
stream = yt.streams.get_by_itag(itag)
prog = []
[prog.append(line) for line in open('streams.tmp') if str(itag) in line]
prog = ''.join(prog).split(' ')
acodec = [i for i, s in enumerate(prog) if 'acodec' in s]
vcodec = [i for i, s in enumerate(prog) if 'vcodec' in s]
if vcodec:
    if acodec:
        print("\nDownloading Video")
        stream.download(output_path="Downloads")
    else:
        print("WARNING\nVideo has no audio")
        aitag = input("Enter itag number of stream or leave blank for no audio: ")
        if aitag != "":
            audio = yt.streams.get_by_itag(aitag)
            print("Downloading Video")
            stream.download(output_path="temp/video")
            print("\nDownloading Audio")
            audio.download(output_path="temp/audio")
            print("\nMerging Audio and Video\n(This may take a while)")
            for file in os.listdir("temp/video"):
                if file.endswith(".mp4"): 
                    video = ffmpeg.input(f"./temp/video/{ytname}.mp4")
                elif file.endswith(".webm"):
                    video = ffmpeg.input(f"./temp/video/{ytname}.webm")
            for file in os.listdir("temp/audio"):
                if file.endswith(".mp4"): 
                    audio = ffmpeg.input(f"./temp/audio/{ytname}.mp4")
                elif file.endswith(".webm"):
                    audio = ffmpeg.input(f"./temp/audio/{ytname}.webm")
            try:
                os.mkdir("Downloads")
            except:
                pass
            ffmpeg.concat(video, audio, v=1, a=1).output(f"./Downloads/{ytname}.mp4").run()
            print("Done")
        else:
            print("Downloading Video")
            stream.download(output_path="Downloads")
elif acodec:
    print("\nDownloading Audio")
    stream.download(output_path="Downloads")
os.remove('streams.tmp')
try:
    shutil.rmtree('temp')
except:
    pass
stream.on_complete(print("\nDownload Successful"))