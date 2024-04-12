from common import QApplication, QMessageBox, subprocess, sys, os, requests

def check_for_updates():
    latest_version = get_latest_version_from_github()
    current_version = get_current_version_from_file()

    if latest_version and current_version and latest_version != current_version:
        app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Mise à jour disponible")
        msg_box.setText("Une nouvelle mise à jour est disponible. Voulez-vous effectuer la mise à jour maintenant?")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = msg_box.exec()
        if response == QMessageBox.StandardButton.Yes:
            download_and_install_update()
            os._exit(0)  # Quitter l'application après avoir lancé la mise à jour
    else:
        remove_existing_update()

def remove_existing_update():
    update_dir = "updates"
    update_file = os.path.join(update_dir, "mainsetup.exe")
    if os.path.exists(update_dir) and os.path.exists(update_file):
        os.remove(update_file)
        print("Fichier de mise à jour précédent supprimé avec succès.")

def get_latest_version_from_github():
    url = "https://api.github.com/repos/marlon2025c/Application-python/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    return None

def get_current_version_from_file():
    with open("version.txt", "r") as file:
        return file.read().strip()

def download_and_install_update():
    # Créer un répertoire pour stocker les mises à jour si nécessaire
    if not os.path.exists("updates"):
        os.makedirs("updates")
    
    # Télécharger mainsetup.exe depuis GitHub
    url = "https://github.com/marlon2025c/Application-python/releases/latest/download/mainsetup.exe"
    response = requests.get(url)
    with open(os.path.join("updates", "mainsetup.exe"), "wb") as file:
        file.write(response.content)
    
    # Lancer mainsetup.exe pour effectuer la mise à jour de manière asynchrone
    subprocess.Popen(os.path.join("updates", "mainsetup.exe"), shell=True)
