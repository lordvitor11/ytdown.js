import re, os, time

def installDep():
    sysName = "win" if str(os.name) == "nt" else "unix";
    state = False;
    distro = "";

    if (sysName == "win"):
        path = f"{os.path.dirname(os.path.realpath(__file__))}\src";
    else:
        path = f"{os.path.dirname(os.path.realpath(__file__))}/src";

        while (True):
            print("Notamos que você está usando uma plataforma UNIX, escolha uma opção abaixo: ");
            print("[ 1 ] Baseada em Debian\n[ 2 ] Baseada em Arch\n[ 3 ] Estou usando windows");
            choice = int(input("> "));

            match (choice):
                case 1: distro = "apt-get install"; break; 
                case 2: distro = "pacman -S"; break;
                case 3: break;
                case _: print("Opção inválida"); time.sleep(2); os.system("clear"); 


    for file in os.listdir(path):
        if (re.search("dependencies.txt", file)):
            state = True;

    if (state):
        print("Dependencias já instaladas!");
    else:
        print("[*] Instalando dependências...");

        if (sysName == "unix"):
            os.system(f"{distro} python3-pip");
            os.system(f"{distro} python3-tk");
            os.system("pip3 install moviepy");
            os.system("pip3 install moviepy"); 
        else:
            os.system("pip install pytube");
            os.system("pip install moviepy");

        dep = open("src/dependencies.txt", "w");
        config = open("src/config.txt", "w");
        history = open("src/history.txt", "w");

        if (sysName == "win"):
            SOConfig = sysName;
        elif (distro == "pacman -S"):
            SOConfig = "arch";
        else:
            SOConfig = "debian"; 

        config.write(SOConfig)
        dep.write("pytube\nmoviepy\ntkinter");

        dep.close()
        config.close();
        history.close();
        
        print("[*] Dependências instaladas!")


installDep();
