import flask as fl
import sqlite3
import alphabot as alpha
import obstacle_sensors as obs
import time

app = fl.Flask(__name__)
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

#-motor page---------------------------------------------------------------------------------------------------------
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


@app.route('/api/v1/motors/botton', methods = ['GET', 'POST'])
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

@app.route('/api/v1/motors/left', methods = ['GET', 'POST'])
def left():
    if ('pwm' in fl.request.args) and ('time' in fl.request.args):
        try:
            pwm = int(fl.request.args['pwm'])
            time_pwm = float(fl.request.args['time'])

            robot.left(pwm)
            time.sleep(time_pwm)
            robot.stop()
            return "1"
        except:
            return "0"      
    else:
        return "ERROR: No PWM or TIME field provided. Please specify"

@app.route('/api/v1/motors/right', methods = ['GET', 'POST'])
def right():
    if ('pwm' in fl.request.args) and ('time' in fl.request.args):
        try:
            pwm = int(fl.request.args['pwm'])
            time_pwm = float(fl.request.args['time'])

            robot.right(pwm)
            time.sleep(time_pwm)
            robot.stop()
            return "1"
        except:
            return "0"      
    else:
        return "ERROR: No PWM or TIME field provided. Please specify"
    
@app.route('/api/v1/motors/both', methods = ['GET', 'POST'])
def both():
    if ('pwmL' in fl.request.args) and ('pwmR' in fl.request.args) and ('time' in fl.request.args):
        try:
            pwmL = int(fl.request.args['pwmL'])
            pwmR = int(fl.request.args['pwmR'])
            time_pwm = float(fl.request.args['time'])

            robot.forward(pwmL, pwmR)
            time.sleep(time_pwm)
            robot.stop()
            return "1"
        except:
            return "0"   
    else:
        return "ERROR: No PWM or TIME field provided. Please specify"

#-sensors page-------------------------------------------------------------------------------------------------------
@app.route('/api/v1/sensors/obstacles', methods=['GET', 'POST'])
def sensors():
    if fl.request.method == 'GET':
        DR, DL = obs.sensors()
        obstacle = {"Left": DL, "Right": DR}
    return fl.jsonify(obstacle)

if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0")