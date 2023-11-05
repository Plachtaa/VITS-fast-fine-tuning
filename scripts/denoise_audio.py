import os
import json
import torchaudio
import concurrent.futures

raw_audio_dir = "./raw_audio/"
denoise_audio_dir = "./denoised_audio/"
filelist = list(os.walk(raw_audio_dir))[0][2]
# 2023/4/21: Get the target sampling rate
with open("./configs/finetune_speaker.json", 'r', encoding='utf-8') as f:
    hps = json.load(f)
target_sr = hps['data']['sampling_rate']

def get_filename(path):
    if os.path.isdir(path):
        print(f"isDir,return: {path}")
        return ""
    else:
        file_name = os.path.basename(path)
        file_name = os.path.splitext(file_name)[0]
        return file_name

def process_file(file):
    file_name = get_filename(file)
    if file_name == "":
        return
    if not os.path.exists(f"./separated/htdemucs/{file_name}/vocals.wav"):
        command = f"demucs --two-stems=vocals {raw_audio_dir}{file}"
        print(f"Process: {command}")
        os.system(command)
        print(f"Seperated: {file}")
    wav, sr = torchaudio.load(f"./separated/htdemucs/{file_name}/vocals.wav", frame_offset=0, num_frames=-1, normalize=True,
                              channels_first=True)
    # merge two channels into one
    wav = wav.mean(dim=0).unsqueeze(0)
    if sr != target_sr:
        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)(wav)
    torchaudio.save(denoise_audio_dir + file, wav, target_sr, channels_first=True)
    print(f"Ok: {file}")

num_threads = 16
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit each file to the executor for processing
    futures = []
    for file in filelist:
        futures.append(executor.submit(process_file, file))
    # Wait for all tasks to complete
    concurrent.futures.wait(futures)
