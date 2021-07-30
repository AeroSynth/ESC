#!/usr/bin/python3
'''
can use import wave instead of numpy, but reads blocks as byte objects--no good
https://docs.python.org/3/library/wave.html
'''

''' the original program requires wave stereo file '''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''#not needed if you don't want to display the navtool
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2TkAgg as nav_tool
'''
from matplotlib.figure import Figure
#from matplotlib import gridspec

from scipy.io import wavfile
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        #self.geometry("700x400")
        self.title("SOUNDART")
        self.init_ui()
        self.set_plot()
       
    def init_ui(self):

        f = ttk.Frame()#padding = 8)
        fig = Figure()
        #fig.subplots_adjust(bottom=0.10, right=0.96, left=0.08, top=0.95, wspace=0.10)
        self.plt = fig.add_subplot()#111, facecolor=('xkcd:light grey'))
        canvas = FigureCanvasTkAgg(fig, f)
        ''' next 3 instructions remove frames and axis '''
        self.plt.set_frame_on(False)
        self.plt.get_xaxis().set_visible(False)
        self.plt.get_yaxis().set_visible(False)
        #toolbar = nav_tool(canvas, f) #comment out to remove tool bar
        #toolbar.update()
        canvas._tkcanvas.pack()#fill=tk.BOTH)#, expand=1)

        f.pack()#fill=tk.BOTH)#, expand=1) #expand optional

    def set_plot(self):
        global data
        fig = plt.figure()#figsize=(8, 8)) #superfluous?
        my_file = 'example-mono.wav'
        samplerate, data = wavfile.read(my_file)
        length = data.shape[0] / samplerate
        #samplerate, data = wavfile.read(my_file)
        time = np.linspace(0., length, data.shape[0])
       
        self.plt.plot(time, data[:])#, label="Left channel") #for mono       
        #self.plt.plot(time, data[:, 0], label="Left channel") #for stereo
        #self.plt.plot(time, data[:, 1], label="Right channel") #for stereo
        '''self.plt.legend()
        self.plt.set_xlabel("Time [s]")
        self.plt.set_ylabel("Amplitude")'''

    def on_exit(self):
        #if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
        self.destroy()
        quit() #returns to prompt.
    
if __name__ == '__main__':
    app = App()
    app.mainloop() #comment out for debugging