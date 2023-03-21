import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key(salt):
    """
    génère une clef de chiffrement AES de 256 bits en utilisant "os.urandom()" pour générer 32 octets aléatoires.
    :param salt: le salt
    :type salt: str
    :return: un clef de 32 chiffrement
    """
    key = os.urandom(32)
    salt_key = hashlib.pbkdf2_hmac('sha256', key, salt.encode('utf-8'), 20000)
    return salt_key

def encrypt(key, plaintext, salt):
    """
    Chiffre le texte en clair en utilisant la clef de chiffrement et le chiffrement AES-GCM.
    Il génère également un nonce de 12 octets et renvoie le texte chiffré, le nonce et le tag associé.
    :param key: la clef à utiliser
    :type key: byte
    :param plaintext: le texte en clair à chiffrer
    :type plaintext: str
    :param salt: le salt
    :type salt: str
    :return: un tuple contenant le texte chiffré, le nonce et le tag généré lors du chiffrement.
    :rtype: tuple
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)          #Un nonce est un nombre qui n'est utilisable qu'une seule fois.
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    tag = aesgcm.tag
    return ciphertext, nonce, tag

def decrypt(key, ciphertext, nonce, tag, salt):
    """
    Déchiffre le texte chiffré en utilisant la clef de chiffrement et le chiffrement AES-GCM
    en utilisant le nonce et le tag associé.
    :param key: la clef de chiffrement
    :type key:
    :param ciphertext: le texte à déchiffrer
    :type ciphertext:
    :param nonce: un nonce (donc un chiffre à usage unique)
    :type nonce:
    :param tag: un tag généré lors du chiffrement
    :type tag:
    :param salt: le salt
    :type salt: str
    :return: le texte déchiffrer.
    :rtype: str
    """
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, tag)
    return plaintext.decode('utf-8')