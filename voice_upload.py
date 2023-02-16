from google.colab import files
import shutil
import os
basepath = os.getcwd()
uploaded = files.upload() # 上传文件
upload_path = "./custom_character_voice/"
if not os.path.exists(upload_path):
  os.mkdir(upload_path)
for filename in uploaded.keys():
    #将上传的文件移动到指定的位置上
    shutil.move(os.path.join(basepath, filename), os.path.join(upload_path, filename))
