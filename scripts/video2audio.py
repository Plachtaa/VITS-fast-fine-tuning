import os
from concurrent.futures import ThreadPoolExecutor

from moviepy.editor import AudioFileClip

video_dir = "./video_data/"
audio_dir = "./raw_audio/"
filelist = list(os.walk(video_dir))[0][2]


def generate_infos():
    videos = []
    for file in filelist:
        if file.endswith(".mp4"):
            videos.append(file)
    return videos


def clip_file(file):
    my_audio_clip = AudioFileClip(video_dir + file)
    my_audio_clip.write_audiofile(audio_dir + file.rstrip(".mp4") + ".wav")


if __name__ == "__main__":
    infos = generate_infos()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(clip_file, infos)
