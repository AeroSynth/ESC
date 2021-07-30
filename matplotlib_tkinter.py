'''
imbeds matplot lib figure into a tkinter canvas.
how to specify size of plot in pixels.
https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/figure_size_units.html
'''
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk) #second item optional if not using Nav Bar
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

dpi=100.  #this is the default value with matplotlib
root = tkinter.Tk()
root.wm_title("Embedding in Tk")
#px=1/plt.rcParams['figure.dpi']
px=1/dpi #can use this if dpi known.
#fig = Figure(figsize=(5, 4), dpi=100)
fig = Figure(figsize=(600*px, 400*px)) #same as previous but uses pixels
#plt.axes.get_xaxis().set_visible(False)

t = np.arange(0, 50, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#.set_frame_on(False)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP)#, fill=tkinter.BOTH, expand=2)
#toolbar = NavigationToolbar2Tk(canvas, root) #comment out to remove tool bar
#toolbar.update() #not needed
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1) #not needed

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect("key_press_event", on_key_press)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.