# --------------------------------------------

# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : message

# --------------------------------------------
# Importations
# --------------------------------------------
import json
# --------------------------------------------
# Functions
# --------------------------------------------


def list_victim_req():
    list_victim_req = {
        'LIST_REQ': None
    }
    ljson = json.dumps(list_victim_req)

    return ljson

def list_victim_resp(id, os, disks, state, nb_files):
    list_victim_resp = {
        'VICTIM': id,
        'OS': os,
        'DISKS': disks,
        'STATE': state,
        'NB_FILES': nb_files
    }
    ljson = json.dumps(list_victim_resp)

    return ljson

def list_victim_end():
    list_victim_end = {
        'LIST_END': None
    }
    ljson = json.dumps(list_victim_end)

    return ljson

def history_req(id):
    history_req = {
        'HIST_REQ': id
    }
    hqjson = json.dumps(history_req)

    return hqjson

def history_resp(id, timestamp, state, nb_files):
    history_resp = {
        'HIST_RESP': id,
        'TIMESTAMP': timestamp,
        'STATE': state,
        'NB_FILES': nb_files
    }
    hrjson = json.dumps(history_resp)

    return hrjson

def history_end(id):
    history_end = {
        'HIST_END': id
    }
    hejson = json.dumps(history_end)

    return hejson

def change_state(id, state):
    change_state = {
        'CHGSTATE': id,
        'STATE': state
    }
    csjson = json.dumps(change_state)

    return csjson

def close_connexion():
    close_connexion = {
        'CLOSE_TCP': None
    }
    ccjson = json.dumps(close_connexion)

    return ccjson

def initialize_req(hash, os, disks):
    initialize_req = {
        'INITIALIZE': hash,
        'OS': os,
        'DISKS': disks
    }
    irjson = json.dumps(initialize_req)

    return irjson

def initialize_key(id, key, state):
    initialize_key = {
        'KEY_RESP': id,
        'KEY': key,
        'STATE': state
    }
    ikjson = json.dumps(initialize_key)

    return ikjson

def initialize_resp(id, disks, paths, file_exit, freq, key, state):
    initialize_resp = {
        'CONFIGURE': id,
        'SETTING': {
            'DISKS': disks,
            'PATHS': paths,
            'FILE_EXIT': file_exit,
            'FREQ': freq,
            'KEY': key,
            'STATE': state
        }
    }
    irjson = json.dumps(initialize_resp)

    return irjson

