# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : main

# --------------------------------------------
import socket
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
    s.connect(("localhost", 8382))
    choix = "19"
    while choix != '4':
        choix = input('Votre choix : ')
        if choix == '1':
            s.send(bytes("1", 'utf-8'))
            data = s.recv(2048).decode()
            print('Réception de données de la part du serveur : ' + str(data))
        elif choix == '2':
            s.send(bytes("2", 'utf-8'))
            data = s.recv(2048).decode()
            print('Réception de données de la part du serveur : ' + str(data))
            id = input('Merci de préciser un ID pour consulter l''historique : ')
            s.send(bytes(id, 'utf-8'))
            data_h = s.recv(2048).decode()
            print('Réception de données de la part du serveur : ' + str(data_h))
        elif choix == '3':
            print(fill_payload())
        elif choix == '4':
            print('Bonne journée')
            s.close()
            break


def listing():
    """ Send msg to TCP server which will interpret IT and give a feed-back"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8382))
    s.send(bytes("1", 'utf-8'))
    data = s.recv(2048).decode()
    s.close()
    print('Réception de données de la part du serveur : ' + str(data))



def history():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8382))
    s.send(bytes("2", 'utf-8'))
    data = s.recv(2048).decode()
    print('Réception de données de la part du serveur : ' + str(data))
    id = input('Merci de préciser un ID pour consulter l''historique : ')
    s.send(bytes(id, 'utf-8'))
    data_h = s.recv(2048).decode()
    print('Réception de données de la part du serveur : ' + str(data_h))
    s.close()


def fill_payload():
    return 'Todo payload'


def quit():
    return 'Bonne journée'


if __name__ == '__main__':
    main()
