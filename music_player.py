from tkinter import Button,Label,Tk,PhotoImage,StringVar,IntVar,Checkbutton,mainloop
from tkinter.ttk import Combobox
from pyglet.media import Player,load
from os import listdir
from ToTime import toTime
from random import randint
from time import sleep


def songs(e=None):
    global song_list
    song_list = listdir("tk_song")
    return song_list


song_len = len(songs())


def main():
    global allSongCombo


    def start_app(e=None):
        songs()
        global data, player, label1, label2, full_song_time,label4
        player = Player()
        
        try:
            with open("current_song.txt") as f:
                data = f.read()

                if data == "":
                    data = "0"

                data = int(data)

        except:
            with open("current_song.txt", "w"):
                pass

            with open("current_song.txt") as f:
                data = f.read()

                if data == "":
                    data = "0"

                data = int(data)

        songs()

        try:
            song = f"tk_song/{song_list[data]}"
            src = load(song)
        
        except:
            song = f"tk_song/{song_list[data-1]}"
            src =load(song)
        player.queue(src)

        try:
            label_text = (((song_list[data]).replace(
                '_', " ").replace(".mp3", ""))).title()

        except:
            label_text = (
                ((song_list[len(song_list)-1]).replace('_', " ").replace('-', ' ').replace(".mp3", ""))).title()

        label1 = Label(root, text='',bg="Light Blue", font=('bold', 20, "normal"))
        label1.grid(row=0, column=1, columnspan=4, pady=20)
        label1.config(text=label_text)

        label2 = Label(root,bg='Light Blue')
        label2.grid(row=5, column=1,pady=10)
        
        full_song_time = src.duration
        
        label3 = Label(root, text=f'{toTime(full_song_time)}',bg='Light Blue')
        label3.grid(row=5, column=2,columnspan=2,pady=10)
        
        label4 = Label(root,text="",bg='Light Blue')
        label4.grid(column=0,row=6,columnspan=10)
        label4.config(text="")

    songs()


    def play_song(e=None):
        
        """Play The Song"""
        
        
        def time_function(e=None):
            
            """Track The Time And Add Subtitle To Song"""
            global timer_
            label2.config(text=f'{toTime(player.time)}    of')
            if loop_var.get() == 0:
                if player.time >= full_song_time:
                    nex()
            else:
                if player.time >= full_song_time:
                    nex()
                    prev()
                
            try:
                with open(f"lyrics\\{label1.cget('text')}.txt",encoding="utf-8")as file:
                    lyrics = eval(file.read()) # --:> A Dictionary
                    
                subtitles_check.config(state='normal',cursor='hand2')
                
                try:
                    label4.config(text = f"♫{(lyrics[label2.cget('text')[:5]])}♫")
                except:
                    pass
                
            except Exception as e:
                label4.config(text='Subtitles Not Available.')
                subtitles_check.config(state='disabled',cursor='arrow')
                
            timer_ = root.after(1000, time_function)
            
        time_function()
        pause_btn.focus_set()
        player.play()
        play_btn.grid_forget()
        pause_btn.grid(row=1, column=2, padx=20)



    def pause_song(e=None): 
        """Pause The Song"""
        root.after_cancel(timer_)
        player.pause()
        pause_btn.grid_forget()
        play_btn.focus_set()
        play_btn.grid(row=1, column=2, padx=20)


    def combo_entry_updater(e=None):
        """Refresh The ComboBox Entries"""
        try:
            allSongCombo.current(data)
        except:
            allSongCombo.current(len(song_list)-1)


    def prev(e=None):
        """Go To The Previous Song On The List"""
        label4.config(text="")
        label1.grid_forget()

        if data > 0:
            with open("current_song.txt", "w") as f:
                f.write(str(data-1))

        else:
            with open("current_song.txt", "w") as f:
                f.write(str(len(song_list)-1))

        pause_song()
        start_app()
        play_song()
        combo_entry_updater()


    def nex(event=None):
        """Go To The Next Song On The List"""
        label4.config(text="")
        label1.grid_forget()

        if data < len(song_list)-1:
            with open("current_song.txt", "w") as f:
                f.write(str(data+1))

        else:
            with open("current_song.txt", "w") as f:
                f.write(str(0))

        pause_song()
        start_app()
        play_song()
        combo_entry_updater()
        
        
    def random_song(e=None):
        """Random Song Form The List Of Song."""
        label1.config(text="")
        label4.config(text="")
        
        with open('current_song.txt','w')as f:
            f.write(str(randint(0,len(song_list)-1)))
            
        pause_song()
        start_app()
        play_song()
        combo_entry_updater()
    
    
    def v_up(e=None):
        """Increase The Volume"""
        player.volume+=2
        if player.volume > 70:
            player.volume=70
        elif player.volume == 2:
            player.volume =1
    def v_down(e=None):
        player.volume-=2
        if player.volume < 0:
            player.volume=0
        
        
        
    def subtitle(e=None):
        """For Subtitles On Or Off"""
        if var_subtitles.get()==1:
            label4.grid(column=0,row=6,columnspan=10)
        else:
            label4.grid_forget()
       
       
    def combo(event=None):
        """Change Song Using ComboBox Entries"""
        label4.config(text="")
        
        with open("current_song.txt")as file:
            file_data = file.read()

        for_write_data = str(allSongCombo.current())

        if file_data != for_write_data:
            
            with open("current_song.txt", "w")as file:
                file.write(for_write_data)

            label1.config(text="")
            pause_song()
            start_app()
            play_song()


    def focusSet(e=None):
        """Focus On The Play And Pause Song"""
        songs()
        i = 1
        song_name = [
        f"{value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
        
        allSongCombo['values'] = song_name
        play_btn.focus_set()
        pause_btn.focus_set()
        
    
    def double_click(e=None):        
        """Play or Pause The Song On Mouse Double Click"""
        if player.playing:
            pause_song()
        else:
            play_song()
            
            
    def supporter():
        """This Function Is Call Inside '(skip_forward and skip_forward)' Because Both Have The Same Line Of Code."""
        label4.config(text="Plese Wait...")
        
        if player.playing:
            pause_song()
            sleep(.05)
            play_song()
        else:
            play_song()
            sleep(.05)
            pause_song()
            
            
    def skip_forward(e=None):
        """Forwards song by 10 seconds."""
        player.seek(player.time+10)
        supporter()
        
        
    def skip_backward(e=None):
        """Backwards song by 10 seconds."""
        player.seek(player.time-10)
        supporter()
          
          
    root = Tk()
    root.config(
        padx=100,
        pady=100,
        bg="Light Blue",
        width=400,
        height=350)
    root.title("Music Player")
    root.maxsize(width=450, height=400)
    root.minsize(width=450, height=400)
    
    start_app()

    play_img = PhotoImage(master=root, file="tk_photo/play.png")
    play_btn = Button(root, image=play_img, text="Play",
                    command=play_song, bg='Light Blue', borderwidth=0, activebackground="Light Blue", cursor="hand2")
    play_btn.grid(row=1, column=2, padx=20)
    play_btn.focus_set()

    pause_img = PhotoImage(master=root, file="tk_photo/pause.png")
    pause_btn = Button(root, image=pause_img, bg="Light Blue",
                    text="Pause", command=pause_song, borderwidth=0, activebackground="Light Blue", cursor="hand2")

    nex_img = PhotoImage(master=root, file="tk_photo/next.png")
    nex_btn = Button(root, image=nex_img, bg="Light Blue",
                    text="next", command=nex, borderwidth=0, activebackground="Light Blue", cursor="hand2")
    nex_btn.grid(row=1, column=4, padx=15)

    prev_img = PhotoImage(master=root, file="tk_photo/previous.png")
    prev_btn = Button(root, image=prev_img, command=prev,
                    bg="Light Blue", borderwidth=0, activebackground="Light Blue", cursor="hand2")
    prev_btn.grid(row=1, column=1, padx=20,)

    allSongCombo_var = StringVar()
    allSongCombo = Combobox(root, width=18,
                    textvariable=allSongCombo_var, state="readonly", height=6)


    def name_changer():
        global song_name
        song_name = [
        f"{value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
        return song_name
    
    
    name_changer()
    allSongCombo['values'] = song_name
    allSongCombo.grid(column=1, row=2, columnspan=4,pady=10)
    allSongCombo.bind("<<ComboboxSelected>>", combo)
    
    shuffle_btn = Button(root,text='Shuffle',cursor="hand2",command=random_song,font=("arial",7,"normal"),bg="Light Blue",activebackground="Light Blue",borderwidth=0)
    shuffle_btn.grid(column=0,row=2)
    
    loop_var = IntVar(value=0)
    loop_btn = Checkbutton(root, text='Loop',cursor="hand2",variable=loop_var, onvalue=1, offvalue=0,bg="Light Blue",activebackground="Light Blue")
    loop_btn.grid(column=5,row=2)
    
    downImage = PhotoImage(file="tk_photo/down.png")
    volume_down_btn = Button(image=downImage, bg="Light Blue", cursor="hand2", command=v_down,
                         borderwidth=0, activebackground="Light Blue")
    volume_down_btn.grid(column=0, row=1, columnspan=1)
    
    upImage = PhotoImage(master=root, file="tk_photo/up.png")
    volume_up_btn = Button(image=upImage, bg="Light Blue", cursor="hand2",
                       command=v_up, borderwidth=0, activebackground="Light Blue")
    volume_up_btn.grid(column=5, row=1, columnspan=1)
    
    var_subtitles = IntVar(value=1)
    subtitles_check = Checkbutton(root, text='lyrics',cursor="hand2",variable=var_subtitles, onvalue=1,command=subtitle, offvalue=0,bg="Light Blue",activebackground="Light Blue")
    subtitles_check.grid(column=3, row=5, columnspan=2,pady=10)
    
    combo_entry_updater()
            
    #----------------------Event add and remove----------------------#
            
#     root.bind('<Double-Button-1>', double_click)  # ----> To Play or Pause Song On Mouse Double Click.
    root.bind('<Button-1>', focusSet)
    root.bind('<Left>', skip_backward)
    root.bind('<Right>', skip_forward)
    root.bind('<Up>', v_up)
    root.bind('<Down>', v_down)
    root.bind('<Control-Right>', nex)
    root.bind('<Control-Left>', prev)
    root.bind('<Control-w>', lambda e:root.destroy())
    allSongCombo.unbind_class("TCombobox", "<MouseWheel>")
# ------------------------------------------------------------------------------------ #


    def isChangeInSongList():
        global song_len,song_list,data
        c = len(songs())
        
        if song_len!= c:
            song_len = c
            name_changer()
            try:
                data = song_name.index(label1['text'])
            except:
                nex()
                
            allSongCombo['values'] = song_name
            
        root.after(100,isChangeInSongList)
        
    isChangeInSongList()
    play_song()
    pause_song()
    mainloop()
    
    
main()
