import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
from google.colab import files

basepath = os.getcwd()
uploaded = files.upload()  # 上传文件
for filename in uploaded.keys():
    assert (filename.endswith(".txt")), "speaker-videolink info could only be .txt file!"
    shutil.move(os.path.join(basepath, filename), os.path.join("./speaker_links.txt"))


def generate_infos():
    infos = []
    with open("./speaker_links.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "").replace(" ", "")
        if line == "":
            continue
        speaker, link = line.split("|")
        filename = speaker + "_" + str(random.randint(0, 1000000))
        infos.append({"link": link, "filename": filename})
    return infos


def download_video(info):
    link = info["link"]
    filename = info["filename"]
    os.system(f"youtube-dl -f 0 {link} -o ./video_data/{filename}.mp4 --no-check-certificate")


if __name__ == "__main__":
    infos = generate_infos()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(download_video, infos)
