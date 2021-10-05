import RPi.GPIO as GPIO
import time




global pwm
global pwm1
global pwm2
global pwm3
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)
pwm = GPIO.PWM(18, 10000)
pwm1 = GPIO.PWM(12, 10000)
pwm2 = GPIO.PWM(13, 10000)
pwm3 = GPIO.PWM(19, 10000)

pwm.start(100)
pwm1.start(100)
pwm2.start(100)
pwm3.start(100)
time.sleep(3)
pwm.start(50)
pwm1.start(50)
pwm2.start(50)
pwm3.start(50)
time.sleep(3)

pwm.stop()
pwm1.stop()
pwm2.stop()
pwm3.stop()
GPIO.cleanup()

