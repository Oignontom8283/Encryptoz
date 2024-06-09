
from crypting import *
from utility import hash_password

key = "bonjour789"

print(encrypt(
    "Obtenez un site Web plus léger et rapide en minifiant le code JS CSS !",
    key
))
print()
print(hash_password(key))