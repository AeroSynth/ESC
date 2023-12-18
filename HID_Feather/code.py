# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython Essentials HID Keyboard example
AAAAAAA
For debounce:
https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors
"""
import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup
keypress_pins = [board.A1, board.A2, board.A3, board.A4, board.A5]
# Our array of key objects
key_pin_array = []
# The Keycode sent for each button, will be paired with a control key
#keys_pressed = [Keycode.A, "Hello World!\n"]
keys_pressed = [Keycode.V, Keycode.S, Keycode.V, Keycode.S, Keycode.QUOTE]
shift_key = Keycode.SHIFT

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.direction = digitalio.Direction.OUTPUT
repeat = False #key repeat flag

print("Waiting for key pin...")

while True:
    # Check each pin
    for key_pin in key_pin_array:
        if not key_pin.value:  # Is it grounded?
            i = key_pin_array.index(key_pin)
            #print("Pin #%d is grounded." % i)
            # Turn on the red LED
            led.value = True
            
            #while not key_pin.value:
            #    pass  # Wait for it to be ungrounded!
            # "Type" the Keycode or stringa
            key = keys_pressed[i]  # Get the corresponding Keycode or string
            #print(key,i)
            if (i == 0) or (i == 1): #check for capital S or V
                keyboard.press(shift_key,key)
            else:
               keyboard.press(key)
               
            keyboard.release_all()  # ..."Release"!
            # Turn off the red LED
            led.value = False
            
    time.sleep(.1)
    
     

