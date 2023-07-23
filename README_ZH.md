English Documentation Please Click [here](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/README.md)
# VITS 快速微调
这个代码库会指导你如何将自定义角色（甚至你自己），加入预训练的VITS模型中，在1小时内的微调使模型具备如下功能：  
1. 在 模型所包含的任意两个角色 之间进行声线转换
2. 以 你加入的角色声线 进行中日英三语 文本到语音合成。  

本项目使用的底模涵盖常见二次元男/女配音声线（来自原神数据集）以及现实世界常见男/女声线（来自VCTK数据集），支持中日英三语，保证能够在微调时快速适应新的声线。

欢迎体验微调所使用的底模！  

中日英：[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer) 作者：我  

中日：[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai) 作者：[SayaSS](https://github.com/SayaSS)  

纯中文：（没有huggingface demo）作者：[Wwwwhy230825](https://github.com/Wwwwhy230825)

### 目前支持的任务:
- [x] 从 10条以上的短音频 克隆角色声音
- [x] 从 3分钟以上的长音频（单个音频只能包含单说话人） 克隆角色声音
- [x] 从 3分钟以上的视频（单个视频只能包含单说话人） 克隆角色声音
- [x] 通过输入 bilibili视频链接（单个视频只能包含单说话人） 克隆角色声音

### 目前支持声线转换和中日英三语TTS的角色
- [x] 任意角色（只要你有角色的声音样本）
（注意：声线转换只能在任意两个存在于模型中的说话人之间进行）




## 微调
若希望于本地机器进行训练，请参考[LOCAL.md](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/LOCAL.md)以进行。  
另外，也可以选择使用 [Google Colab](https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing)
进行微调任务。
### 我需要花多长时间？
1. 安装依赖 (10 min在Google Colab中)
2. 选择预训练模型，详细区别参见[Colab 笔记本页面](https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing)。
3. 上传你希望加入的其它角色声音，详细上传方式见[DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA.MD)
4. 进行微调，根据选择的微调方式和样本数量不同，花费时长可能在20分钟到2小时不等。

微调结束后可以直接下载微调好的模型，日后在本地运行（不需要GPU）

## 本地运行和推理
0. 记得下载微调好的模型和config文件！
1. 下载最新的Release包（在Github页面的右侧）
2. 把下载的模型和config文件放在 `inference`文件夹下, 其文件名分别为 `G_latest.pth` 和 `finetune_speaker.json`。
3. 一切准备就绪后，文件结构应该如下所示:
```
inference
├───inference.exe
├───...
├───finetune_speaker.json
└───G_latest.pth
```
4. 运行 `inference.exe`, 浏览器会自动弹出窗口, 注意其所在路径不能有中文字符或者空格.
5. 请注意，声线转换功能需要安装`ffmpeg`才能正常使用.

## 在MoeGoe使用
0. MoeGoe以及类似其它VITS推理UI使用的config格式略有不同，需要下载的文件为模型`G_latest.pth`和配置文件`moegoe_config.json`
1. 按照[MoeGoe](https://github.com/CjangCjengh/MoeGoe)页面的提示配置路径即可使用。
2. MoeGoe在输入句子时需要使用相应的语言标记包裹句子才能正常合成。（日语用[JA], 中文用[ZH], 英文用[EN]），例如：  
[JA]こんにちわ。[JA]  
[ZH]你好！[ZH]  
[EN]Hello![EN]  

## 帮助
如果你在使用过程中遇到了任何问题，可以在[这里](https://github.com/Plachtaa/VITS-fast-fine-tuning/issues/new)开一个issue，或者加入Discord服务器寻求帮助：[Discord](https://discord.gg/TcrjDFvm5A)。
