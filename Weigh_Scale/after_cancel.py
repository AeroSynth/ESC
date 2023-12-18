#! /usr/bin/env python
from tkinter import *
import time
import random


tk = Tk()
canvas = Canvas(tk, width=1920, height=1080, background="grey")
canvas.pack()

def xy(event):
    xm, ym = event.x, event.y

def task():
    w=random.randint(1,1000)
    h=random.randint(1,1000)
    canvas.create_rectangle(w,h,w+150,h+150)
    def callback(event):
        if True:  # not sure why this is here...
            print(event,"clicked2")    
            tk.after_cancel(tk.after_id)    # cancel it
    canvas.bind("<Button-1>",callback)        
    tk.after_id = tk.after(1000,task)
    print(tk.after_id)
    # ^^^^^^^^^^^ this captures the after ID for later canceling.
#tk.after(1000,task)
task()
# no need to capture this ID since there's no way to cancel it yet

tk.mainloop()   