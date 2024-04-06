#From et import personnelle 
import minecraft_launcher_lib as Launcher
from common import QApplication, QPushButton, QVBoxLayout, QWidget, QMainWindow, sys, os, configparser, subprocess, QWebEngineView, QWebEngineProfile, QUrl, QLocale

# Créer un objet ConfigParser
config = configparser.ConfigParser()

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

    ("rechiseled", "https://cdn.modrinth.com/data/B0g2vT6l/versions/ChrMlKQC/rechiseled-1.1.5c-forge-mc1.20.jar"),
    ("supermartijn642corelib", "https://cdn.modrinth.com/data/rOUBggPv/versions/U92Le4sE/supermartijn642corelib-1.1.17-forge-mc1.20.1.jar"),
    ("supermartijn642configlib", "https://cdn.modrinth.com/data/LN9BxssP/versions/ZKor79dR/supermartijn642configlib-1.1.8-forge-mc1.20.jar"),
    ("fusion", "https://cdn.modrinth.com/data/p19vrgc2/versions/oA5jxU4i/fusion-1.1.1-forge-mc1.20.1.jar"),
    ("toughasnails", "https://cdn.modrinth.com/data/ge1sOdFH/versions/40SuKdWl/ToughAsNails-1.20.1-9.0.0.96.jar"),
    ("sereneSeasons", "https://cdn.modrinth.com/data/e0bNACJD/versions/gvqNV855/SereneSeasons-1.20.1-9.0.0.46.jar"),

    ("cfm", "mods/cfm.jar"),  # Exemple de mod local
    ("optifine", "mods/optifine.jar"),  # Exemple de mod local
]

# Function to load login information from login.ini
def load_login_info():
    login_info = {}
    if os.path.exists("config/login.ini"):
        config.read("config/login.ini")
        login_info['username'] = config['LOGIN'].get('username', '')
        login_info['uuid'] = config['LOGIN'].get('uuid', '')
        login_info['token'] = config['LOGIN'].get('token', '')
        login_info['remember'] = config['LOGIN'].getint('remember', 0)
    else:
        # Créer le fichier login.ini avec remember à 0 par défaut
        with open("config/login.ini", "w") as file:
            file.write("[LOGIN]\n")
            file.write("username = \n")
            file.write("uuid = \n")
            file.write("token = \n")
            file.write("remember = 0\n")
        # Charger les informations par défaut
        login_info['username'] = ''
        login_info['uuid'] = ''
        login_info['token'] = ''
        login_info['remember'] = 0
    return login_info

# Function to save login information to login.ini
def save_login_info(username, uuid, token, remember):
    config['LOGIN'] = {'username': username, 'uuid': uuid, 'token': token, 'remember': str(remember)}
    with open("config/login.ini", 'w') as configfile:
        config.write(configfile)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 200)  # Remplacez 400 et 200 par la largeur et la hauteur souhaitées
        self.setWindowTitle("Luancher MARLON 2000 :)")

        # Read existing login information if available
        self.login_info = load_login_info()

        if self.login_info['remember'] == 1:
            self.show_logout_button()
        else:
            self.show_login_button()

        from update import check_for_updates
        check_for_updates()

    def login(self):
        # Charger les données à partir du fichier config.ini
        config.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
        CLIENT_ID = config['IDS'].get('client_id', '')
        REDIRECT_URL = config['IDS'].get('redirect_url', '')
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
            config.read('Config/id.ini')  # Assurez-vous de fournir le bon chemin vers votre fichier config.ini
            CLIENT_ID = config['IDS'].get('client_id', '')
            REDIRECT_URL = config['IDS'].get('redirect_url', '')
            # Get the code from the url
            auth_code = Launcher.microsoft_account.parse_auth_code_url(url.toString(), self.state)
            # Do the login
            account_information = Launcher.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code, self.code_verifier)

            # Save the username, UUID, token, and remember in the config file
            save_login_info(account_information["name"], account_information["id"], account_information["access_token"], 1)
            self.web_view.close()
            self.show_logout_button()
        except AssertionError:
            print("States do not match!")
        except KeyError:
            print("Url not valid")

    def launch_minecraft(self):
        vanille_version = "1.20.1"
        login_info = load_login_info()
        options = {
            "username": login_info["username"],
            "uuid": login_info["uuid"],
            "token": login_info["token"],
            # Autres options
            "executablePath": "java", # The path to the java executable
            # "defaultExecutablePath": "java", # The path to the java executable if the version.json has none
            "jvmArguments": ["-Xmx8G", "-Xms8G"], #The jvmArguments
            "launcherName": "SpaziaCraft", # The name of your launcher
            "launcherVersion": "1.0.3", # The version of your launcher
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
        Launcher.forge.install_forge_version(forge_version, minecraft_directory, callback=callback)

        # Obtenez la commande de lancement de Minecraft
        minecraft_command = Launcher.command.get_minecraft_command(full_name_forge_version, minecraft_directory, options)
        
        from mod_manager import download_and_install_mods
        download_and_install_mods(MODS_TO_DOWNLOAD, minecraft_directory)
        # Lancez Minecraft en utilisant subprocess
        print("Lancement de Minecraft avec la commande :")
        print(minecraft_command)
        lancer = subprocess.Popen(minecraft_command, creationflags=subprocess.CREATE_NO_WINDOW)
        print(lancer)


    def logout(self):
        # Charger les informations de connexion
        login_info = load_login_info()
        # Effacer les informations de connexion sauf remember du fichier login.ini
        config.read("config/login.ini")
        if 'LOGIN' in config:
            config.remove_option('LOGIN', 'username')
            config.remove_option('LOGIN', 'uuid')
            config.remove_option('LOGIN', 'token')
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
        # Charger les informations de connexion depuis login.ini
        login_info = load_login_info()
        username = login_info['username']

        # Créer les boutons
        game_button = QPushButton(f"Lancer Minecraft")
        game_button.clicked.connect(self.launch_minecraft)

        logout_button = QPushButton(f"Logout ({username})")
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