import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led = 26
tr = 6
GPIO.setup(led, GPIO.OUT)
GPIO.setup(tr, GPIO.IN)
while True:
    GPIO.output(led, not(GPIO.input(tr)))