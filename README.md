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


## Inference with CLI
In this example, we will show how to run inference with the default pretrained model. We are now in the main repository directory.
1. Create the necessary folders and download the necessary files.
```
cd monotonic_align/
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
# download data for fine-tuning
wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
unzip sampled_audio4ft_v2.zip
```

For your finetuned model you may need to create additional directories:
```
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice
```
2. Download pretrained models. For example, trilingual model:
```
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/D_trilingual.pth -O ./pretrained_models/D_0.pth
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth -O ./pretrained_models/G_0.pth
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/configs/uma_trilingual.json -O ./configs/finetune_speaker.json
```
3. Activate your environment and run the following code:
`python3 cmd_inference.py -m pretrained_models/G_0.pth -c configs/finetune_speaker.json -t 你好，训练员先生，很高兴见到你。 -s "派蒙 Paimon (Genshin Impact)" -l "简体中文"`
You can choose another language, customize output folder, change text and character, but all these parameters you can see in the file `cmd_inference.py`.
Below I'll show only how to change the character.
4. To change the character please open config file (`configs/finetune_speaker.json`). There you can find dictionary `speakers`, where you'll be able to see full list of speakers. Just copy the name of the character you need use it instead of `"派蒙 Paimon (Genshin Impact)"`
5. If you have success, you can find output `.wav` file in the `output/vits`


## Use in MoeGoe
0. Prepare downloaded model & config file, which are named `G_latest.pth` and `moegoe_config.json`, respectively.
1. Follow [MoeGoe](https://github.com/CjangCjengh/MoeGoe) page instructions to install, configure path, and use.

## Looking for help?
If you have any questions, please feel free to open an [issue](https://github.com/Plachtaa/VITS-fast-fine-tuning/issues/new) or join our [Discord](https://discord.gg/TcrjDFvm5A) server.
