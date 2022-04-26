import flask as fl
import sqlite3
import string 
import random
import alphabot as alpha
import time

app = fl.Flask(__name__)
token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
robot = alpha.AlphaBot() # istanziamo alphabot

#-login page---------------------------------------------------------------------------------------------------------
def validate(username, password): 
    completion = False # usato per la validità delle credenziali

    #-db login page---------------------------------------------------------------------
    connection = sqlite3.connect('./db.db') # connetto al db
    cursor = connection.cursor() # creo il cursore

    list_user = cursor.execute("SELECT * FROM USERS").fetchall() # ricerca delle credenziali nel db

    connection.close() # chiudo la connessione con il db
    #-----------------------------------------------------------------------------------
   
    # verifica delle credenziali
    for row in list_user:
        dbUsername = row[0]
        dbPassword = row[1]

        # verifichiamo lo username
        if dbUsername == username:
            completion = check_password(dbPassword, password) # verifichiamo la password

    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods = ['GET', 'POST']) # decoratore della login page
def login():
    error = None

    # 
    if fl.request.method == 'POST':
        username = fl.request.form['username']
        password = fl.request.form['password']

        completion = validate(username, password)

        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return fl.redirect(fl.url_for('botton'))

    return fl.render_template('login.html', error = error)

#-input page---------------------------------------------------------------------------------------------------------
def move_symple(data):
    if data == 'w' :
        robot.forward() # avanti
    elif data == 's' :
        robot.backward() # indietro
    elif data == 'a' :
        robot.left() # sinistra
    elif data == 'd' :
        robot.right() # destra
    elif data == 'r' :
        robot.stop() # stop

def move_complex(data):
    connection = sqlite3.connect('db_alpha.db') # mi connetto al db
    cursor = connection.cursor() # creo il cursore

    # ricerca del comando nel db
    list_seq = cursor.execute(f"SELECT sequenza FROM Movimenti where movimento = '{data}' ").fetchall()
    
    connection.close() # chiudo la connessione con il db

    if len(list_seq) == 0:
        print("ERROR SEQUENCE") # controllo se il comando inserito è errato
    else:
        print(list_seq[0][0]) # stampo la lista dei comandi che esegue il bot

        list_move = list_seq[0][0].split(";")

        for s in list_move: # eseguo la lista dei movimenti
            move_symple(s.split(",")) 


@app.route(f'/{token}', methods = ['GET', 'POST'])
def botton():
    if fl.request.method == 'POST': 
        dir = fl.request.form.get('dir') # direzioni base
        txt = fl.request.form.get('txt') # movimenti complessi

        if txt == "":
            # lato bottoni 
            move_symple(dir)
        else:
            # lato casella testo
            move_complex(txt)

        # fermiamo noi il robot dopo 1 secondo 
        time.sleep(1)
        robot.stop()        
        
    else:
        print("Please, use POST!!")
    
    return fl.render_template("control.html")


if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0")