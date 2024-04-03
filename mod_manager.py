import os
import requests
import shutil

def download_mod(url, destination_folder, mod_name):
    mod_folder = os.path.join(destination_folder, "mods")
    os.makedirs(mod_folder, exist_ok=True)

    mod_path = os.path.join(mod_folder, f"{mod_name}.jar")
    if os.path.exists(mod_path):
        print(f"Le mod {mod_name} est déjà présent dans le dossier des mods.")
        return mod_path

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(mod_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        print(f"Mod {mod_name} téléchargé avec succès !")
        return mod_path
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement du mod {mod_name} depuis {url}: {e}")
        return None

def install_mod(mod_path, minecraft_directory):
    mod_filename = os.path.basename(mod_path)
    destination_path = os.path.join(minecraft_directory, "mods", mod_filename)

    if os.path.exists(destination_path):
        print(f"Le mod {mod_filename} est déjà présent dans le dossier des mods.")
        return

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.move(mod_path, destination_path)
    print(f"Mod {mod_filename} installé avec succès !")

def download_and_install_mods(mods_to_download, minecraft_directory):
    for mod_name, mod_url in mods_to_download:
        mod_path = download_mod(mod_url, minecraft_directory, mod_name)
        if mod_path:
            install_mod(mod_path, minecraft_directory)
