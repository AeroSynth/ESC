import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time
from scipy.fftpack import fft

bufSize=512
x = np.linspace(0, bufSize,num=bufSize)
#y = np.sin(x)
y=np.zeros(bufSize)

plt.ion()
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
bx = fig.add_subplot(121)
line1, = bx.plot(x, y, 'b-')
line2, = ax.semilogx(x, y, 'ro-')
i=0
bx.set_ylim(-1.,1)#time domain limits
ax.set_ylim(0,.1) #fft window limits
for i in range(0,40):#phase in x:#np.linspace(0, 10*np.pi, 100):
    print(i)
    i+=1
    #plt.clf()
    data = sd.rec(bufSize,samplerate=11025,channels=1)
    sd.wait()
    fft_out=fft(data)
    #data[0:4]=data[4:8]
    #line1.set_ydata(np.sin(0.5 * x + phase))
    #line1.set_ydata(data)
    line2.set_ydata(np.abs(fft_out))
    #fig.canvas.draw()
    #plt.draw()
    plt.show(block=False)
    plt.pause(.01)

#time.sleep(4)
plt.close()
