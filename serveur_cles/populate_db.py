import string
import random
import time
import utile.data as data

# valeurs de simulation
fake_victims = [
    ['WORKSTATION', 'c:,e:,f:', 'PENDING', 108],
    ['SERVEUR', 'c:,e:', 'PROTECTED', 23],
    ['WORKSTATION', 'c:,f:', 'INITIALIZE', 0],
    ['WORKSTATION', 'c:,f:,y:,z:', 'PROTECTED', 108]
]

fake_histories1 = [
    ['INITIALIZE', 0],
    ['CRYPT', 0],
    ['CRYPT', 89],
    ['PENDING', 108]
]

fake_histories2 = [
    ['INITIALIZE', 0],
    ['CRYPT', 0],
    ['PENDING', 20],
    ['PENDING', 23],
    ['DECRYPT', 23],
    ['PROTECTED', 23]
]

fake_histories3 = [
    ['INITIALIZE', 0],
]

fake_histories4 = [
    ['INITIALIZE', 0],
    ['CRYPT', 0],
    ['CRYPT', 89],
    ['PENDING', 108],
    ['DECRYPT', 65],
    ['DECRYPT', 108],
    ['PROTECTED', 108]
]

fake_histories = {
    1: fake_histories1,
    2: fake_histories2,
    3: fake_histories3,
    4: fake_histories4
}


def simulate_key(longueur=0):
    letters = ".éèàçùµ()[]" + string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(longueur))


def simulate_hash(longueur=0):
    letters = string.hexdigits
    return ''.join(random.choice(letters) for i in range(longueur))


def main():
    conn = data.connect_db()

    # victims --> os, hash, disks, key
    for victim in fake_victims:
        data_victim = (victim[0], simulate_hash(256), victim[1], simulate_key(512))
        data.insert_data(conn, 'victims', '(os, hash, disks, key)', f'{data_victim}')

    # history
    # states --> id_victim, datetime, state
    # encrypted --> id_victim, datetime, nb_files
    # decrypted --> id_victim, datetime, nb_files
    date_start = int(time.time())
    id_victim = 0
    for histories in fake_histories.values():
        id_victim += 1
        date_start = date_start - 3660 * random.randint(2, 10)  # remonte de quelque jours dans le passé (2 à 10j)
        for history in histories:
            data_state = (id_victim, date_start, history[0])
            print("STATES :", data_state)
            data.insert_data(conn, 'states', '(id_victim, datetime, state)', f'{data_state}')
            if history[0] == 'DECRYPT' or history[0] == 'PROTECTED':
                data_decrypted = (id_victim, date_start, history[1])
                print("DECRYPTED :", data_decrypted)
                data.insert_data(conn, 'decrypted', '(id_victim, datetime, nb_files)', f'{data_decrypted}')
            elif history[0] == 'CRYPT' or history[0] == 'PENDING':
                data_encrypted = (id_victim, date_start, history[1])
                print("ENCRYPTED :", data_encrypted)
                data.insert_data(conn, 'encrypted', '(id_victim, datetime, nb_files)', f'{data_encrypted}')
            date_start += random.randint(50, 600)  # calcule un delta entre chaque phase de l'attaque
    test = data.list_victims(conn)
    print("list victim)")
    print(test)
    conn.close()


if __name__ == '__main__':
    main()
