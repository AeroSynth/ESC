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

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import butter, lfilter, freqz
from scipy import signal
import time
#from tkinter import TclError

''' FIR Filter Sub routines '''
# Butterworth FIR Low Pass Filter 
def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_highpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='high', analog=False)

# Butterworht Low Pass Filter coefficients to plot frequency response
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 22050#44100           # samples per second

'''******** Set the high-pass and low pass filter settings ********'''
#filter order
HPorder = 6 
HP1oder = 3
LPorder = 6
#filter cuttoff frequency (-3dB point)
HP1cutoff = 30 
HPcutoff = 500
LPcutoff = 500

#set type of filter
IIR = False

''' If dispFFT true, FFT is displayed on right screen and full bandwidth audio on left screen.
    Else low frequency analog is left, high frequency on right
'''
dispFFT = True

''' Set max signal range '''
AMPLITUDE_LIMIT = 32000#4096

# pyaudio class instance
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

#next is to make fig and axis of matplotlib plt
#plt.rcParams['toolbar'] = 'None' #bcs first, turn off toolbar
plt.ion()
fig = plt.figure(figsize=(18,5),facecolor='grey') #set color of center line

ax1 = fig.add_subplot(111)# 2 ro2s, 1 column, plot #1
ax2 = fig.add_subplot(121)
#ax3 = fig.add_subplot(133)

ax2.set_facecolor((0,0,0))
ax1.set_facecolor((.1,.1,0))

#remove tick marks
ax2.set_yticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax1.set_xticks([])

#remove grid marks
ax1.grid(False)
ax2.grid(False)

#Adjust size and position of both subplots
border = .05    #thickness of border 
plt.subplots_adjust(left=border,
                    bottom=border,
                    right=1.-border,
                    top=1.-border,
                    wspace=0.01, #center bar
                    hspace=0.0) #not sure what this does

# create matplotlib figure and axes
#fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()  #comment out to supress full screen display

# create a line object with random data
LeftLine, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
RightLine, = ax2.plot(x, np.random.rand(CHUNK), '-', lw=2)


ax1.set_title('Low Frequency')
ax2.set_title('High Frequency')

ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax2.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
# ax1.set_xlim(0, 2 * CHUNK)
#plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()
#
sosHP = signal.butter(LPorder, LPcutoff, 'hp', fs=RATE, output='sos')
sosLP = signal.butter(LPorder, LPcutoff, 'lp', fs=RATE, output='sos')

while frame_count < 100:#True:
    
    # binary data
    data = stream.read(CHUNK)    
    #data[0:10]=b'0'
    data_np = np.frombuffer(data, dtype= 'h') #h=16-bit signed int, same as i2
    #data_np[0:10]=0
    if IIR == True:
        #sos = signal.butter(LPorder, HPcutoff, 'hp', fs=RATE, output='sos')
        HPdata = signal.sosfilt(sosHP, data_np)
        #sos = signal.butter(LPorder, LPcutoff, 'lp', fs=RATE, output='sos')
        LPdata = signal.sosfilt(sosLP, data_np)
    else:
        HPdata = butter_highpass_filter(data_np, HPcutoff, RATE, HPorder)
        LPdata = butter_lowpass_filter(data_np, LPcutoff, RATE, LPorder)
        #print('FIR')
    
    RightLine.set_ydata(HPdata)
    LeftLine.set_ydata(LPdata)
   
    #yf = butter_lowpass_filter(data_np, LPcutoff, RATE, LPorder)
    
        #print(np.max(yf),np.argmax(yf,axis=0)*11025/(2*CHUNK))
        #line_fft.set_ydata(np.abs(yf[0:CHUNK])  / (CHUNK/4 * CHUNK))
    
         
    # update figure canvas
    plt.show()
    plt.pause(.001)

    frame_count += 1

plt.close()
frame_rate = frame_count / (time.time() - start_time)
        
print('stream stopped')
print('average frame rate = {:.0f} FPS'.format(frame_rate))
quit()