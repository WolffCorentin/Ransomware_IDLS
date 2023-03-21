# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : configgbetter
# Purpose : Stop hardcoding on server-setup, use json config

# --------------------------------------------
# Importations
# --------------------------------------------

import json

# --------------------------------------------
# Classes & Functions
# --------------------------------------------


def get_ip(path):
    """
    Fonctions pour récupérer des données en configuration
    (config en json)
    """
    # On ouvre la config en mode lecture
    with open(path, "r") as confile:
        # On récupère les data grâce à l'api json
        data = json.load(confile)
        # On ferme le fichier pour des questions de propreté
        # Et éviter de futures conflicts
        confile.close()

    # On renvoie la donnée server (l'ip)
    return data['server_ip']


def get_port(path):
    """
    Fonction pour récupérer des données en configuration
    (config en json)
    """
    # On ouvre la config en mode lecture
    with open(path, "r") as confile:
        # On récupère les data grâce à l'api json
        data = json.load(confile)
        # On ferme le fichier pour des questions de propreté
        # Et éviter de futures conflicts
        confile.close()
    # On renvoie la donnée port
    return data['port_server']


def get_specific_data(path, cdata):
    """
        Fonction pour récupérer des données en configuration
        (config en json)
        """
    # On ouvre la config en mode lecture
    with open(path, "r") as confile:
        # On récupère les data grâce à l'api json
        data = json.load(confile)
        # On ferme le fichier pour des questions de propreté
        # Et éviter de futures conflicts
        confile.close()
    # On renvoie la donnée port
    return data[cdata]


def set_specific_data_value(path, key, value):
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data[key] = value

    with open(path, "w+") as jFile:
        jFile.write(json.dumps(data))
    jFile.close()

