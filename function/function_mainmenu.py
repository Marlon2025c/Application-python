from import_perso import QMainWindow, Qt, os, QtGui, QtWidgets, QPoint, zipfile, shutil, Launcher, configparser, requests, json, QtCore


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.resize(950, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.dragPosition = QPoint()  # Initialize dragPosition here

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragPosition = QPoint()
        event.accept()



global isFullScreen
isFullScreen = False

def toggleFullScreen(main_window, restore_window_button):
        global isFullScreen
        if not isFullScreen:
            # Passez en mode plein écran
            main_window.showFullScreen()
            isFullScreen = True
            # Changez l'icône du bouton pour refléter le mode plein écran
            icon9 = QtGui.QIcon()
            icon9.addPixmap(QtGui.QPixmap("asset/fantome.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            restore_window_button.setIcon(icon9)
        else:
            # Quittez le mode plein écran
            main_window.showNormal()
            isFullScreen = False
            # Changez l'icône du bouton pour refléter le mode fenêtré
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("asset/augmenter-loption-de-taille.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            restore_window_button.setIcon(icon8)

global lateral_parametressetVisible
lateral_parametressetVisible = False

def toggleSetVisible(label_configuration, lateral_parametres, stackedWidget, home_btn_1):
        global lateral_parametressetVisible
        if not lateral_parametressetVisible:
            label_configuration.setVisible(True)
            lateral_parametressetVisible = True
            lateral_parametres.setVisible(True)
            stackedWidget.setCurrentIndex(1)
        else:
            if stackedWidget.currentIndex() >= 1:  # Si la page actuelle est la page des paramètres
                home_btn_1.setChecked(True)  # Cocher le bouton Home
                stackedWidget.setCurrentIndex(0)
            label_configuration.setVisible(False)
            lateral_parametressetVisible = False
            lateral_parametres.setVisible(False)

def on_home_btn_1_toggled(stackedWidget, lateral_parametres, label_configuration):
        global lateral_parametressetVisible
        stackedWidget.setCurrentIndex(0)
        print(stackedWidget)
        # Vérifiez si la barre latérale des paramètres est visible
        if lateral_parametres.isVisible():
            # Cachez la barre latérale des paramètres lorsque vous revenez à la page d'accueil
            label_configuration.setVisible(False)
            lateral_parametressetVisible = False
            lateral_parametres.setVisible(False)

def on_parametres_btn_toggled(stackedWidget):
        stackedWidget.setCurrentIndex(1)

def on_skins_btn_toggled(stackedWidget):
        stackedWidget.setCurrentIndex(2)    

def on_packsderesources_btn_toggled(stackedWidget):
        stackedWidget.setCurrentIndex(3)

def on_packsdeshaders_btn_toggled(stackedWidget):    
        stackedWidget.setCurrentIndex(4)

def on_console_btn_toggled(stackedWidget):    
        stackedWidget.setCurrentIndex(5)

def on_capturedecran_btn_toggled(stackedWidget):    
        stackedWidget.setCurrentIndex(6)  

def on_rapportsdecrash_btn_toggled(stackedWidget):    
        stackedWidget.setCurrentIndex(7)

def on_mod_additionnel_btn_toggled(stackedWidget):    
        stackedWidget.setCurrentIndex(8)



    # -------------------------------------------------------------------------------- #
    #                           EASTER EGGS DU LOGICIEL                                #
    # -------------------------------------------------------------------------------- #


global click_count
click_count = 0
def on_easter_eggs_maomao(event, logo_label_1):
    global click_count
    # Vérifier si le clic est un clic gauche de la souris
    if event.button() == Qt.MouseButton.LeftButton:
        click_count += 1
        # Vérifier si le nombre de clics atteint 10
        if click_count == 10:
            # Changer l'icône du label après 10 clics
            logo_label_1.setPixmap(QtGui.QPixmap("asset/MaoMao.jpg"))
            click_count = 0  # Réinitialiser le compteur après avoir changé l'icône


    # -------------------------------------------------------------------------------- #
    #                   SYSTEM DE GESTION DE LA RESOURCEPACKS                          #
    # -------------------------------------------------------------------------------- #


class DrangandDropButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) > 0:
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.endswith(('.zip', '.rar')):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        self.setStyleSheet('''
                    QWidget{
                        background-color: lightblue;
                        border: 2px dashed green;
                    }
                ''')
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.endswith(('.zip', '.rar')):
                event.setDropAction(Qt.DropAction.CopyAction)
                process_zip(self, file_path)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
    def dragLeaveEvent(self, event):
        self.setStyleSheet('''
            QWidget{
                background-color: white;
            }
        ''')


global minecraft_directory
minecraft_directory = Launcher.utils.get_minecraft_directory().replace('minecraft','spaziacraft')

def process_zip(self, file_path):

    # Join the "packs" directory to the current directory
    destination_dir = os.path.join(minecraft_directory, "resourcepacks")

    # Extract pack.mcmeta if exists
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for f in zip_ref.namelist():
            if os.path.basename(f) == 'pack.mcmeta':
                # Copy the file to the destination directory
                shutil.copy2(file_path, destination_dir)
                from vue.mains_menu import refresh_file_lists
                refresh_file_lists(minecraft_directory)
                break
            else:
                # If pack.mcmeta doesn't exist, don't copy the file
                print("No pack.mcmeta found in the zip file.")

    # Reset the style sheet to remove the blue background
    self.setStyleSheet('''
        page_btn_deposer_pack{
        background-color: white;
        }
    ''')
global pack_widgets
pack_widgets = {}

def create_widget_with_label(filename, scrollAreaWidgetContents_2, verticalLayout_9):
    global pack_widgets
     # Créez le widget
    widget_2 = QtWidgets.QWidget(parent=scrollAreaWidgetContents_2)
    widget_2.setMaximumSize(QtCore.QSize(16777215, 30))
    widget_2.setObjectName("widget_2")
    gridLayout_11 = QtWidgets.QGridLayout(widget_2)
    gridLayout_11.setContentsMargins(0, 0, 0, 0)
    gridLayout_11.setSpacing(0)
    gridLayout_11.setObjectName("gridLayout_11")
    # Créez le bouton de suppression
    page_btn_sup_pack = QtWidgets.QPushButton(parent=widget_2)
    page_btn_sup_pack.setMaximumSize(QtCore.QSize(40, 20))
    page_btn_sup_pack.setObjectName("page_btn_sup_pack")
    icon80 = QtGui.QIcon()
    icon80.addPixmap(QtGui.QPixmap("asset/poubelle"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    page_btn_sup_pack.setIcon(icon80)
    # Change le curseur quand la souris entre sur le bouton
    page_btn_sup_pack.enterEvent = lambda event: page_btn_sup_pack.setCursor(Qt.CursorShape.PointingHandCursor)
    # Restaure le curseur par défaut quand la souris quitte le bouton
    page_btn_sup_pack.leaveEvent = lambda event: page_btn_sup_pack.setCursor(Qt.CursorShape.ArrowCursor)
    # Connectez le signal clicked du bouton à la fonction de suppression avec le nom du fichier en argument
    page_btn_sup_pack.clicked.connect(lambda _, filename=filename: delete_pack(filename))

    gridLayout_11.addWidget(page_btn_sup_pack, 0, 2, 1, 1)
    verticalLayout_12 = QtWidgets.QVBoxLayout()
    verticalLayout_12.setSpacing(0)
    verticalLayout_12.setObjectName("verticalLayout_12")
    page_label_name_pack = QtWidgets.QLabel(filename, parent=widget_2)
    page_label_name_pack.setObjectName("page_label_name_pack")
    verticalLayout_12.addWidget(page_label_name_pack)
    label_2 = QtWidgets.QLabel(parent=widget_2)
    label_2.setObjectName("label_2")
    verticalLayout_12.addWidget(label_2)
    gridLayout_11.addLayout(verticalLayout_12, 0, 1, 1, 1)
    verticalLayout_9.addWidget(widget_2)

    # Ajoutez le widget au dictionnaire avec le nom du pack comme clé
    pack_widgets[filename] = widget_2

def delete_pack(filename):
        destination_dir = os.path.join(minecraft_directory, "resourcepacks")
        file_path = os.path.join(destination_dir, f"{filename}.zip")  # Ajoutez l'extension du fichier
        try:
            os.remove(file_path)
            print(f"Pack '{filename}' supprimé avec succès.")
            global new_filenames
            new_filenames = set()
            
            # Supprimez le widget associé à ce pack
            widget = pack_widgets.get(filename)
            if widget:
                widget.deleteLater()
                del pack_widgets[filename]
                from vue.mains_menu import refresh_file_lists
                refresh_file_lists(minecraft_directory)
                
        except FileNotFoundError:
            print(f"Le pack '{filename}' n'existe pas.")

    # -------------------------------------------------------------------------------- #
    #                    SYSTEM DE GESTION DE LA SHADERS                               #
    # -------------------------------------------------------------------------------- #

class DrangandDropButtonShader(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) > 0:
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.endswith(('.zip', '.rar')):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        self.setStyleSheet('''
                    QWidget{
                        background-color: lightblue;
                        border: 2px dashed green;
                    }
                ''')
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.endswith(('.zip', '.rar')):
                event.setDropAction(Qt.DropAction.CopyAction)
                process_zip_shader(self, file_path)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
    def dragLeaveEvent(self, event):
        self.setStyleSheet('''
            QWidget{
                background-color: white;
            }
        ''')

def process_zip_shader(self, file_path):
    # Join the "packs" directory to the current directory
    destination_dir = os.path.join(minecraft_directory, "shaderpacks")

    # Vérifiez s'il y a au moins un dossier dans le fichier zip
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_contents = zip_ref.infolist()
        for member in zip_contents:
            if member.is_dir():
                # Si un dossier est trouvé, vous pouvez faire ce que vous avez besoin de faire
                # Par exemple, vous pouvez copier le fichier zip vers un autre répertoire
                shutil.copy2(file_path, destination_dir)
                print("Un dossier est présent dans le fichier zip.")
                break
        else:
            # Si aucun dossier n'est trouvé, vous pouvez faire ce que vous voulez en conséquence
            print("Aucun dossier n'est présent dans le fichier zip.")
    
    # Actualisez les listes de fichiers après avoir traité le zip
    from vue.mains_menu import refresh_file_lists
    refresh_file_lists(minecraft_directory)

    # Réinitialisez la feuille de style pour supprimer l'arrière-plan bleu
    self.setStyleSheet('''
        page_btn_deposer_pack{
        background-color: white;
        }
    ''')

global pack_shaders_widgets
pack_shaders_widgets = {}

def create_widget_with_label_shader(filename, scrollAreaWidgetContents_3, verticalLayout_11):

    global pack_shaders_widgets

    widget_3 = QtWidgets.QWidget(parent=scrollAreaWidgetContents_3)
    widget_3.setMaximumSize(QtCore.QSize(16777215, 30))
    widget_3.setObjectName("widget_3")

    gridLayout_12 = QtWidgets.QGridLayout(widget_3)
    gridLayout_12.setContentsMargins(0, 0, 0, 0)
    gridLayout_12.setSpacing(0)
    gridLayout_12.setObjectName("gridLayout_12")


    # Créez le bouton de suppression
    page_btn_sup_shagers = QtWidgets.QPushButton(parent=widget_3)
    page_btn_sup_shagers.setMaximumSize(QtCore.QSize(40, 20))
    page_btn_sup_shagers.setObjectName("page_btn_sup_pack")
    icon804 = QtGui.QIcon()
    icon804.addPixmap(QtGui.QPixmap("asset/poubelle"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    page_btn_sup_shagers.setIcon(icon804)
    # Change le curseur quand la souris entre sur le bouton
    page_btn_sup_shagers.enterEvent = lambda event: page_btn_sup_shagers.setCursor(Qt.CursorShape.PointingHandCursor)
    # Restaure le curseur par défaut quand la souris quitte le bouton
    page_btn_sup_shagers.leaveEvent = lambda event: page_btn_sup_shagers.setCursor(Qt.CursorShape.ArrowCursor)
    # Connectez le signal clicked du bouton à la fonction de suppression avec le nom du fichier en argument
    page_btn_sup_shagers.clicked.connect(lambda _, filename=filename: delete_pack_shaders(filename))

    gridLayout_12.addWidget(page_btn_sup_shagers, 0, 2, 1, 1)
    verticalLayout_15 = QtWidgets.QVBoxLayout()
    verticalLayout_15.setSpacing(0)
    verticalLayout_15.setObjectName("verticalLayout_15")
    page_label_name_pack_shaders = QtWidgets.QLabel(filename, parent=widget_3)
    page_label_name_pack_shaders.setObjectName("page_label_name_pack_shaders")
    verticalLayout_15.addWidget(page_label_name_pack_shaders)
    label_5 = QtWidgets.QLabel(parent=widget_3)
    label_5.setObjectName("label_2")
    verticalLayout_15.addWidget(label_5)
    gridLayout_12.addLayout(verticalLayout_15, 0, 1, 1, 1)
    verticalLayout_11.addWidget(widget_3)

    # Ajoutez le widget au dictionnaire avec le nom du pack comme clé
    pack_shaders_widgets[filename] = widget_3

def delete_pack_shaders(filename):
        destination_dir = os.path.join(minecraft_directory, "shaderpacks")
        file_path = os.path.join(destination_dir, f"{filename}.zip")  # Ajoutez l'extension du fichier
        try:
            os.remove(file_path)
            print(f"Pack '{filename}' supprimé avec succès.")
            global new_filenames
            new_filenames = set()
            
            # Supprimez le widget associé à ce pack
            widget = pack_widgets.get(filename)
            if widget:
                widget.deleteLater()
                del pack_widgets[filename]
                from vue.mains_menu import refresh_file_lists
                refresh_file_lists(minecraft_directory)
                
        except FileNotFoundError:
            print(f"Le pack '{filename}' n'existe pas.")


def read_initial_slider_value():
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        if 'Launcher' in config and 'jvmArguments' in config['Launcher']:
            jvm_arguments = config['Launcher']['jvmArguments']
            # Extraire la valeur de -Xmx et -Xms de jvmArguments
            max_memory_value = jvm_arguments.split('-Xmx')[1].split('G')[0]
            return int(max_memory_value)  # Convertir la valeur en entier


    # -------------------------------------------------------------------------------- #
    #                    SYSTEM DE GESTION DE LA RAM                                   #
    # -------------------------------------------------------------------------------- #


def save_slider_value(horizontalSlider):
        value = horizontalSlider.value()  # Obtenir la valeur actuelle du slider
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        # Mettez à jour la valeur de 'jvmArguments'
        config['Launcher']['jvmArguments'] = f'["-Xmx{value}G", "-Xms{value}G"]'
        
        # Enregistrez les modifications dans le fichier
        with open('config/config.ini', 'w') as configfile:
            config.write(configfile)
            
        # Connectez la fonction d'enregistrement au signal valueChanged du slider
def handle_slider_moved(value, horizontalSlider):
    # Arrondir la valeur du curseur à la valeur paire la plus proche
        new_value = value if value % 2 == 0 else value + 1
        horizontalSlider.setValue(new_value)  # Définir la nouvelle valeur du curseur


    # -------------------------------------------------------------------------------- #
    #                   SYSTEM DE GESTION DE LA MODS ADD                               #
    # -------------------------------------------------------------------------------- #

# Dictionnaire pour stocker les QCheckBox pour chaque mod
mod_checkboxes = {}
# URL du fichier JSON hébergé sur GitHub
json_url = 'https://raw.githubusercontent.com/Marlon2025c/Application-python/master/mods/liste_mods.json'
states_file = 'config/mod_states.json'
# Fonction pour lire les mods depuis une URL
def load_mods_from_url():
    response = requests.get(json_url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    return response.json()
# Fonction pour charger les états depuis un fichier JSON
def load_mod_states():
    if os.path.exists(states_file):
        with open(states_file, 'r') as f:
            return json.load(f)
    return {}
# Fonction pour sauvegarder l'état des QCheckBox dans un fichier JSON
def save_mod_states():
    mod_states = {mod_name: checkBox.isChecked() for mod_name, checkBox in mod_checkboxes.items()}
    with open(states_file, 'w') as f:
        json.dump(mod_states, f, indent=4)
        print("Mod states saved:", mod_states)  # Debug print to confirm save