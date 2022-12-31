import os, subprocess, sys, threading, tkinter, tkinter.messagebox, customtkinter;

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("ytdown.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Criador:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "YouTube", command=lambda:self.sidebar_button_event(1))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text = "GitHub", command=lambda:self.sidebar_button_event(2))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text = "Instagram", command=lambda:self.sidebar_button_event(3))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Claro", "Escuro", "Sistema"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
    

        self.appearance_mode_optionemenu.set("Sistema")
        self.edited = False;
        self.urls = [];

        self.preVerify();
        
    def sidebar_button_event(self, button):
        match (button):
            case 1: button = "https://www.youtube.com/c/lordvitor11";
            case 2: button = "https://www.github.com/lordvitor11"; 
            case 3: button = "https://www.instagram.com/whoslv_";

        config = open("./src/config.txt");
        so = [item for item in config]
        so = so[0];

        if ("win" in so):
            os.system(f'start "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "{button}"');
        else:
            threading.Thread(target=lambda:os.system(f'firefox "{button}"')).start();


    def change_appearance_mode_event(self, new_appearance_mode: str):
        match (new_appearance_mode):
            case "Claro": new_appearance_mode = "light";
            case "Escuro": new_appearance_mode = "dark";
            case "Sistema": new_appearance_mode = "system";

        customtkinter.set_appearance_mode(new_appearance_mode)


    def preVerify(self):
        try:
            dirFile = os.listdir("./src");
            self.configRaw = open("./src/config.txt", "r");
            self.config = [linha for linha in self.configRaw];
        except FileNotFoundError:
            tkinter.messagebox.showwarning("ERRO", "Instale as dependências antes de começar, tutorial na página do github: lordvitor11");
            quit();

        try: 
            if (str(self.config[1]) != ""):
                self.mainScreen();
        except IndexError:
            if (len(dirFile) > 1):
                self.configScreen();
            else:
                tkinter.messagebox.showwarning("ERRO", "Instale as dependências antes de começar, tutorial na página do github: lordvitor11");
                quit();
    

    def rootConfig(self):
        app.directory = tkinter.filedialog.askdirectory();
        self.entry.configure(placeholder_text = app.directory);
        self.label2.configure(text = "*Se o caminho não estiver correto, adicione novamente");
        self.continueBtn.configure(state = "enabled");


    def addValues(self):
        mUrl = self.entry.get();
        if (mUrl != "" and mUrl != None and not mUrl in self.urls):
            self.entry.delete(0, "end");
            tkinter.messagebox.showinfo("", "Música adicionada!");
            self.urls.append(mUrl);
        else:
            tkinter.messagebox.showinfo("", "Música já adicionada anteriormente!");
            self.entry.configure(placeholder_text = "");


    def configScreen(self):
        def unpackAll():
            config = open("./src/config.txt", "a");
            config.write(f"\n{app.directory}");

            self.label.destroy();
            self.label2.destroy();
            self.entry.destroy();
            self.pathBtn.destroy();
            self.continueBtn.destroy();
            self.mainScreen();

        self.label = customtkinter.CTkLabel(self, text="Escolha o local para baixar as músicas:", font = customtkinter.CTkFont(size=20, weight="bold"));
        self.label.grid(row=0, column=1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.label2 = customtkinter.CTkLabel(self, text = "", font = customtkinter.CTkFont(size = 15, weight = "bold"));
        self.label2.grid(row = 2, column = 1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.entry = customtkinter.CTkEntry(self, placeholder_text="", width = 450)
        self.entry.grid(row=1, column=1, columnspan=2, padx=(20, 100), pady=(20, 20))

        self.pathBtn = customtkinter.CTkButton(master = self, text = "Clique", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), width=80, command=self.rootConfig)
        self.pathBtn.grid(row=1, column=2, padx=(0, 200), pady=(20, 20))

        self.continueBtn = customtkinter.CTkButton(master = self, text = "Continuar", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), command=lambda:unpackAll());
        self.continueBtn.grid(row = 3, column = 2, padx = 0, pady = (20, 20));        
        self.continueBtn.configure(state = "disabled");


    def mainScreen(self):
        def unpackAll():
            self.label.destroy();
            self.label2.destroy();
            self.entry.destroy();
            self.linkBtn.destroy();
            self.downBtn.destroy();
            self.editBtn.destroy();
            self.quitBtn.destroy();
            self.btnFrame.destroy();
            self.downScreen()

        def edit():
            app.directory = tkinter.filedialog.askdirectory();
            self.label2.configure(text = app.directory);
            self.edited = True if app.directory != "" else False;

            if (self.edited):
                self.config.pop();
                self.config.append(app.directory);
                self.configRaw = open("./src/config.txt", "w");
                for c in range(len(self.config)): self.configRaw.write(f"{self.config[c]}");
                self.configRaw.close();

        self.label = customtkinter.CTkLabel(self, text="Adicione os links das músicas e clique em baixar", font = customtkinter.CTkFont(size=20, weight="bold"));
        self.label.grid(row=0, column=1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.label2 = customtkinter.CTkLabel(self, text="", font = customtkinter.CTkFont(size=20, weight="bold"));
        self.label2.grid(row=2, column=1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.entry = customtkinter.CTkEntry(self, placeholder_text="", width = 450);
        self.entry.grid(row=1, column=1, columnspan=2, padx=(20, 100), pady=(20, 20))

        self.linkBtn = customtkinter.CTkButton(master = self, text = "Adicionar", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), width=80, command=self.addValues);
        self.linkBtn.grid(row=1, column=2, padx=(0, 200), pady=(20, 20));

        self.btnFrame = customtkinter.CTkFrame(self)
        self.btnFrame.grid(row=3, column=2, padx=(20, 20), pady=(20, 0))

        self.downBtn = customtkinter.CTkButton(master = self.btnFrame, text = "Baixar", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), width=173, command=unpackAll);
        self.downBtn.grid(row = 3, column=1, padx=0, pady = (20, 60), sticky="s");

        self.editBtn = customtkinter.CTkButton(master = self.btnFrame, text = "Editar caminho de download", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), command=edit);
        self.editBtn.grid(row = 3, column = 1, padx = 0, pady = (20, 30), sticky="s");

        self.quitBtn = customtkinter.CTkButton(master = self.btnFrame, text = "Sair", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), width=173, command=lambda:quit());
        self.quitBtn.grid(row = 3, column = 1, padx = 0, pady = (20, 0), sticky="s");


    def downScreen(self):
        downRaw = open("./src/downloads.txt", "a");

        for item in self.urls:
            downRaw.write(f"{item}\n");

        downRaw.close();

        self.label = customtkinter.CTkLabel(self, text="Baixando músicas... Aguarde", font = customtkinter.CTkFont(size=20, weight="bold"));
        self.label.grid(row=0, column=1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.label2 = customtkinter.CTkLabel(self, text="*Avisaremos quando terminar, não feche o aplicativo até lá", font = customtkinter.CTkFont(size=10, weight="bold"));
        self.label2.grid(row=1, column=1, columnspan = 2, padx=(20, 0), pady=(20, 20), sticky = "nsew");

        self.btnFrame = customtkinter.CTkFrame(self)
        self.btnFrame.grid(row=3, column=2, padx=(20, 20), pady=(20, 0))

        self.downBtn = customtkinter.CTkButton(master = self.btnFrame, text = "Abrir pasta", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), width=173);
        self.downBtn.grid(row = 3, column=1, padx=0, pady = (20, 60), sticky="s");

        self.quitBtn = customtkinter.CTkButton(master = self.btnFrame, text = "Sair", fg_color = "transparent", border_width = 2, text_color=("gray10", "#DCE4EE"), width=173, command=lambda:quit());
        self.quitBtn.grid(row = 3, column = 1, padx = 0, pady = (20, 0), sticky="s");

        self.downBtn.configure(state = "disabled");
        self.quitBtn.configure(state = "disabled");

        threading.Thread(target=self.downScreen2).start();

    def downScreen2(self):
        def openDir():
            configRaw = open("./src/config.txt");
            config = [item for item in configRaw];
            config = config[1];
            print(config)
            configRaw.close();

            if ("win" in so):
                config = config.replace("/", "\\")
                os.system(f"explorer {config}");
            else:
                try:
                    os.system(f"nemo {config}");
                except:
                    os.system(f"thunar {config}");

        configRaw = open("./src/config.txt", "r");
        config = [item for item in configRaw];
        so = config[0];

        if ("win" in so):
            os.system("python download.pyw");
        else:
            os.system("python3 download.pyw");

        if ("win" in so):        
            os.system(r'del ".\src\complete.txt"');
        else:
            os.system("rm ./src/complete.txt");

        self.downBtn.configure(command = openDir);
        self.downBtn.configure(state = "enabled");
        self.quitBtn.configure(state = "enabled");

        tkinter.messagebox.showinfo("Concluído", "Todas as músicas foram baixadas!");
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
