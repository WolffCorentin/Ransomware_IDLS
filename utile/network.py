# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : network

# --------------------------------------------
# Importations
# --------------------------------------------
import utile.security as security
import pickle
# --------------------------------------------
# Classes & Functions
# --------------------------------------------


def send_msg_clear(c, message, HEADERSIZE=10):
    """
    Créer un header pour la connexion TCP afin de savoir de où à où lire
    """
    serialized_payload = pickle.dumps(message)
    c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
    c.sendall(serialized_payload)


def recv_msg_clear(c, HEADERSIZE=10):
    data_size = c.recv(HEADERSIZE)
    if not data_size:
        return None
    data_size = int(float(data_size))
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += c.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return payload


def send_msg(c, msg, secKey, HEADERSIZE=10):
    r = security.crypt(msg, secKey)
    serialized_payload = pickle.dumps(r)
    c.sendall(bytes(f"{len(serialized_payload):<{HEADERSIZE}}", 'utf-8'))
    c.sendall(serialized_payload)


def recv_msg(c, secKey, HEADERSIZE=10):
    data_size = c.recv(HEADERSIZE)
    if not data_size:
        return None
    data_size = int(float(data_size))
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += c.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    payload = security.decrypt(payload, secKey)
    return payload

