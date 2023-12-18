''' For RPi4 '''

import RPi.GPIO as GPIO
from time import sleep

'''
Event handler for button
called when the button is released
event is the gpio number
requires rising edge and a 0.1uF cap.
Falling edge bounces so a 5ms debounce wait time is required.
(may need longer debounce time for "bouncier" switches)
'''
def Button(event):
    global greenbutton,redbutton#, state
    sleep(.005) #debounce 5ms.
    print(event)
    if GPIO.input(event) != 0:
        if event == 23:
            greenbutton +=1
            print('green button',greenbutton)
        if event == 24:
            redbutton +=1
            print('red button',redbutton)
    #print('tick')

print("starting...")
greenbutton=0
redbutton = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23,GPIO.RISING,callback=Button)#,bouncetime=50)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24,GPIO.RISING,callback=Button)