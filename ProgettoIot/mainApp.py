import RPi.GPIO as GPIO
import time
import multiprocessing
from multiprocessing import Process

from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
#Creo un dizionario per le due luci con nome e stato e il suo pin
lights = {
   18:{'button': "OFF", 'sensor': 23, 'pwm': False,'p': 'start'},
   13:{'button': "OFF", 'sensor': 22, 'pwm': False,'p': 'start'} 
   }
#setup delle 2 luci e impostazione a low
for light in lights:
   GPIO.setup(lights[light]['sensor'], GPIO.IN)

#setup delle luci e dei due pwm
for light in lights:

   GPIO.setup(light, GPIO.OUT)
   GPIO.output(light, GPIO.LOW)
   lights[light]['pwm'] = GPIO.PWM(light,1000)#modifica
#pin sensore ldr
ldr = 4

#codice per fotoresistenza
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
      if(valueFoto(ldr) > 10000):
         #le luci si accendono al 50%
         j.start(0)
         j.ChangeDutyCycle(40)
         #se passa qualcosa sul sensore a infrarossi si accendono al 100%
         if(GPIO.input(i) == False):
            j.ChangeDutyCycle(100)
            time.sleep(2)
            j.ChangeDutyCycle(40)
      #se la luce è accesa la spegne sennò non fa niente
      #elif(j.start(0) == True):
      else:
         j.stop()


@app.route('/')
def main():

   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'lights' : lights
   }
   
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)
   
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route('/light', methods = ['POST'])

def click():
   
   for light in lights: 
      value = request.form.get(str(light))

      if value == 'On':
         lights[light]['button'] = "ON"
         if not lights[light]['p'] == 'start': 
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
         #GPIO.output(light, True)
         lights[light]['pwm'].start(0)
         lights[light]['pwm'].ChangeDutyCycle(100)
         

      if value == 'Off':
         lights[light]['button'] = "OFF"
         if not lights[light]['p'] == 'start':
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
             
         #GPIO.output(light, False)
         lights[light]['pwm'].stop()
         

      if value == 'Automatic':
         #dimmerLuce(lights[light]['pwm'], lights[light]['sensor'])
         lights[light]['button'] = "AUTO"
         lights[light]['pwm'].stop()   
         lights[light]['p'] = Process(target = dimmerLuce, args=(lights[light]['pwm'], lights[light]['sensor']))
         lights[light]['p'].start()
         
         

      if value == 'AutomaticTwo':
         p = Process(target = dimmerLuce, args=(lights[light]['pwm'], lights[light]['sensor']))
         p.start()
         lights[light]['button'] = "AUTO"

   

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'lights' : lights
    }

   return render_template('main.html', **templateData)






if __name__ == "__main__":
   try:
      app.run(host='192.168.1.2', port=80, debug=True)
                       
   except KeyboardInterrupt:
      print("KeyboardInterrupt")
      for light in lights:
         if not lights[light]['p'] == 'start':
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
              
               
   finally:      
      GPIO.cleanup()

   

