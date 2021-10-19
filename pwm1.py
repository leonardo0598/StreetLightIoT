import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

#setup infrarossi
GPIO.setup(23, GPIO.IN)
GPIO.setup(4, GPIO.IN)
#setup luci
GPIO.setup(18, GPIO.OUT)
pwm1 = GPIO.PWM(18, 1000)

#prende in input luce e sensore IR accende la luce al 50% e appena passa qualcosa la alza al 100%
def dimmerLuce(j, i): 
    
    if(GPIO.input(i) == False):
        j.ChangeDutyCycle(100)
        time.sleep(2)
        j.ChangeDutyCycle(50)



if __name__ == '__main__':
    try:
        
        pwm1.start(0)
        pwm1.ChangeDutyCycle(50)
        while(True ):
            dimmerLuce(pwm1, 23)
                
                
               
           
            
    except KeyboardInterrupt:
        pwm1.stop()
        GPIO.cleanup()   