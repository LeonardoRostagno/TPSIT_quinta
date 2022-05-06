import socket as sck
import sqlite3
import threading as thr

#-socket------------------------------------------------------------------------------------------------------------------
porta = 5000 # porta
ip = '127.0.0.1' # ip

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.bind((ip, porta)) # bind
s.listen() # server si mette in listen

#-thread------------------------------------------------------------------------------------------------------------------
class Client_manager(thr.Thread):
    def __init__(self, conn, addr):
        thr.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.running = True

    def run(self):
        while self.running:
            data = self.conn.recv(4096) # dati che arrivano
            data = data.decode().split(',') # splitto per le informazioni

            liv_mis = float(data[0])

            #-database----------------------------------------------------------------------------------------------------
            connection = sqlite3.connect('fiumi.db') # mi connetto al db
            cursor = connection.cursor() # creo il cursore

            # prelevo i dati che mi interessano
            guardia = cursor.execute(f"SELECT livello FROM livelli WHERE id_stazione = '{data[3]}'").fetchall()
            fiume = cursor.execute(f"SELECT fiume FROM livelli WHERE id_stazione = '{data[3]}'").fetchall()
            localita = cursor.execute(f"SELECT localita FROM livelli WHERE id_stazione = '{data[3]}'").fetchall()

            connection.close() # chiudo la connessione al db
            print(guardia[0][0])

            perc30 = guardia[0][0] * 30/100
            perc70 = guardia[0][0] * 70/100

            if liv_mis < perc30: # valore inferiore al 30%
                s.sendto("Valore_ricevuto".encode(), addr) # messaggio per il client
            elif liv_mis >= perc30 and liv_mis < perc70: # valore compreso tra 30% and 70%
                s.sendto("Valore_ricevuto".encode(), addr) # messaggio per il client

                print(f"\tPERICOLO IMMINENTE\nFiume:{fiume[0][0]}\tLocalita:{localita[0][0]}\n{data[1]} - {data[2]}")
            else: # valore superiore o uguale al 70%
                s.sendto("Accensione_sirena".encode(), addr) # messaggio per il client

                print(f"\tPERICOLO in CORSO\nFiume:{fiume[0][0]}\tLocalita:{localita[0][0]}\n{data[1]} - {data[2]}")

#-program-----------------------------------------------------------------------------------------------------------------
while True:
    conn, addr = s.accept() 

    #-----PUNTO 2------------------------------------------------------------
    client = Client_manager(conn, addr)
    client.start()
    #------------------------------------------------------------------------