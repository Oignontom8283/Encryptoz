import sys, os, bcrypt
from enum import Enum

class Res(Enum):
    SaveIcon = "resources/save.png"

class Intercafe_File(Enum):
    main = "interface/main.ui"
    key_input = "interface/key_input.ui"

def resource_path(relative_path: Res):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path.value)

def Decryption(data, key):
    pass

def hash_password(password: str) -> str:
    # Convertir le mot de passe en bytes
    password_bytes = password.encode('utf-8')
    # Générer un salt et hacher le mot de passe
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Retourner le mot de passe haché sous forme de chaîne de caractères
    return hashed_password.decode('utf-8')

# Fonction pour vérifier un mot de passe haché
def check_password(password: str, hashed_password: str) -> bool:
    try:
        # Convertir les deux mots de passe en bytes
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        # Vérifier si le mot de passe correspond au hachage
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except:
        return False