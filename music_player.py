import sys
import subprocess
import pkg_resources


def required_module():
    """Install The Required Module If Not Installed In System"""
    required = {'pyglet', 'pynput','mutagen'}
    installed = {pkg.key for pkg in pkg_resources.working_set}

    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

required_module()

from tkinter import *
from tkinter import ttk
import pyglet
import os
from pynput.keyboard import Key, Controller
from mutagen.mp3 import MP3
from ToTime import toTime

    

def songs(e=None):
    global song_list
    song_list = os.listdir("tk_song")


def main():
    
    global currentSong

    def start_app(e=None):
        
        songs()
        global data, player, label1, label2, full_song_time,label4
        player = pyglet.media.Player()
        
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
            src = pyglet.media.load(song)

        except Exception as e:
            song = f"tk_song/{song_list[data-1]}"
            src = pyglet.media.load(song)

        player.queue(src)

        try:
            label_text = (((song_list[data]).replace(
                '_', " ").replace(".mp3", ""))).title()

        except:
            label_text = (
                ((song_list[len(song_list)-1]).replace('_', " ").replace('-', ' ').replace(".mp3", ""))).title()

        label1 = Label(root, text='', bg="Light Blue", font=('bold', 20, "normal"))

        label1.grid(row=0, column=1, columnspan=4, pady=20)
        label1.config(text=label_text)

        label2 = Label(root,bg='Light Blue')
        label2.grid(row=5, column=1,pady=10)
        full_song_time = round(MP3(f'tk_song/{song_list[data]}').info.length)
        label3 = Label(root, text=f'{toTime(full_song_time)}',bg='Light Blue')
        label3.grid(row=5, column=2,columnspan=2,pady=10)
        label4 = Label(root,text="",bg='Light Blue')
        label4.grid(column=0,row=6,columnspan=10)
        label4.config(text=" ")

    songs()

    def play_song(e=None):
        """Play The Song"""
        def time_function(e=None):
            """Track The Time And Add Subtitle To Song"""
            global timer_
            label2.config(text=f'{toTime(round(player.time))}    of')
            if player.time >= full_song_time:
                nex()
            try:
                with open(f"lyrics\\{label1.cget('text')}.txt",encoding="utf-8")as file:
                    
                    lyrics = eval(file.read()) # --:> A Dictionary
                subtitles_check.config(state='normal')
                try:
                    label4.config(text = f"♫{(lyrics[label2.cget('text')[:5]])}♫")
                except:
                    pass
            except Exception as e:
                label4.config(text='Subtitles Not Available.')
                subtitles_check.config(state='disabled')
                
            timer_ = root.after(1000, time_function)
        time_function()
        button_2.focus_set()
        player.play()
        button_1.grid_forget()
        button_2.grid(row=1, column=2, padx=20)

    def pause_song(e=None):
        """Pause The Song"""
        root.after_cancel(timer_)
        player.pause()
        button_2.grid_forget()
        button_1.focus_set()
        button_1.grid(row=1, column=2, padx=20)

    def combo_entry_updater(e=None):
        """Refresh The ComboBox Entries"""
        try:
            currentSong.current(data)
        except:
            currentSong.current(len(song_list)-1)

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

    root = Tk()
    root.config(
        padx=100,
        pady=100,
        bg="Light Blue",
        width=400,
        height=350
    )

    root.maxsize(width=400, height=400)
    root.minsize(width=400, height=400)
    start_app()

    btn1 = PhotoImage(master=root, file="tk_photo/play.png")
    button_1 = Button(root, image=btn1, text="Play",
                    command=play_song, bg='Light Blue', borderwidth=0, activebackground="Light Blue", cursor="hand2")

    button_1.grid(row=1, column=2, padx=20)
    button_1.focus_set()

    btn2 = PhotoImage(master=root, file="tk_photo/pause.png")
    button_2 = Button(root, image=btn2, bg="Light Blue",
                    text="Pause", command=pause_song, borderwidth=0, activebackground="Light Blue", cursor="hand2")

    btn3 = PhotoImage(master=root, file="tk_photo/next.png")
    button_3 = Button(root, image=btn3, bg="Light Blue",
                    text="next", command=nex, borderwidth=0, activebackground="Light Blue", cursor="hand2")

    button_3.grid(row=1, column=4, padx=15)

    btn4 = PhotoImage(master=root, file="tk_photo/previous.png")
    button_4 = Button(root, image=btn4, command=prev,
                    bg="Light Blue", borderwidth=0, activebackground="Light Blue", cursor="hand2")
    button_4.grid(row=1, column=1, padx=20,)

    n = StringVar()
    currentSong = ttk.Combobox(root, width=18,
                    textvariable=n, state="readonly", height=6)


    i = 1
    song_name = [
        f"{i+song_list.index(value)}. {value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
    currentSong['values'] = song_name

    currentSong.grid(column=1, row=2, columnspan=4,pady=10)

    keyboard = Controller()

    def v_up(e=None):
        """Increase The Volume"""
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)

    def v_down(e=None):
        """Decrease The Volume"""
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    def subtitle(e=None):
        if var_subtitles.get()==1:
            label4.grid(column=0,row=6,columnspan=10)
        else:
            label4.grid_forget()

    downImage = PhotoImage(file="tk_photo/down.png")
    volume_down = Button(image=downImage, bg="Light Blue", cursor="hand2", command=v_down,
                         borderwidth=0, activebackground="Light Blue")

    volume_down.grid(column=0, row=1, columnspan=1)

    upImage = PhotoImage(master=root, file="tk_photo/up.png")
    volume_up = Button(image=upImage, bg="Light Blue", cursor="hand2",
                       command=v_up, borderwidth=0, activebackground="Light Blue")
    volume_up.grid(column=5, row=1, columnspan=1)
    var_subtitles = IntVar(value=1)
    subtitles_check = Checkbutton(root, text='lyrics',variable=var_subtitles, onvalue=1,command=subtitle, offvalue=0,bg="Light Blue",activebackground="Light Blue")
    subtitles_check.grid(column=3, row=5, columnspan=2,pady=10)
    
    combo_entry_updater()
    
    
    def combo(event=None):
        """Change Song Using ComboBox Entries"""
        label4.config(text="")
        length = len(song_list)
        with open("current_song.txt")as file:
            file_data = file.read()

        for_write_data = str(currentSong.current())

        if file_data != for_write_data:
            with open("current_song.txt", "w")as file:
                file.write(for_write_data)

            label1.config(text="")
            pause_song()
            start_app()
            play_song()

    currentSong.bind("<<ComboboxSelected>>", combo)

    def focusSet(e=None):
        """Focus On The Play And Pause Song"""
        songs()
        i = 1
        song_name = [
        f"{i+song_list.index(value)}. {value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
        currentSong['values'] = song_name
        button_1.focus_set()
        button_2.focus_set()
    
    def double_click(e=None):
        """Play or Pause The Song On Mouse Double Click"""
        if player.playing:
            pause_song()
        else:
            play_song()
        
    root.bind('<Button-1>', focusSet)
#     root.bind('<Double-Button-1>', double_click)
#     root.bind('<Left>', prev)
#     root.bind('<Right>', nex)
    root.bind('<Up>', v_up)
    root.bind('<Down>', v_down)
    play_song()
    pause_song()
    
    mainloop()
main()