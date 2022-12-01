'''
Weigh Class to determine parameters from weigh scale,
for example how high one jumps.
Assumes Sample rage of 12.5ms (80Hz)
Example here:  https://stackoverflow.com/questions/13320262/calculating-the-area-under-a-curve-given-a-set-of-coordinates-without-knowing-t
'''
import numpy as np
#from scipy.integrate import simps #simpsons rule for inegration.  More accurate than trapazoid rule
import matplotlib.pyplot as plt
#from scipy.signal import find_peaks
import tkinter as tk
from tkinter import messagebox


class Weigh:

    def __init__(self,data):
        self.data = data
        print("Data lengh, type",len(self.data), type(self.data))
        #plt.ion()

    def plot_it(self):
        #plt.style.use('fivethirtyeight')#ggplot')
        #plt.style.use('dark_background')
        plt.style.use('classic')
        fig=plt.figure(figsize=(9,8)) #sets size of window.
        ax = fig.add_subplot(111)# 2 rows, 1 column, plot #1
        ax.set(xlabel='Samples', ylabel="Newtons",title="How High Can You Jump?")
        ax.grid(True)
        
        #bx = fig.add_subplot(212)# plot #2 to show gradient
        #bx.set(xlabel='Time (ms)', ylabel="Gradient")
        #bx.grid(True)
        #fig.subplots_adjust(bottom=0.20) #allows room for buttons        
        #plot top plot with data
        xaxis= np.arange(0,len(self.data))
        ax.plot(xaxis,self.data,color='g')      
        m0 = np.argmin(data) #find min value in array
        print(m0)
        m0=int(m0-.005*m0) #go back 0.5% of y axis.
        ''' try walking back from min value to find thresh? '''
        ''' TRY FILTER '''
        #m0=m0-1 #causes error???
        #m0=206  
        print(m0)
        thresh = data[m0]
        print(thresh)
        m1=m0
        while data[m1] <= thresh: #walk through min values to find endpoint
            m1 += 1
        m1=m1-1    
        #m1 = data[m0:m0+20]
        #print(m0,m0-int(.01*m0))
        print(m0,m1)
        
        t=(m1-m0)/2
        t=t/80
        print('time =', t)
        h = (t**2)*9.81/2
        print('Jump Height =',round(h,3), 'meters ', round(h*100,3),
              'cm', round(h*39.37,2),'inches')
        print('Air Time =', round(t*2,3),'seconds')
        
        
        #tk.messagebox.showinfo('Results',message=str(h))
        #plot filtered data
        self.ma=self.moving_average(self.data,2)
        ax.plot(xaxis,self.ma)#,'y')
        ax.plot(xaxis[m0],self.ma[m0],'ro') 
        ax.plot(xaxis[m1],self.ma[m1],'ro')
        print(m0,m1,self.data[m0],self.data[m1])
        plt.pause(0.001)
        plt.show()
        
              
    def derivative(self):
        print("derivative")
        #self.datad = np.diff(self.data)
        self.datad = np.gradient(self.data)
        #self.datad = np.append(self.datad,self.datad[0])#adjust array size if using diff
              
#moving average filter array c of len n    
    def moving_average(self,c, n=8): 
        ret = np.cumsum(c)
        ret[n:] = ret[n:] - ret[:-n] #normal 
        mv=ret/n #return same array size
        mv[0:n-1]=mv[n] #fill end with mv[n]
        return mv
    
'''
Test Program
'''
from numpy import savetxt #used to save nparray as .csv file
path = './'#C:/Repo/EugeneScienceCenter/WeighScale/'

data = np.loadtxt('brad.csv')#'tim_7-8in.csv')
data=np.array(data,dtype=float)
w=Weigh(data)
w.plot_it()
calib = 210



              
