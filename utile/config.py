import json

JSON_FILENAME = '../serveur_cles/data/test.json'
dictionnaire = {"nom": "John", "age": 30, "ville": "Paris"}

def write_json(dictionnaire, JSON_FILENAME):
    """
    Écrit un dictionnaire encodé en JSON dans un fichier.
    """
    with open(JSON_FILENAME, "w") as f:
        json.dump(dictionnaire, f)

def read_json(JSON_FILENAME):
    """
    Lit un dictionnaire encodé en JSON depuis un fichier et le retourne.
    """
    with open(JSON_FILENAME, "r") as f:
        dictionnaire = json.load(f)
    return dictionnaire


# Écrire le dictionnaire dans le fichier
write_json(dictionnaire, JSON_FILENAME)

# Lire le dictionnaire depuis le fichier
dictionnaire_lu = read_json(JSON_FILENAME)

# Afficher le dictionnaire lu
print(dictionnaire_lu)