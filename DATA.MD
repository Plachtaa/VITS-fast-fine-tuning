本仓库的pipeline支持多种声音样本上传方式，您只需根据您所持有的样本选择任意一种或其中几种即可。  

1.`.zip`文件打包的，按角色名排列的短音频，该压缩文件结构应如下所示：  
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
注意音频的格式和名称都不重要，只要它们是音频文件。  
质量要求：2秒以上，10秒以内，尽量不要有背景噪音。  
数量要求：一个角色至少10条，最好每个角色20条以上。  
2. 以角色名命名的长音频文件，音频内只能有单说话人，背景音会被自动去除。命名格式为：`{CharacterName}_{random_number}.wav`  
(例如：`Diana_234135.wav`, `MinatoAqua_234252.wav`)，必须是`.wav`文件，长度要在20分钟以内（否则会内存不足）。  

3. 以角色名命名的长视频文件，视频内只能有单说话人，背景音会被自动去除。命名格式为：`{CharacterName}_{random_number}.mp4`  
(例如：`Taffy_332452.mp4`, `Dingzhen_957315.mp4`)，必须是`.mp4`文件，长度要在20分钟以内（否则会内存不足）。  
注意：命名中，`CharacterName`必须是英文字符，`random_number`是为了区分同一个角色的多个文件，必须要添加，该数字可以为0~999999之间的任意整数。   

4. 包含多行`{CharacterName}|{video_url}`的`.txt`文件，格式应如下所示：
```
Char1|https://xyz.com/video1/
Char2|https://xyz.com/video2/
Char2|https://xyz.com/video3/
Char3|https://xyz.com/video4/
```
视频内只能有单说话人，背景音会被自动去除。目前仅支持来自bilibili的视频，其它网站视频的url还没测试过。  
若对格式有疑问，可以在[这里](https://drive.google.com/file/d/132l97zjanpoPY4daLgqXoM7HKXPRbS84/view?usp=sharing)找到所有格式对应的数据样本。
