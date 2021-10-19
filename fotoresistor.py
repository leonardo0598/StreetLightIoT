import os
import RPi.GPIO as GPIO
import time
#il valore della fotoresistenza si salva in una variabile d'ambiente "fotoresistenza"
GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit

def rc_time (pin_to_circuit):
    os.environ["fotoresistenza"] = 0
    count = os.environ["fotoresistenza"]
    #Output on the pin for 
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(4, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(4) == GPIO.LOW):
        count += 1
        
    

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        print(rc_time(4))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()