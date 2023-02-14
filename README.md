# VITS Voice Conversion
This repo will guide you to add your voice into an existing VITS TTS model
to make it a high-quality voice converter to all existing character voices in the model.  

Welcome to play around with the base model, a Trilingual Anime VITS!
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer)

### Currently Supported Tasks:
- [x] Convert user's voice to characters listed below
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

1. Clone this repo
2. Install dependencies
3. run VC_inference.py
