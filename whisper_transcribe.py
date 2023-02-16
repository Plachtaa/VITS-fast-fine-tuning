import whisper
import os
import torchaudio

lang2token = {
    'zh': "[ZH]",
    'ja': "[JA]",
    "en": "[EN]",
}




def transcribe_one(audio_path):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    lang = max(probs, key=probs.get)
    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    return lang, result.text
if __name__ == "__main__":
    model = whisper.load_model("medium")
    parent_dir = "./custom_character_voice/"
    speaker_names = list(os.walk(parent_dir))[0][1]
    speaker2id = {}
    speaker_annos = []
    # resample audios
    for speaker in speaker_names:
        speaker2id[speaker] = 1000 + len(speaker2id)
        for i, wavfile in enumerate(list(os.walk(parent_dir + speaker))[0][2]):
            # try to load file as audio
            if wavfile.startswith("processed_"):
                continue
            try:
                wav, sr = torchaudio.load(parent_dir + speaker + "/" + wavfile, frame_offset=0, num_frames=-1, normalize=True,
                                          channels_first=True)
                wav = wav.mean(dim=0).unsqueeze(0)
                if sr != 22050:
                    wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
                if wav.shape[1] / sr > 20:
                    print(f"{wavfile} too long, ignoring\n")
                save_path = parent_dir + speaker + "/" + f"processed_{i}.wav"
                torchaudio.save(save_path, wav, 22050, channels_first=True)
                # transcribe text
                lang, text = transcribe_one(save_path)
                if lang not in ['zh', 'en', 'ja']:
                    print(f"{lang} not supported, ignoring\n")
                text = lang2token[lang] + text + lang2token[lang] + "\n"
                speaker_annos.append(save_path + "|" + str(speaker2id[speaker]) + "|" + text)
            except:
                continue

    # clean annotation
    import argparse
    import text
    from utils import load_filepaths_and_text
    for i, line in enumerate(speaker_annos):
        path, sid, txt = line.split("|")
        cleaned_text = text._clean_text(txt, ["cjke_cleaners2"])
        cleaned_text += "\n" if not cleaned_text.endswith("\n") else ""
        speaker_annos[i] = path + "|" + sid + "|" + cleaned_text
    # write into annotation
    with open("custom_character_anno.txt", 'w', encoding='utf-8') as f:
        for line in speaker_annos:
            f.write(line)

    import json
    # generate new config
    with open("./configs/finetune_speaker.json", 'r', encoding='utf-8') as f:
        hps = json.load(f)
    # modify n_speakers
    hps['data']["n_speakers"] = 999 + len(speaker2id)
    # add speaker names
    for speaker in speaker_names:
        hps['speakers'][speaker] = speaker2id[speaker]
    # save modified config
    with open("./configs/modified_finetune_speaker.json", 'w', encoding='utf-8') as f:
        json.dump(hps, f, indent=2)
    print("finished")
