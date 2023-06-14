import os
import glob
import sys
import argparse
import logging
import json
import subprocess
import numpy as np
from scipy.io.wavfile import read
import torch
import regex as re

MATPLOTLIB_FLAG = False

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging



zh_pattern = re.compile(r'[\u4e00-\u9fa5]')
en_pattern = re.compile(r'[a-zA-Z]')
jp_pattern = re.compile(r'[\u3040-\u30ff\u31f0-\u31ff]')
kr_pattern = re.compile(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f\ua960-\ua97f]')
num_pattern=re.compile(r'[0-9]')
comma=r"(?<=[.。!！?？；;，,、:：'\"‘“”’()（）《》「」~——])"    #向前匹配但固定长度
tags={'ZH':'[ZH]','EN':'[EN]','JP':'[JA]','KR':'[KR]'}

def tag_cjke(text):
    '''为中英日韩加tag,中日正则分不开，故先分句分离中日再识别，以应对大部分情况'''
    sentences = re.split(r"([.。!！?？；;，,、:：'\"‘“”’()（）【】《》「」~——]+ *(?![0-9]))", text) #分句，排除小数点
    sentences.append("")
    sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]
    # print(sentences)
    prev_lang=None
    tagged_text = ""
    for s in sentences:
        #全为符号跳过
        nu = re.sub(r'[\s\p{P}]+', '', s, flags=re.U).strip()   
        if len(nu)==0:
            continue
        s = re.sub(r'[()（）《》「」【】‘“”’]+', '', s)
        jp=re.findall(jp_pattern, s)
        #本句含日语字符判断为日语
        if len(jp)>0:  
            prev_lang,tagged_jke=tag_jke(s,prev_lang)
            tagged_text +=tagged_jke
        else:
            prev_lang,tagged_cke=tag_cke(s,prev_lang)
            tagged_text +=tagged_cke
    return tagged_text

def tag_jke(text,prev_sentence=None):
    '''为英日韩加tag'''
    # 初始化标记变量
    tagged_text = ""
    prev_lang = None
    tagged=0
    # 遍历文本
    for char in text:
        # 判断当前字符属于哪种语言
        if jp_pattern.match(char):
            lang = "JP"
        elif zh_pattern.match(char):
            lang = "JP"
        elif kr_pattern.match(char):
            lang = "KR"
        elif en_pattern.match(char):
            lang = "EN"
        # elif num_pattern.match(char):
        #     lang = prev_sentence
        else:
            lang = None
            tagged_text += char
            continue
        # 如果当前语言与上一个语言不同，就添加标记
        if lang != prev_lang:
            tagged=1
            if prev_lang==None: # 开头
                tagged_text =tags[lang]+tagged_text
            else:
                tagged_text =tagged_text+tags[prev_lang]+tags[lang]

            # 重置标记变量
            prev_lang = lang

        # 添加当前字符到标记文本中
        tagged_text += char
    
    # 在最后一个语言的结尾添加对应的标记
    if prev_lang:
            tagged_text += tags[prev_lang]
    if not tagged:
        prev_lang=prev_sentence
        tagged_text =tags[prev_lang]+tagged_text+tags[prev_lang]

    return prev_lang,tagged_text

def tag_cke(text,prev_sentence=None):
    '''为中英韩加tag'''
    # 初始化标记变量
    tagged_text = ""
    prev_lang = None
    # 是否全略过未标签
    tagged=0
    
    # 遍历文本
    for char in text:
        # 判断当前字符属于哪种语言
        if zh_pattern.match(char):
            lang = "ZH"
        elif kr_pattern.match(char):
            lang = "KR"
        elif en_pattern.match(char):
            lang = "EN"
        # elif num_pattern.match(char):
        #     lang = prev_sentence
        else:
            # 略过
            lang = None
            tagged_text += char
            continue

        # 如果当前语言与上一个语言不同，添加标记
        if lang != prev_lang:
            tagged=1
            if prev_lang==None: # 开头
                tagged_text =tags[lang]+tagged_text
            else:
                tagged_text =tagged_text+tags[prev_lang]+tags[lang]

            # 重置标记变量
            prev_lang = lang

        # 添加当前字符到标记文本中
        tagged_text += char
    
    # 在最后一个语言的结尾添加对应的标记
    if prev_lang:
            tagged_text += tags[prev_lang]
    # 未标签则继承上一句标签
    if tagged==0:
        prev_lang=prev_sentence
        tagged_text =tags[prev_lang]+tagged_text+tags[prev_lang]
    return prev_lang,tagged_text



def load_checkpoint(checkpoint_path, model, optimizer=None, drop_speaker_emb=False):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location='cpu')
    iteration = checkpoint_dict['iteration']
    learning_rate = checkpoint_dict['learning_rate']
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint_dict['optimizer'])
    saved_state_dict = checkpoint_dict['model']
    if hasattr(model, 'module'):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():
        try:
            if k == 'emb_g.weight':
                if drop_speaker_emb:
                    new_state_dict[k] = v
                    continue
                v[:saved_state_dict[k].shape[0], :] = saved_state_dict[k]
                new_state_dict[k] = v
            else:
                new_state_dict[k] = saved_state_dict[k]
        except:
            logger.info("%s is not in the checkpoint" % k)
            new_state_dict[k] = v
    if hasattr(model, 'module'):
        model.module.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(new_state_dict)
    logger.info("Loaded checkpoint '{}' (iteration {})".format(
        checkpoint_path, iteration))
    return model, optimizer, learning_rate, iteration


def save_checkpoint(model, optimizer, learning_rate, iteration, checkpoint_path):
    logger.info("Saving model and optimizer state at iteration {} to {}".format(
        iteration, checkpoint_path))
    if hasattr(model, 'module'):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    torch.save({'model': state_dict,
                'iteration': iteration,
                'optimizer': optimizer.state_dict() if optimizer is not None else None,
                'learning_rate': learning_rate}, checkpoint_path)


def summarize(writer, global_step, scalars={}, histograms={}, images={}, audios={}, audio_sampling_rate=22050):
    for k, v in scalars.items():
        writer.add_scalar(k, v, global_step)
    for k, v in histograms.items():
        writer.add_histogram(k, v, global_step)
    for k, v in images.items():
        writer.add_image(k, v, global_step, dataformats='HWC')
    for k, v in audios.items():
        writer.add_audio(k, v, global_step, audio_sampling_rate)


def extract_digits(f):
    digits = "".join(filter(str.isdigit, f))
    return int(digits) if digits else -1


def latest_checkpoint_path(dir_path, regex="G_[0-9]*.pth"):
    f_list = glob.glob(os.path.join(dir_path, regex))
    f_list.sort(key=lambda f: extract_digits(f))
    x = f_list[-1]
    print(f"latest_checkpoint_path:{x}")
    return x


def oldest_checkpoint_path(dir_path, regex="G_[0-9]*.pth", preserved=4):
    f_list = glob.glob(os.path.join(dir_path, regex))
    f_list.sort(key=lambda f: extract_digits(f))
    if len(f_list) > preserved:
        x = f_list[0]
        print(f"oldest_checkpoint_path:{x}")
        return x
    return ""


def plot_spectrogram_to_numpy(spectrogram):
    global MATPLOTLIB_FLAG
    if not MATPLOTLIB_FLAG:
        import matplotlib
        matplotlib.use("Agg")
        MATPLOTLIB_FLAG = True
        mpl_logger = logging.getLogger('matplotlib')
        mpl_logger.setLevel(logging.WARNING)
    import matplotlib.pylab as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 2))
    im = ax.imshow(spectrogram, aspect="auto", origin="lower",
                   interpolation='none')
    plt.colorbar(im, ax=ax)
    plt.xlabel("Frames")
    plt.ylabel("Channels")
    plt.tight_layout()

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data


def plot_alignment_to_numpy(alignment, info=None):
    global MATPLOTLIB_FLAG
    if not MATPLOTLIB_FLAG:
        import matplotlib
        matplotlib.use("Agg")
        MATPLOTLIB_FLAG = True
        mpl_logger = logging.getLogger('matplotlib')
        mpl_logger.setLevel(logging.WARNING)
    import matplotlib.pylab as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(alignment.transpose(), aspect='auto', origin='lower',
                   interpolation='none')
    fig.colorbar(im, ax=ax)
    xlabel = 'Decoder timestep'
    if info is not None:
        xlabel += '\n\n' + info
    plt.xlabel(xlabel)
    plt.ylabel('Encoder timestep')
    plt.tight_layout()

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data


def load_wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def load_filepaths_and_text(filename, split="|"):
    with open(filename, encoding='utf-8') as f:
        filepaths_and_text = [line.strip().split(split) for line in f]
    return filepaths_and_text


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_hparams(init=True):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default="./configs/modified_finetune_speaker.json",
                        help='JSON file for configuration')
    parser.add_argument('-m', '--model', type=str, default="pretrained_models",
                        help='Model name')
    parser.add_argument('-n', '--max_epochs', type=int, default=50,
                        help='finetune epochs')
    parser.add_argument('--cont', type=str2bool, default=False, help='whether to continue training on the latest checkpoint')
    parser.add_argument('--drop_speaker_embed', type=str2bool, default=False, help='whether to drop existing characters')
    parser.add_argument('--train_with_pretrained_model', type=str2bool, default=True,
                        help='whether to train with pretrained model')
    parser.add_argument('--preserved', type=int, default=4,
                        help='Number of preserved models')

    args = parser.parse_args()
    model_dir = os.path.join("./", args.model)

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    config_path = args.config
    config_save_path = os.path.join(model_dir, "config.json")
    if init:
        with open(config_path, "r") as f:
            data = f.read()
        with open(config_save_path, "w") as f:
            f.write(data)
    else:
        with open(config_save_path, "r") as f:
            data = f.read()
    config = json.loads(data)

    hparams = HParams(**config)
    hparams.model_dir = model_dir
    hparams.max_epochs = args.max_epochs
    hparams.cont = args.cont
    hparams.drop_speaker_embed = args.drop_speaker_embed
    hparams.train_with_pretrained_model = args.train_with_pretrained_model
    hparams.preserved = args.preserved
    return hparams


def get_hparams_from_dir(model_dir):
    config_save_path = os.path.join(model_dir, "config.json")
    with open(config_save_path, "r") as f:
        data = f.read()
    config = json.loads(data)

    hparams = HParams(**config)
    hparams.model_dir = model_dir
    return hparams


def get_hparams_from_file(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        data = f.read()
    config = json.loads(data)

    hparams = HParams(**config)
    return hparams


def check_git_hash(model_dir):
    source_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(source_dir, ".git")):
        logger.warn("{} is not a git repository, therefore hash value comparison will be ignored.".format(
            source_dir
        ))
        return

    cur_hash = subprocess.getoutput("git rev-parse HEAD")

    path = os.path.join(model_dir, "githash")
    if os.path.exists(path):
        saved_hash = open(path).read()
        if saved_hash != cur_hash:
            logger.warn("git hash values are different. {}(saved) != {}(current)".format(
                saved_hash[:8], cur_hash[:8]))
    else:
        open(path, "w").write(cur_hash)


def get_logger(model_dir, filename="train.log"):
    global logger
    logger = logging.getLogger(os.path.basename(model_dir))
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    h = logging.FileHandler(os.path.join(model_dir, filename))
    h.setLevel(logging.DEBUG)
    h.setFormatter(formatter)
    logger.addHandler(h)
    return logger


class HParams():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if type(v) == dict:
                v = HParams(**v)
            self[k] = v

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        return self.__dict__.__repr__()