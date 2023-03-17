import json

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
    return data['server']


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
    return data['port']