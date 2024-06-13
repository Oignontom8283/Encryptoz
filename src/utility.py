import sys, os, bcrypt, sqlite3, datetime, logging, datetime, configparser
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

    __version__ = "1.0.0"

    LogFile = None
    loggin = None

    @classmethod
    def __init__(cls, LogsDirectory:str, LogFile:str=None) -> None:
        
        cls.LogFile = absolute_path( f'{LogsDirectory}/{ Get_UTC_time(format="%Y-%m-%d %H.%M.%S") } (UTC).log' ) if LogFile is None else LogFile
        
        DirPath = os.path.dirname(cls.LogFile)
        os.makedirs(DirPath, exist_ok=True)

        # Création d'un logger
        cls.loggin = logging.getLogger('logger')
        cls.loggin.setLevel(logging.DEBUG)

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
        cls.loggin.addHandler(file_handler)
        cls.loggin.addHandler(console_handler)

        # Utilisation du logger

        # self.logger.debug("Ceci est un message de débogage.")
        # self.logger.info("Ceci est un message d'information.")
        # self.logger.warning("Ceci est un message d'avertissement.")
        # self.logger.error("Ceci est un message d'erreur.")
        # self.logger.critical("Ceci est un message critique.")

    @classmethod
    def _convert_memory(cls, memory_str:str):
        """Convert memory size from string to bytes."""
        unit = memory_str.strip() [-2:] .lower()
        size = int( memory_str[:-2] .strip() )
        if unit == 'ko':
            return size * 1024
        elif unit == 'mo':
            return size * 1024 * 1024
        elif unit == 'go':
            return size * 1024 * 1024 * 1024
        else:
            raise ValueError("Unsupported memory unit. Use 'Ko', 'Mo', or 'Go'.")

    @classmethod
    def _convert_time(cls, time_str:str):
        """Convert time duration from string to seconds."""
        unit = time_str.strip() [-1] .lower()
        value = int( time_str[:-1] .strip() )
        if unit == 's':
            return datetime.timedelta(seconds=value)
        elif unit == 'm':
            return datetime.timedelta(minutes=value)
        elif unit == 'h':
            return datetime.timedelta(hours=value)
        elif unit == 'd':
            return datetime.timedelta(days=value)
        else:
            raise ValueError("Unsupported time unit. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'D' for days.")

    @classmethod
    def delete_old_logs(cls, directory, max_memory, max_age):
        # Convert max_memory from string to bytes
        max_memory_bytes = cls._convert_memory(max_memory)
        # Convert max_age from string to timedelta
        max_age_timedelta = cls._convert_time(max_age)
        # Calculate the cutoff time
        cutoff_time = datetime.now() - max_age_timedelta

        total_size = 0
        log_files = []

        # Gather all .log files and calculate the total size
        for filename in os.listdir(directory):
            if filename.endswith('.log'):
                filepath = os.path.join(directory, filename)
                file_stats = os.stat(filepath)
                file_size = file_stats.st_size
                file_mtime = datetime.fromtimestamp(file_stats.st_mtime)

                total_size += file_size
                log_files.append((filepath, file_size, file_mtime))

        # Check if the total size exceeds the maximum allowed size
        if total_size > max_memory_bytes:
            # Sort files by modification time (oldest first)
            log_files.sort(key=lambda x: x[2])
            for filepath, file_size, file_mtime in log_files:
                # Check if the file is older than the cutoff time
                if file_mtime < cutoff_time:
                    os.remove(filepath)
                    total_size -= file_size
                    print(f"Deleted {filepath}")
                    # Stop deleting if the total size is under the limit
                    if total_size <= max_memory_bytes:
                        break

    @classmethod
    def log(cls, message, **args):
        cls.loggin.debug(message, **args)

    @classmethod
    def debug(cls, message, **args):
        cls.loggin.debug(message, **args)

    @classmethod
    def info(cls, message, **args):
        cls.loggin.info(message, **args)

    @classmethod
    def warning(cls, message, **args):
        cls.loggin.warning(message, **args)

    @classmethod
    def error(cls, message, **args):
        cls.loggin.error(message, **args)

    @classmethod
    def critical(cls, message, **args):
        cls.loggin.critical(message, **args)



class Config():

    _config:configparser.ConfigParser

    @classmethod
    def __init__(cls, config_file:str) -> None:
        cls.confi_file = absolute_path(config_file)

        cls._config = configparser.ConfigParser()
        cls._config.read(cls.confi_file)

    @classmethod
    def get(cls, section, option, fallback=None):
        return cls._config.get(section, option, fallback=fallback)
    
    @classmethod
    def getint(cls, section, option, fallback=None):
        return cls._config.getint(section, option, fallback=fallback)
    
    @classmethod
    def getfloat(cls, section, option, fallback=None):
        return cls._config.getfloat(section, option, fallback=fallback)
    
    @classmethod
    def getboolean(cls, section, option, fallback=None):
        return cls._config.getboolean(section, option, fallback=fallback)

def Get_UTC_time(TimeZone:datetime.timezone=datetime.timezone.utc, format:str="%Y-%m-%d %H:%M:%S"):
    # Obtenir l'heure actuelle au format UTC avec un objet timezone-aware
    heure_utc = datetime.datetime.now(TimeZone)

    return heure_utc.strftime(format)
