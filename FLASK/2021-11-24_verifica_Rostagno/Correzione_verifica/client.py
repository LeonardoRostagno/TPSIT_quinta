import socket as sck
import datetime as dt
import random as rnd
from time import sleep

attesa_invio_dati = 10

def lettura_sensore():
    return rnd.uniform(0.1, 9)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect("127.0.0.1", 5000)

    id_stazione = int(input("Inserimento id_stazione"))
    s.sendall(f"{id_stazione}".encode())

    pericolo = False

    while True:
        misurazioni = lettura_sensore()
        data_misurazioni = dt.datetime.now()
        s.sendall(f"{misurazioni}#{data_misurazioni}#{id_stazione}".encode())

        risposta = s.recv(4096).decode()

        if risposta == "OK":
            if pericolo:
                print("Segnale luce off")
            elif risposta == "Pericolo":
                print("Segnale luce on")
                pericolo = True

if __name__ == '__main__':
    main()