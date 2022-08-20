from tkinter import Button,Label,Tk,PhotoImage,StringVar,IntVar,Checkbutton,mainloop,Frame,Listbox,Entry
from tkinter.ttk import Combobox
from tkinter.messagebox import askyesno
from pyglet.media import Player,load
from os import listdir,startfile
from os.path import realpath,dirname
from random import randint
from time import sleep



full_path = dirname(realpath(__file__))
song_p = realpath(f'{full_path}\\Songs')
photo_p = realpath(f'{full_path}\\Photos')
lyrics_p = realpath(f'{full_path}\\Lyrics')
c_song_p = realpath(f'{full_path}\\Current Song.txt')
music_ico = realpath(f'{full_path}\\music.ico')
nextWindow = None

def second_win():
    r = Tk()
    frame = Frame(r,bg='#f1f8f3')
    r.config(padx=100,bg='#f1f8f3')
    r.iconbitmap(music_ico)
    r.title("Music Player")
    r.geometry('690x100')
    Label(frame,text="You Have No Song In Folder:-",font=('arial',15,'normal'),bg='#f1f8f3').grid(column=0,row=0)
    l1 = Label(frame,text=f' {song_p} ',fg='Blue',cursor='hand2',font=('arial',15,'underline'),bg='#f1f8f3')
    l1.grid(column=1,ipadx=0,row=0)

    Label(frame,text="_"*100,bg='#f1f8f3',fg='#f1f8f3').grid(column=0,row=2,columnspan=3)
    Label(frame,text='Please Upload Songs And',font=('arial',15,'normal'),bg='#f1f8f3').grid(column=0,row=3)
    l2 = Label(frame,text='Restart The App',font=('arial',15,'underline'),fg='Blue',cursor='hand2',bg='#f1f8f3')
    l2.grid(column=1,row=3,sticky='w')
    frame.pack(fill='both',expand=True)

    def abc(e):
        l1.config(fg='#66bfbf')
        startfile(song_p)
        def _():
            l1.config(fg='Blue')
        r.after(100,_)

    l1.bind('<Button-1>',abc)
    def restart(e):
        global song_len
        r.destroy()
        song_len = len(songs())
        main_func()
    l2.bind('<Button-1>',restart)
    r.mainloop()

def toTime(timeInSec=0):
    timeInSec = round(timeInSec)
    hour = (timeInSec//60)
    minute = (timeInSec%60)
    return('{:02}:{:02}'.format(hour,minute))


def toDict(path):
    with open(path) as f:
        a = f.read().replace('\ufeff','')
    string = a.splitlines()
    out = ""
    for line in string:
        line = line.split(' ')
        i = 0
        while True:
            try:
                if len(' '.join(line[i:]))>=45:
                    i+=7
                    line.insert(i,r'\n')

                else:
                    break
            except Exception as e:

                break
        line = ' '.join(line).replace('"',"'")
        line = list(line)
        del line[0]
        del line[5:9]
        line.insert(0,'"')
        line.insert(6,'"')
        line.insert(7,':')
        line.insert(8,'"')
        line.insert(len(line),'"')
        line.insert(len(line),',')

        out+=''.join(line)
    dict_ = eval('{'+out+'}')

    return(dict_)



def songs(e=None):
    global song_list
    song_list = listdir(song_p)
    return song_list


song_len = len(songs())


def main_func():
    global allSongCombo

    if len(songs()) <= 0:
        second_win()
    else:
        def start_app(e=None,volume=None):
            songs()
            global data, player, label1, label2, full_song_time,label4,next_song_index
            next_song_index = None
            player = Player()

            try:
                with open(c_song_p,encoding='utf-8') as f:
                    pass

            except:
                with open(c_song_p, "w"):
                    pass
            finally:
                with open(c_song_p,encoding='utf-8') as f:
                    f_list=['0',"0",'1']
                    _Flist = f.read().replace('\n','').split(',')
                    f_list[:len(_Flist)] = _Flist
                    data = f_list[0]
                    try:
                        int(data)
                    except ValueError:
                        data=0
                    if int(data)>=len(song_list):
                        data = len(song_list)-1
                    data = int(data)


            songs()

            try:
                song = f"{song_p}/{song_list[data]}"
                src = load(song)

            except:
                song = f"{song_p}/{song_list[data-1]}"
                src =load(song)

            player.queue(src)
            player.seek(float(f_list[1]))
            player.volume = volume if volume is not None else float(f_list[2])

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
                """Track The Time And Add Lyrics To Song"""
                global timer_,next_song_index,next_song_name

                label2.config(text=f'{toTime(player.time)}    of')
                if loop_var.get() == 0:
                    if player.time >= full_song_time:
                        if next_song_index is not None:
                            combo(None,str(next_song_index))
                            combo_entry_updater()
                            next_song_index = None

                        else:
                            nex()
                    elif player.time >= full_song_time:
                        if not next_song_name in name_changer():
                            next_song_index = None
                            next_song_name = None


                else:
                    if player.time+1 >= full_song_time:
                        nex()
                        prev()

                try:
                    if label4['text'] == 'Subtitles Not Available.':
                        label4['text']='Please Wait...'


                    lyrics = toDict(f"{lyrics_p}\\{label1.cget('text')}.lrc")

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
            if player.time<=3:
                label4.config(text="")
                label1.grid_forget()

                if data > 0:
                    with open(c_song_p, "w") as f:
                        f.write(str(data-1))

                else:
                    with open(c_song_p, "w") as f:
                        f.write(str(len(song_list)-1))
                pause_song()
                
                start_app(volume=player.volume)
                play_song()
                combo_entry_updater()
            else:
                player.seek(0)
                supporterFunc()

                


        def nex(event=None):
            """Go To The Next Song On The List"""
            label4.config(text="")
            label1.grid_forget()

            if data < len(song_list)-1:
                with open(c_song_p, "w") as f:
                    f.write(str(data+1))

            else:
                with open(c_song_p, "w") as f:
                    f.write(str(0))

            pause_song()
            start_app(volume=player.volume)
            play_song()
            combo_entry_updater()


        def random_song(e=None):
            global data
            """Random Song Form The List Of Song."""
            label1.config(text="")
            label4.config(text="")

            with open(c_song_p,'w')as f:
                f.write(str(randint(0,len(song_list)-1)))

            pause_song()
            start_app(volume=player.volume)
            play_song()
            combo_entry_updater()


        def v_up(e=None):
            """Increase The Volume"""
            global volume
            player.volume+=0.066
            if player.volume > 1:
                player.volume=1
            volume = player.volume

        def v_down(e=None):
            global volume
            player.volume-=0.066
            if player.volume < 0:
                player.volume=0
            volume = player.volume


        def subtitle(e=None):
            """For Subtitles On Or Off"""
            if var_subtitles.get()==1:
                label4.grid(column=0,row=6,columnspan=10)
            else:
                label4.grid_forget()


        def combo(event=None,for_write_data = None):
            """Change Song Using ComboBox Entries"""
            label4.config(text="")
            if for_write_data is None:
                for_write_data = str(allSongCombo.current())

            with open(c_song_p, encoding='utf-8')as file:
                file_data = file.read()



            if file_data != for_write_data:
                with open(c_song_p, "w")as file:
                    file.write(for_write_data)

                label1.config(text="")
                pause_song()
                start_app(volume=player.volume)
                play_song()


        def focusSet(e=None):
            """Focus On The Play And Pause Song"""

            songs()
            song_name = [
            f"{value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
            allSongCombo['values'] = song_name
            play_btn.focus_set()
            pause_btn.focus_set()
            if nextWindow is not None:
                nextWindow.focus_force()


        def supporterFunc():
            """This Function Is Call Inside '(skip_forward and skip_forward)' Because Both Have The Same Line Of Code."""
            label4.config(text="Please Wait...")

            if player.playing:
                pause_song()
                sleep(.02)
                play_song()
            else:
                play_song()
                sleep(.02)          
                pause_song()


        def skip_forward(e=None):
            """Forwards song by 10 seconds."""
            player.seek(player.time+10)
            supporterFunc()


        def skip_backward(e=None):
            """Backwards song by 10 seconds."""
            player.seek(player.time-10)
            supporterFunc()


        def isChangeInSongList():
            global song_len,song_list,data,changeInSongListLoop
            c = len(songs())
            if len(song_name[data]) > 13:
                label1['font']=('bold', 20-(len(song_name[data])%13), "normal")
            else:
                label1['font']=('bold', 20, "normal")
            if len(songs()) <= 0:
                pause_song()
                root.destroy()
                second_win()
            elif song_len!= c:
                song_len = c
                name_changer()
                try:
                    data = name_changer().index(label1['text'])
                except:
                    prev()
                combo_entry_updater()
                allSongCombo['values'] = song_name
                allSongCombo.current(data)
            elif song_name != name_changer():
                songs()
                name_changer()
                combo_entry_updater()
                allSongCombo['values'] = song_name
                allSongCombo.current(data)
                label1['text']=song_name[data]


            changeInSongListLoop = root.after(1000,isChangeInSongList)
        def name_changer():
            global song_name
            song_name = [
            f"{value.replace('.mp3', '').replace('-', ' ').replace('_', ' ').title()}" for value in song_list]
            return song_name

        def on_closing(e=None):
            with open(c_song_p,'w') as f:
                f.write(f"{data},{player.time},{player.volume}")
            root.destroy()

        root = Tk()

        root.config(
            padx=100,
            pady=100,
            bg="Light Blue")
        root.iconbitmap(music_ico)
        root.title("Music Player")
        root.geometry('480x420')
        root.resizable(False,False)

        start_app()

        play_img = PhotoImage(master=root, file=f"{photo_p}/play.png")
        play_btn = Button(root, image=play_img, text="Play",
                        command=play_song, bg='Light Blue', borderwidth=0, activebackground="Light Blue", cursor="hand2")
        play_btn.grid(row=1, column=2, padx=20)
        play_btn.focus_set()

        pause_img = PhotoImage(master=root, file=f"{photo_p}/pause.png")
        pause_btn = Button(root, image=pause_img, bg="Light Blue",
                        text="Pause", command=pause_song, borderwidth=0, activebackground="Light Blue", cursor="hand2")

        nex_img = PhotoImage(master=root, file=f"{photo_p}/next.png")
        nex_btn = Button(root, image=nex_img, bg="Light Blue",
                        text="next", command=nex, borderwidth=0, activebackground="Light Blue", cursor="hand2")
        nex_btn.grid(row=1, column=4, padx=15)

        prev_img = PhotoImage(master=root, file=f"{photo_p}/previous.png")
        prev_btn = Button(root, image=prev_img, command=prev,
                        bg="Light Blue", borderwidth=0, activebackground="Light Blue", cursor="hand2")
        prev_btn.grid(row=1, column=1, padx=20,)

        allSongCombo_var = StringVar()
        allSongCombo = Combobox(root, width=18,
                        textvariable=allSongCombo_var, state="readonly", height=10)

        name_changer()
        allSongCombo['values'] = song_name
        allSongCombo.grid(column=1, row=2, columnspan=4,pady=10)
        allSongCombo.bind("<<ComboboxSelected>>", combo)

        shuffle_btn = Button(root,text='Shuffle',cursor="hand2",command=random_song,font=("arial",7,"normal"),bg="Light Blue",activebackground="Light Blue",borderwidth=0)
        shuffle_btn.grid(column=0,row=2)

        loop_var = IntVar(value=0)
        loop_btn = Checkbutton(root, text='Loop',cursor="hand2",variable=loop_var, onvalue=1, offvalue=0,bg="Light Blue",activebackground="Light Blue")
        loop_btn.grid(column=5,row=2)

        downImage = PhotoImage(file=f"{photo_p}/down.png")
        volume_down_btn = Button(image=downImage, bg="Light Blue", cursor="hand2", command=v_down,
                             borderwidth=0, activebackground="Light Blue")
        volume_down_btn.grid(column=0, row=1, columnspan=1)

        upImage = PhotoImage(master=root, file=f"{photo_p}/up.png")
        volume_up_btn = Button(image=upImage, bg="Light Blue", cursor="hand2",
                           command=v_up, borderwidth=0, activebackground="Light Blue")
        volume_up_btn.grid(column=5, row=1, columnspan=1)

        var_subtitles = IntVar(value=1)
        subtitles_check = Checkbutton(root, text='lyrics',cursor="hand2",variable=var_subtitles, onvalue=1,command=subtitle, offvalue=0,bg="Light Blue",activebackground="Light Blue")
        subtitles_check.grid(column=3, row=5, columnspan=2,pady=10)
        def next_song():
            global nextWindow,next_lst

            next_song_btn['state'] = 'disabled'
            next_song_btn['cursor'] = ''
            nextWindow = Tk()
            nextWindow.geometry("400x270")
            nextWindow.focus_force()
            nextWindow.title("Next Song")
            variable = StringVar(nextWindow)
            e = Entry(nextWindow,textvariable=variable,)
            e.insert(0,"SEA"+'\u0280'+"CH")
            e.pack()
            e.bind('<FocusIn>',lambda a:e.delete(0,'end'))
            e.bind('<FocusOut>',lambda a:e.insert(0,"SEA"+'\u0280'+"CH"))


            listbox = Listbox(nextWindow, width=40, height=10)
            next_lst = name_changer()
            for i,v in enumerate(next_lst):
                    listbox.insert(i,v)
            def f():
                global next_lst,next_loop
                l = name_changer()
                if next_lst != l:
                    for a in range(len(next_lst)):
                        listbox.delete(0)
                    next_lst = l

                    for i,v in enumerate(next_lst):
                        listbox.insert(i,v)
                next_loop = nextWindow.after(100,f)


            f()
            listbox.pack()

            def func(var,index,mode):
                lst = [a for a in name_changer() if a.lower().startswith(variable.get().lower()) or variable.get()=="SEA"+'\u0280'+"CH"]
                for a in range(len(name_changer())):
                    listbox.delete(0)
                for i,v in enumerate(lst):
                    listbox.insert(i,v)
            variable.trace_add(mode='write',callback=func)
            def selected_item():
                global next_song_index,nextWindow,next_song_name
                try:
                    next_song_index = name_changer().index(listbox.get(listbox.curselection()))
                    next_song_name = listbox.get(listbox.curselection())
                except IndexError:
                    pass
                if next_song_index == data:
                    next_song_index+=1
                noNeed()
            def noNeed():
                global nextWindow,next_loop
                nextWindow.after_cancel(next_loop)
                nextWindow.destroy()
                nextWindow = None

                next_song_btn['state'] = 'normal'
                next_song_btn['cursor'] = 'hand2'

            nextWindow.protocol("WM_DELETE_WINDOW",noNeed)
            Button(nextWindow,text='Ok',command=selected_item,borderwidth=.5).pack()

        next_song_btn = Button(root,text="Next Song",command=next_song,bg="Light Blue", cursor="hand2", activebackground="Light Blue")
        next_song_btn.place(x=100,y=250)

        combo_entry_updater()

# ------------------------------Event add and remove--------------------------------- #

        root.bind('<Button-1>', focusSet)
        root.bind('<Left>', skip_backward)
        root.bind('<Right>', skip_forward)
        root.bind('<Up>', v_up)
        root.bind('<Down>', v_down)
        root.bind('<Control-Right>', nex)
        root.bind('<Control-Left>', prev)
        root.bind('<Control-w>', on_closing)
        allSongCombo.unbind_class("TCombobox", "<MouseWheel>")

        root.protocol("WM_DELETE_WINDOW", on_closing)
# ------------------------------------------------------------------------------------ #

        isChangeInSongList()
        play_song()
        pause_song()
        mainloop()
        
if __name__ == '__main__':
    main_func()
    with open(c_song_p,'w') as f:
        f.write(f"{data},{player.time},{player.volume}")
