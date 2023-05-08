import utile.configgetter as configg
import serveur_frontale.serveur_frontal as front_s

s = front_s.serveur_frontal(configg.get_specific_data("config.json","frontal_server_ip"),configg.get_specific_data("config.json","frontal_server_port"))
s.start_server()