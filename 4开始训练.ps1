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

Write-Output "��ʼѵ��..."
python finetune_speaker_v2.py -m Shota --max_epochs 40 --drop_speaker_embed True

Write-Output "ѵ�����..."
Read-Host | Out-Null ;