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
import binascii, os


# --------------------------------------------
# CLasses
# --------------------------------------------
class SecurityLayer(object):

    def __init__(self, text):
        self.cipher = None
        self.text = text
        self.nonce = ""
        self.authTag = ""
        self.key = os.urandom(32)
        print('Encryption key: ', binascii.hexlify(self.key))

    def encrypt(self):
        self.cipher = AES.new(self.key, AES.MODE_GCM)
        self.ciphertext, self.authTag = self.cipher.encrypt_and_digest(self.text)
        return self.ciphertext, self.cipher.nonce, self.authTag


    def decrypt(self):
        if self.cipher is not None:
            (ciphertext, self.nonce, self.authTag) = self.ciphertext
            aesCipher = AES.new(self.key, AES.MODE_GCM, self.nonce)
            plainText = aesCipher.decrypt_and_verify(ciphertext, self.authTag)
            return plainText
        else:
            return f"You need to encrypt before trying to decrypt"
# --------------------------------------------
# Functions
# --------------------------------------------
