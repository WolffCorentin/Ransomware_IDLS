import socket
def test_server(host, port):
    msg = input(b"ClientA: Entrez un message ou STOP pour sortir:")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while msg != 'STOP':
        s.send(bytes(msg,'utf-8'))
        data = s.recv(2048)
        print("ClientA a reçu des données:", data)
        msg = input("Entrez un message pour continuer ou STOP pour sortir:")
    s.close()

test_server("localhost", 8380)