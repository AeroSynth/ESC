''' For RPi4 '''

import RPi.GPIO as GPIO
from time import sleep
from tkinter import *
import random



'''
Event handler for button
called when the button is released
event is the gpio number
requires rising edge and a 0.1uF cap.
Falling edge bounces so a 5ms debounce wait time is required.
(may need longer debounce time for "bouncier" switches)
'''
def Button(bevent):
    global greenbutton,redbutton#, state
    sleep(.005) #debounce 5ms.
    #print(event)
    if GPIO.input(bevent) != 0:
        if bevent == 23:
            greenbutton +=1
            print('green button',greenbutton)
        if bevent == 24:
            redbutton +=1
            print('red button',redbutton)


def callback(label):#label):
   global elabel
   elabel=label
   #print(label)
   value = label.char
   print(value, ' A button is pressed')   
        
def task():
    global greenbutton,elabel
    
    while greenbutton ==0:
        greenbutton=0
        print("should cancel")         
        tk.after_cancel(elabel)#tk.after_id)    # cancel it
      
    #tk.after_id = tk.after(1,task)
    #print(tk.after_id)

print("starting...") 
greenbutton=0
redbutton = 0
elabel=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23,GPIO.RISING,callback=Button)#,bouncetime=50)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(24,GPIO.RISING,callback=Button)

tk = Tk()
tk.geometry('300x150')
tk.bind('<Key>', callback)#lambda i : PressAnyKey(i))
task()

mainloop()



#tk.mainloop() 