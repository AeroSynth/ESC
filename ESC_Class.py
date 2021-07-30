#ESC Class
VERSION = 0.1
import sys
import tkinter as tk
from scipy.io import wavfile
import sounddevice as sd
import re
from time import perf_counter
from tkinter import ttk
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

class ESC(object,w,Frame8):
    def __init__(self):
        f1=ttk.Frame(w.Frame8)
        self.fig=Figure()
        self.plt = fig.add_subplot()
        fig.subplots_adjust(bottom=0.0, right=1.04, left=-.06, top=1.,wspace=0.0)
        plt.set_frame_on(False)
        plt.get_xaxis().set_visible(False)
        plt.get_yaxis().set_visible(False)
        plt_canvas = FigureCanvasTkAgg(fig, f1)
       

    def plot_wave(self,frame,filename):
        samplerate, data = wavfile.read(wfile)
        length = data.shape[0] / samplerate
        plt_canvas._tkcanvas.pack()#fill=tk.BOTH)#, expand=1)
        f.pack()#fill=tk.BOTH, expand=1) #expand optional, so is fill (for now)
        #t0=perf_counter()
        time=np.linspace(0.,(len(data)/samplerate),(len(data)))
        plt.plot(time,data[:],linewidth=.1)
   
