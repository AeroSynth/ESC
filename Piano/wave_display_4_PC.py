'''
https://pyshine.com/How-to-make-a-real-time-voice-plot/

'''


# Quickly import essential libraries
import queue
#import sys
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
#from matplotlib.backend_tools import ToolBase, ToolToggleBase #bcs

# Lets define audio variables
# We will use the default PC or Laptop mic to input the sound
''' Note:  for external USB, need to enable it in settings '''

device = 1#6#0 # id of the audio device by default
window = 50#32#128#512 #1000# window for the data.  Same as time base
downsample = 1 # how much samples to drop
channels = [2] # a list of audio channels
print(channels,len(channels))
interval = 20 # this is update interval in miliseconds for plot.  May need to increase if window size too long

# lets make a queue
q = queue.Queue()
q1 = queue.Queue()

# Please note that this sd.query_devices has an s in the end.
device_info =  sd.query_devices(device, 'input')
di=sd.query_devices()
print(di)
print("devices",device_info)
print(device_info)

samplerate = device_info['default_samplerate']
samplerate= 16000#22050#44100#11025#22050
length  = int(window*samplerate/(1000*downsample))


# lets print it 
print("Sample Rate: ", samplerate)
print(length)

# Now we require a variable to hold the samples 
#plotdata =  np.zeros( (length,len(channels)) )
plotdata =  np.zeros( (length,channels[0]) )
# Lets look at the shape of this plotdata 
print("plotdata shape: ", plotdata.shape)
# So its vector of length 44100
# Or we can also say that its a matrix of rows 44100 and cols 1

# next is to make fig and axis of matplotlib plt
plt.rcParams['toolbar'] = 'None' #bcs first, turn off toolbar
fig = plt.figure(figsize=(18,10),facecolor='grey') #set color of center line

bx = fig.add_subplot(121)# 2 ro2s, 1 column, plot #1
ax = fig.add_subplot(122)

ax.set_facecolor((0,0,0))
bx.set_facecolor((0,0,0))
#remove tick marks
ax.set_yticks([])
bx.set_yticks([])
ax.set_xticks([])
bx.set_xticks([])

#Adjust size and position of both subplots
plt.subplots_adjust(left=0.0025,
                    bottom=0.,
                    right=1.,
                    top=1.,
                    wspace=0.005,
                    hspace=0.0)
#plt.tight_layout(pad=.05) #bcs

# lets set the title
#bx.set_title("Left Side")
#ax.set_title("Right Side")
#set line colors and width.
lines = ax.plot(plotdata,color = (0,1,0.29))#color = 'g',linewidth=5
linesb = bx.plot(plotdata,color = (0,1,0.29))#color = 'g',linewidth=5

ax.autoscale(tight=True) #remove padding from X plots
bx.autoscale(tight=True)

#set vertical range
ax.set_ylim(bottom=-.9,top=.9)
bx.set_ylim(bottom=-.9,top=.9)

# We will use an audio call back function to put the data in queue
def audio_callback(indata,frames,time,status):
    q.put(indata[::downsample,[0]])
    q1.put(indata[::downsample,[1]])

# now we will use an another function 
# It will take frame of audio samples from the queue and update
# to the lines

def update_plot(frame):

    global plotdata, plot_side
    #plot left channel
    if plot_side==True:
        plot_side = False
        while True:

            try: 
                data = q.get_nowait()
                #data1=q1.get_nowait()
            except queue.Empty:
                break
                
            shift = len(data)
            plotdata = np.roll(plotdata, -shift,axis = 0)
        # Elements that roll beyond the last position are 
        # re-introduced 
        #while True:
            plotdata[-shift:,:] = data
            #plotdata[-1:]=0
  
        for column, line in enumerate(linesb):
            line.set_ydata(plotdata[:,column])
            #plot_side=False
            return linesb
            
    #plot right channel
    if plot_side==False:
        plot_side = True
        while True:

            try: 
                #data = q.get_nowait()
                data=q1.get_nowait()
            except queue.Empty:
                break
                
            shift = len(data)
            #print(shift)
            plotdata = np.roll(plotdata, -shift,axis = 0)
        # Elements that roll beyond the last position are 
        # re-introduced 
        #while True:
            plotdata[-shift:,:] = data
            #plotdata[-1:]=0
            
        for column, line in enumerate(lines):
            line.set_ydata(plotdata[:,column])
            #plot_side=False
            return lines

""" Main Routine """
plot_side = True

#set up for full screen
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
#mng.resize(*mng.window.maxsize())
#define the audio stream
stream  = sd.InputStream( device = device, channels = max(channels), samplerate = samplerate, callback  = audio_callback)
#set up matplotlib animation
ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
#ani1  = FuncAnimation(fig,update_plot1, interval=interval,blit=True)

with stream:
    plt.show()
    
 

