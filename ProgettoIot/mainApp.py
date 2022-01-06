import RPi.GPIO as GPIO
import time
import multiprocessing
from multiprocessing import Process

from flask import (Flask, render_template, request, redirect, session) #LOGIN redirect e session
app = Flask(__name__)
app.secret_key = "3482121"
GPIO.setmode(GPIO.BCM)

#Creo un dizionario per le due luci con bottone sensore abbinato stato pwm e processo in automatico
lights = {
   18:{'button': "OFF", 'sensor': 23, 'pwm': False,'p': 'start'},
   13:{'button': "OFF", 'sensor': 22, 'pwm': False,'p': 'start'} 
   }
#LOGIN credenziali in un dizionario
user = {"username": "tiziocaio", "psw": "1234"}

#setup dei 2 sensori a infrarossi in gpio.in
for light in lights:
   GPIO.setup(lights[light]['sensor'], GPIO.IN)

#setup delle luci e dei due pwm
for light in lights:

   GPIO.setup(light, GPIO.OUT)
   GPIO.output(light, GPIO.LOW)
   lights[light]['pwm'] = GPIO.PWM(light,1000)

#pin sensore ldr
ldr = 4

#codice per fotoresistenza
def valuePhoto (pin):
   count = 0
   #Output del pin ldr
   GPIO.setup(ldr, GPIO.OUT)
   GPIO.output(ldr, GPIO.LOW)
   time.sleep(0.1)
   #cambio del pin a input
   GPIO.setup(ldr, GPIO.IN)
   #count fino a quando ldr è a low
   while (GPIO.input(ldr) == GPIO.LOW):
      count += 1

   return count

#prende in input luce e sensore IR accende la luce al 40% e appena passa qualcosa la alza al 100% considerando la luce circostante
def dimmerLights(j, i):
   
   while(True):
      
      #condizione per accendere le luci
      if(valuePhoto(ldr) > 10000):
         #le luci si accendono al 40%
         j.start(0)
         j.ChangeDutyCycle(40)
         #se passa qualcosa sul sensore a infrarossi si accendono al 100% e dopo 2 secondi tornano al 40%
         if(GPIO.input(i) == False):
            j.ChangeDutyCycle(100)
            time.sleep(2)
            j.ChangeDutyCycle(40)
      #se la luce è accesa la spegne sennò non fa niente
      else:
         j.stop()




#all'apertura apre la pagina di login
@app.route('/')
def index():
   return render_template('login.html')


#gestione autenticazione login
@app.route('/login', methods = ['POST', 'GET'])
def login():
   if(request.method == 'POST'):
      username = request.form.get('username')
      password = request.form.get('psw')     
      if username == user['username'] and password == user['psw']:
            
         session['user'] = username
         return redirect('/dashboard')

      return "<h1>Wrong username or password</h1>"    

   return render_template("login.html")



#logout dell'utente
@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')

###---------------------------------------------------




#funzioni all'apertura della pagina
@app.route('/dashboard') 
def main():
   if('user' in session and session['user'] == user['username']):
      #all'apertura della pagina web passa il dizionario lights in templateData
      templateData = {
         'lights' : lights
      }
      #passa il templatedata nel template main.html e lo ritorna all'utente
      return render_template('main.html', **templateData)
   return "non sei loggato"
#funzioni quando riceve una richiesta POST per l'action /light
@app.route('/light', methods = ['POST'])
def click():
   #recupera il valore di light trasformandolo in stringa
   for light in lights: 
      value = request.form.get(str(light))
      #se On cambia button in ON, accende la luce al 100%, inoltre se è attivo un processo p(automatico) lo termina
      if value == 'On':
         lights[light]['button'] = "ON"
         if not lights[light]['p'] == 'start': 
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
         
         lights[light]['pwm'].start(0)
         lights[light]['pwm'].ChangeDutyCycle(100)
         
      #Se Off cambia button in OFF e spegne la luce, inoltre se è attivo un processo p(automatico) lo termina
      if value == 'Off':
         lights[light]['button'] = "OFF"
         #questa prima condizione serve solo per gestire il caso base ovvero quando si clicca OFF senza far partire alcun processo
         if not lights[light]['p'] == 'start':
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
             
         lights[light]['pwm'].stop()
         
      #se Automatic cambia button in Auto spegne il pwm della luce e fa partire il processo relativo p(dimmerLuce)
      if value == 'Automatic':
         
         lights[light]['button'] = "AUTO"
         lights[light]['pwm'].stop()   
         lights[light]['p'] = Process(target = dimmerLights, args=(lights[light]['pwm'], lights[light]['sensor']))
         lights[light]['p'].start()
   

   #Aggiorna il dizionario e lo ritorna nel main.html
   templateData = {
      'lights' : lights
    }

   return render_template('main.html', **templateData)






if __name__ == "__main__":
   try:
      #host del raspberry 
      app.run(host='192.168.1.2', port=80, debug=True)
   #in caso di interruzione del programma termina gli eventuali processi attivi                   
   except KeyboardInterrupt:
      print("KeyboardInterrupt")
      for light in lights:
         if not lights[light]['p'] == 'start':
            if lights[light]['p'].is_alive():
               lights[light]['p'].terminate()
               lights[light]['p'].join()
              
               
   finally: 
      #infine fa una pulizia delle GPIO     
      GPIO.cleanup()

   

