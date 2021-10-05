import RPi.GPIO as GPIO
import time

ledPin = 18


global pwm
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.output(ledPin, GPIO.LOW)
pwm = GPIO.PWM(ledPin, 10000)
count = 0;
try:
    while(True):
        pwm.start(50)
        if(GPIO.input(4) == False):
            count = count + 1
            if(count > 3):
                pwm.start(100)
                time.sleep(3)
                count = 0
        
        pwm.start(50)
            
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()