import os
import torch
import torchaudio

audio_dir = "./user_voice/"
wavfiles = []
for filename in list(os.walk(audio_dir))[0][2]:
    if filename.endswith(".wav"):
        wavfiles.append(filename)

# denoise with demucs
for i, wavfile in enumerate(wavfiles):
    os.system(f"demucs --two-stems=vocals {audio_dir}{wavfile}")

# read & store the denoised vocals back
for wavfile in wavfiles:
    i = wavfile.strip(".wav")
    wav, sr = torchaudio.load(f"./separated/htdemucs/{i}/vocals.wav", frame_offset=0, num_frames=-1, normalize=True, channels_first=True)
    # merge two channels into one
    wav = wav.mean(dim=0).unsqueeze(0)
    if sr != 22050:
        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
    torchaudio.save(f"./user_voice/{i}.wav", wav, 22050, channels_first=True)