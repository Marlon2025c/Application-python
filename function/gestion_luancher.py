import minecraft_launcher_lib as Launcher
import threading
from function.gestion_langues import language_system
from function.gestion_mods import download_and_install_mods
from import_perso import subprocess, configparser
import ast
def launch_minecraft(account_information, progressBar, launcher_button, comboBox_langue, label_progrssBar):
        # Désactiver le bouton de lancement
    launcher_button.setStyleSheet("background-color: gris;")
    launcher_button.setEnabled(False)
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # Récupérer et convertir les valeurs de jvmArguments
    jvm_arguments_str = config['Launcher'].get('jvmarguments', '[]')
    jvm_arguments = ast.literal_eval(jvm_arguments_str)  # Convertit la chaîne en une liste Python
    vanille_version = "1.20.1"
    options = {
        "username": account_information["name"],
        "uuid": account_information["id"],
        "token": account_information["access_token"],
        "executablePath": "javaw",
        "jvmArguments": jvm_arguments,
        "launcherName": "SpaziaCraft",
        "launcherVersion": "2.0.0",
        "customResolution": False,
        "resolutionWidth": "854",
        "resolutionHeight": "480",
        "server": "82.66.194.176",
        "port": "25565",
    }

    forge_version = Launcher.forge.find_forge_version(vanille_version)
    minecraft_directory = Launcher.utils.get_minecraft_directory().replace('minecraft','spaziacraft')
    full_name_forge_version = forge_version.replace("-", "-forge-")

    callback = {
        "setStatus": lambda text: label_progrssBar.setText(text),
        "setProgress": lambda value: progressBar.setValue(value),
        "setMax": lambda maximum: progressBar.setMaximum(maximum)
    }
    selected_language_code = comboBox_langue.currentData()
    language_system.current_language = selected_language_code  # Met à jour la langue actuelle dans le système de langue
    language_system.load_translations(selected_language_code)  # Charge les traductions pour la nouvelle langue
    launcher_button.setText(language_system.translate("launcher_minecraft_encours"))

    progressBar.setVisible(True)
    label_progrssBar.setVisible(True)
    
    Launcher.forge.install_forge_version(forge_version, minecraft_directory, callback)
    
    download_and_install_mods(minecraft_directory, callback)
    progressBar.setVisible(False)
    label_progrssBar.setVisible(False)
    minecraft_command = Launcher.command.get_minecraft_command(full_name_forge_version, minecraft_directory, options)
    
    # Lancer Minecraft en utilisant subprocess
    minecraft_process = subprocess.Popen(minecraft_command, creationflags=subprocess.CREATE_NO_WINDOW)
    
    # Créer un thread pour surveiller le processus Minecraft
    def monitor_minecraft_process():
        minecraft_process.wait()  # Attend que le processus se termine
        launcher_button.setEnabled(True)  # Réactive le bouton de lancement
        launcher_button.setStyleSheet("background-color: white;")  # Rétablit la couleur de base
        launcher_button.setText(language_system.translate("launcher_minecraft"))

    threading.Thread(target=monitor_minecraft_process, daemon=True).start()