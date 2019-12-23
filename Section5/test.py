import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text);'
cur.execute(create_table)

insert_query = 'INSERT INTO users VALUES (?,?,?);'
users = [
    (1, 'jose', 'asdf'),
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz'),
]

cur.executemany(insert_query, users)

conn.commit()
cur.close()
conn.close()