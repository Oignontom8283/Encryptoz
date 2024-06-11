# import logging

# # Création d'un logger
# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.DEBUG)

# # Création d'un gestionnaire de fichier
# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.DEBUG)

# # Création d'un gestionnaire de flux (console)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# # Création d'un formateur et ajout au gestionnaire de fichier
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# # Ajout des gestionnaires au logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# # Utilisation du logger
# logger.debug("Ceci est un message de débogage.")
# logger.info("Ceci est un message d'information.")
# logger.warning("Ceci est un message d'avertissement.")
# logger.error("Ceci est un message d'erreur.")
# logger.critical("Ceci est un message critique.")

# from datetime import datetime, timezone

# # Obtenir l'heure actuelle au format UTC avec un objet timezone-aware
# heure_utc = datetime.now(timezone.utc)

# # Formater l'heure UTC
# heure_formatee = heure_utc.strftime("%Y-%m-%d %H:%M:%S")

# # Afficher l'heure formatée
# print("Heure UTC formatée:", heure_formatee)

from utility import console

console = console()

console.log.debug("Ceci est un message de débogage.")
console.log.info("Ceci est un message d'information.")
console.log.warning("Ceci est un message d'avertissement.")
console.log.error("Ceci est un message d'erreur.")
console.log.critical("Ceci est un message critique.")
