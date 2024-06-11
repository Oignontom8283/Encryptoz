import sys, os, bcrypt, sqlite3, datetime, logging
from enum import Enum
from PyQt5.QtWidgets import QLineEdit

__version__ = "1.0.0"

class Res(Enum):
    SaveIcon = "resources/save.png"

class Intercafe_File(Enum):
    main = "interface/main.ui"
    key_input = "interface/key_input.ui"

def resource_path(ressource_path: Res):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return absolute_path(ressource_path.value)

def absolute_path(relative_path:str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


def Set_LineInput_Password(object:QLineEdit, state:bool):
    """
    If @staet is True put the QlineEdit in Password mode otherwise put it in Normal mods
    """

    object.setEchoMode(QLineEdit.Password if state else QLineEdit.Normal)


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


class DataBase_DATA():
    def __init__(self, version, hint, hash, content) -> None:
        self._data = {
            "version": version,
            "hint": hint,
            "hash": hash,
            "content": content
        }

    # version
    @property
    def version(self):
        return self._data["version"]
    
    @version.setter
    def version(self, new_value):
        self._data["version"] = new_value

    # --- hint
    @property
    def hint(self):
        return self._data["hint"]
    
    @hint.setter
    def hint(self, new_value):
        self._data["hint"] = new_value

    # --- hash
    @property
    def hash(self):
        return self._data["hash"]
    
    @hash.setter
    def hash(self, new_value):
        self._data["hash"] = new_value

    # --- hash
    @property
    def content(self):
        return self._data["content"]
    
    @content.setter
    def content(self, new_value):
        self._data["content"] = new_value

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return self._data


class Database():
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


# Fonction pour créer une base de données chiffrée et insérer des données
def create_db(db_path) -> Database:
    # Connexion à la base de données (elle sera créée si elle n'existe pas)
    db = Database(db_path)

    # Création de la table et insertion de données
    db.cursor.execute('''CREATE TABLE eyz_data (
                        version TEXT,
                        hint TEXT,
                        hash TEXT,
                        content TEXT)''')
    
    db.cursor.execute("INSERT INTO eyz_data (version, hint, hash, content) VALUES (?, ?, ?, ?)", 
                   ("1.0", "example hint", "examplehash", "example content"))

    # Sauvegarde des changements et fermeture de la connexion
    db.conn.commit()
    return db

def connect_db(db_path) -> Database:
    return Database(db_path)

# Fonction pour récupérer des données de la base de données chiffrée
def fetch_data_from_db(db:Database):

    db.cursor.execute("SELECT version, hint, hash, content FROM eyz_data WHERE ROWID = 1")
    rows = db.cursor.fetchone()

    return rows

# Fonction pour modifier des données dans la base de données chiffrée
def update_db(db:Database, version, hint, hash, content):

    db.cursor.execute("UPDATE eyz_data SET version = ?, hint = ?, hash = ?, content = ? WHERE ROWID = ?", 
                      (version, hint, hash, content, "1"))

    db.conn.commit()

class console():

    LogFile = None
    log = None

    @classmethod
    def __init__(cls, LogFile:str=None) -> None:
        
        cls.LogFile = absolute_path( f'log/{ Get_UTC_time(format="%Y-%m-%d %H.%M.%S") } (UTC).log' ) if LogFile is None else LogFile
        
        DirPath = os.path.dirname(cls.LogFile)
        os.makedirs(DirPath, exist_ok=True)

        # Création d'un logger
        cls.log = logging.getLogger('logger')
        cls.log.setLevel(logging.DEBUG)

        # Création d'un gestionnaire de fichier
        file_handler = logging.FileHandler(cls.LogFile, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Création d'un gestionnaire de flux (console)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Création d'un formateur et ajout au gestionnaire de fichier
        formatter = logging.Formatter('[%(asctime)s - %(levelname)s] : %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Ajout des gestionnaires au logger
        cls.log.addHandler(file_handler)
        cls.log.addHandler(console_handler)

        # Utilisation du logger

        # self.logger.debug("Ceci est un message de débogage.")
        # self.logger.info("Ceci est un message d'information.")
        # self.logger.warning("Ceci est un message d'avertissement.")
        # self.logger.error("Ceci est un message d'erreur.")
        # self.logger.critical("Ceci est un message critique.")



def Get_UTC_time(TimeZone:datetime.timezone=datetime.timezone.utc, format:str="%Y-%m-%d %H:%M:%S"):
    # Obtenir l'heure actuelle au format UTC avec un objet timezone-aware
    heure_utc = datetime.datetime.now(TimeZone)

    return heure_utc.strftime(format)
