"""该模块用于生成VITS文件
使用方法

python cmd_inference.py -m 模型路径 -c 配置文件路径 -o 输出文件路径 -l 输入的语言 -t 输入文本 -s 合成目标说话人名称

可选参数
-ns 感情变化程度
-nsw 音素发音长度
-ls 整体语速
-on 输出文件的名称

"""

from pathlib import Path
import utils
from models import SynthesizerTrn
import torch
from torch import no_grad, LongTensor
import librosa
from text import text_to_sequence, _clean_text
import commons
import scipy.io.wavfile as wavf
import os

device = "cuda:0" if torch.cuda.is_available() else "cpu"

language_marks = {
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "Mix": "",
}


def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='vits inference')
    #必须参数
    parser.add_argument('-m', '--model_path', type=str, default="logs/44k/G_0.pth", help='模型路径')
    parser.add_argument('-c', '--config_path', type=str, default="configs/config.json", help='配置文件路径')
    parser.add_argument('-o', '--output_path', type=str, default="output/vits", help='输出文件路径')
    parser.add_argument('-l', '--language', type=str, default="日本語", help='输入的语言')
    parser.add_argument('-t', '--text', type=str, help='输入文本')
    parser.add_argument('-s', '--spk', type=str, help='合成目标说话人名称')
    #可选参数
    parser.add_argument('-on', '--output_name', type=str, default="output", help='输出文件的名称')
    parser.add_argument('-ns', '--noise_scale', type=float,default= .667,help='感情变化程度')
    parser.add_argument('-nsw', '--noise_scale_w', type=float,default=0.6, help='音素发音长度')
    parser.add_argument('-ls', '--length_scale', type=float,default=1, help='整体语速')
    
    args = parser.parse_args()
    
    model_path = args.model_path
    config_path = args.config_path
    output_dir = Path(args.output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    language = args.language
    text = args.text
    spk = args.spk
    noise_scale = args.noise_scale
    noise_scale_w = args.noise_scale_w
    length = args.length_scale
    output_name = args.output_name
    
    hps = utils.get_hparams_from_file(config_path)
    net_g = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()
    _ = utils.load_checkpoint(model_path, net_g, None)
    
    speaker_ids = hps.speakers


    if language is not None:
        text = language_marks[language] + text + language_marks[language]
        speaker_id = speaker_ids[spk]
        stn_tst = get_text(text, hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                                length_scale=1.0 / length)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid

        wavf.write(str(output_dir)+"/"+output_name+".wav",hps.data.sampling_rate,audio)
    

    
    