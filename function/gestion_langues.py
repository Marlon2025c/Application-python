from import_perso import configparser, json

language_config = configparser.ConfigParser()
language_config.read('config/config.ini') 
default_language= language_config['DEFAULT'].get('langue', '')

class LanguageSystem:
    def __init__(self):
        self.default_language = default_language
        self.current_language = default_language  # Ajoutez cette ligne pour suivre la langue actuelle
        self.translations = {}
        # print(self.translate("label_configuration"))

    def load_translations(self, language):
        with open(f'translations/{language}.json', 'r', encoding='utf-8') as file:
            self.translations[language] = json.load(file)
            language_config_save = configparser.ConfigParser()
            language_config_save.read('config/config.ini')
            language_config_save['DEFAULT']['langue'] = language

            with open('config/config.ini', 'w') as configfile:
                language_config_save.write(configfile)

    def translate(self, text, language=None):
        if language is None:
            language = self.current_language
        if language not in self.translations:
            self.load_translations(language)
        if language in self.translations and text in self.translations[language]:
            return self.translations[language][text]
        return text

    def set_default_language(self, language):
        self.default_language = language

global language_system
language_system = LanguageSystem()
language_system.load_translations(default_language)