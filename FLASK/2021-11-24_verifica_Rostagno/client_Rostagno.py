import socket as sck
import time

#-socket------------------------------------------------------------------------------------------------------------------
porta = 5000 # porta della connessione
ip = 'localhost' # ip

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
s.connect((ip, porta)) 

#-program-----------------------------------------------------------------------------------------------------------------
time_reinvio = float(input("Inserire il tempo di reinvio: "))

# se non viene inserito un tempo consono, gli viene attribuito un valore di default
if time_reinvio <= 0 and time_reinvio >= 30 : 
    time_reinvio = 15

while True:
    #-----PUNTO 1------------------------------------------------------------
    liv_mis = input("Inserire il livello misurato del fiume: ")
    date = input("Inserire la data della misurazione (GG/MM/AA): ")
    ora = input("Inserire l'ora della misurazione (ore:minuti:secondi): ")
    id = input("Inserire l'id della stazione: ")

    stringa = liv_mis + "," + date + "," + ora + "," + id # stringa composta
    #------------------------------------------------------------------------
    s.sendall(stringa.encode()) # invio al server

    #-----PUNTO 3------------------------------------------------------------
    risp = s.recv(4096) # risposta dl server
    risp = risp.decode()
    
    # esecuzione del ordine del server: 
    if risp == "Accensione_sirena":
        print("\tACCENSIONE SIRENA")
    #------------------------------------------------------------------------

    time.sleep(time_reinvio) # tempo di attesa prima del reinvio dei dati

s.close()
