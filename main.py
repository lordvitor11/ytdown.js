import eel, os, json, youtube_dl, time, random, re;
from tkinter import Tk;
# import moviepy.editor as mp
from tkinter import filedialog;

# Comando para descobrir o gerenciador de arquivos do sistema linux: 
# xdg-mime query default inode/directory 

path = "";
root = Tk();
root.withdraw();
root.attributes("-topmost", True);

eel.init("web");

def getJson():
    with open('./source/settings.json', 'r') as openfile:
        array = json.load(openfile);

    return array


def setJson(array):
    json_object = json.dumps(array, indent=4);

    with open("./source/settings.json", "w") as outfile:
        outfile.write(json_object);


@eel.expose
def setPath():
    global path;
    path = filedialog.askdirectory();

    return f"{path}";

@eel.expose
def createJson():
    settings = {
        "path" : f"{path}",
        "links" : [],
    }

    # json_object = json.dumps(settings, indent=4);
    #
    # with open("./source/settings.json", "w") as outfile:
    #     outfile.write(json_object);

    setJson(settings);

@eel.expose
def editPath():
    settings = getJson();
    settings['path'] = path;
    setJson(settings);


@eel.expose
def appendLink(link):
    clone = 0;
    settings = getJson();
    
    for item in settings['links']:
        if (link == item):
            clone += 1; break;

    if (clone < 1):
        settings['links'].append(link);
        setJson(settings);
        return "none";
    else:
        return "duplicate";


@eel.expose
def clearJson():
    # with open('./source/settings.json', 'r') as openfile:
    #     settings = json.load(openfile);

    settings = getJson();

    settings['links'].clear()
    setJson(settings);
    # json_object = json.dumps(settings, indent=4);

    # with open("./source/settings.json", "w") as outfile:
    #     outfile.write(json_object);


@eel.expose
def openDir():
    settings = getJson();
    if (settings['so'] == "win"):
        os.system(f"explorer '{settings['path']}'");
    else:
        os.system(f"nemo '{settings['path']}'");


@eel.expose
def getArrayLinks():
    settings = getJson();
    return settings['links'];


@eel.expose
def getInfo(link):
    options = {
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(link, download=False)
        return f"{info['title']}";


@eel.expose
def download(link):
    print(path);
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': "./downloads" + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([link])

    so = getJson()['so'];
    finalPath = getJson()['path'];

    if ("win" in so):
        os.system(f"move downloads\*.mp3 {finalPath}");
    else:
        os.system(f"mv ./downloads/*.mp3 '{finalPath}'");

    return "complete";


# @eel.expose
# def convert():
#     for file in os.listdir("./downloads"):          
#         if (re.search('mp4', file)):                                     
#             mp4_path = os.path.join("./downloads" , file);
#             mp3_path = os.path.join("./downloads", os.path.splitext(file)[0]+'.mp3');
#             new_file = mp.AudioFileClip(mp4_path);  
#             new_file.write_audiofile(mp3_path);     
#             os.remove(mp4_path);

#     so = getJson()['so'];
#     if ("win" in so):
#         os.system(f"move downloads\*.mp3 {str(path)}");
#     else:
#         os.system(f"mv ./downloads/*.mp3 {str(path)}");

#     return "complete";


if (os.path.isfile("./source/settings.json")):
    file = "./html/index.html";
else:
    file = "./html/setup.html";

eel.start(file, size = (1000, 580));
