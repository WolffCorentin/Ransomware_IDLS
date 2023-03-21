import json
import configgetter
import security
import binascii

JSON_FILENAME = configgetter.get_specific_data('../config.json', 'json_file_name')
dictionnaire = {"nom": "John", "age": 30, "ville": "Paris"}

def write_json(dictionnaire, JSON_FILENAME):
    """
    Écrit un dictionnaire encodé en JSON dans un fichier.
    """
    with open(JSON_FILENAME, "w") as f:
        dataset = json.dump(dictionnaire, f)
    f.close()

    return dataset


def add_json(dictionnaire, JSON_FILENAME):
    with open(JSON_FILENAME, "a") as f:
        dataset = json.dump(dictionnaire, f)
    f.close()

    return dataset


def read_json(JSON_FILENAME):
    """
    Lit un dictionnaire encodé en JSON depuis un fichier et le retourne.
    """
    with open(JSON_FILENAME, "r") as f:
        dataset = json.load(f)
    f.close()
    return dataset

"""
def chiffrer_fichier(JSON_FILENAME):
        
    dataset = read_json(JSON_FILENAME)
    sec = security.SecurityLayer()
    datasetciphered = sec.encrypt(dataset)
    datasetciphered = json.dumps(datasetciphered)
    write_json(datasetciphered)
    configgetter.set_specific_data_value(JSON_FILENAME, 'json_file_key', str(binascii.hexlify(sec.key)))
    return "Json file has been encrypted"


def dechiffrer_fichier(JSON_FILENAME):

    Déchiffrer un fichier
    
    key = configgetter.get_specific_data(JSON_FILENAME, 'json_file_key')
    dataset = read_json(JSON_FILENAME)
    decrypted = security.decrypt(dataset, key)
    return str(decrypted)


print(write_json(dictionnaire, JSON_FILENAME))
print(read_json(JSON_FILENAME))
chiffrer_fichier(JSON_FILENAME)
"""