"""
Notebook for streaming data from a microphone in realtime

audio is captured using pyaudio
then converted from binary data to ints using struct
then displayed using matplotlib

scipy.fftpack computes the FFT

if you don't have pyaudio, then run

>>> pip install pyaudio

note: with 2048 samples per chunk, I'm getting 20FPS
when also running the spectrum, its about 15FPS
"""

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError

# to display in separate Tk window
#%matplotlib tk

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100#22050                 # samples per second

#plt.ion()
plt.rcParams['toolbar'] = 'None' #bcs first, turn off toolbar
fig = plt.figure(figsize=(12,6),facecolor='grey') #set color of center line
#fig = plt.figure(figsize=(12,6))
ax2 = fig.add_subplot(111)
ax1 = fig.add_subplot(121)


#ax1.set_facecolor((0,0,0))
#ax2.set_facecolor((0,0,0))
#remove tick marks
ax1.set_yticks([])
ax2.set_yticks([])
ax1.set_xticks([])
ax2.set_xticks([])
ax2.autoscale(tight=True) #remove padding from X plots
ax1.autoscale(tight=True)

# create matplotlib figure and axes
#fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()




# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 4096

# format waveform axes
# ax1.set_title('AUDIO WAVEFORM')
# ax1.set_xlabel('samples')
# ax2.set_ylabel('volume')
# ax2.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
# ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

# format spectrum axes
ax2.set_xlim(20, RATE / 2)

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)
print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()
count=0
# 
while frame_count<100:#True:
    
    # binary data
    data = stream.read(CHUNK)    

    data_np = np.frombuffer(data, dtype='h')
    
    line.set_ydata(data_np)#20*np.log10(data_np))
    
    # compute FFT and update line
    yf = fft(data_np)
    line_fft.set_ydata(np.abs(yf[0:CHUNK]) *2 / (AMPLITUDE_LIMIT * CHUNK))
    line_fft.set_ydata(np.abs(yf[0:CHUNK])  / (512 * CHUNK))
    
    # update figure canvas
    try:
        plt.show(block=False)
        plt.pause(.01)
        #fig.canvas.draw()
        #fig.canvas.flush_events()
        frame_count += 1
        
    except KeyboardInterrupt:
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
    
frame_rate = frame_count / (time.time() - start_time)
    
print('stream stopped')
print('average frame rate = {:.0f} FPS'.format(frame_rate))

