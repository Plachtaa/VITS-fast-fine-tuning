import os
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
    # user voices need to occupy 1/4 of the total dataset
    if num_user_voices:
        user_duplicate = num_old_voices // num_user_voices // 3
    else:
        user_duplicate = 0

    # find corresponding existing annotation lines
    actual_user_annos = ["./user_voice/" + line for line in user_annos if line.split("|")[0] in wavfiles]
    final_annos = old_annos + actual_user_annos * user_duplicate

    # load custom characters
    if os.path.exists("custom_character_anno.txt"):
        with open("custom_character_anno.txt", 'r', encoding='utf-8') as f:
            custom_character_anno = f.readlines()
        if len(custom_character_anno):
            # custom character voices need to be at least equal to number of sample_audio4ft
            num_character_voices = len(custom_character_anno)
            cc_duplicate = num_old_voices // num_character_voices
            if cc_duplicate == 0:
                cc_duplicate = 1
            final_annos = final_annos + custom_character_anno * cc_duplicate
    # save annotation file
    with open("final_annotation_train.txt", 'w', encoding='utf-8') as f:
        for line in final_annos:
            f.write(line)
    # save annotation file for validation
    with open("final_annotation_val.txt", 'w', encoding='utf-8') as f:
        for line in actual_user_annos:
            f.write(line)
        if os.path.exists("custom_character_anno.txt"):
            for line in custom_character_anno:
                f.write(line)
