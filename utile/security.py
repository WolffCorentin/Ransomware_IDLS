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
import binascii, os, random


# --------------------------------------------
# CLasses
# --------------------------------------------
class SecurityLayer(object):

    def __init__(self):
        self.cipher = None
        self.text = ""
        self.nonce = self.gen_nonce()
        self.authTag = ""
        self.key = self.gen_key()
        print('Encryption key: ', binascii.hexlify(self.key))

    def gen_key(self):
        return os.urandom(32)

    def gen_nonce(self):
        return random.randint(1, 100)

    def encrypt(self, text):
        self.text = text
        self.cipher = AES.new(self.key, AES.MODE_GCM)
        self.ciphertext, self.authTag = self.cipher.encrypt_and_digest(bytes(text, 'utf-8'))
        return (self.ciphertext, self.authTag, self.cipher.nonce)

    def decrypt(self, ciphertext):
        if self.cipher is not None:
            (ciphertext, authTag, nonce) = ciphertext
            aesCipher = AES.new(self.key, AES.MODE_GCM, nonce)
            plainText = aesCipher.decrypt_and_verify(ciphertext, authTag)
            return plainText
        else:
            return f"You need to encrypt before trying to decrypt"

# --------------------------------------------
# Functions
# --------------------------------------------
