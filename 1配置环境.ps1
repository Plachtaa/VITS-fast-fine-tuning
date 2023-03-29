$Env:HF_HOME = "huggingface"
$Env:PIP_DISABLE_PIP_VERSION_CHECK = 1
$Env:PIP_NO_CACHE_DIR = 1
function InstallFail {
    Write-Output "��װʧ�ܡ�"
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
    Write-Output "���ڴ������⻷��..."
    python -m venv venv
    Check "�������⻷��ʧ�ܣ����� python �Ƿ�װ����Լ� python �汾��"
}

.\venv\Scripts\activate
Check "�������⻷��ʧ�ܡ�"

Write-Output "��װ������������..."
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "torch ��װʧ�ܣ���ɾ�� venv �ļ��к��������С�"
pip install imageio==2.4.1 -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "imageio ��װʧ�ܡ�"
pip install --upgrade youtube-dl -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "youtube-dl ��װʧ�ܡ�"
pip install moviepy -i https://mirrors.bfsu.edu.cn/pypi/web/simple
Check "moviepy ��װʧ�ܡ�"
pip install -r requirements.txt
Check "����������װʧ�ܡ�"
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

Write-Output "��װ��ϡ�"
Read-Host | Out-Null ;