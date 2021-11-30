import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
indirizzo = '0.0.0.0' # nostro indirizzo 
porta = 5000 # la porta

registro_nick_name = {} 
# dizionario che contiene tutti i vari nickname come valore e gli addr come chiave

stringa_ok = "OK" # stringa usata per permettere ai client di chattare

s.bind((indirizzo, porta))

while True:
    data, addr = s.recvfrom(4096) # buffer di 4 kB

    if data.decode().split(":")[0].lower() == "nickname" :
        nick_name_data = data.decode().split(":")[1]

        registro_nick_name[nick_name_data] = addr
        print(f"{nick_name_data} ha joinnato, benvenuto")

        s.sendto(stringa_ok.encode(), (addr, porta))

    elif data.decode().split(":", ",")[0].lower() == "sender":
        nick_reciver = data.decode().split(":", ",")[3]
        mex = data.decode().split(":", ",")[4]

        print(f"Mex:{mex}\tRec:{nick_reciver}")
        s.sendto(mex.encode(), registro_nick_name[nick_reciver])

s.close()

