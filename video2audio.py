from moviepy.editor import AudioFileClip
import os
video_dir = "./video_data/"
audio_dir = "./raw_audio/"
filelist = list(os.walk(video_dir))[0][2]
for file in filelist:
    if file.endswith(".mp4"):
        my_audio_clip = AudioFileClip(video_dir + file)
        my_audio_clip.write_audiofile(audio_dir + file.rstrip(".mp4") + ".wav")

