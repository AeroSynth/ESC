'''
UO/ESC Speech Perception and Recognitioin Exhibit Application

Need to add licese info

Software written by Brad Stewart and Jeff Elms

Jan 16 2022
    * added root.after where listen_phrase is invoked.
    * add listen_phrase_button called directly by event.
        Need to change command name in UO_Linguistics.py to 'listen_phrase_button'
'''

import sys
import os
import tkinter as tk
import sounddevice as sd
from time import perf_counter
from tkinter import ttk
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import time 
import json
#from pynput.mouse import Listener #respond to mouse clicks.
from threading import *
#import vlc #media player

def set_Tk_var():
    global che45
    che45 = tk.IntVar() #check button (playback speed)
    global selectedButton
    selectedButton = tk.IntVar() #radio buttons (reveal)
    global selectedPhrase
    selectedPhrase = tk.IntVar() #radio buttons (select phrase for display/playback)

### Global Values ###
'''for now, phrasess are hard-coded. For future, put into the json file'''
PHRASE =["1...2...3...4...5\n6...7...8...9...10", \
"Ducks are great!", \
"Have a nice day", \
"Hello", "How are you?", \
"My name is ...\nWhat is your name?"]

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    global jdata,language_choice
    global sdata#, mouse_event, t1,listener,elapsed,pFlah,player
    global mouse_event,tl,recFlag
   
    w = gui
    top_level = top
    root = top
    root.protocol("WM_DELETE_WINDOW", on_closing)
                   
    w.Radiobutton1_6.select() #start with English button enabled
    sdata=[0]*10000
    init_plot(w.Frame5) #initialize top waveform display
    init_plot(w.Frame6)
    plot_recording(False) #init recording display
    #open the json file 
    f= open('config.json',encoding='utf8')
    #load the json file into jdata as a dictionary
    jdata = json.load(f)
    language_choice = 5 #start with english

    # set up a timer thread to play attention video
    mouse_event=False
    recFlag = 0 #allows recording once after button press.
    #t1 = Play_Video("UO Linguistics Attract Loop.mp4",60)
    #t1.start() #start it
    
'''     
### set up mouse event listener 
    listener = Listener(on_click=clicker,on_move=move)
    listener.start()
    print("listener invoked")
'''
def on_closing():
    destroy_window()    
    print("system exit")
    sys.stdout.flush()
    sys.exit()
'''                   
#mouse click listener thread
def clicker(x,y,button,pressed):
    global mouse_event#, elapsed,pFlag
    print("mouse clicked")
    mouse_event=True
def move(x,y):
    global mouse_event
    mouse_event = True

#play video thread
class Play_Video(Thread):
    def __init__(self,filename,wait):
        
        #call the Thread class init function
        Thread.__init__(self)
        self.filename=filename
        self.waitTimer = wait
        #self.pFlag = False #flag to indicate playing video
        self.tFlag = False #flag to turn on off timer
        self.haltFlag = False
        

    #override the run function of the Thread class
    def run(self):

        #create an instance of the VLC player
        self.mplayer = vlc.Instance('--input-repeat=999999')  
        self.player = self.mplayer.media_player_new(self.filename)
        self.player.set_fullscreen(True) 
        #self.player = vlc.MediaPlayer(self.filename)
        #self.player.set_fullscreen(True)
        #em = self.player.event_manager()
        #em.event_attach(vlc.EventType.MediaPlayerEndReached, self.onEnd)
        self.elapsed = 0
        self.Vstart()
        
    """run a timer and reset if mouse event occurs
       If it times out, start the video and loop it unti another
       mouse our touch event occurs """ 
    def Vstart(self): 
        global mouse_event
       
        while True:
            if True:#self.tFlag == False:
                print(self.elapsed)#
                time.sleep(1)
                self.elapsed += 1
                               
            if mouse_event == True: #reset timer if mouse click event
                self.elapsed = 0
                mouse_event=False
                #self.pFlag = False
                self.tFlag = False
                self.player.stop()

            if (self.elapsed == self.waitTimer): #start video if time elapsed
                #root.withdraw()
                self.tFlag=True
                time.sleep(1)
                self.player.play()
                
            if self.haltFlag: #way to get out of infinite loop
                break

    def halt(self):
        self.haltFlag= True
'''          
   
### get a list of languages in json file ###
def get_languages():
    return list(jdata['languages'].keys())    

# set all phrase button labels to "Phrase n"
def clear_phraseButtons():
    global recFlag
    recFlag=0
    pblist = [w.Radiobutton2_1, w.Radiobutton2_2, w.Radiobutton2_3, \
                 w.Radiobutton2_4, w.Radiobutton2_5, w.Radiobutton2_6]
    #sd.stop()
    i=1
    print("clear_phrasebutton")
    for wdgt in pblist:
        #print()        
        wdgt.config(text="Phrase "+str(i))
       # wdgt.deselect()
        i+=1

def deselect_phraseButtons():
    pblist = [w.Radiobutton2_1, w.Radiobutton2_2, w.Radiobutton2_3, \
                 w.Radiobutton2_4, w.Radiobutton2_5, w.Radiobutton2_6]
    print("deselect_phrasebutton")
    for wdgt in pblist:         
        #pass
        wdgt.deselect()
    sd.stop() #stop audio playback   
    
### select phrase ###
def phrase_select(n: int):
    global phrase_choice,language_choice,file_list,jdata
    sd.stop()
    #phrase_choice = n
    #print(phrase_choice)
    if n is not None and language_choice is not None:
        ll = jdata['languages'][get_languages()[language_choice]]
        file_list = [ os.path.join('data', ll['dir'], x['file']) for x in ll['phrases'] ]

        if n < len(file_list):
            print(file_list[n])
            return file_list[n]
        else:
            print("error load_sound {}".format(n))
    clear_phraseButtons()

#Initialize the waveform for display into a frame
def init_plot(myframe):
    global w
    global fig,plt,plt_canvas,f    
   
    f=ttk.Frame(myframe)
    clear_phraseButtons()
    fig=Figure()
    plt = fig.add_subplot()
    fig.subplots_adjust(bottom=0.0, right=1.04, left=-.06, top=1.,wspace=0.0)
    plt_canvas = FigureCanvasTkAgg(fig, f)

    plt.set_frame_on(False)
    #plt.get_xaxis().set_visible(False)
    #plt.get_yaxis().set_visible(False)
    #print("init")
    #plt.ion()

#clear out the waveform in a frame.  Necessary to destroy it.
def clear_plot(myframe):
    global w
    sd.stop()

    for widget in myframe.winfo_children():
        widget.destroy()
    init_plot(myframe)

#read the wavefile and display data into the frame passed to this function 
def plot_phrase(wfile,myframe):    
    global w,f,fig,plt,plt_canvas,sdata,samplerate
    sd.stop()
    #t0=perf_counter()
    clear_plot(myframe)
    #t0=perf_counter() #debug
    samplerate, sdata = wavfile.read(wfile)
    length = sdata.shape[0] / samplerate
    #print(length) #debug
    f.pack(fill=tk.BOTH) #add figure
    
    plt_canvas._tkcanvas.pack(fill=tk.BOTH) #add canvas
    time=np.linspace(0.,(len(sdata)/samplerate),(len(sdata))) #x axis values

    plt.plot(time,sdata[:],linewidth=.4)
    #t1=perf_counter() #debug
    #print(t1-t0) #debug -- time it takes to plot
    
### LANGUAGE SELECTION -------------------------------------------#
### ['Spanish', 'French','Japanese', 'Ichishkiin', 'Mandarin', 'English']
    
def english():
    global language_choice
    print('brad_mpl_support.english')
    language_choice = 5
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
def spanish():
    global language_choice
    print('brad_mpl_support.spanish')
    #sys.stdout.flush()
    language_choice = 0
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
def french():
    global language_choice
    print('brad_mpl_support.french')
    language_choice = 1
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
def ichishkiin():
    global language_choice
    print('brad_mpl_support.ichishkiin')
    language_choice = 3
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
def japanese():
    global language_choice
    print('brad_mpl_support.japanese')
    language_choice = 2
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
def mandarin():
    global language_choice
    print('brad_mpl_support.mandarin')
    language_choice = 4
    print(language_choice)
    deselect_phraseButtons()
    plot_phrase("silence.wav",w.Frame5)
    
# END OF LANGUAGE SELECTION ---------------------------------------#

# LOAD WAVEFORM INTO DISPLAY --------------------------------------#
# calling listen_phrase() #this by itself often causes alsa under-run errors
# so fixed by delaying the tkinter loop using 'after'
def ph1():
    print('brad_mpl_support.ph1')
    plot_phrase(phrase_select(0),w.Frame5) 
    che45.set(0) #set playback speed to normal
    #root.after(500,lambda:listen_phrase()) #lambda useful if passing parameters to function
    root.after(100,listen_phrase)

def ph2():
    print('brad_mpl_support.ph2')
    plot_phrase(phrase_select(1),w.Frame5)
    che45.set(0)
    #listen_phrase() #this by itself often causes alsa under-run errors
    root.after(100,listen_phrase)

def ph3():
    print('brad_mpl_support.ph3')
    #sys.stdout.flush()
    plot_phrase(phrase_select(2),w.Frame5)
    che45.set(0)
    root.after(100,listen_phrase)#listen_phrase()

def ph4():
    print('brad_mpl_support.ph4')
    #sys.stdout.flush()
    plot_phrase(phrase_select(3),w.Frame5)
    che45.set(0)
    root.after(100,listen_phrase)#listen_phrase()

def ph5():
    print('brad_mpl_support.ph5')
    #sys.stdout.flush()
    plot_phrase(phrase_select(4),w.Frame5)
    che45.set(0)
    root.after(100,listen_phrase)#listen_phrase()
    

def ph6():
    print('brad_mpl_support.ph6')
    ##sys.stdout.flush()
    plot_phrase(phrase_select(5),w.Frame5)
    che45.set(0)
    root.after(100,listen_phrase)#isten_phrase()
# END OF PLOT WAVEFORM PHRASE ---------------------------------#
    
def listen_phrase_button(): #called by gui
    root.after(100,listen_phrase)
    
def listen_phrase():
    global sdata,samplerate
    sd.stop()
    sr=samplerate
    print('brad_mpl_support.listen_phrase')
    
    if che45.get() == 1:  #change playback using checkbox widget
        sr = int(samplerate*.75)
        print("sr change")
    
    print(sr, samplerate)
    sd.play(sdata,sr)
    
def play_recording():
    print('brad_mpl_support.play_recording')
    sd.stop()
    freq=11025
    sd.play(recording,samplerate=freq)
#     
# def record0():#called by gui
#     #global recFlag
#     sd.stop()
#     #recFlag=1
#     root.after(500,record1)
#     #recFlag=0
    
def record():
    #disable button2 ?
    global recording,freq,sdata, f
    
    w.Button2.configure(state = "disabled")
    sd.stop()
    
    print('brad_mpl_support.record')#,recFlag)
    freq=11025
    
    ''' optional message box to ask to record... comment out if not wanted'''
#     res=tk.messagebox.askyesno(message="Press Yes to Record          \rNo to Exit",title="*** RECORDING ***")
#     print(res)
#     if res == False:
#         w.Button2.configure(state = "normal")
#         return
    ''' end of messagebox '''
    
    tlabel4 = w.Label4.cget('text')
    tlabel5 = w.Label5.cget('text')
    w.Label4.configure(fg="red",text="RECORDING") 
    w.Label5.configure(fg="red",text="GRABACI\u00D3N") 
    root.update() #need this to allow label to be updated.
    print(len(sdata)/44100.)
    #set recording duration to pre-recorded length + 1 second
    duration = (len(sdata)/44100.)+1
    print(duration)
    
    recording = sd.rec(int(duration * freq), 
               samplerate=freq, channels=1,dtype="int16")
    print("recording...")
   
    sd.wait() #blocking...this also shows button depressed until recording finished
    
    plot_recording(True)
    
    w.Label4.configure(fg="black",text=tlabel4) #kills the recording 
    w.Label5.configure(fg="black",text=tlabel5)
    w.Button2.configure(state = "normal")
        

def plot_recording(a):
    global f,recording,freq
    clear_plot(w.Frame6)
    if a==False:
        recording = [0]*48000
        freq=16000
    length = len(recording)
    
    #print(length) #debug
    f.pack(fill=tk.BOTH) #add figure
    plt_canvas._tkcanvas.pack(fill=tk.BOTH) #add canvas
    
    ''' TODO: put in silence stripping'''
    
    time=np.linspace(0.,(len(recording)/freq),(len(recording))) #x axis values
    plt.plot(time,recording[:],linewidth=.4)

'''
REVEAL PHRASE Buttons
Reveals for only two seconds.
Also, not enabed if phrase not selected (highlight in organge)
'''
def rp1():
    print('brad_mpl_support.rp1')
    try:
        if selectedPhrase.get() == 21:  #button highlighted?
            w.Radiobutton2_1.config(text=PHRASE[0])#yes, update text
            root.after(2000,lambda:clear_phraseButtons())#clear phrase text after 2 seconds
    except: #only occurs after changing languages. Not sure why TODO:find out why
        print("exception")
        pass 

def rp2():
    print('brad_mpl_support.rp2')
    try:
        if selectedPhrase.get() == 22:
            w.Radiobutton2_2.config(text=PHRASE[1])
            root.after(2000,lambda:clear_phraseButtons())
    except:
        pass

def rp3():
    print('brad_mpl_support.rp3')
    try:
        if selectedPhrase.get() == 23:
            w.Radiobutton2_3.config(text=PHRASE[2])
            root.after(2000,lambda:clear_phraseButtons())
    except:
        pass

def rp4():
    print('brad_mpl_support.rp4')
    try:
        if selectedPhrase.get() == 24:
            w.Radiobutton2_4.config(text=PHRASE[3])
            root.after(2000,lambda:clear_phraseButtons())
    except:
        pass

def rp5():
    print('brad_mpl_support.rp5')
    try:
        if selectedPhrase.get() == 25:
            w.Radiobutton2_5.config(text=PHRASE[4])
            root.after(2000,lambda:clear_phraseButtons())
    except:
        pass
    
def rp6():
    print('brad_mpl_support.rp6')
    try:
        if selectedPhrase.get() == 26:
            w.Radiobutton2_6.config(text=PHRASE[5])
            root.after(2000,lambda:clear_phraseButtons())
    except:
        pass

def destroy_window():
    global top_level#,listener,t1
    #listener.stop()
    #t1.halt()
    #print("stop listener")
    top_level.destroy()
    top_level = None
    

if __name__ == '__main__':
    import UO_Linguistics
    UO_Linguistics.vp_start_gui()




