def get_int_between(valeur_min=0, valeur_max=0):
    while True:
        choix = input("Merci de préciser votre choix : ")
        if choix.isdigit():
            choix = int(choix)
            if valeur_min <= choix <= valeur_max:
                return choix
