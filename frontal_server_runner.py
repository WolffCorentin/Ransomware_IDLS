import utile.configgetter as configg
import serveur_frontale.serveur_frontal as front_s

s = front_s.serveur_frontal(configg.get_specific_data("config.json","frontal_server_ip"), 8443)
s.start_server()