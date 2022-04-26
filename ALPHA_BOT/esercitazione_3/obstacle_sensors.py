import RPi.GPIO as GPIO

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

def sensors():
	try:
		return GPIO.input(DR), GPIO.input(DL)
	except KeyboardInterrupt:
		GPIO.cleanup()