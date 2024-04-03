import tkinter as tk
from tkinter import messagebox as tkMessageBox
import minecraft_launcher_lib as Launcher
import subprocess
import sys
import requests
from mod_manager import download_and_install_mods
import configparser


""" 
import requests
import shutil
from tqdm import tqdm
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse, parse_qs 
"""

# Créer un objet ConfigParser
config = configparser.ConfigParser()
# Charger les données à partir du fichier config.ini
config.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini

# Accéder aux valeurs dans la section [ID]
client_id = config['ID']['client_id']
secret = config['ID']['secret']
redirect_url = config['ID']['redirect_url']

MODS_TO_DOWNLOAD = [
    ("create", "https://cdn.modrinth.com/data/LNytGWDc/versions/HNYrbfZZ/create-1.20.1-0.5.1.f.jar"),
    ("jei", "https://cdn.modrinth.com/data/u6dRKJwZ/versions/PeYsGsQy/jei-1.20.1-forge-15.3.0.4.jar")
]

def launch_minecraft(options=None):
    vanille_version = "1.20.1"
    # Find the latest forge version for that Minecraft version
    forge_version = Launcher.forge.find_forge_version(vanille_version)
    # Checks if a forge version exists for that version
    if forge_version is None:
        print("This Minecraft version is not supported by forge")
        sys.exit(0)
    # Vérifie si la version peut être installée automatiquement
    minecraft_directory = Launcher.utils.get_minecraft_directory().replace('minecraft','spaziacraft')
    full_name_forge_version = forge_version.replace("-", "-forge-")
    callback = {
        "setStatus": lambda text: print(text)
    }
    # Transformer l'identifiant de version pour correspondre au format attendu
    full_name_forge_version = forge_version.replace("-", "-forge-")
    print(f"Nom complet de la version de Forge : {full_name_forge_version}")

    # Installez la version de Forge
    Launcher.forge.install_forge_version(forge_version, minecraft_directory, callback=callback)
    print(minecraft_directory)

    # Définissez les options de lancement (si nécessaire)
    if options is None:
        options = Launcher.utils.generate_test_options()  
        print(options) 


    # Obtenez la commande de lancement de Minecraft
    print("testestsetsetes")
    minecraft_command = Launcher.command.get_minecraft_command(full_name_forge_version, minecraft_directory, options)
    print(minecraft_command)
    download_and_install_mods(MODS_TO_DOWNLOAD, minecraft_directory)
    # Lancez Minecraft en utilisant subprocess
    subprocess.run(minecraft_command)
    tkMessageBox.showinfo("FIN", "Votre Minecraft est fermé. Merci d'avoir utilisé mon lanceur.")



def microsoft_login():
    # Login
    login_url, state, code_verifier = Launcher.microsoft_account.get_secure_login_data(client_id, redirect_url)
    print(f"Please open {login_url} in your browser and copy the code after the '?' in the URL when you are redirected.")

    # Get the code from the user input (just the code part)
    code_url = input("Enter the code: ")

    try:
        auth_code = Launcher.microsoft_account.parse_auth_code_url(code_url, state)
        login_data = Launcher.microsoft_account.complete_login(client_id, None, redirect_url, auth_code, code_verifier)
        
        # Get Minecraft command options from user login data
        options = {
            "username": login_data["name"],
            "uuid": login_data["id"],
            "token": login_data["access_token"],
            # This is optional
            # "executablePath": "java", # The path to the java executable
            # "defaultExecutablePath": "java", # The path to the java executable if the version.json has none
            "jvmArguments": ["-Xmx4G", "-Xms4G"], #The jvmArguments
            "launcherName": "SpaziaCraft Luancher", # The name of your launcher
            "launcherVersion": "1.0.0", # The version of your launcher
            # "gameDirectory": "/home/user/.minecraft", # The gameDirectory (default is the path given in arguments)
            "demo": False, # Run Minecraft in demo mode
            "customResolution": False, # Enable custom resolution
            "resolutionWidth": "854", # The resolution width
            "resolutionHeight": "480", # The resolution heigth
            # "server": "play.vikicraft.fr", # The IP of a server where Minecraft connect to after start
            # "port": "25565", # The port of a server where Minecraft connect to after start
            # "nativesDirectory": "minecraft_directory/versions/version/natives", # The natives directory
            "enableLoggingConfig": False, # Enable use of the log4j configuration file
            "disableMultiplayer": False, # Disables the multiplayer
            "disableChat": False, # Disables the chat
            "quickPlayPath": None, # The Quick Play Path
            "quickPlaySingleplayer": None, # The Quick Play Singleplayer
            "quickPlayMultiplayer": None, # The Quick Play Multiplayer
            "quickPlayRealms": None, # The Quick Play Realms
        }
        print("Options de connexion récupérées :", options)

        # Lancer Minecraft avec les options de connexion
        launch_minecraft(options)

    except AssertionError:
        print("Les états ne correspondent pas !")
    except ValueError:
        print("Code invalide")


# Créer une fenêtre Tkinter
window = tk.Tk()
window.title("Premier APP en Python")
window.geometry("400x400")

button = tk.Button(window, text="Lancer TEST", command=launch_minecraft)
button.pack()

# Ajoutez un bouton pour lancer le processus de connexion Microsoft
ms_button = tk.Button(window, text="Connexion Microsoft", command=microsoft_login)
ms_button.pack(pady=10)

def get_current_version():
    # Lire la version depuis un fichier
    with open("version.txt", "r") as file:
        return file.read().strip()

def get_latest_release_info(repo_owner, repo_name):
    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest")
    if response.status_code == 200:
        release_info = response.json()
        return release_info
    else:
        return None

def check_for_updates(repo_owner, repo_name):
    current_version = get_current_version()
    latest_release = get_latest_release_info(repo_owner, repo_name)
    if latest_release:
        latest_version = latest_release["tag_name"]
        if latest_version != current_version:
            print(f"Une mise à jour est disponible ! Version actuelle : {current_version}, Dernière version : {latest_version}")
        else:
            print("Vous utilisez déjà la dernière version.")
    else:
        print("Impossible de récupérer les informations sur la dernière release.")

# Exemple d'utilisation :
check_for_updates("Marlon2025c", "Application-python")

# Ajouter un bouton pour afficher la version
version_button = tk.Button(window, text="Afficher la version")
version_button.pack(pady=10)

# Boucle principale de l'interface utilisateur
window.mainloop()