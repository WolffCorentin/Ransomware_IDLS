import json
import utile.configgetter as configgetter
import utile.security as security
import pickle

JSON_FILENAME = configgetter.get_specific_data('config.json', 'json_file_name')
dictionnaire = {"nom": "John", "age": 30, "ville": "Paris"}

global config


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
    with open(JSON_FILENAME, "rb") as f:
        dataset = json.load(f)
    f.close()
    return dataset


def crypt_file(key, FILE_NAME, FILENAMEKEY):
    sk = save_key(key, FILENAMEKEY)
    print(sk)
    with open(FILE_NAME, "rb") as f:
        dataset = f.read()
    f.close()
    encrypted = security.crypt(dataset, key)
    with open(FILE_NAME, "wb") as fw:
        fw.write(pickle.dumps(encrypted))
    fw.close()
    return "File encrypted"


def decrypt_file(KEYFILE, FILENAME):
    key = get_key(KEYFILE)
    with open(FILENAME, "rb") as f:
        dataset = f.read()
    f.close()
    dataset = pickle.loads(dataset)
    decrypted = security.decrypt(dataset, key)
    jdecrypt = json.loads(decrypted)
    with open(FILENAME, "wb") as fw:
        fw.write(decrypted)
    fw.close()
    return "File decrypted"


def save_key(key, FILE_NAME):
    with open(FILE_NAME, "wb") as fw:
        fw.write(key)
    fw.close()
    return f"Key has been stored in file {str(FILE_NAME)}"


def get_key(FILENAMEKEY):
    with open(FILENAMEKEY, "rb") as f:
        dataset = f.read()
    f.close()
    return dataset


def load_config(config_path, key_path):
    global config
    with open(key_path, 'rb') as f:
        key = f.read()
    with open(config_path, 'rb') as cf:
         config_content = cf.read()
    data = pickle.loads(config_content)
    data = security.decrypt(data, key)
    config = json.loads(data)
    return config


def get_data_config(data):
    global config
    if config[data] is not None:
        return config[data]
    else:
        return None

