import RPi.GPIO as GPIO
import time
from threading import Thread
import signal
import threading

from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
#Creo un dizionario per le due luci con nome e stato e il suo pin
lights = {
   18: {'name' : 'lightOne', 'state' : GPIO.LOW},
   13 : {'name' : 'lightTwo', 'state' : GPIO.LOW}
   }

#setup delle 2 luci e impostazione a low
for light in lights:

   GPIO.setup(light, GPIO.OUT)
   GPIO.output(light, GPIO.LOW)

@app.route('/')

def main():

   # For each pin, read the pin state and store it in the pins dictionary:
   for light in lights:
       
      lights[light]['state'] = GPIO.input(light)

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
         GPIO.output(light, True)
      if value == 'Off':     
         GPIO.output(light, False)
      # For each pin, read the pin state and store it in the pins dictionary:
   for light in lights:
      lights[light]['state'] = GPIO.input(light)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'lights' : lights
    }

   return render_template('main.html', **templateData)


def action():
   for light in lights:
      value = request.form.get(light)
      print("vado")
      if value == "Automatic":
         print("Automatic", light)
      if value == 'On':
         print ("luce accesa", light)
      if value == 'Off':
         print ("luce spenta", light)

  

   # For each pin, read the pin state and store it in the pins dictionary:
   for light in lights:
      lights[light]['state'] = GPIO.input(light)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'lights' : lights
    }

   return render_template('main.html', **templateData)



if __name__ == "__main__":
   app.run(host='192.168.1.2', port=80, debug=True)

