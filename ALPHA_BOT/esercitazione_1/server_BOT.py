import socket as sck
import alphabot as alpha
import sqlite3
import time

#-socket--------------------------------------------------------------------
porta = 5000 # porta della connessione
ip = '0.0.0.0' # ip del socket

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) # creazione socket
s.bind((ip, porta)) # bind
s.listen() # server si mette in listen
conn, addr = s.accept() 

#-robot---------------------------------------------------------------------
robot = alpha.AlphaBot() # istanzio la classe

#-program-------------------------------------------------------------------
def bot_move_standard(data) : # funzione per le funzioni standard del movimento
    if data[0] == 'w' :
        robot.forward() # avanti
    elif data[0] == 'wp' :
        tempo = float(data[1])
        robot.forward_progressive(tempo) # avanti progressivo
    elif data[0] == 's' :
        robot.backward() # indietro
    elif data[0] == 'sp' :
        tempo = float(data[1])
        robot.backward_progressive(tempo) # indietro progressivo
    elif data[0] == 'a' :
        robot.left() # sinistra
    elif data[0] == 'd' :
        robot.right() # destra
    elif data[0] == 'r' :
        robot.stop() # stop

    if  data[0] != 'r' : # controllo qualunque movimento tranne lo stop
        tempo = float(data[1]) # prendo il tempo dal messaggio del client

        time.sleep(tempo) 
        robot.stop() # stoppo l'azione

def bot_move_db(data) : # funzione per i movimenti preseti nel database
    connection = sqlite3.connect('db_alpha.db') # mi connetto al db
    cursor = connection.cursor() # creo il cursore

    # ricerca del comando nel db
    list_seq = cursor.execute(f"SELECT sequenza FROM Movimenti where movimento = '{data[0]}' ").fetchall()
    
    connection.close() # chiudo la connessione con il db

    if len(list_seq) == 0:
        print("ERROR SEQUENCE") # controllo se il comando inserito è errato
    else:
        print(list_seq[0][0]) # stampo la lista dei comandi che esegue il bot

        list_move = list_seq[0][0].split(";")

        for s in list_move: # eseguo la lista dei movimenti 
            bot_move_standard(s.split(",")) 
    

def main() :
    while True:
        data = conn.recv(4096) # dati che arrivano
        data = data.decode().lower().split(',') # splitto per dividere il comando dal tempo

        # controllo se si tratta di un comando standard o di un comando dal db
        if data[0] == 'w' or data[0] == 'wp' or data[0] == 'a' or data[0] == 's' or data[0] == 'sp' or data[0] == 'd' or data[0] == 'r' :
            bot_move_standard(data) # richiamo la funzione
        else:
            bot_move_db(data) # richiamo la funzione

    s.close() # close del socket

if __name__ == '__main__':
    main()