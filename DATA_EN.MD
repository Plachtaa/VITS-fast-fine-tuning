The pipeline of this repo supports multiple voice uploading options，you can choose one or more options depending on the data you have.

1. Short audios packed by a single `.zip` file, whose file structure should be as shown below:
```
Your-zip-file.zip
├───Character_name_1
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───Character_name_2
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───...
├
└───Character_name_n
    ├───xxx.wav
    ├───...
    ├───yyy.mp3
    └───zzz.wav
```
Note that the format of the audio files does not matter as long as they are audio files。  
Quality requirement: >=2s, <=10s, contain as little background sound as possible.   
Quantity requirement: at least 10 per character, 20+ per character is recommended.

2. Long audio files named by character names, which should contain single character voice only. Background sound is 
acceptable since they will be automatically removed. File name format `{CharacterName}_{random_number}.wav`  
(E.G. `Diana_234135.wav`, `MinatoAqua_234252.wav`), must be `.wav` files.  
  

3. Long video files named by character names, which should contain single character voice only. Background sound is 
acceptable since they will be automatically removed. File name format `{CharacterName}_{random_number}.mp4`  
(E.G. `Taffy_332452.mp4`, `Dingzhen_957315.mp4`), must be `.mp4` files.  
Note: `CharacterName` must be English characters only, `random_number` is to identify multiple files for one character,
which is compulsory to add. It could be a random integer between 0~999999.

4. A `.txt` containing multiple lines of`{CharacterName}|{video_url}`, which should be formatted as follows:
```
Char1|https://xyz.com/video1/
Char2|https://xyz.com/video2/
Char2|https://xyz.com/video3/
Char3|https://xyz.com/video4/
```
One video should contain single speaker only. Currently supports videos links from bilibili, other websites are yet to be tested.
Having questions regarding to data format? Fine data samples of all format from [here](https://drive.google.com/file/d/132l97zjanpoPY4daLgqXoM7HKXPRbS84/view?usp=sharing).
