from import_perso import Qt, QApplication, QMessageBox, QProgressDialog, subprocess, requests, os, sys
def check_for_updates():
    latest_version = get_latest_version_from_github()
    current_version = get_current_version_from_file()

    if latest_version and current_version and latest_version != current_version:
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
            print("Non")
            os._exit(0)
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
    app = QApplication(sys.argv)  # Création de l'objet QApplication ici

    # Créer un répertoire pour stocker les mises à jour si nécessaire
    if not os.path.exists("updates"):
        os.makedirs("updates")

    # URL de téléchargement
    url = "https://github.com/marlon2025c/Application-python/releases/latest/download/mainsetup.exe"
    file_path = os.path.join("updates", "mainsetup.exe")

    # Créer une boîte de dialogue de progression
    progress = QProgressDialog("Téléchargement de la mise à jour...", "Annuler", 0, 100)
    progress.setWindowTitle("Mise à jour")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setAutoClose(True)
    progress.show()

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(file_path, "wb") as file:
        for data in response.iter_content(chunk_size=8192):
            downloaded_size += len(data)
            file.write(data)
            progress.setValue(int(downloaded_size / total_size * 100))
            if progress.wasCanceled():
                break

    if progress.wasCanceled():
        os.remove(file_path)
        print("Téléchargement annulé.")
    else:
        print("Téléchargement terminé.")
        subprocess.Popen(file_path, shell=True)

    app.quit()  # Fermer l'application après avoir lancé la mise à jour
