import socket as sck
import threading 
import logging
import time

#----------------------------------------------------------------------------------

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
indirizzo = '127.0.0.1' # indirizzo con cui ci colleghiamo
porta = 5000 # la porta

# Informazioni base per il server
nick_name = str(input("Inserisci il Nickname con cui vuoi apparire al server:"))
stringa_nick = f"Nickname:{nick_name}"
s.sendto(stringa_nick.encode(), (indirizzo, porta))

#----------------------------------------------------------------------------------

def thread_client(name):
    logging.info("Thread %s: inizialize",name)

    while True:
        data, addr = s.recvfrom(4096)
        print(data.decode())

#----------------------------------------------------------------------------------

def main():
    format = "%(asctime)s : %(message)s"
    logging.basicConfig(format = format, level = logging.INFO, datefmt="%H:%M:%S")   
    logging.info("Main:\tcreate thread")
    client = threading.Thread(target = thread_client, args=(1, ), daemon = True)
    logging.info("Main:\tstart thread")
    client.start()

    data_risp, addr = s.recvfrom(4096)  # error

    while data_risp.decode() == "OK" :
        mex = str("Scrivi il messaggio: ")
        reciver = str("Inserire il nick del destinatario: ")

        stringa_send = f"Sender:{nick_name},Reciver:{reciver},{mex}"
        s.sendto(stringa_send.encode(), addr)

    s.close()

if __name__ == '__main__':
    main()