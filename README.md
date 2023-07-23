[中文文档请点击这里](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/README_ZH.md)
# VITS Fast Fine-tuning
This repo will guide you to add your own character voices, or even your own voice, into existing VITS TTS model
to make it able to do the following tasks in less than 1 hour:  

1. Many-to-many voice conversion between any characters you added & preset characters in the model.
2. English, Japanese & Chinese Text-to-Speech synthesis with the characters you added & preset characters  
  

Welcome to play around with the base models!  
Chinese & English & Japanese：[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer) Author: Me  

Chinese & Japanese：[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai) Author: [SayaSS](https://github.com/SayaSS)  

Chinese only：(No running huggingface spaces) Author: [Wwwwhy230825](https://github.com/Wwwwhy230825)


### Currently Supported Tasks:
- [x] Clone character voice from 10+ short audios
- [x] Clone character voice from long audio(s) >= 3 minutes (one audio should contain single speaker only)
- [x] Clone character voice from videos(s) >= 3 minutes (one video should contain single speaker only)
- [x] Clone character voice from BILIBILI video links (one video should contain single speaker only)

### Currently Supported Characters for TTS & VC:
- [x] Any character you wish as long as you have their voices!
(Note that voice conversion can only be conducted between any two speakers in the model)



## Fine-tuning
See [LOCAL.md](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/LOCAL.md) for local training guide.  
Alternatively, you can perform fine-tuning on [Google Colab](https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing)


### How long does it take? 
1. Install dependencies (3 min)
2. Choose pretrained model to start. The detailed differences between them are described in [Colab Notebook](https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing)
3. Upload the voice samples of the characters you wish to add，see [DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA_EN.MD) for detailed uploading options.
4. Start fine-tuning. Time taken varies from 20 minutes ~ 2 hours, depending on the number of voices you uploaded.


## Inference or Usage (Currently support Windows only)
0. Remember to download your fine-tuned model!
1. Download the latest release
2. Put your model & config file into the folder `inference`, which are named `G_latest.pth` and `finetune_speaker.json`, respectively.
3. The file structure should be as follows:
```
inference
├───inference.exe
├───...
├───finetune_speaker.json
└───G_latest.pth
```
4. run `inference.exe`, the browser should pop up automatically.
5. Note: you must install `ffmpeg` to enable voice conversion feature.

## Use in MoeGoe
0. Prepare downloaded model & config file, which are named `G_latest.pth` and `moegoe_config.json`, respectively.
1. Follow [MoeGoe](https://github.com/CjangCjengh/MoeGoe) page instructions to install, configure path, and use.

## Looking for help?
If you have any questions, please feel free to open an [issue](https://github.com/Plachtaa/VITS-fast-fine-tuning/issues/new) or join our [Discord](https://discord.gg/TcrjDFvm5A) server.
