[中文文档请点击这里](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/README_ZH.md)
# VITS Voice Conversion
This repo will guide you to add your voice into an existing VITS TTS model
to make it a high-quality voice converter to all existing character voices in the model.  

Welcome to play around with the base model, a Trilingual Anime VITS!
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer)

### Currently Supported Tasks:
- [x] Convert user's voice to characters listed [here](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/configs/finetune_speaker.json)
- [x] Chinese, English, Japanese TTS with user's voice
- [x] Chinese, English, Japanese TTS with custom characters!

### Currently Supported Characters for TTS & VC:
- [x] Umamusume Pretty Derby (Used as base model pretraining)
- [x] Sanoba Witch (Used as base model pretraining)
- [x] Genshin Impact (Used as base model pretraining)
- [x] Any character you wish as long as you have their voices!




## Fine-tuning
It's recommended to perform fine-tuning on [Google Colab](https://colab.research.google.com/drive/1omMhfYKrAAQ7a6zOCsyqpla-wU-QyfZn?usp=sharing)
because the original VITS has some dependencies that are difficult to configure.

### How long does it take? 
1. Install dependencies (2 min)
2. Record at least 20 your own voice (5~10 min)
3. Upload your character voices, which should be a `.zip` file,
it's file structure should be like:
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
Note that the format & name of the audio files does not matter as long as they are audio files.  
Audio quality requirements: >=2s, <=20s per audio, background noise should be as less as possible.
Audio quantity requirements: at least 10 per character, better if 20+ per character.   
You can either choose to perform step 2, 3, or both, depending on your needs.
4. Fine-tune (30 min)  
After everything is done, download the fine-tuned model & model config

## Inference or Usage (Currently support Windows only)
0. Remember to download your fine-tuned model!
1. Download the latest release
2. Put your model & config file into the folder `inference`, make sure to rename the model to `G_latest.pth` and config file to `finetune_speaker.json`
3. The file structure should be as follows:
```shell
inference
├───inference.exe
├───...
├───finetune_speaker.json
└───G_latest.json
```
4. run `inference.exe`, the browser should pop up automatically.
