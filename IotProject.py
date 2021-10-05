#definizione per accendere luci al 50% aggiungendo input e nome luce
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


#setup luci
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)


#setup moduli IR
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(27, GPIO.IN)

#GPIO.output(18, GPIO.LOW)
#do i nomi con pwm data e frequenza
pwm = GPIO.PWM(18, 10000)
pwm1 = GPIO.PWM(12, 10000)
pwm2 = GPIO.PWM(13, 10000)
pwm3 = GPIO.PWM(19, 10000)

#liste per eseguire in parallelo la funzione dimmerLuce
LucePwm = ["pwm", "pwm1", "pwm2", "pwm3"] #lista delle luci da salvare con queste variabili
IrSensors = [22, 23, 24, 27] #GPIO dei sensori di movimento

#prende in input luce e sensore IR accende la luce al 50% e appena passa qualcosa la alza al 100%
def dimmerLuce(i, j):  
    #count = 0
    j.start(50)
    if(GPIO.input(i) == False):
        time.sleep(1) #se falso si ferma un secondo per risolvere il problema del sensore
        if(GPIO.input(i) == False):
            j.start(100)
            time.sleep(3)

#funzione main per eseguire tutto
while(True):
    time.sleep(0.1) #per regolare il ciclo while 
    for i in LucePwm: #esegue le 5 operazioni in parallelo
        dimmerLuce(IrSensors[i], LucePwm[i]) #esegue dimmer su tutte le luci
    
