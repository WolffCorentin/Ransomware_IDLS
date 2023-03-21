# --------------------------------------------
import random

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : security

# --------------------------------------------
# Importations
# --------------------------------------------
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import binascii, os


# --------------------------------------------
# Classes
# --------------------------------------------
class SecurityLayer(object):

    def __init__(self):
        self.cipher = None
        self.key = self.gen_key()
        self.cipher = AES.new(self.key, AES.MODE_GCM)

    def gen_key(self):
        return get_random_bytes(16)

    def encrypt(self, text):
        self.text = text
        self.ciphertext = self.cipher.encrypt(text)
        return self.ciphertext

    def showValues(self):
        return self.key


# --------------------------------------------
# Functions
# --------------------------------------------

def decrypt(ciphertexta, key):
    #(ciphertext, authTag, nonce) = ciphertexta
    encobj = AES.new(key, AES.MODE_GCM)
    return encobj.decrypt(ciphertexta)
