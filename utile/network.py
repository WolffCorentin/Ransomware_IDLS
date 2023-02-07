# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : network

# --------------------------------------------
# Importations
# --------------------------------------------
import socket
# --------------------------------------------
# Functions
# --------------------------------------------


def start_key_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        server.bind((host, port))
        server.listen(1)

        client, adressClient = server.accept()
        print(f'Connexion de {adressClient}')

        data = client.recv(1024)
        if not data:
            print(f'Erreur de réception')
        else:
            print(f'Reception de : {data}')

            response = data.upper()
            print(f'Envoi de {response}')
            n = client.send(response)
            if (n != len(response)):
                print("Erreur d'envoi")
            else:
                print(f'Envoi ok')

        print(f'Fermeture de la connexion avec le Client.')
        client.close()
        print(f'Arret dy serveur.')
    server.close()


def test_server(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))
    data = conn.recv(1024)
    print(f'Received {data}')



def check_packet_validity(header, message):
    """
    Protocole servant à contrôler la validité d'un packet en fonction de la taille de son header
    :param header: packet's header
    :type header: str
    :param message: packet's message
    :type message: str
    :return: True if packet is valid or False if not
    :rtype: bool
    """
    return message[9:9+header]
