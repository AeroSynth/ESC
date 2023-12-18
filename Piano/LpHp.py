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


''' FIR Filter Sub routines.  Not all used'''
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
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        sos = butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos, data)
        return y

# def butter_bandpass(lowcut, highcut, fs, order=5):
#     return butter(order, [lowcut, highcut], fs=fs, btype='band')
# 
# def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
#     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#     y = lfilter(b, a, data)
#     return y

def destroy_window(event):
    global frame_count, start_time
    print("Destroy...")
    frame_rate = frame_count / (time.time() - start_time)
    print('average frame rate = {0:.2f} FPS'.format(frame_rate))
    quit()

if True:#__name__ == "--main--":
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.fftpack import fft
    from scipy.signal import butter, lfilter, freqz, sosfreqz, sosfilt
    from scipy import signal
    import time
    from matplotlib.ticker import ScalarFormatter, NullFormatter
    #from tkinter import TclError

    # constants
    CHUNK = 1024 * 2             # samples per frame
    FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
    CHANNELS = 1                 # single channel for microphone
    RATE = 22050#44100           # samples per second

    #set type of filter
    IIR = False

    ''' Set max signal range '''
    AMPLITUDE_LIMIT = 4096
    AMPLITUDE_LIMITh = 16000
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

    ax2 = fig.add_subplot(122)# 1 row, 2 columns, first column 
    ax1 = fig.add_subplot(121)# 1 row, 2 columns, second column

    ax2.set_facecolor((.1,0,0))
    ax1.set_facecolor((.0,.0,0))

    #remove tick marks
    ax2.set_yticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax1.set_xticks([])

    #remove padding from X plots
    ax1.autoscale(tight=True)
    ax2.autoscale(tight=True)

    #Adjust size and position of both subplots
    border = .04
    #thickness of border 
    plt.subplots_adjust(left=border,
                        bottom=border*2,#,.1,
                        right=1.-border,
                        top=1.-.03,
                        wspace=0.01, #center bar
                        hspace=0.1) #not sure what this does

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()  #comment out to supress full screen display

    # create a line object with random data
    LeftLine, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
    RightLine, = ax2.plot(x, np.random.rand(CHUNK), 'r-', lw=2)

    #ax1.set_title('Low Frequency')
    ax1.set_xlabel('Low Frequencies',fontsize=24)
    ax2.set_xlabel('High Frequencies',fontsize=24)

    #set vertical limits
    ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
    ax2.set_ylim(-AMPLITUDE_LIMITh, AMPLITUDE_LIMITh)

    print('stream started')

    # for measuring frame rate
    frame_count = 0
    start_time = time.time()
   
    '''	Set the high-pass, low-pass, and band-pass filter settings ********
        Note:  not all used
    '''
    #filter order
    HPorder = 6 
    BPlorder = 6
    BProrder = 6
    LPorder = 6
    #filter cuttoff frequency (-3dB point)
    BPlLow = 20 #left figure
    BPlHigh = 200
    BPrLow = 200 #left figure
    BPrHigh = 4500

    HPcutoff = 5
    200
    LPcutoff = 200
    while True:#frame_count < 30:#True:
        # binary data
        data = stream.read(CHUNK)    
        data_np = np.frombuffer(data, dtype= 'h') #h=16-bit signed int, same as i2
        #HPdata = butter_highpass_filter(data_np, HPcutoff, RATE, HPorder)
        #LPdata = butter_lowpass_filter(data_np, LPcutoff, RATE, LPorder)
        BPlData = butter_bandpass_filter(data_np, BPlLow, BPlHigh ,RATE, BPlorder)
        BPrData = butter_bandpass_filter(data_np, BPrLow, BPrHigh ,RATE, BProrder)
        
        #RightLine.set_ydata(HPdata)
        RightLine.set_ydata(BPrData)
        LeftLine.set_ydata(BPlData)
        #LeftLine.set_ydata(LPdata)
        
        plt.show()
        plt.pause(.001)

        frame_count += 1

    plt.close()
    frame_rate = frame_count / (time.time() - start_time)
            
#     print('stream stopped')
#     print(frame_rate)
#     #print('average frame rate = {:.2f} FPS'.format(frame_rate))
    

#    exit()
