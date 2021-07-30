'''
program to plot wave data onto a tkinter canvas using matplotlib.
toolbars, nav bar, and keybindings are removed
reference:  display-wave.py
Brad Stewart, July 1, 2021
'''
import time as sleep
import matplotlib.pyplot as plt
import numpy as np
#from playsound import playsound
#import wave
#import sys
import tkinter as tk
from tkinter import ttk
from scipy.io import wavfile
import sounddevice as sd



from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#, NavigationToolbar2Tk) #second item optional if not using Nav Bar
# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
'''
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata
'''
f = ttk.Frame()#padding = 8)#,width=500)
fig = Figure(figsize=(8,2))
fig.subplots_adjust(bottom=0.0, right=1.04, left=-.04, top=1.,wspace=0.0)
plt = fig.add_subplot()#111, facecolor=('xkcd:light grey'))
canvas = FigureCanvasTkAgg(fig, f)
#next 3 instructions remove frames and axis
#hidden in any even as the subplot adjusts to cover them.
plt.set_frame_on(False)
plt.get_xaxis().set_visible(False)
plt.get_yaxis().set_visible(False)
canvas._tkcanvas.pack()#fill=tk.BOTH)#, expand=1)
f.pack(fill=tk.BOTH, expand=1) #expand optional, so is fill (for now)
#canvas.show()

my_file = 'example.wav'
samplerate, data = wavfile.read(my_file)
length = data.shape[0] / samplerate
time = np.linspace(0., length, data.shape[0])
       
plt.plot(time, data[:])
print(length,data.shape[0])
#plt.draw()
#sleep.sleep(2)
#data, fs = sd.read(my_file)#, dtype='float32')  
#while True:
#sd.sleep(int(1000))
print("playing audio")

#sd.play(data, samplerate)

    #sleep.sleep(2)
    #status = sd.wait()  # Wait until file is done playing
