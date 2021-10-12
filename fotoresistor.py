import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit

def rc_time (pin_to_circuit):
    count = 0

    #Output on the pin for 
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    time.sleep(0.5)

    #Change the pin back to input
    GPIO.setup(4, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(4) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        print(rc_time(4))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()