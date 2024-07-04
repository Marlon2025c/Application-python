from import_perso import requests, os, shutil, json

# URL du fichier JSON hébergé sur GitHub
json_url = 'https://raw.githubusercontent.com/Marlon2025c/Application-python/master/mods/liste_mods.json'

# Fonction pour lire les mods depuis une URL
def load_mods_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    return response.json()

# Charger les mods depuis l'URL
mods_list = load_mods_from_url(json_url)

def download_mod(url, destination_folder, mod_name, callback):
    mod_folder = os.path.join(destination_folder, "mods")
    os.makedirs(mod_folder, exist_ok=True)

    mod_path = os.path.join(mod_folder, f"{mod_name}.jar")
    if os.path.exists(mod_path):
        # Si le mod existe déjà, ne pas réessayer de le télécharger
        return None

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(mod_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        callback['setStatus'](f"Mod {mod_name} téléchargé avec succès !")
        return mod_path
    except requests.RequestException as e:
        callback['setStatus'](f"Erreur lors du téléchargement du mod {mod_name} depuis {url}: {e}")
        return None

def install_mod(mod_path, minecraft_directory, callback):
    mod_filename = os.path.basename(mod_path)
    destination_path = os.path.join(minecraft_directory, "mods", mod_filename)

    if os.path.exists(destination_path):
        # Si le mod existe déjà, ne pas réessayer de l'installer
        return

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.move(mod_path, destination_path)
    callback['setStatus'](f"Mod {mod_filename} installé avec succès !")

def remove_mod(mod_name, minecraft_directory, callback):
    mods_folder = os.path.join(minecraft_directory, 'mods')
    mod_path = os.path.join(mods_folder, f"{mod_name}.jar")
    if os.path.exists(mod_path):
        os.remove(mod_path)
        callback['setStatus'](f"Le mod {mod_name} a été supprimé du dossier des mods.")
    else:
        callback['setStatus'](f"Le mod {mod_name} n'a pas été trouvé dans le dossier des mods.")

def load_mod_states(states_file):
    if os.path.exists(states_file):
        with open(states_file, 'r') as f:
            return json.load(f)
    return {}

def download_and_install_mods(minecraft_directory, callback):
    states_file = 'config/mod_states.json'
    mod_states = load_mod_states(states_file)

    total_mods = len(mods_list)
    callback['setMax'](total_mods)
    
    for index, mod in enumerate(mods_list):
        mod_name = mod["name"]
        mod_filename = f"{mod_name}.jar"
        mod_path_in_mods_folder = os.path.join(minecraft_directory, "mods", mod_filename)

        if mod["is_additional"]:
            # Vérifier si le mod additionnel est activé dans le fichier mod_states.json
            if mod_states.get(mod_name, False):
                callback['setStatus'](f"Téléchargement et installation du mod additionnel : {mod_name}")
            else:
                callback['setStatus'](f"Passage du mod additionnel : {mod_name}")
                remove_mod(mod_name, minecraft_directory, callback)
                continue  # Ignorer ce mod additionnel

        # Si le mod est déjà présent, afficher un seul message et passer au suivant
        if os.path.exists(mod_path_in_mods_folder):
            callback['setStatus'](f"Le mod {mod_filename} est déjà présent dans le dossier des mods.")
            callback['setProgress'](index + 1)
            continue

        if mod["url"].startswith("http"):
            mod_path = download_mod(mod["url"], minecraft_directory, mod_name, callback)
            if mod_path:
                install_mod(mod_path, minecraft_directory, callback)
        else:
            # Supposons que mod["url"] est le chemin local du mod
            mod_path = mod["url"]
            install_mod(mod_path, minecraft_directory, callback)
        
        callback['setProgress'](index + 1)



