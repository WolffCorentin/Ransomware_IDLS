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
from Cryptodome.Random import get_random_bytes
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


