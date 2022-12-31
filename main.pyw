import re, os, time, tkinter.filedialog, tkinter.messagebox;
import moviepy.editor as mp;
from pytube import YouTube, Playlist;
from tkinter import *

urls = [];

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.configRaw = open("./src/config.txt", "r");
        self.historyRaw = open("src/history.txt", "r");
        self.config = [linha for linha in self.configRaw];
        self.history = [linha for linha in self.historyRaw];
       
        self.preVerify();


    def preVerify(self):
        dirFile = os.listdir("./src");

        try:
            if (str(self.config[1]) != ""):
                self.gotoMenu();
        except IndexError:
            if (len(dirFile) > 1):
                self.gotoSetup();
            else:
                tkinter.messagebox.showwarning("ERRO", "Instale as dependências antes de começar, tutorial na página do github: lordvitor11");
                quit();


    def setupConfig(self):
        root.directory = tkinter.filedialog.askdirectory();
        self.mensagem2["text"] = f"Caminho: {root.directory}";
        self.rDict = root.directory;
        
            
    def addValues(self):
        mUrl = self.url.get();
        if (mUrl != "" and mUrl != None and not mUrl in urls):
            if (str(mUrl) in self.history):
                self.mensagem["text"] = "Música já baixada";
            else:
                self.mensagem["text"] = "Música adicionada!";
                urls.append(mUrl);
                self.history.append(mUrl);
                self.url.delete(0, "end");
        else:
            self.mensagem["text"] = "";

    
    def gotoSetup(self):
        def unpackAll():
            self.mensagem.destroy();
            self.mensagem2.destroy();
            self.add.destroy();
            self.autenticar.destroy();
            self.gotoMenu();

        self.titulo["text"] = "Escolha o local para baixar as músicas";

        self.mensagem = Label(self.terceiroContainer, text="Caso o caminho não esteja correto, adicione novamente", font=self.fontePadrao);
        self.mensagem2 = Label(self.terceiroContainer, text="", font=self.fontePadrao);
        self.mensagem.pack();
        self.mensagem2.pack();

        self.add = Button(self.segundoContainer)
        self.add["text"] = "Escolha";
        self.add["font"] = ("Calibri", "8");
        self.add["width"] = 12;
        self.add["command"] = lambda: self.setupConfig(); #self.mensagem.pack();    
        self.add.pack()

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Prosseguir"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = unpackAll; 
        self.autenticar.pack()


    def gotoMenu(self):
        def unpackAll():
            self.url.destroy();
            self.add.destroy();
            self.autenticar.destroy();
            self.mensagem.destroy();
            self.gotoDownload();

        self.titulo["text"] = "Digite os links das músicas";

        self.url = Entry(self.segundoContainer)
        self.url["width"] = 30
        self.url["font"] = self.fontePadrao
        self.url.pack(side=LEFT)

        self.add = Button(self.segundoContainer)
        self.add["text"] = "Adicionar";
        self.add["font"] = ("Calibri", "8");
        self.add["width"] = 12;
        self.add["command"] = self.addValues;        
        self.add.pack()

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Baixar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = unpackAll;
        self.autenticar.pack()

        self.mensagem = Label(self.terceiroContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()


    def gotoDownload(self):
        self.titulo["text"] = "Downloads concluidos";

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Sair"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = lambda:quit();
        self.autenticar.pack()
          
        self.downloadVideo();

    def downloadVideo(self):
        if (len(self.config) == 1):
            self.config.append(root.directory);
            
            self.configRaw = open("./src/config.txt", "w");
            for c in range(len(self.config)): self.configRaw.write(f"{self.config[c]}\n");

        for link in urls:
            yt = YouTube(link);
            ys = yt.streams.filter(only_audio=True).first().download("./downloads");

        for file in os.listdir("./downloads"):          
            if re.search('mp4', file):                                     
                mp4_path = os.path.join("./downloads" , file);
                mp3_path = os.path.join("./downloads", os.path.splitext(file)[0]+'.mp3');
                new_file = mp.AudioFileClip(mp4_path);  
                new_file.write_audiofile(mp3_path);     
                os.remove(mp4_path);

        if ("win" in self.config[0]):
            os.system(f"move downloads\*.mp3 {str(self.config[1])}")
        else:
            os.system(f"mv downloads/*.mp3 {str(self.config[1])}")

        
        self.historyRaw = open("src/history.txt", "w");
        for item in self.history:
            self.historyRaw.write(f"{item}\n");

        self.configRaw.close();
        self.historyRaw.close();


root = Tk();
Application(root);
root.mainloop();
