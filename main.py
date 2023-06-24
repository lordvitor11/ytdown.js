import eel, os, json, pytube, time, random;
from tkinter import Tk;
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
    yt = pytube.YouTube(link);
    return f"{yt.title.strip()} - {yt.author.strip()}";


@eel.expose
def download(link):
    time.sleep(random.randint(1, 5));
    return "completo";


if (os.path.isfile("./source/settings.json")):
    file = "./html/index.html";
else:
    file = "./html/setup.html";

eel.start(file, size = (1000, 580));
