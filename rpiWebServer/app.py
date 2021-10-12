'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
Lamp1 = 13
Lamp2 = 18

#initialize GPIO status variables
Lamp1stat = 0
Lamp2stat = 0

# Define led pins as output
GPIO.setup(Lamp1, GPIO.OUT)   
GPIO.setup(Lamp2, GPIO.OUT) 

# turn leds OFF 
GPIO.output(Lamp1, GPIO.LOW)
GPIO.output(Lamp2, GPIO.LOW)
	
@app.route("/")
def index():
	# Read Sensors Status
	Lamp1stat = GPIO.input(Lamp1)
	Lamp2stat = GPIO.input(Lamp2)
	templateData = {
              'title' : 'GPIO output Status!',
              'Lamp1'  : Lamp1stat,
              'Lamp2'  : Lamp2stat,
        }
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'Lamp1':
		actuator = Lamp1
	if deviceName == 'Lamp2':
		actuator = Lamp2
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	Lamp1stat = GPIO.input(Lamp1)
	Lamp2stat = GPIO.input(Lamp2)
   
	templateData = {
              'Lamp1'  : Lamp1stat,
              'Lamp2'  : Lamp2stat,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='192.168.1.2', port=80, debug=True)