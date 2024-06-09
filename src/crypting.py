import hashlib, random, string

def generate_substitution_table(key):
    # Crée une seed à partir de la clé pour assurer la reproductibilité
    seed = int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16)
    random.seed(seed)
    
    # Alphabet et chiffres
    characters = string.ascii_letters + string.digits
    
    # Mélange les caractères pour créer la table de substitution
    shuffled_characters = list(characters)
    random.shuffle(shuffled_characters)
    
    # Crée une table de substitution sous forme de dictionnaire
    substitution_table = {original: shuffled for original, shuffled in zip(characters, shuffled_characters)}
    
    return substitution_table

def add_random_padding(text, target_length):
    # Ajoute des caractères aléatoires pour atteindre la longueur cible
    if len(text) >= target_length:
        return text
    
    padding_length = target_length - len(text)
    padding = ''.join(random.choices(string.ascii_letters + string.digits, k=padding_length))
    
    return text + padding

def encrypt(text, key):
    substitution_table = generate_substitution_table(key)
    
    # Détermine une longueur cible aléatoire plus grande que le texte original
    target_length = len(text) + random.randint(5, 10)
    
    # Ajoute des caractères aléatoires pour atteindre la longueur cible
    padded_text = add_random_padding(text, target_length)
    
    # Chiffre le texte en utilisant la table de substitution
    encrypted_text = ''.join(substitution_table.get(char, char) for char in padded_text)
    
    return encrypted_text

def decrypt(encrypted_text, key):
    substitution_table = generate_substitution_table(key)
    
    # Inverse la table de substitution pour le déchiffrement
    inverse_substitution_table = {v: k for k, v in substitution_table.items()}
    
    # Déchiffre le texte en utilisant la table de substitution inversée
    decrypted_text = ''.join(inverse_substitution_table.get(char, char) for char in encrypted_text)
    
    # Retire les caractères de padding (non présent dans l'original)
    original_length = len(decrypted_text.rstrip(string.ascii_letters + string.digits))
    decrypted_text = decrypted_text[:original_length]
    
    return decrypted_text