from google.colab import files
import shutil
import os
basepath = os.getcwd()
uploaded = files.upload() # 上传文件
for filename in uploaded.keys():
    assert(filename.endswith(".txt")), "speaker-videolink info could only be .txt file!"
    shutil.move(os.path.join(basepath, filename), os.path.join("./speaker_links.txt"))

with open("./speaker_links.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
speakers = []
for line in lines:
    line = line.replace("\n", "").replace(" ", "")
    if line == "":
        continue
    speaker, link = line.split("|")
    if speaker not in speakers:
        speakers.append(speaker)
    # download link
    import random
    filename = speaker + "_" + str(random.randint(0, 1000000))
    os.system(f"youtube-dl -f 0 {link} -o ./video_data/{filename}.mp4")