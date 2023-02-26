import text

with open("custom_character_anno.txt", 'r', encoding='utf-8') as f:
    speaker_annos = f.readlines()
# clean annotation
cleaned_speaker_annos = []
for i, line in enumerate(speaker_annos):
    path, sid, txt = line.split("|")
    if len(txt) > 100:
        continue
    cleaned_text = text._clean_text(txt, ["cjke_cleaners2"])
    cleaned_text += "\n" if not cleaned_text.endswith("\n") else ""
    cleaned_speaker_annos.append(path + "|" + sid + "|" + cleaned_text)
# write into annotation
with open("custom_character_anno.txt", 'w', encoding='utf-8') as f:
    for line in speaker_annos:
        f.write(line)


