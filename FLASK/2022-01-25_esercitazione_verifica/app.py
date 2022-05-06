import flask as fl
import sqlite3
import socket as sck

app = fl.Flask(__name__)
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) # socket

@app.route('/', methods = ['GET', 'POST'])
def controlla():
    if fl.request.method == 'POST':
        ip = fl.request.form['ip_address']
        port_min = int(fl.request.form['porta_min'])
        port_max = int(fl.request.form['porta_max'])

        #-db-----------------------------------
        connection = sqlite3.connect('./database.db')
        cursor = connection.cursor()
        #--------------------------------------
        for addr in range(port_min, port_max):
            if s.connect_ex((ip, addr)) == 0:
                cursor.execute("INSERT INTO SCAN_PORT (ip_address, port, status) VALUES (?,?,?)", (ip, addr, "OPEN"))
            else:
                cursor.execute("INSERT INTO SCAN_PORT (ip_address, port, status) VALUES (?,?,?)", (ip, addr, "CLOSE"))
            connection.commit()
            
        connection.close()

        print("Port scan concluded")

    return fl.render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)