[中文文档请点击这里](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/README_CN.md)
# VITS Voice Conversion
This repo will guide you to add your voice into an existing VITS TTS model
to make it a high-quality voice converter to all existing character voices in the model.  

Welcome to play around with the base model, a Trilingual Anime VITS!
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer)

### Currently Supported Tasks:
- [x] Convert user's voice to characters listed [here](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/configs/finetune_speaker.json)
- [x] Chinese, English, Japanese TTS with user's voice
- [ ] Chinese, English, Japanese TTS with custom characters...

### Currently Supported Characters for TTS & VC:
- [x] Umamusume Pretty Derby
- [x] Sanoba Witch
- [x] Genshin Impact
- [ ] Custom characters...




## Fine-tuning
It's recommended to perform fine-tuning on [Google Colab](https://colab.research.google.com/drive/1omMhfYKrAAQ7a6zOCsyqpla-wU-QyfZn?usp=sharing)
because the original VITS has some dependencies that are difficult to configure.

### How long does it take?
1. Install dependencies (2 min)
2. Record at least 10 your own voice (5 min)
3. Fine-tune (30 min)

## Inference or Usage

1. Install Python if you haven't done so (Python >= 3.7)
2. Clone this repo:  
`git clone https://github.com/SongtingLiu/VITS_voice_conversion.git`
3. Install dependencies  
`pip install -r requirements_infer.txt`
4. run VC_inference.py  
`python VC_inference.py`
