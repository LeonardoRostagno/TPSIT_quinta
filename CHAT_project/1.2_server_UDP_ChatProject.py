import socket as sck
import sqlite3

# socket
s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
indirizzo = '0.0.0.0' # nostro indirizzo 
porta = 5000 # la porta
s.bind((indirizzo, porta))

#----------------------------------------------------------------------------------

# database
connection = sqlite3.connect('database_server_UDP_ChatProject.db')
cursor = connection.cursor()

#----------------------------------------------------------------------------------

stringa_ok = "OK" # stringa usata per permettere ai client di chattare

while True:
    data, addr = s.recvfrom(4096) # buffer di 4 kB
    info_data = data.decode().split(":")

    if info_data[0].lower() == "nickname" :
        nick_name_data = info_data[1]

        cursor.execute(f"INSERT INTO utenti VALUES ('{nick_name_data}', '{addr[0]}', {addr[1]})") # le stringhe si passano con '...'
        connection.commit()

        print(f"{nick_name_data} ha joinnato, benvenuto")

        s.sendto(stringa_ok.encode(), addr)
        # error

    elif info_data[0].lower() == "sender":
        nick_reciver = info_data[2].split(",")[0]
        mex = info_data[2].split(",")[1]

        if nick_reciver in cursor.execute("SELECT * FROM utenti"):
            print(f"Mex:{mex}\tRec:{nick_reciver}")

            row = cursor.execute(f"SELECT {nick_reciver} FROM utenti")
            s.sendto(mex.encode(), (row[1], row[2]))
        else:
            print(f"ERROR...{nick_reciver} not found")        

connection.close()
s.close()

