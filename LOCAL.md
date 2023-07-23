# Train locally
### Build environment
0. Make sure you have installed `Python==3.8`, CMake & C/C++ compilers, ffmpeg; 
1. Clone this repository;
2. Run `pip install -r requirements.txt`;
3. Install GPU version PyTorch: (Make sure you have CUDA 11.6 or 11.7 installed)
    ```
   # CUDA 11.6
    pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
    # CUDA 11.7
    pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
   ```
4. Install necessary libraries for dealing video data:
    ```
   pip install imageio==2.4.1
   pip install moviepy
   ```
5. Build monotonic align (necessary for training)
    ```
    cd monotonic_align
    mkdir monotonic_align
    python setup.py build_ext --inplace
    cd ..
    ```
6. Download auxiliary data for training
    ```
    mkdir pretrained_models
    # download data for fine-tuning
    wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
    unzip sampled_audio4ft_v2.zip
    # create necessary directories
    mkdir video_data
    mkdir raw_audio
    mkdir denoised_audio
    mkdir custom_character_voice
    mkdir segmented_character_voice
   ```
7. Download pretrained model, available options are:
    ```
   CJE: Trilingual (Chinese, Japanese, English)
   CJ: Dualigual (Chinese, Japanese)
   C: Chinese only
   ```
   ### Linux
   To download `CJE` model, run the following:
    ```
   wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/D_trilingual.pth -O ./pretrained_models/D_0.pth
   wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth -O ./pretrained_models/G_0.pth
   wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/configs/uma_trilingual.json -O ./configs/finetune_speaker.json
   ```
   To download `CJ` model, run the following:
   ```
   wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/D_0-p.pth -O ./pretrained_models/D_0.pth
   wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/G_0-p.pth -O ./pretrained_models/G_0.pth
   wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/config.json -O ./configs/finetune_speaker.json
   ```
   To download `C` model, run the follwoing:
   ```
   wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/D_0.pth -O ./pretrained_models/D_0.pth
   wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/G_0.pth -O ./pretrained_models/G_0.pth
   wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/config.json -O ./configs/finetune_speaker.json
   ```
   ### Windows
   Manually download `G_0.pth`, `D_0.pth`, `finetune_speaker.json` from the URLs in one of the options described above.
   
   Rename all `G` models to `G_0.pth`, `D` models to `D_0.pth`, config files (`.json`) to `finetune_speaker.json`.  
   Put `G_0.pth`, `D_0.pth` under `pretrained_models` directory;  
   Put `finetune_speaker.json` under `configs` directory  
   
   #### Please note that when you download one of them, the previous model will be overwritten.
9. Put your voice data under corresponding directories, see [DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA_EN.MD) for detailed different uploading options.
   ### Short audios
   1. Prepare your data according to [DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA_EN.MD) as a single `.zip` file;  
   2. Put your file under directory `./custom_character_voice/`;
   3. run `unzip ./custom_character_voice/custom_character_voice.zip -d ./custom_character_voice/`
   
   ### Long audios
   1. Name your audio files according to [DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA_EN.MD);
   2. Put your renamed audio files under directory `./raw_audio/`
   
   ### Videos
   1. Name your video files according to [DATA.MD](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/DATA_EN.MD);
   2. Put your renamed video files under directory `./video_data/`
10. Process all audio data.
   ```
   python scripts/video2audio.py
   python scripts/denoise_audio.py
   python scripts/long_audio_transcribe.py --languages "{PRETRAINED_MODEL}" --whisper_size large
   python scripts/short_audio_transcribe.py --languages "{PRETRAINED_MODEL}" --whisper_size large
   python scripts/resample.py
   ```
   Replace `"{PRETRAINED_MODEL}"` with one of `{CJ, CJE, C}` according to your previous model choice.  
   Make sure you have a minimum GPU memory of 12GB. If not, change the argument `whisper_size` to `medium` or `small`.

10. Process all text data.  
   If you choose to add auxiliary data, run `python preprocess_v2.py --add_auxiliary_data True --languages "{PRETRAINED_MODEL}"`  
   If not, run `python preprocess_v2.py --languages "{PRETRAINED_MODEL}"`  
   Do replace `"{PRETRAINED_MODEL}"` with one of `{CJ, CJE, C}` according to your previous model choice.

11. Start Training.  
   Run `python finetune_speaker_v2.py -m ./OUTPUT_MODEL --max_epochs "{Maximum_epochs}" --drop_speaker_embed True`  
   Do replace `{Maximum_epochs}` with your desired number of epochs. Empirically, 100 or more is recommended.  
   To continue training on previous checkpoint, change the training command to: `python finetune_speaker_v2.py -m ./OUTPUT_MODEL --max_epochs "{Maximum_epochs}" --drop_speaker_embed False --cont True`. Before you do this, make sure you have previous `G_latest.pth` and `D_latest.pth` under `./OUTPUT_MODEL/` directory.  
   To view training progress, open a new terminal and `cd` to the project root directory, run `tensorboard --logdir=./OUTPUT_MODEL`, then visit `localhost:6006` with your web browser.

12. After training is completed, you can use your model by running:  
   `python VC_inference.py --model_dir ./OUTPUT_MODEL/G_latest.pth --share True`
13. To clear all audio data, run:  
   ### Linux
   ```
   rm -rf ./custom_character_voice/* ./video_data/* ./raw_audio/* ./denoised_audio/* ./segmented_character_voice/* ./separated/* long_character_anno.txt short_character_anno.txt
   ```
   ### Windows
   ```
   del /Q /S .\custom_character_voice\* .\video_data\* .\raw_audio\* .\denoised_audio\* .\segmented_character_voice\* .\separated\* long_character_anno.txt short_character_anno.txt
   ```


