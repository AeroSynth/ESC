from tkinter import *

# Press a buton in keyboard
def PressAnyKey(label):#label):
   #print(label)
   value = label.char
   print(value, ' A button is pressed')

base = Tk()
base.geometry('300x150')
base.bind('<Key>', PressAnyKey)#lambda i : PressAnyKey(i))
mainloop()