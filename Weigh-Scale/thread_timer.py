from time import sleep
import threading

restart = True

def hello():
    global restart
    restart=True
    print("thread finished")
    
a=0
while a<=21:
    if restart == True:
        restart = False
        t=threading.Timer(5.0,hello)
        t.start()
    print(a)
    a+=1
    sleep(1.5)
    
t.cancel()
print("done")