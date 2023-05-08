from utile.network import server_tcp


class srv_frontale(server_tcp):
    def __init__(self, ip, port, port2):
        # herita
        super().__init__(ip, port, port2)

    #polymorphisme
    def gestion_msg(self, c, msg):
        # faire polymorphisme ici
        super().gestion_msg(c, msg)
