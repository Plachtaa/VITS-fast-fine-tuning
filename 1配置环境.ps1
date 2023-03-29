$Env:HF_HOME = "huggingface"
$Env:PIP_DISABLE_PIP_VERSION_CHECK = 1
$Env:PIP_NO_CACHE_DIR = 1
function InstallFail {
    Write-Output "安装失败。"
    Read-Host | Out-Null ;
    Exit
}

function Check {
    param (
        $ErrorInfo
    )
    if (!($?)) {
        Write-Output $ErrorInfo
        InstallFail
    }
}

if (!(Test-Path -Path "venv")) {
    Write-Output "正在创建虚拟环境..."
    python -m venv venv
    Check "创建虚拟环境失败，请检查 python 是否安装完毕以及 python 版本。"
}

.\venv\Scripts\activate
Check "激活虚拟环境失败。"

Write-Output "安装程序所需依赖..."
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "torch 安装失败，请删除 venv 文件夹后重新运行。"
pip install imageio==2.4.1 -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "imageio 安装失败。"
pip install --upgrade youtube-dl -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "youtube-dl 安装失败。"
pip install moviepy -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "moviepy 安装失败。"
pip install -r requirements.txt
Check "其他依赖安装失败。"
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice

Write-Output "安装完毕。"
Read-Host | Out-Null ;