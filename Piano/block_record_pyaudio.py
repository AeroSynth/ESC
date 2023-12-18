import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import sounddevice as sd
import time
from scipy.fftpack import fft

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
#fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()


# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

plt.ion()
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
bx = fig.add_subplot(121)
line1, = bx.plot(x, xf, 'b-')
line2, = ax.semilogx(x, xf, 'r-')
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
