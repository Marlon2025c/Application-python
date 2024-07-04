from cryptography.fernet import Fernet

# Générer une clé de chiffrement
key = Fernet.generate_key()
print(f'Clé de chiffrement : {key}')
with open("key.key", "wb") as key_file:
        key_file.write(key)
fernet = Fernet(key)

# Informations d'identification à crypter
client_id = "Client ID de Votre Azure"
url_redirect = "url_redirect de Votre Azure"
secret = "secret de Votre Azure"
# Afficher la clé de chiffrement et les informations d'identification cryptées
print(f'client_id : {fernet.encrypt(client_id.encode())}')
print(f'url_redirect : {fernet.encrypt(url_redirect.encode())}')
print(f'secret : {fernet.encrypt(secret.encode())}')