import os
import torchaudio
raw_audio_dir = "./raw_audio/"
denoise_audio_dir = "./denoised_audio/"
filelist = list(os.walk(raw_audio_dir))[0][2]

for file in filelist:
    if file.endswith(".wav"):
        os.system(f"demucs --two-stems=vocals {raw_audio_dir}{file}")
for file in filelist:
    file = file.replace(".wav", "")
    wav, sr = torchaudio.load(f"./separated/htdemucs/{file}/vocals.wav", frame_offset=0, num_frames=-1, normalize=True,
                              channels_first=True)
    # merge two channels into one
    wav = wav.mean(dim=0).unsqueeze(0)
    if sr != 22050:
        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
    torchaudio.save(denoise_audio_dir + file + ".wav", wav, 22050, channels_first=True)