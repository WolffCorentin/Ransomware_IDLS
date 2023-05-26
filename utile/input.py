# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : security
# --------------------------------------------
# Importations
# --------------------------------------------
def get_int_between(msg, valeur_min=0, valeur_max=0):
    while True:
        choix = input(f'{msg} {valeur_min} à {valeur_max} : ')
        if choix.isdigit():
            choix = int(choix)
            if valeur_min <= choix <= valeur_max:
                return choix
