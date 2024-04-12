from common import requests, os, shutil

MODS_TO_DOWNLOAD = [
    ("create", "https://cdn.modrinth.com/data/LNytGWDc/versions/HNYrbfZZ/create-1.20.1-0.5.1.f.jar"),
    ("rechiseledcreate", "https://cdn.modrinth.com/data/E6867niZ/versions/ZWTqq1kk/rechiseledcreate-1.0.0a-forge-mc1.20.jar"),
    ("jei", "https://cdn.modrinth.com/data/u6dRKJwZ/versions/PeYsGsQy/jei-1.20.1-forge-15.3.0.4.jar"),
    ("farmersdelight","https://cdn.modrinth.com/data/R2OftAxM/versions/AxgOboGq/FarmersDelight-1.20.1-1.2.4.jar"),
    ("delightful", "https://cdn.modrinth.com/data/JtSnhtNJ/versions/noAl23LW/Delightful-1.20.1-3.4.3.jar"),
    ("corndelight", "https://cdn.modrinth.com/data/uxLAKWU8/versions/F7Advb7w/corn_delight-1.0.3-1.20.1.jar"),
    ("mysterious_mountain_lib", "https://cdn.modrinth.com/data/ntMyNH8c/versions/nB8NuTIO/mysterious_mountain_lib-1.4.4-1.20.1.jar"),
    ("automobility", "https://cdn.modrinth.com/data/rqIsPf9F/versions/46g3IiWw/automobility-0.4.2%2B1.20.1-forge.jar"),
    ("furniture", "https://cdn.modrinth.com/data/ulloLmqG/versions/cmWbslFO/another_furniture-forge-1.20.1-3.0.1.jar"),
    ("minimap", "https://cdn.modrinth.com/data/1bokaNcj/versions/voIrfIDP/Xaeros_Minimap_24.0.3_Forge_1.20.jar"),

    ("terrablender", "https://cdn.modrinth.com/data/kkmrDlKT/versions/htFwnGWu/TerraBlender-forge-1.20.1-3.0.1.4.jar"),
    ("BiomesOPlenty", "https://cdn.modrinth.com/data/HXF82T3G/versions/peO5lWzX/BiomesOPlenty-1.20.1-18.0.0.598.jar"),
    ("Mekanism", "https://cdn.modrinth.com/data/Ce6I4WUE/versions/gNIc57RO/Mekanism-1.20.1-10.4.6.20.jar"),
    ("MekanismAdditions", "https://cdn.modrinth.com/data/a6F3uASn/versions/pXrqwQNY/MekanismAdditions-1.20.1-10.4.6.20.jar"),
    ("MekanismGenerators", "https://cdn.modrinth.com/data/OFVYKsAk/versions/1E44ANCP/MekanismGenerators-1.20.1-10.4.6.20.jar"),
    ("MekanismTools", "https://cdn.modrinth.com/data/tqQpq1lt/versions/tsH6SxFL/MekanismTools-1.20.1-10.4.6.20.jar"),
    ("travelersbackpack", "https://cdn.modrinth.com/data/rlloIFEV/versions/FKixWJhX/travelersbackpack-forge-1.20.1-9.1.13.jar"),

    ("ironchest", "https://cdn.modrinth.com/data/P3iIrPH3/versions/YjbOtYwN/ironchest-1.20.1-14.4.4.jar"),
    ("naturalist", "https://cdn.modrinth.com/data/F8BQNPWX/versions/fapHaClR/naturalist-forge-4.0.3-1.20.1.jar"),
    ("geckolib", "https://cdn.modrinth.com/data/8BmcQJ2H/versions/vv4Q0406/geckolib-forge-1.20.1-4.4.4.jar"),

    # Version 1.0.6
    ("rechiseled", "https://cdn.modrinth.com/data/B0g2vT6l/versions/ChrMlKQC/rechiseled-1.1.5c-forge-mc1.20.jar"),
    ("supermartijn642corelib", "https://cdn.modrinth.com/data/rOUBggPv/versions/U92Le4sE/supermartijn642corelib-1.1.17-forge-mc1.20.1.jar"),
    ("supermartijn642configlib", "https://cdn.modrinth.com/data/LN9BxssP/versions/ZKor79dR/supermartijn642configlib-1.1.8-forge-mc1.20.jar"),
    ("fusion", "https://cdn.modrinth.com/data/p19vrgc2/versions/oA5jxU4i/fusion-1.1.1-forge-mc1.20.1.jar"),
    ("toughasnails", "https://cdn.modrinth.com/data/ge1sOdFH/versions/40SuKdWl/ToughAsNails-1.20.1-9.0.0.96.jar"),
    ("sereneSeasons", "https://cdn.modrinth.com/data/e0bNACJD/versions/gvqNV855/SereneSeasons-1.20.1-9.0.0.46.jar"),

    # Version 1.0.7
    ("gravestone", "https://cdn.modrinth.com/data/RYtXKJPr/versions/OmP48Fw1/gravestone-forge-1.20.1-1.0.15.jar"),
    ('CorgiLib', 'https://cdn.modrinth.com/data/ziOp6EO8/versions/L3Etx6qQ/CorgiLib-forge-1.20.1-4.0.1.1.jar'),
    ('coroutil', 'https://cdn.modrinth.com/data/rLLJ1OZM/versions/6rPDKAT8/coroutil-forge-1.20.1-1.3.7.jar'),
    ('ExtremeReactors2', 'https://cdn.modrinth.com/data/idkvShUy/versions/5CYl80HP/ExtremeReactors2-1.20.1-2.0.75.jar'),
    ('ZeroCore2', 'https://cdn.modrinth.com/data/rHpb85Mf/versions/kR2IVnv0/ZeroCore2-1.20.1-2.1.39.jar'),
    ('zombieawareness', 'mods/zombieawareness.jar'),
    ('BadMobs', 'mods/BadMobs.jar'),

    ("cfm", "mods/cfm.jar"),  # Exemple de mod local
    ("optifine", "mods/optifine.jar"),  # Exemple de mod local
]


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

def download_and_install_mods(minecraft_directory):

    for mod_name, mod_source in MODS_TO_DOWNLOAD:
        if mod_source.startswith("http"):
            mod_path = download_mod(mod_source, minecraft_directory, mod_name)
            if mod_path:
                install_mod(mod_path, minecraft_directory)
        else:
            # Supposons que mod_source est le chemin local du mod
            mod_path = mod_source
            install_mod(mod_path, minecraft_directory)
