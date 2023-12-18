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
when also running the spectrum, its about 8-11 FPS
"""

import pyaudio

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import butter, lfilter, freqz
from scipy import signal
import time
from matplotlib.ticker import ScalarFormatter, NullFormatter
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

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def destroy_window(event):
    global frame_count, start_time
    print("Destroy...")
    frame_rate = frame_count / (time.time() - start_time)
    print('average frame rate = {:.0f} FPS'.format(frame_rate))
    quit()
    
# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 22050#44100           # samples per second

'''******** Set the high-pass and low pass filter settings ********'''
#filter order
HPorder = 6 
BPorder = 3
LPorder = 6
#filter cuttoff frequency (-3dB point)
BPlow = 30
BPhigh = 500
HPcutoff = 500
LPcutoff = 500

#set type of filter
IIR = False#True

''' Set max signal range '''
AMPLITUDE_LIMIT = 64000#4096

# pyaudio class instance
p = pyaudio.PyAudio()

#list all input devcice
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ",              
              p.get_device_info_by_host_api_device_index(0, i).get('name'))

# for i in range(p.get_device_count()):
#      print( p.get_device_info_by_index(i))

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK,
    input_device_index=1
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

#next is to make fig and axis of matplotlib plt
plt.rcParams['toolbar'] = 'None' #bcs first, turn off toolbar
plt.rcParams["keymap.quit"] = ['enter', 'q'] #exit plot with one of three keys

plt.ion()

fig = plt.figure(figsize=(18,5),facecolor='grey') #set color of center line
fig.canvas.mpl_connect('close_event', destroy_window)#only way to close this style of program

# ax1 = fig.add_subplot(131)# 1 row, 2 columns, first column 
# ax2 = fig.add_subplot(132)# 1 row, 2 columns, second column
# ax3 = fig.add_subplot(133)

ax1 = fig.add_subplot(221)# divide as 2x2, plot top left
ax2 = fig.add_subplot(222)# divide as 2x2, plot top right
ax3 = fig.add_subplot(212)# divide as 2x1, plot bottom

ax2.set_facecolor((0,0,0))
ax1.set_facecolor((.1,.1,0))
ax3.set_facecolor((0,0,0))

#remove tick marks
ax2.set_yticks([])
ax1.set_yticks([])
ax3.set_yticks([])
ax2.set_xticks([])
ax1.set_xticks([])
#ax3.set_xticks([])

#remove padding from X plots
ax1.autoscale(tight=True)
ax2.autoscale(tight=True)
ax3.autoscale(tight=True)

#remove grid marks
ax1.grid(False)
ax2.grid(False)
#define grid marks for bottom
ax3.grid(True,which='both',ls='-',color='w',lw=.3)



#Adjust size and position of both subplots
border = .01    #thickness of border 
plt.subplots_adjust(left=border,
                    bottom=.1,
                    right=1.-border,
                    top=1.-.03,
                    wspace=0.005, #center bar
                    hspace=0.1) #not sure what this does

# create matplotlib figure and axes
#fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()  #comment out to supress full screen display

# create a line object with random data
LeftLine, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
RightLine, = ax2.plot(x, np.random.rand(CHUNK), 'r-', lw=2)

# create semilogx or linear line for spectrum
line_fft, = ax3.semilogx(xf, np.random.rand(CHUNK), 'g-', lw=2)
#ax3.set_xticks( np.geomspace(100, 10000 ).round() ) #alternative log setup

#or create linear plot.
#line_fft, = ax3.plot(xf, np.random.rand(CHUNK), 'g-', lw=2)

#could use seaborn for histobram plot
#ax3 = sns.histplot(xf, np.random.rand(CHUNK), 'g-', lw=2)


ax1.set_title('Low Frequency')
ax2.set_title('High Frequency')
ax3.set_title('FFT')

ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax2.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax3.set_xlim(50, 4 * CHUNK)
#plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

#try to remove scientific notation on bottom display
for axis in [ax3.xaxis]:
    axis.set_major_formatter(ScalarFormatter())
    axis.set_minor_formatter(NullFormatter())
   
#ax3.xaxis.set_major_formatter(ScaleFormatter())

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()
#
#initialize IIR values
sosHP = signal.butter(LPorder, LPcutoff, 'hp', fs=RATE, output='sos')
sosLP = signal.butter(LPorder, LPcutoff, 'lp', fs=RATE, output='sos')

while True:#frame_count < 30:#True:
    
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
        BPdata = LPdata
    else:
        HPdata = butter_highpass_filter(data_np, HPcutoff, RATE, HPorder)
        #HPdata=data_np
        #LPdata = butter_lowpass_filter(data_np, LPcutoff, RATE, LPorder)
        #LPdata=data_np
        BPdata = butter_bandpass_filter(data_np, BPlow, BPhigh ,RATE, BPorder)
    
    
    RightLine.set_ydata(HPdata)
    #LeftLine.set_ydata(LPdata)
    LeftLine.set_ydata(BPdata)
   
    # compute FFT and update line
    yf = fft(data_np)
    yf = np.abs(yf[0:CHUNK])  / (CHUNK/2 * CHUNK)
    line_fft.set_ydata(yf)

    plt.show()
    plt.pause(.001)

    frame_count += 1

plt.close()
frame_rate = frame_count / (time.time() - start_time)
        
print('stream stopped')
print('average frame rate = {:.0f} FPS'.format(frame_rate))

exit()#quit()