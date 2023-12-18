"""
https://www.youtube.com/watch?v=aQKX3mrDFoY
https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/audio%20spectrum_pt2_spectrum_analyzer.ipynb
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
#import os
#import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
#from tkinter import TclError

# to display in separate Tk window
#%matplotlib tk

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 22050#44100                 # samples per second

p = pyaudio.PyAudio()

# for i in range(p.get_device_count()):
#      print( p.get_device_info_by_index(i))

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

#next is to make fig and axis of matplotlib plt
plt.rcParams['toolbar'] = 'None' #bcs first, turn off toolbar
fig = plt.figure(figsize=(18,5),facecolor='grey') #set color of center line
#fig.canvas.mpl_connect('close_event', destroy_window)#only way to close this style of program
ax1 = fig.add_subplot(121)# 2 ro2s, 1 column, plot #1
ax2 = fig.add_subplot(122)

ax2.set_facecolor((0,0,0))
ax1.set_facecolor((.1,.1,0))

#remove tick marks
ax2.set_yticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax1.set_xticks([])

ax1.grid(False)
ax2.grid(False)
#Adjust size and position of both subplots
border=.05
plt.subplots_adjust(left=border,
                    bottom=border,
                    right=1.-border,
                    top=1.-border,
                    wspace=0.01, #center bar
                    hspace=0.0) #not sure what this does

# create matplotlib figure and axes
#fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
# pyaudio class instance


# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

#remove tick marks
# ax2.set_yticks([])
# ax1.set_yticks([])
# ax2.set_xticks([])
# ax1.set_xticks([])

# Signal range is -32k to 32k
# limiting amplitude 
AMPLITUDE_LIMIT = 16000#4096

# format waveform axes
ax1.set_title('TIME DOMAIN')
ax2.set_title('FREQUENCY DOMAIN')
# ax1.set_xlabel('samples')
#ax1.set_ylabel('Amplitude')
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
# ax1.set_xlim(0, 2 * CHUNK)
#plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

# format spectrum axes
ax2.set_xlim(30, RATE / 2)
plt.ion()

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()
# 
while frame_count < 200:#True:
    
    # binary data
    data = stream.read(CHUNK)    
    #data[0:10]=b'0'
    data_np = np.frombuffer(data, dtype= 'h') #h=16-bit signed int, same as i2
    #data_np[0:10]=0
    line.set_ydata(data_np)
    
    
    # compute FFT and update line
    yf = fft(data_np)
    #yf=np.log10(yf)
    yf = np.abs(yf[0:CHUNK])  / (CHUNK/4 * CHUNK)
    #print(np.max(yf),np.argmax(yf,axis=0)*11025/(2*CHUNK))
    #line_fft.set_ydata(np.abs(yf[0:CHUNK])  / (CHUNK/4 * CHUNK))
    line_fft.set_ydata(yf)#np.abs(yf[0:CHUNK])  / (CHUNK/4 * CHUNK))
    
    
    # update figure canvas
    #try:
    plt.show()
    plt.pause(.001)
#         fig.canvas.draw()
#         fig.canvas.flush_events()
    frame_count += 1
        
        
#     except KeyboardInterrupt:
#         
#         # calculate average frame rate
#         frame_rate = frame_count / (time.time() - start_time)
#         
#         print('stream stopped')
#         print('average frame rate = {:.0f} FPS'.format(frame_rate))
#         break

plt.close()
frame_rate = frame_count / (time.time() - start_time)
        
print('stream stopped 1')
print('average frame rate = {:.0f} FPS'.format(frame_rate))
quit()