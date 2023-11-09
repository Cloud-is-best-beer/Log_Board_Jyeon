import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
                userid CHAR(20) PRIMARY KEY,
                username CHAR(10) NOT NULL,
                password CHAR(20) NOT NULL
        )


    ''')

    #board table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS board(
                id INTEGER PRIMARY KEY,
                title CHAR(30) NOT NULL,
                body TEXT NOT NULL,
                time DATETIME NOT NULL,
                userid CHAR(20) NOT NULL,
                FOREIGN KEY (userid) REFERENCES user (userid)
        )

    ''')

    cursor.close()
    conn.close()


def hashing(password):
    hash = hashlib.sha256()
    hash.update(password.encode('utf-8'))
    password = hash.hexdigest()
    return password