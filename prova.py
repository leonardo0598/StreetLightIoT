import time
import os

os.environ["prova"] = '0'

while(True):
    string = os.environ.get("prova")
    number = int(string)
    stringrec = str(number + 2)
    os.environ["prova"] = stringrec
    time.sleep(2)
    print(string)
