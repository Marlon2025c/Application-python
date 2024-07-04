#From et import personnelle 
from minecraft_launcher_lib.microsoft_account import AccountNotOwnMinecraft
from import_perso import (
    QApplication, Qt, QIcon, QPushButton, QVBoxLayout, QWidget, QMainWindow, sys, os, configparser,
    QWebEngineView, QUrl, QFile, QTextStream, Launcher, QProcess
)
from vue.mains_menu import setupUi, refresh_file_lists
from function.gestion_updates import check_for_updates

def apiazure():
        from cryptography.fernet import Fernet
        # Créer un objet Fernet avec la clé de chiffrement
        KEY = b'RTp1WDhKEokF844oN7GJVD6LVlR2kfqQhsjSK3Bq168='
        fernet = Fernet(KEY)
    
        azure_config = configparser.ConfigParser()
        azure_config.read('config/id.ini') 
        # Lire les données binaires à partir du fichier id.ini
        client_id= azure_config['AZURE'].get('client_id', '')
        redirect_url= azure_config['AZURE'].get('redirect_url', '')
    
        # Déchiffrer les valeurs du client ID et de l'URL de redirection
        CLIENT_ID = fernet.decrypt(client_id.encode()).decode()
        REDIRECT_URL  = fernet.decrypt(redirect_url.encode()).decode()
    
        return CLIENT_ID, REDIRECT_URL

def reload_app():
    QApplication.quit()
    QProcess.startDetached(sys.executable, sys.argv)

def main():
    
    def login_info():
        config = configparser.ConfigParser()
        login_info = {}
        if os.path.exists("config/login.ini"):
            config.read("config/login.ini")
            login_info['remember'] = config['LOGIN'].getint('remember', 0)
            if login_info['remember'] == 1:   
                login_info['refresh_token'] = config['LOGIN'].get('refresh_token', '')
                CLIENT_ID, REDIRECT_URL = apiazure()
                try:
                    global account_informaton
                    account_informaton = Launcher.microsoft_account.complete_refresh(CLIENT_ID, None, REDIRECT_URL, login_info['refresh_token'])
                    print(account_informaton["name"])
                except Launcher.exceptions.InvalidRefreshToken:
                    print("InvalidRefreshToken", Launcher.CompleteLoginResponse)
                    pass
        else:
            # Créer le fichier login.ini avec remember à 0 par défaut
            with open("config/login.ini", "w") as file:
                file.write("[LOGIN]\n")
                file.write("remember = 0\n")
            # Charger les informations par défaut
            login_info['remember'] = 0
        return login_info
        

    def login(login_window):
        global new_window
        CLIENT_ID, REDIRECT_URL = apiazure()
        login_url, state, code_verifier = Launcher.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URL)
    
        def handle_url_change(url):
            try:
                auth_code = Launcher.microsoft_account.parse_auth_code_url(url.toString(), state)
                account_information = Launcher.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code, code_verifier)
                    
                # Save the username, UUID, token, and remember in the config file
                config = configparser.ConfigParser()
                config['LOGIN'] = {'refresh_token': account_information["refresh_token"], 'remember': 1}
                with open("config/login.ini", 'w') as configfile:
                    config.write(configfile)

                reload_app()
            except AssertionError:
                print("States do not match!")
            except KeyError:
                print("Url not valid")
            except AccountNotOwnMinecraft:
                print("Pas de compte Minecraft")

        new_window = QWebEngineView()
        new_window.setWindowTitle("Connextion Microsoft")
        new_window.load(QUrl(login_url))
        new_window.show()
        new_window.urlChanged.connect(handle_url_change)

    def login_window():
        global login_window
        login_window = QMainWindow()
        login_window.setWindowTitle("Spaziacraft Launcher")
        login_window.setFixedSize(350, 500)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-image: url('asset/MinecraftWallpaper'); background-repeat: no-repeat; background-position: center;")
        
        # Create the button with icon and styling
        button = QPushButton("Connexion")
        button.setIcon(QIcon("asset/Microsoft_icon"))  # Chemin vers l'icône
        button.setFixedSize(200, 100)  # Définition de la taille du bouton
        button.setStyleSheet("font-size: 20px; background: white;")  # Ajuster la taille du texte
        button.clicked.connect(lambda: login(login_window))  # Passer la fenêtre de connexion comme argument à la fonction de connexion

        # Center the button horizontally within the layout
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        # Set the central widget of the main window
        login_window.setCentralWidget(central_widget)
        login_window.show()
    
    def main():
        minecraft_directory = Launcher.utils.get_minecraft_directory().replace('minecraft','spaziacraft')
        setupUi(account_informaton, logout)
        refresh_file_lists(minecraft_directory)

    def logout():
        # Effacer les informations de connexion sauf remember du fichier login.ini
        config = configparser.ConfigParser()
        config.read("config/login.ini")
        if 'LOGIN' in config:
            if config.has_option('LOGIN', 'refresh_token'):
                config.remove_option('LOGIN', 'refresh_token')
            config.set('LOGIN', 'remember', '0')
            with open("config/login.ini", 'w') as configfile:
                config.write(configfile)
            # Afficher le bouton de connexion
            reload_app()

    login_info = login_info()
    if login_info['remember'] == 0:     
        login_window = login_window()
        sys.exit(app.exec())
    else:
        logout = main()
        sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = QFile("style.qss")
    style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    check_for_updates()
    main()