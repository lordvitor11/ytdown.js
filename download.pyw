import os, re, pytube
import moviepy.editor as mp

urlsRaw = open("./src/downloads.txt", "r");
urls = [item for item in urlsRaw];

configRaw = open("./src/config.txt", "r")
config = [item for item in configRaw]

for link in urls:
    yt = pytube.YouTube(link);
    ys = yt.streams.filter(only_audio=True).first().download("./downloads");

for file in os.listdir("./downloads"):          
    if re.search('mp4', file):                                     
        mp4_path = os.path.join("./downloads" , file);
        mp3_path = os.path.join("./downloads", os.path.splitext(file)[0]+'.mp3');
        new_file = mp.AudioFileClip(mp4_path);  
        new_file.write_audiofile(mp3_path);     
        os.remove(mp4_path);

if ("win" in config[0]):
    os.system(f"move downloads\*.mp3 {str(config[1])}");
else:
    os.system(f"mv downloads/*.mp3 {str(config[1])}");

urlsRaw = open("./src/downloads.txt", "w");
urlsRaw.write("");

complete = open("./src/complete.txt", "w");

complete.close();
urlsRaw.close();
configRaw.close();
