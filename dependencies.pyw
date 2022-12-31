import re, os, time

def installDep():
    sysName = "win" if str(os.name) == "nt" else "unix";
    state = False;
    distro = "";

    os.system("mkdir downloads");
    os.system("mkdir src")

    if (sysName == "win"):
        path = f"{os.path.dirname(os.path.realpath(__file__))}\src";
    else:
        path = f"{os.path.dirname(os.path.realpath(__file__))}/src";

        while (True):
            print("Notamos que você está usando uma plataforma UNIX, escolha uma opção abaixo: ");
            print("[ 1 ] Baseada em Debian\n[ 2 ] Baseada em Arch\n[ 3 ] Estou usando windows");
            choice = int(input("> "));

            match (choice):
                case 1: distro = "sudo apt-get install"; break; 
                case 2: distro = "sudo pacman -S"; break;
                case 3: break;
                case _: print("Opção inválida"); time.sleep(2); os.system("clear"); 


    for file in os.listdir(path):
        if (re.search("dependencies.txt", file)):
            state = True;

    if (state):
        print("Dependencias já instaladas!");
    else:
        print("[*] Instalando dependências...");

        depList = ["customtkinter", "darkdetect", "typing-extensions", "pytube", "moviepy"];
        
        if (sysName == "unix"):
            os.system(f"{distro} python3-pip");
            os.system(f"{distro} python3-tk");

            for item in depList:
                os.system(f"pip3 install {item}");
        else:
            for item in depList:
                os.system(f"pip install {item}");

        dep = open("src/dependencies.txt", "w");
        config = open("src/config.txt", "w");
        downs = open("src/downloads.txt", "w");

        if (sysName == "win"):
            SOConfig = sysName;
        elif (distro == "pacman -S"):
            SOConfig = "arch";
        else:
            SOConfig = "debian"; 

        config.write(SOConfig)
        dep.write("pytube\nmoviepy\ntkinter\ncustomtkinter\ndarkdetect\ntyping-extensions");

        dep.close()
        config.close();
        downs.close();
        print("[*] Dependências instaladas!")


installDep();
