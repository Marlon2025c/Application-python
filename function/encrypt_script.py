from cryptography.fernet import Fernet

# Générer une clé de chiffrement
key = Fernet.generate_key()
print(f'Clé de chiffrement : {key}')
with open("key.key", "wb") as key_file:
        key_file.write(key)
fernet = Fernet(key)

# Informations d'identification à crypter
client_id = "4fa65ec1-aa5c-41b4-8714-4313b34f1cd6"
url_redirect = "https://login.microsoftonline.com/common/oauth2/nativeclient"
secret = "765641af-6b79-488b-b572-e846909a99a4"
# Afficher la clé de chiffrement et les informations d'identification cryptées
print(f'client_id : {fernet.encrypt(client_id.encode())}')
print(f'url_redirect : {fernet.encrypt(url_redirect.encode())}')
print(f'secret : {fernet.encrypt(secret.encode())}')