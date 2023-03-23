# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : security
# --------------------------------------------
# Importations
# --------------------------------------------
import random, os

from Cryptodome.Cipher import AES
# --------------------------------------------
# Classes
# --------------------------------------------
def create_key():
    key = os.urandom(16)
    return key

