English Documentation Please Click [here](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/README_EN.md)
# VITS 快速微调
这个代码库会指导你如何将自定义角色，甚至你自己的声线加入一个现有的VITS模型中，在1小时内的微调使模型具备如下功能：  
1. 在 你 & 你加入的角色 & 预设角色 之间进行任意声线转换
2. 以 你的声线 & 你加入的角色声线 & 预设角色声线 进行中日英三语 文本到语音合成。  

本项目使用的底模涵盖常见二次元男/女配音声线（来自原神数据集）以及现实世界常见男/女声线（来自VCTK数据集），支持中日英三语，保证能够在微调时快速适应新的声线。

欢迎体验微调所使用的底模！ 
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer)

### 目前支持的任务:
- [x] 转换用户声线到 [这些角色](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/configs/finetune_speaker.json)
- [x] 自定义角色的中日英三语TTS！

### 目前支持声线转换和中日英三语TTS的角色
- [x] 赛马娘 （仅已实装角色）（预训练时使用的角色）
- [x] 魔女的夜宴（柚子社） （5人）（预训练时使用的角色）
- [x] 原神 （仅已实装角色）（预训练时使用的角色）
- [x] 任意角色（只要你有角色的声音样本）




## 微调
建议使用 [Google Colab](https://colab.research.google.com/drive/1omMhfYKrAAQ7a6zOCsyqpla-wU-QyfZn?usp=sharing)
进行微调任务，因为VITS在多语言情况下的某些环境依赖相当难以配置。
### 在Google Colab里，我需要花多长时间？
1. 安装依赖 (2 min)
2. 录入你自己的声音，阅读内容会在UI中提供，每句不超过20个字。 (5~10 min)
3. 上传你希望加入的其它角色声音，用一个`.zip`文件打包
文件结构应该如下所示:
```
Your-zip-file.zip
├───Character_name_1
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───Character_name_2
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───...
├
└───Character_name_n
    ├───xxx.wav
    ├───...
    ├───yyy.mp3
    └───zzz.wav
```
注意音频的格式和名称都不重要，只要它们是音频文件。  
质量要求：2秒以上，20秒以内，尽量不要有背景噪音。  
数量要求：一个角色至少10条，最好每个角色20条以上。  
你可以选择进行步骤2或3，或二者一起，取决于你的需求。  

4. 进行微调 (30 min)  

微调结束后可以直接下载微调好的模型，日后在本地运行（不需要GPU）

## 本地运行和推理
0. 记得下载微调好的模型和config文件！
1. 下载最新的Release包（在Github页面的右侧）
2. 把下载的模型和config文件放在 `inference`文件夹下, 确保模型的文件名为 `G_latest.pth` ，config文件名为 `finetune_speaker.json`
3. 一切准备就绪后，文件结构应该如下所示:
```shell
inference
├───inference.exe
├───...
├───finetune_speaker.json
└───G_latest.pth
```
4. 运行 `inference.exe`, 浏览器会自动弹出窗口, 注意其所在路径不能有中文字符或者空格.

