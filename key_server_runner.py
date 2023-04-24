import utile.network as network
import utile.configgetter as config

# On initialise l'objet serveur avec les paramètres ip et port contenu dans le fichier config
# Pour éviter le hard-coding et des modifications plus aisée...
srv = network.server_tcp(config.get_ip("config.json"), config.get_port("config.json"), config.get_specific_data("config.json", "second_port_server"))
# On démarre le serveur
srv.start_server()