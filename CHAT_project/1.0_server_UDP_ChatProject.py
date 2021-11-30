import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
indirizzo = '0.0.0.0' # nostro indirizzo 

registro_nick_name = {} 
# dizionario che contiene tutti i vari nickname come valore e gli addr come chiave

s.bind((indirizzo, 5000))

while True:
    data, addr = s.recvfrom(4096) # buffer di 4 kB

    if data.decode().split(":")[0] == "Nickname" :
        nick_name_data = data.decode().split(":")[1]

        registro_nick_name[addr] = nick_name_data

        print(f"{registro_nick_name[addr]} ha joinnato, benvenuto")
    else :
        print(f"{registro_nick_name[addr]} : {data.decode()}")

s.close()