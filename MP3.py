from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

from tkinter import messagebox

root=Tk()
#root properties
root.title("MP3 Player")#root title
root.geometry("600x500")#window size
root.iconbitmap("logo1.ico")#logo
root.resizable(100,100)

#initialize Pygame
pygame.mixer.init()

#to get play time
def play_time():
   
    #check if song is stopped
    if stopped:
        return
    
    #Grab Current time
    current_time = pygame.mixer.music.get_pos()/1000
    #convert song time to time format
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
    
    song = myListbox.get(ACTIVE)
    song =f'C:/Playlist/audio/{song}.mp3'
    #finding current time
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    #convert to time 
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    '''
    #myLabel.config(text=converted_song_length)
    song_slider.config(to=song_length)
    myLabel.config(text=song_slider.get())
    '''
    #check if the song is over
    if int(song_slider.get())== int (song_length):
        stop()

    elif paused:
        pass
        
    else:
        #move slider along 1sec at a time
        next_time = int(song_slider.get()) + 1
        
        #output new time value to slider
        song_slider.config(to=song_length, value=next_time)
        #convert slider position to time format
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(song_slider.get())))
        statusBar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
        
        
        
    if current_time > 0:
        statusBar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
        
    #create loop to check every sector
    statusBar.after(1000,play_time)
    

def add_song():
   

    song = filedialog.askopenfilename(initialdir='audio/',title="choose a song",filetypes=(("mp3 Files","*.mp3"), ) )
    
    song=song.replace("C:/Playlist/audio/", "")
    song=song.replace(".mp3", "")
    myListbox.insert(END,song)
    

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/',title="choose a song",filetypes=(("mp3 Files","*.mp3"), ) )
    #myLabel.config(text=song)
    #strip out directory str from title
    for song in songs:
        song=song.replace("C:/Playlist/audio/", "")
        song=song.replace(".mp3", "")
        myListbox.insert(END,song)

#create  function to delete songs
def delete_song():
    myListbox.delete(ANCHOR)

def delete_many_songs():
    
    myListbox.delete(0,END)
    
def play():
    global stopped
    stopped = False
    #Reconstructing song with directory structure
    song = myListbox.get(ACTIVE)
    song =f'C:/Playlist/audio/{song}.mp3'
    myLabel.config(text=song)
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    
global stopped
stopped = False
def stop():
    #stop song
    pygame.mixer.music.stop()
    #clear playlist bar
    myListbox.selection_clear(ACTIVE)
    statusBar.config(text='')
    song_slider.config(value=0)
    global stopped
    stopped = True

        
def forward():
    #reset slider position and status bar
    statusBar.config(text='')
    song_slider.config(value=0)
    next_one = myListbox.curselection()
    #myLabel.config(text=next_one)
    #add one to current song number
    next_one = next_one[0] + 1
    #grab song title
    song = myListbox.get(next_one)
     #Reconstructing song with directory structure
    song =f'C:/Playlist/audio/{song}.mp3'
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #clear active Bar
    myListbox.selection_clear(0,END)
    #move to next song
    myListbox.activate(next_one)
    #set Active Bar
    myListbox.selection_set(next_one, last=None)
    
    
#create function to move towards previous song    
def backward():
    #reset slider position and status bar
    statusBar.config(text='')
    song_slider.config(value=0)
    next_one = myListbox.curselection()
    #myLabel.config(text=next_one)
    #add one to current song number
    next_one = next_one[0] - 1
    #grab song title
    song = myListbox.get(next_one)
     #Reconstructing song with directory structure
    song =f'C:/Playlist/audio/{song}.mp3'
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #clear active Bar
    myListbox.selection_clear(0,END)
    #move to next song
    myListbox.activate(next_one)
    #set Active Bar
    myListbox.selection_set(next_one, last=None)

#create pause variable
    
global paused
paused = False

#function for pause
def pause(is_paused):
    global paused
    paused=is_paused
    
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
    
#create volume function
def volume(x):
    #myLabel.config(text=volume_slider.get())
    pygame.mixer.music.set_volume(volume_slider.get())
    
#create song_slide function
def song_slide(x):
    song = myListbox.get(ACTIVE)
    song =f'C:/Playlist/audio/{song}.mp3'
    #myLabel.config(text=song)
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=song_slider.get())
    
    
    
    
    
    
    


#General Terms
myfont = ("Times New Roman",12)

#create Main Frame

main_frame = Frame(root)
main_frame.pack(pady=20)

#volume Frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0,column=1,padx=7)

#create volume slider
volume_slider = ttk.Scale(volume_frame,from_=1, to=0, orient=VERTICAL, length=125,value=1,command=volume)
volume_slider.pack(pady=10)

#create a song slider
song_slider = ttk.Scale(main_frame,from_=0, to=100, orient=HORIZONTAL, length=360,value=0,command=song_slide)
song_slider.grid(row=2, column=0,pady=20)


#ListBox
myListbox = Listbox(main_frame, bg="black",fg="green",width=60,selectbackground="green", selectforeground="black")
myListbox.grid(row=0,column=0)

#define Button Img

back_btn = PhotoImage(file='images/back50.png')
forward_btn = PhotoImage(file='images/forward50.png')
play_btn = PhotoImage(file='images/play50.png')
pause_btn = PhotoImage(file='images/pause50.png')
stop_btn = PhotoImage(file='images/stop50.png')


#create Buttons Frame
buttonFrame = Frame(main_frame)
buttonFrame.grid(row=1,column=0,pady=20)

#create buttons
backButton = Button(buttonFrame,image=back_btn,borderwidth=0,command=backward)
forwardButton = Button(buttonFrame,image=forward_btn,borderwidth=0,command=forward)
playButton = Button(buttonFrame,image=play_btn,borderwidth=0,command=play)
pauseButton = Button(buttonFrame,image=pause_btn,borderwidth=0,command=lambda: pause(paused))
stopButton = Button(buttonFrame,image=stop_btn,borderwidth=0,command=stop)

backButton.grid(row=0,column=0,padx=10)
forwardButton.grid(row=0,column=1,padx=10,ipadx=10)
playButton.grid(row=0, column=2, padx=10, ipadx=10)
pauseButton.grid(row=0,column=3,padx=10,ipadx=10)
stopButton.grid(row=0,column=4,padx=10,ipadx=10)
#create menu
myMenu = Menu(root)
root.config(menu=myMenu)


#create add song
addsong = Menu(myMenu,tearoff=0)
myMenu.add_cascade(label="Add Songs",menu=addsong)
addsong.add_command(label="Add One Song to playlist",command=add_song)
#Add Many Songs
addsong.add_command(label="Add Many Songs to playlist",command=add_many_songs)

#create delete song
deletesong = Menu(myMenu,tearoff=0)
myMenu.add_cascade(label="Remove Songs",menu=deletesong)
deletesong.add_command(label="Remove One Song from playlist",command=delete_song)
#Delete Many Songs
deletesong.add_command(label="Remove All Songs from playlist",command=delete_many_songs)

#Creating Status Bar
statusBar = Label(root,text='',borderwidth=1,relief=GROOVE,anchor=E)
statusBar.pack(fill=X,side=BOTTOM,ipady=2)
#creating Label
myLabel = Label(root, text="")
myLabel.pack(pady=20)



#mainloop
root.mainloop()
