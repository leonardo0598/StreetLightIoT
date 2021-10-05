#GPIO.output(18, GPIO.LOW)

#do i nomi con pwm data e frequenza

pwm = GPIO.PWM(18, 10000)

#pwm1 = GPIO.PWM(12, 10000)

pwm2 = GPIO.PWM(19, 10000)

#pwm3 = GPIO.PWM(19, 10000)



#liste per eseguire in parallelo la funzione dimmerLuce

#LucePwm = [pwm, pwm1, pwm2, pwm3] #lista delle luci da salvare con queste variabili
LucePwm = [pwm,pwm2] 
#IrSensors = [22, 23, 24, 27] #GPIO dei sensori di movimento
IrSensors = [22, 24]


#prende in input luce e sensore IR accende la luce al 50% e appena passa qualcosa la alza al 100%

def dimmerLuce(i, j):  

    #count = 0
    m = j
    m.start(40)

    if(GPIO.input(i) == False):

        time.sleep(0.1) #se falso si ferma un secondo per risolvere il problema del sensore

        if(GPIO.input(i) == False):

            m.start(100)

            time.sleep(3)



#funzione main per eseguire tutto

try:
  
    while(True):

        #time.sleep(0.1) #per regolare il ciclo while 
    
        for f in range(0,2) : #esegue le 5 operazioni in parallelo

            dimmerLuce(IrSensors[f], LucePwm[f]) #esegue dimmer su tutte le luci

except KeyboardInterrupt:

    pwm.stop()

    pwm1.stop()

    pwm2.stop()

    pwm3.stop()

    GPIO.cleanup()