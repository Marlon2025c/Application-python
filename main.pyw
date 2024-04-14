#From et import personnelle 
import minecraft_launcher_lib as Launcher
from common import QApplication, QPushButton,  QMessageBox, QVBoxLayout, QWidget, QMainWindow, sys, os, configparser, subprocess, QWebEngineView, QWebEngineProfile, QUrl, QLocale

# Créer un objet ConfigParser
idini= configparser.ConfigParser()
config = configparser.ConfigParser()


# Function to load login information from login.ini
def load_login_info():
    login_info = {}
    if os.path.exists("config/login.ini"):
        config.read("config/login.ini")
        login_info['remember'] = config['LOGIN'].getint('remember', 0)
    else:
        # Créer le fichier login.ini avec remember à 0 par défaut
        with open("config/login.ini", "w") as file:
            file.write("[LOGIN]\n")
            file.write("remember = 0\n")
        # Charger les informations par défaut
        login_info['remember'] = 0
    return login_info

# Function to save login information to login.ini
def save_login_info(refresh_token, remember):
    config = configparser.ConfigParser()
    config['LOGIN'] = {'refresh_token': refresh_token, 'remember': remember}
    with open("config/login.ini", 'w') as configfile:
        config.write(configfile)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 200)  # Remplacez 400 et 200 par la largeur et la hauteur souhaitées
        self.setWindowTitle("Luancher MARLON 2000 :)")

        # Read existing login information if available
        self.login_info = load_login_info()

        if os.path.exists("config/login.ini"):
                refresh_token = configparser.ConfigParser()
                refresh_token.read('Config/login.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
                refresh_token = refresh_token['LOGIN'].get('refresh_token', '')
                try:
                    idini.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
                    CLIENT_ID = idini['AZURE'].get('client_id', '')
                    REDIRECT_URL = idini['AZURE'].get('redirect_url', '')
                    account_informaton = Launcher.microsoft_account.complete_refresh(CLIENT_ID, None, REDIRECT_URL, refresh_token)
                    print("complete_refresh: le test du code pour rien")
                    print(account_informaton["name"])
                # Show the window if the refresh token is invalid
                except Launcher.exceptions.InvalidRefreshToken:
                    pass
        else:
            print("pas de compte dans le luancher")

        if self.login_info['remember'] == 1:
            
            self.show_logout_button()
        else:
            self.show_login_button()

        from update import check_for_updates
        check_for_updates()

    # def show_account_information(self, information_dict):
    #     information_string = f'Username: {information_dict["name"]}<br>'
    #     information_string += f'UUID: {information_dict["id"]}<br>'
    #     information_string += f'Token: {information_dict["access_token"]}<br>'

    #     # Save the refresh token in a file
    #     config.read('Config/refresh_token.ini')
    #     config['TOKEN'] = {'refresh_token': information_dict["refresh_token"], 'remember': 1}
    #     with open("config/refresh_token.ini", 'w') as configfile:
    #         config.write(configfile)

    #     message_box = QMessageBox()
    #     message_box.setWindowTitle("Account information")
    #     message_box.setText(information_string)
    #     message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    #     message_box.exec()

    def login(self):
        # Charger les données à partir du fichier config.ini
        idini.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
        CLIENT_ID = idini['AZURE'].get('client_id', '')
        REDIRECT_URL = idini['AZURE'].get('redirect_url', '')
        # Open the login url
        login_url, self.state, self.code_verifier = Launcher.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URL)
        self.web_view = QWebEngineView()
        self.setWindowTitle("Connexion avec Microsoft")
        self.web_view.load(QUrl(login_url))
        self.web_view.show()
        self.web_view.urlChanged.connect(self.new_url)

    def new_url(self, url: QUrl):
        try:
            # Charger les données à partir du fichier config.ini
            idini.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
            CLIENT_ID = idini['AZURE'].get('client_id', '')
            REDIRECT_URL = idini['AZURE'].get('redirect_url', '')
            # Get the code from the url
            auth_code = Launcher.microsoft_account.parse_auth_code_url(url.toString(), self.state)
            # Do the login
            account_information = Launcher.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code, self.code_verifier)

            # Save the username, UUID, token, and remember in the config file
            save_login_info(account_information["refresh_token"], 1)
            self.web_view.close()
            self.show_logout_button()
        except AssertionError:
            print("States do not match!")
        except KeyError:
            print("Url not valid")

    def launch_minecraft(self):
        vanille_version = "1.20.1"
        if os.path.exists("config/login.ini"):
                refresh_token = configparser.ConfigParser()
                refresh_token.read('Config/login.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
                refresh_token = refresh_token['LOGIN'].get('refresh_token', '')
                try:
                    idini.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
                    CLIENT_ID = idini['AZURE'].get('client_id', '')
                    REDIRECT_URL = idini['AZURE'].get('redirect_url', '')
                    account_informaton = Launcher.microsoft_account.complete_refresh(CLIENT_ID, None, REDIRECT_URL, refresh_token)
                    print("complete_refresh: le test du code pour rien")
                    print(account_informaton["name"])
                # Show the window if the refresh token is invalid
                except Launcher.exceptions.InvalidRefreshToken:
                    pass
        else:
            print("pas de compte dans le luancher")
        print(account_informaton["id"],account_informaton["access_token"])
        options = {
            "username":account_informaton["name"],
            "uuid": account_informaton["id"],
            "token": account_informaton["access_token"],
            # Autres options
            "executablePath": "java", # The path to the java executable
            # "defaultExecutablePath": "java", # The path to the java executable if the version.json has none
            "jvmArguments": ["-Xmx8G", "-Xms8G"], #The jvmArguments
            "launcherName": "SpaziaCraft", # The name of your launcher
            "launcherVersion": "1.0.7", # The version of your launcher
            # "gameDirectory": "/home/user/.minecraft", # The gameDirectory (default is the path given in arguments)
            # "demo": False, # Run Minecraft in demo mode
            "customResolution": False, # Enable custom resolution
            "resolutionWidth": "854", # The resolution width
            "resolutionHeight": "480", # The resolution heigth
            "resolutionHeight": "480", # The resolution heigth
            "server": "82.66.194.176", # The IP of a server where Minecraft connect to after start
            "port": "25565", # The port of a server where Minecraft connect to after start
            # "nativesDirectory": "minecraft_directory/versions/version/natives", # The natives directory
            "enableLoggingConfig": False, # Enable use of the log4j configuration file
            "disableMultiplayer": False, # Disables the multiplayer
            "disableChat": False, # Disables the chat
            "quickPlayPath": None, # The Quick Play Path
            "quickPlaySingleplayer": None, # The Quick Play Singleplayer
            "quickPlayMultiplayer": None, # The Quick Play Multiplayer
            "quickPlayRealms": None, # The Quick Play Realms
        }

        # Find the latest forge version for that Minecraft version
        forge_version = Launcher.forge.find_forge_version(vanille_version)

        # Vérifie si la version peut être installée automatiquement
        minecraft_directory = Launcher.utils.get_minecraft_directory().replace('minecraft','spaziacraft')
        full_name_forge_version = forge_version.replace("-", "-forge-")

        callback = {
            "setStatus": lambda text: print(text)
        }
        # Installez la version de Forge
        #if not os.path.exists(minecraft_directory):
            #print("merder ça marche pas ")
        Launcher.forge.install_forge_version(forge_version, minecraft_directory, callback=callback)

        # Obtenez la commande de lancement de Minecraft
        minecraft_command = Launcher.command.get_minecraft_command(full_name_forge_version, minecraft_directory, options)
        
        from mod_manager import download_and_install_mods
        download_and_install_mods(minecraft_directory)
        # Lancez Minecraft en utilisant subprocess
        print("Lancement de Minecraft avec la commande :")
        print(minecraft_command)
        # Lancez Minecraft en utilisant subprocess
        lancer = subprocess.Popen(minecraft_command, creationflags=subprocess.CREATE_NO_WINDOW)


    def logout(self):
        # Charger les informations de connexion
        login_info = load_login_info()
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
            self.show_login_button()

    def show_login_button(self):
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(login_button)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def show_logout_button(self):
        # Créer les boutons
        game_button = QPushButton(f"Lancer Minecraft")
        game_button.clicked.connect(self.launch_minecraft)


        logout_button = QPushButton(f"Logout")
        logout_button.clicked.connect(self.logout)

        # Créer un layout principal pour les boutons
        main_layout = QVBoxLayout()
        main_layout.addWidget(game_button)
        main_layout.addWidget(logout_button)

        # Créer le widget central et définir le layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Définir le widget central de la fenêtre principale
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # This line sets the language of the webpage to the system language
    QWebEngineProfile.defaultProfile().setHttpAcceptLanguage(QLocale.system().name().split("_")[0])
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())