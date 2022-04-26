import requests
import time

host = "192.168.0.132"
port = "5000"
pwm = 50
times = 0.5

def get_sensor(): # funzione per vedere i valori dei sensori
    sensors = requests.get(f'http://{host}:{port}/api/v1/sensors/obstacles') # sensori
    print(sensors.json())

    dx = int(sensors.json()['Right']) # assegno ad una variabile il valore di dx
    sx = int(sensors.json()['Left']) # assegno ad una variabile il valore di sx

    time.sleep(times / 5)

    return sx, dx

def watch_sx(): # funzione che gira il robot per guardare a sinistra
    requests.get(f'http://{host}:{port}/api/v1/motors/left?pwm={pwm}&time={times / 2}') # giro a sx

    sen_sx, sen_dx = get_sensor() # leggo i sensori

    if sen_sx == 1 and sen_dx == 1: # osservo se ho campo libero
        return True
    else:
        return False

def watch_dx(): # funzione che gira il robot per guardare a destra
    requests.get(f'http://{host}:{port}/api/v1/motors/right?pwm={pwm}&time={times / 2}') # giro a dx 

    sen_sx, sen_dx = get_sensor() # leggo i sensori

    if sen_sx == 1 and sen_dx == 1: # osservo se ho campo libero
        return True
    else:
        return False

if __name__ == '__main__':
    while True:
        sen_sx, sen_dx = get_sensor() # leggo i sensori

        if sen_sx == 1 and sen_dx == 1: # osservo se ho campo libero
            requests.get(f'http://{host}:{port}/api/v1/motors/both?pwmL={pwm}&pwmR={pwm}&time={times}') # avanzo
        elif sen_sx == 1 and sen_dx == 0: # osservo se ho sinistra libera, ma ostacolo verso destra
            requests.get(f'http://{host}:{port}/api/v1/motors/left?pwm={pwm}&time={times / 2}') # giro a sx piano
        elif sen_sx == 0 and sen_dx == 1: # osservo se ho destra libera, ma ostacolo verso sinistra
            requests.get(f'http://{host}:{port}/api/v1/motors/right?pwm={pwm}&time={times / 2}') # giro a dx piano
        else: # se trovo un ostacolo frontalmente.
            if watch_sx(): # guardo a sinistra
                continue # se ha sinistra ho libero avanzo
            else:
                if watch_dx():# guardo a destra
                    continue # se ho destra libera avanzo
                else: # se sinistra e destra hanno un ostacolo
                    requests.get(f'http://{host}:{port}/api/v1/motors/right?pwm={pwm}&time={times}') # torno indietro           