import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)#, NavigationToolbar2Tk) #second item optional if not using Nav Bar
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
root = tkinter.Tk()
root.wm_title("Embedding in Tk")
fig = Figure(figsize=(7, 3), dpi=100)

spf = wave.open("example.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.frombuffer(signal, dtype=int)#"int16")
fs = spf.getframerate()

# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)


Time = np.linspace(0, len(signal) / fs, num=len(signal))
fig.add_subplot(111).plot(signal)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

'''
plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time, signal)
plt.show()
'''