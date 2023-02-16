import numpy as np
import torch
import torchaudio
import gradio as gr
import os

anno_lines = []
with open("./user_voice/user_voice.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        anno_lines.append(line.strip("\n"))

text_index = 0

def display_text(index):
    index = int(index)
    global text_index
    text_index = index
    return f"{text_index}: " + anno_lines[index].split("|")[2].strip("[ZH]").strip("[EN]")

def display_prev_text():
    global text_index
    if text_index != 0:
        text_index -= 1
    return f"{text_index}: " + anno_lines[text_index].split("|")[2].strip("[ZH]").strip("[EN]")

def display_next_text():
    global text_index
    if text_index != len(anno_lines)-1:
        text_index += 1
    return f"{text_index}: " + anno_lines[text_index].split("|")[2].strip("[ZH]").strip("[EN]")

def save_audio(audio):
    global text_index
    if audio:
        sr, wav = audio
        wav = torch.tensor(wav).type(torch.float32) / max(wav.max(), -wav.min())
        wav = wav.unsqueeze(0) if len(wav.shape) == 1 else wav
        if sr != 22050:
            res_wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
        else:
            res_wav = wav
        torchaudio.save(f"./user_voice/{str(text_index)}.wav", res_wav, 22050, channels_first=True)
        return f"Audio saved to ./user_voice/{str(text_index)}.wav successfully!"
    else:
        return "Error: Please record your audio!"


if __name__ == "__main__":
    app = gr.Blocks()
    with app:
        with gr.Row():
            text = gr.Textbox(value="0: " + anno_lines[0].split("|")[2].strip("[ZH]"), label="Please read the text here")
        with gr.Row():
            audio_to_collect = gr.Audio(source="microphone")
        with gr.Row():
            with gr.Column():
                prev_btn = gr.Button(value="Previous")
            with gr.Column():
                next_btn = gr.Button(value="Next")
        with gr.Row():
            index_dropdown = gr.Dropdown(choices=[str(i) for i in range(len(anno_lines))], value="0",
                                         label="No. of text", interactive=True)
        with gr.Row():
            with gr.Column():
                save_btn = gr.Button(value="Save Audio")
            with gr.Column():
                audio_save_message = gr.Textbox(label="Message")
        index_dropdown.change(display_text, inputs=index_dropdown, outputs=text)
        prev_btn.click(display_prev_text, inputs=None, outputs=text)
        next_btn.click(display_next_text, inputs=None, outputs=text)
        save_btn.click(save_audio, inputs=audio_to_collect, outputs=audio_save_message)
    app.launch()