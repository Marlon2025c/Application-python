import tkinter as tk
from tkinter import messagebox as tkMessageBox
import minecraft_launcher_lib as Launcher
import subprocess
import sys

def launch_minecraft():
    # Obtenez le répertoire Minecraft
    minecraft_directory = Launcher.utils.get_minecraft_directory()
    print("testsetsts " + minecraft_directory)

    # Définir les options de lancement
    options = Launcher.utils.generate_test_options()
    # Obtenir la commande Minecraft pour la version 1.20.4
    minecraft_command = Launcher.command.get_minecraft_command("1.20", minecraft_directory, options)
    # Lancer Minecraft en utilisant subprocess
    subprocess.Popen(minecraft_command)

# Configuration de la fenêtre principale
window = tk.Tk()
window.title("Premier APP en Python")
window.geometry("400x400")

# Création des éléments de l'interface utilisateur
hello = tk.Label(window, text="Hello World", bg="red", fg="white")
hello.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Lancer TEST", command=launch_minecraft)
button.pack()

# Boucle principale de l'interface utilisateur
window.mainloop()