import socket as sck

#-socket--------------------------------------------------------------------
porta = 5000 # porta della connessione
ip = '192.168.0.131' #ip bot

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.connect((ip, porta)) 

#-program-------------------------------------------------------------------
print("\n\n\tALPHABOT METHODS:\n" # elenco dei metodi
        "insert 'w' for forward\n"
        "insert 'wp' for forward_progressive\n" 
        "insert 's' for backward\n"
        "insert 'sp' for backward_progressive"
        "insert 'a' for left\n"
        "insert 'd' for right\n"
        "insert 'r' for stop\n"
        "------------------------------------------------------------------\n"
        "insert 'curve_forward_left' for curve_forward_left\n"
        "insert 'curve_forward_right' for curve_forward_right\n"
        "insert 'curve_backward_left' for curve_backward_left\n"
        "insert 'curve_backward_right' for curve_backward_right\n"
        "insert '360_left' for 360_left\n"
        "insert '360_right' for 360_right\n"
        "insert 'zig_zag' for zig_zag\n"
        "------------------------------------------------------------------\n")

while True:
    stringa = input("Insert method: ").lower() # chiediamo all'utenti di inserire il metodo da eseguire
    
    # selezione di controllo del metodo
    if stringa != 'w' and stringa != 'wp' and stringa != 's' and stringa != 'sp' and stringa != 'a' and stringa != 'd':
        # se è un metodo che non richede tempo lo spedisce
        s.sendall(stringa.encode())
    else: 
        # altrimenti richiede il tempo di esecuzione del movimento all'utente
        temp = input("Insert time for the movement: ")
        stringa += "," + temp
        s.sendall(stringa.encode())

s.close()