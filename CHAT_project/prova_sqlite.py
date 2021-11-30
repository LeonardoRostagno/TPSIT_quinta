import sqlite3

connection = sqlite3.connect('database_server_UDP_ChatProject.db')
cursor = connection.cursor()

for row in cursor.execute("SELECT * FROM utenti"):
    print(f"Nickname : {row[0]}\tAddress : {row[1]}\tPort : {row[2]}")

connection.close()