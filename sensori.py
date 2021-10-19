import RPi.GPIO as GPIO
import time
from threading import Thread


GPIO.setmode(GPIO.BCM)

#setup infrarossi
GPIO.setup(23, GPIO.IN)
GPIO.setup(22, GPIO.IN)
#setup luci
GPIO.setup(18, GPIO.OUT)
pwm1 = GPIO.PWM(18, 1000)
GPIO.setup(13, GPIO.OUT)
pwm2 = GPIO.PWM(13, 1000)
ldr = 4


def valueFoto (pin):
    count = 0
    #Output on the pin for 
    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, GPIO.LOW)
    time.sleep(0.1)
    #Change the pin back to input
    GPIO.setup(ldr, GPIO.IN)
    #Count until the pin goes high
    while (GPIO.input(ldr) == GPIO.LOW):
        count += 1

    return count

#prende in input luce e sensore IR accende la luce al 50% e appena passa qualcosa la alza al 100% considerando la luce circostante
def dimmerLuce(j, i):

  while(True):
    #condizione per accendere le luci
    if(valueFoto(ldr) > 3000):
        #le luci si accendono al 50%
        j.start(0)
        j.ChangeDutyCycle(50)
        #se passa qualcosa sul sensore a infrarossi si accendono al 100%
        if(GPIO.input(i) == False):
            j.ChangeDutyCycle(100)
            time.sleep(2)
            j.ChangeDutyCycle(50)
    #se la luce è accesa la spegne sennò non fa niente
    elif(j.start(0) == True):
        j.stop()
    
    


if __name__ == '__main__':
    try:
        #esegue 2 thread contemporaneamente per gestire le 2 luci installate
        t = Thread(target=dimmerLuce, args=(pwm1, 23))
        t2 = Thread(target=dimmerLuce, args=(pwm2, 22))
        t.start()
        t2.start()
        
                        
    except KeyboardInterrupt: 
      
        GPIO.cleanup()
           