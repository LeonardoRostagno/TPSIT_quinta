import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
indirizzo = '192.168.88.94' # indirizzo con cui ci colleghiamo

nick_name = str(input("Inserisci il Nickname con cui vuoi apparire al server: "))

while True:  
    stringa = f"Nickname:{nick_name}"

    s.sendto(stringa.encode(), (indirizzo, 5000))

s.close()