import json

def get_ip(path):
    with open(path, "r") as confile:
        data = json.load(confile)
        confile.close()

    return data['server']


def get_port(path):
    with open(path, "r") as confile:
        data = json.load(confile)
        confile.close()

    return data['port']