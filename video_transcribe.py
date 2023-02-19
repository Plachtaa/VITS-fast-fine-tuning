from moviepy.editor import AudioFileClip
import whisper
import os
import torchaudio
parent_dir = "../"
filelist = ["taffy1.mp4", "taffy2.mp4"]
for file in filelist:
    my_audio_clip = AudioFileClip(parent_dir + file)
    my_audio_clip.write_audiofile(parent_dir + file.rstrip(".mp4") + ".wav")
for file in filelist:
    file = file.replace(".mp4", ".wav")
    os.system(f"demucs --two-stems=vocals {parent_dir}{file}")
for file in filelist:
    file = file.strip(".mp4")
    wav, sr = torchaudio.load(f"./separated/htdemucs/{file}/vocals.wav", frame_offset=0, num_frames=-1, normalize=True,
                              channels_first=True)
    # merge two channels into one
    wav = wav.mean(dim=0).unsqueeze(0)
    if sr != 22050:
        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
    torchaudio.save(file + ".wav", wav, 22050, channels_first=True)
model = whisper.load_model("medium")
def transcribe_one(audio_path):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)
    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    return result

result = model.transcribe("taffy2.wav")
# segment audio based on segment results

