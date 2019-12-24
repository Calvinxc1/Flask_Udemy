import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

create_table = """CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	username text,
	password text
);"""
cur.execute(create_table)

create_table = """CREATE TABLE IF NOT EXISTS items (
	name text,
	price real
);"""
cur.execute(create_table)

cur.execute("INSERT INTO items VALUES ('test', 10.99);")

conn.commit()
cur.close()
conn.close()