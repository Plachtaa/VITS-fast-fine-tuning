import os
MIN_VOICE_NUM = 10
if __name__ == "__main__":
    # load sampled_audio4ft
    with open("sampled_audio4ft.txt", 'r', encoding='utf-8') as f:
        old_annos = f.readlines()
    num_old_voices = len(old_annos)
    # load user text
    with open("./user_voice/user_voice.txt.cleaned", 'r', encoding='utf-8') as f:
        user_annos = f.readlines()
    # check how many voices are recorded
    wavfiles = [file for file in list(os.walk("./user_voice"))[0][2] if file.endswith(".wav")]
    num_user_voices = len(wavfiles)
    if num_user_voices < MIN_VOICE_NUM:
        raise Exception(f"You need to record at least {MIN_VOICE_NUM} voices for fine-tuning!")
    # user voices need to occupy 1/4 of the total dataset
    duplicate = num_old_voices // num_user_voices // 3
    # find corresponding existing annotation lines
    actual_user_annos = ["./user_voice/" + line for line in user_annos if line.split("|")[0] in wavfiles]
    actual_user_annos *= duplicate
    final_annos = old_annos + actual_user_annos
    # save annotation file
    with open("final_annotation.txt", 'w', encoding='utf-8') as f:
        for line in final_annos:
            f.write(line)
