''' For RPi4 '''

import RPi.GPIO as GPIO
from time import sleep
import asyncio


#called when the button is released
async def sw_callback():
    global button, state
    #sleep(.005) #debounce 5ms.
    if GPIO.input(24) != 0:
        button +=1
    #state = state +1
        print('button',button)
    await asyncio.sleep(.05)

print("starting...")
button=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(24,GPIO.RISING,callback=sw_callback,bouncetime=50)
asyncio.create_task(sw_callback())
#asyncio.run(sw_callback())
while True:
    pass
