
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import time
import tkinter.ttk as ttk


window = Tk() 
window.title('MP3 Player')
window.iconbitmap('MusicPlayer\\image\\mp3_file_47R_icon.ico')
window_width = 450
window_height = 530

screen_width = window.winfo_screenwidth()
screen_heigth = window.winfo_screenheight()

x = (screen_width/2) - (window_width/2)
y = (screen_heigth/2) - (window_height/2)
window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')





# Initialize Pygame Mixer
pygame.mixer.init()




#Grab song length time info
def play_time():
    #Check for double timing
    if stopped:
        return
    #Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos()/1000
    #Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    

    #Grab song title from playlist
    song = song_box.get(ACTIVE)
    #Add directory structure and mp3 to song title
    song = f'E:/Document/CODE/Python/MusicPlayer/Music/{song}.mp3'

    #Load song with mutagen
    song_mut = MP3(song)
    #Get song length
    global song_length
    song_length = song_mut.info.length
    #Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    #Increase current time by 1 second
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}')

    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

        #Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    else:
        #Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        #Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        #Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        
        #Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        
 
    #Update time
    status_bar.after(1000, play_time)



#Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='MusicPlayer\\Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    #Strip out the directory info and .mp3 extension from the song name
    song = song.replace("E:/Document/CODE/Python/MusicPlayer/Music/", "")
    song = song.replace(".mp3", "")
    #Add song to listbox
    song_box.insert(END, song)



#Add many songs to Playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='MusicPlayer\\Music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    #Loop thru the song list and replace directory info and mp3
    for song in songs:
        song = song.replace("E:/Document/CODE/Python/MusicPlayer/Music/", "")
        song = song.replace(".mp3", "")
        #Insert to Playlist
        song_box.insert(END, song)



#Play selected song
def play():
    #Set Stopped varible to False so song can play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'E:/Document/CODE/Python/MusicPlayer/Music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Call the play_time function to get song length
    play_time()



# Stop playing current song
global stopped
stopped = False
def stop():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #Stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    #Clear the status bar
    status_bar.config(text='')
    #Set stop varible to true
    global stopped 
    stopped = True



# Play the next song in the playlist
def next_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    #Get the current song tuple number
    next_one = song_box.curselection()
    #Add one to the current song number
    next_one = next_one[0]+1
    #Grab song title from playlist
    song = song_box.get(next_one)
    #Add directory structure and mp3 to song title
    song = f'E:/Document/CODE/Python/MusicPlayer/Music/{song}.mp3'
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist listbox
    song_box.select_clear(0, END)
    #Activate new song bar
    song_box.activate(next_one)
    #Set Activate Bar to next song
    song_box.selection_set(next_one, last=None)



# Play the previous song in the playlist
def previous_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    #Get the current song tuple number
    previous_one = song_box.curselection()
    #Sub one to the current song number
    previous_one = previous_one[0]-1
    #Grab song title from playlist
    song = song_box.get(previous_one)
    #Add directory structure and mp3 to song title
    song = f'E:/Document/CODE/Python/MusicPlayer/Music/{song}.mp3'
    #Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist listbox
    song_box.select_clear(0, END)
    #Activate new song bar
    song_box.activate(previous_one)
    #Set Activate Bar to previous song
    song_box.selection_set(previous_one, last=None)



#Delete A Song
def delete_song():
    stop()
    #Delete A Song
    song_box.delete(ANCHOR)
    #Stop music if it's playing
    pygame.mixer.music.stop()

   

#Delete All Songs
def delete_all_songs():
    stop()
    #Delete All Song
    song_box.delete(0, END)
    #Stop music if it's playing
    pygame.mixer.music.stop()



# Create Global
global paused
paused = False
# Pause and Unpause The Current Song
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused = True
        


#Create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'E:/Document/CODE/Python/MusicPlayer/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))






#Create Playlist Box
song_box = Listbox(window, bg="black", fg="white", width=90, height=20, selectbackground="gray", selectforeground="black")
song_box.pack(pady=0)



#Define Player Control Buttons Images
back_btn_img = PhotoImage(file = 'MusicPlayer\\image\\back50.png')
forward_btn_img = PhotoImage(file = 'MusicPlayer\\image\\forward50.png')
play_btn_img = PhotoImage(file = 'MusicPlayer\\image\\play50.png')
pause_btn_img = PhotoImage(file = 'MusicPlayer\\image\\pause50.png')
stop_btn_img = PhotoImage(file = 'MusicPlayer\\image\\stop50.png')



#Create Player Control Frames
control_frame = Frame(window)
control_frame.pack()



#Create Player Control Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10, pady=20)
forward_button.grid(row=0, column=1, padx=10,pady=20)  
play_button.grid(row=0, column=2, padx=10, pady=20)
pause_button.grid(row=0, column=3, padx=10, pady=20) 
stop_button.grid(row=0, column=4, padx=10, pady=20) 



#Create Menu
my_menu = Menu(window)
window.config(menu=my_menu)



#Add Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)



#Add Many Songs to Playlist
add_song_menu.add_command(label="Add many songs to playlist", command=add_many_songs)



#Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)



#Create Status Bar
status_bar = Label(window, text ='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)



#Create music position slider
my_slider = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=10)



window.mainloop()