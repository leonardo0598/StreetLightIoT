import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#setup infrarossi
GPIO.setup(22, GPIO.IN)

#setup luci
GPIO.setup(13, GPIO.OUT)
pwm2 = GPIO.PWM(13, 1000)

#prende in input luce e sensore IR accende la luce al 50% e appena passa qualcosa la alza al 100%
def dimmerLuce(j, i):  
    
    if(GPIO.input(i) == False):
        j.ChangeDutyCycle(100)
        time.sleep(3)
        j.ChangeDutyCycle(50)



if __name__ == '__main__':
    try:
        pwm2.start(0)
        pwm2.ChangeDutyCycle(50)
        while(True):
            dimmerLuce(pwm2, 22)
                
                
               
           
            
    except KeyboardInterrupt:
        pwm2.stop()
        GPIO.cleanup()   