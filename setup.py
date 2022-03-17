from posixpath import dirname
import sys
import os

code = r"""#!/usr/bin/python


from base64 import b64encode, b64decode
from io import BytesIO
import requests
import zipfile
import random
import shutil
import sys
import os

WHITE  = "\33[0m"
YELLOW = "\33[33m"
GREEN  = "\33[32m"
RED    = "\33[31m"
BLUE   = "\33[34m"
PURPLE = "\33[35m"

RAW_GITHUB_URL = "https://raw.githubusercontent.com/fxndone/ImageHider/"
GITHUB_URL     = "https://github.com/fxndone/ImageHider/"

goodby = [
    "Au revoir",
    "A bientot",
    "Tchao !",
    "Je m'en retourne vaquer a mes occupations",
    "Bonne fin de journee",
]

def ChecForUpdates():
    print()
    print(GREEN + "Verification de la version...")
    if os.path.isfile(".files/.version"):
        with open(".files/.version", "r") as f:
            vers = f.read().replace("\n", "").replace("\t", "").replace("\r", "")
    else:
        vers = "0.0"
    try:
        requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        print(RED + "Vous avez une mauvaise connection !")
        print(YELLOW + "Utilisation de la version actuelle (" + vers + ")")
        return
    v = requests.get(RAW_GITHUB_URL+"master/.files/.version").text.strip()
    print("Version actuelle :", vers)
    print("Derniere version :", v)

    if vers != v:
        print()
        print(YELLOW + "Vous n'avez pas la derniere version !")
        print(GREEN + "Voullez vous mettre a jour ImageHider ? (O/N) : ", end="")
        chx = input()
        while not chx.upper() in ("O", "N"):
            print(BLUE + "(O/N) : ")
        if chx.upper() == "N":
            print(YELLOW + "Veuillez envisager de mettre a jour ImageHider")
            return
        else:
            response = requests.get(GITHUB_URL+"/archive/master.zip")
            if response.status_code == 200:
                zip_content = response.content
                try:
                    with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
                        for member in zip_file.namelist():
                            filename = os.path.split(member)
                            if not filename[1]:
                                continue
                            new_filename = os.path.join(
                                filename[0].replace("ImageHider-main", "."),
                                filename[1])
                            source = zip_file.open(member)
                            target = open(new_filename, "wb")
                            with source, target:
                                shutil.copyfileobj(source, target)
                    print(GREEN + "ImageHider mis a jour !")
                    print(GREEN + "Veuillez redemarer, appuyez sur entre")
                    input()
                    print(WHITE, end="")
                    sys.exit(0)
                except Exception as e:
                    EXIT(e)
            else:
                print(YELLOW + "Reponse du serveur invalide, veuillez reessayer plus tard")

def banner(data):
    try:
        __import__("pyfiglet")
    except:
        have_pyfiglet = False
    else:
        have_pyfiglet = True

    if have_pyfiglet:
        return YELLOW + __import__("pyfiglet").figlet_format(data)
    else:
        return YELLOW + " " * ((os.get_terminal_size()[0] - len(data))//2) + data

def EXIT(error):
    print(PURPLE + "Erreur :", error)
    print(BLUE + "Appuyez sur entre", end="")
    input()
    print(WHITE, end="")
    sys.exit(1)

def write_jpg(imagename, content):
    with open(imagename, "ab") as f:
        f.write(content)

def read_jpg(imagename):
    with open(imagename, "rb") as f:
        content = f.read()
        offset = content.index(bytes.fromhex("FFD9"))

        f.seek(offset + 2)
        return f.read()


def write_png(filename, content):
    with open(filename, "ab") as f:
        f.write(content)

def read_png(filename):
    with open(filename, "rb") as f:
        content = f.read()
        offset = content.index(b"\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82")
        f.seek(offset + 11)
        return f.read()

def write(filename, content):
    _, ext = os.path.splitext(filename)
    if ext in (".jpg", ".jpeg"):
        write_jpg(filename, b64encode(content.encode()))
    elif ext in (".png",):
        write_png(filename, b64encode(content.encode()))
    else:
        EXIT("Format non suporte")

def read(filename):
    _, ext = os.path.splitext(filename)
    if ext in (".jpg", ".jpeg"):
        return b64decode(read_jpg(filename)).decode()
    elif ext in (".png",):
        return b64decode(read_png(filename)).decode()
    else:
        EXIT("Format non suporte")

def clean(filename):
    _, ext = os.path.splitext(filename)
    if ext in (".jpg", ".jpeg"):
        with open(filename, "rb") as f:
            data = f.read().replace(read_jpg(filename), b"")
        with open(filename, "wb") as f:
            f.write(data)
    elif ext in (".png",):
        with open(filename, "rb") as f:
            data = f.read().replace(read_png(filename), b"")
        with open(filename, "wb") as f:
            f.write(data)
    else:
        EXIT("Format non suporte")

def main():
    print(banner("ImageHider"))
    ChecForUpdates()
    print()
    print(BLUE + "Bienvenue !")
    print()
    print(GREEN + "Voullez vous :")
    print(BLUE + "\tEcrire des donnes dans une image (E)")
    print(BLUE + "\tLire des donnes depuis une image (L)")
    print(BLUE + "\tNetoyer une image de son donnes suplementaires (N)")
    print(RED + "\tQuitter (Q)")
    print()
    print(YELLOW + "> " + WHITE, end="")
    chx = input()

    while not chx.upper() in ("E", "L", "N", "Q"):
        print(YELLOW + "> " + WHITE, end="")
        chx = input()
    if chx.upper() == "E":
        print()
        print(GREEN + "Fichier : " + WHITE, end="")
        file = input()
        while not os.path.isfile(file):
            print(GREEN + "Fichier : " + WHITE, end="")
            file = input()
        print(YELLOW + "Veuillez entrer vos donnes, puis ecrivez EOF (en majuscule) pour terminer :" + WHITE)
        data = ""
        tmp = input()
        while tmp != "EOF":
            data += tmp
            data += "\n"
            tmp = input()
        write(file, data)
        print(PURPLE + "Le fichier", file, "a ete modifie avec succes !")
        input(BLUE + "Appuyez sur entre")
        print(WHITE, end="")
        sys.exit(0)

    elif chx.upper() == "L":
        print()
        print(GREEN + "Fichier : " + WHITE, end="")
        file = input()
        while not os.path.isfile(file):
            print(GREEN + "Fichier : " + WHITE, end="")
            file = input()
        print(PURPLE + "Donnes :" + WHITE)
        print(read(file))
        input(BLUE + "Appuyez sur entre")
        print(WHITE, end="")
        sys.exit(0)

    elif chx.upper() == "N":
        print()
        print(GREEN + "Fichier : " + WHITE, end="")
        file = input()
        while not os.path.isfile(file):
            print(GREEN + "Fichier : " + WHITE, end="")
            file = input()
        print(YELLOW + "Netoyage du fichier", file, "en cour...")
        clean(file)
        __import__("time").sleep(1)
        print(GREEN + "Netoyage effectue avec succes")
        input(BLUE + "Appuyez sur entre")
        print(WHITE, end="")
        sys.exit(0)

    else:
        print(RED + random.choice(goodby))
        input(BLUE + "Appuyez sur entre")
        print(WHITE, end="")
        sys.exit(666)


if __name__ == "__main__":
    main()
"""

def setup():
    print(BLUE + "Creation des dossiers et fichiers necessaires au bon fonctionnement")
    if os.name == "nt":
        dirname = "files"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        os.system("attrib +h " + dirname)
    else:
        dirname = ".files"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
    
    formated = code.replace("FILES", dirname)
    with open("ImageHider.py", "w+") as f:
        f.write(formated)
    
    print()
    print(PURPLE + "Veuillez utiliser le script ImageHider.py !")
    print()
    print(BLUE + "Appuyez sur entre")
    input()
    
    os.remove(sys.argv[0])
    
    print(WHITE, end="")

RED    = "\33[31m"
YELLOW = "\33[33m"
BLUE   = "\33[34m"
WHITE  = "\33[0m"
PURPLE = "\33[35m"

needed_modules = [
    "base64",
    "io",
    "requests",
    "zipfile",
    "random",
    "shutil"
]

usefull_modules = [
    "pyfiglet",

]

uninstalled = {}

for m in usefull_modules:
    try:
        __import__(m)
    except:
        uninstalled[m] = 0

for m in needed_modules:
    try:
        __import__(m)
    except:
        uninstalled[m] = 1

if len(uninstalled.keys()):
    print(PURPLE + "Vous avez des modules non installes :")

    for m in uninstalled.keys():
        if uninstalled[m]:
            print(RED + m)
        else:
            print(YELLOW + m)
    
    print()
    print(RED + "Modules necessaires")
    print(YELLOW + "Modules visuels")

    print()

    print(BLUE + "Les installer ? (O/N) : " + WHITE, end="")

    chx = input()

    while not chx.upper() in ("O", "N"):
        print(BLUE + "(O/N) : " + WHITE, end="")
        chx = input()
    
    if chx.upper() == "N":
        if any([uninstalled[x] for x in uninstalled.keys()]):
            print(RED + "Des modules necessaires ne sont pas installes !")
            print(BLUE + "Appuyez sur entre", end="")
            input()
            print(WHITE, end="")
            sys.exit(0)
        else:
            setup()
    else:
        failure = []
        print()
        print(YELLOW + "Installation...")
        for m in uninstalled.keys():
            print(f"Installation de {m}")
            __import__("os").system(f"{sys.executable} -m pip install {m}")
            try:
                __import__(m)
            except:
                failure.append(m)
        if len(failure):
            print(RED + "L'installation a echoue pour les modules suivants :")
            for m in failure:
                print(YELLOW + m)
            print()
            print(BLUE + "Veuillez les installer et reessayer")
            input()
            sys.exit(0)
        print()
        print(BLUE + "Installation reussie !")


setup()
