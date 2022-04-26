import requests
import time

#---function---------------------------------------------------------------------------------------------------
def sensor(host, port):
    r_sensors = requests.get(f'http://{host}:{port}/api/v1/sensors/obstacles')
    print(r_sensors.json())

def left(host, port):
    pwm = int(input("Insert the PWM power: "))
    time_pwm = input("Insert the time for move: ")

    r_left = requests.get(f'http://{host}:{port}/api/v1/motors/left?pwm={pwm}&time={time_pwm}')
    print(r_left.json())

def right(host, port):
    pwm = int(input("Insert the PWM power: "))
    time_pwm = input("Insert the time for move: ")

    r_right = requests.get(f'http://{host}:{port}/api/v1/motors/right?pwm={pwm}&time={time_pwm}')
    print(r_right.json())

def f_forward(host, port):
    pwmL = int(input("Insert the PWM power for the left motor: "))
    pwmR = int(input("Insert the PWM power for the right motor: "))
    time_pwm = input("Insert the time for move: ")

    r_left = requests.get(f'http://{host}:{port}/api/v1/motors/both?pwmL={pwmL}&pwmR={pwmR}&time={time_pwm}')
    print(r_left.json())

#---main-------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    host = input("Insert the IP host: ")
    port = input("Insert the host port: ")

    print("########### INPUT CHOOSE ##########\n"
        "Choose wht you want...\n"
        "0 --> sensors obstacle\n"
        "1 --> left move\n"
        "2 --> right move\n"
        "3 --> move fucking forward\n")

    while True:
        time.sleep(1)
        scelta = int(input("Inser your choose: "))

        if scelta == 0:
            sensor(host, port)
        elif scelta == 1:
            left(host, port)
        elif scelta == 2:
            right(host, port)
        elif scelta == 3:
            f_forward(host, port)
        else:
            print("Insert a possible choose")
