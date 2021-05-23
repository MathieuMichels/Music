# ----------------------------------------------------------
# import some packages
# ----------------------------------------------------------
from mido import MidiFile                         # Open midi files
import moviepy.editor as mp                       # Video editor
from moviepy.editor import concatenate_videoclips # Merging videos
import time                                       # Because speed is important
from tkinter import *                             # Visual interface
from tkinter.filedialog import *                  # Easy file opening
import subprocess, os, platform                   # Easy file opening ep. 2
# ----------------------------------------------------------
# init
# ----------------------------------------------------------
t = time.time()   # Because speed is important (lol)
duration = 0      # Because I don't know why I initialize this variable anymore
clips = []        # List of every video created with the video() function
# ----------------------------------------------------------
# Open midifile
# ----------------------------------------------------------
def midifile(filename):
    """
    :param filename: name of the .mid file to analyze.
    :return: a list of the number of notes per second: notes[i]= [second number #i, #j notes/sec]
    """
    # --------------------------------------------------------------------
    # Import some globals variables
    # --------------------------------------------------------------------
    global duration
    # --------------------------------------------------------------------
    # Generate a dictionary with the info from the midi file
    # --------------------------------------------------------------------
    mid = MidiFile(filename)
    mididict = []
    for i in mid:
        if i.type == 'note_on' or i.type == 'note_off' or i.type == 'time_signature':
            mididict.append(i.dict())
    # --------------------------------------------------------------------
    # Generate a list from the dictionary with only note_on and time info
    # --------------------------------------------------------------------
    mem1 = 0
    mem2 = [] # Stores each time a note is played
    for i in mididict:
        time = i['time'] + mem1
        i['time'] = time
        mem1 = i['time']
        if i['type'] == 'note_on' and i['velocity'] == 0:
            i['type'] = 'note_off'
        if i['type'] == 'note_on':
            mem2.append(int(i['time']))
    # --------------------------------------------------------------------
    # Print some stupid stuff
    # --------------------------------------------------------------------
    duration = max(mem2)
    minutes = duration // 60
    secondes = duration - (minutes * 60)

    print("Number of notes:", len(mem2), "\n\n")
    print("The song has a duration of {} seconds, which is {} minutes and {} seconds..\n\n".format(duration, minutes, secondes))
    # --------------------------------------------------------------------
    # Generate a list with the total amount of note per second
    # --------------------------------------------------------------------
    notes = [[0,0]] # Add one frame for second 0 and 0 note
    for i in range(int(duration)+1):
        notes.append([i+1,mem2.count(i)])
    notes.append([int(duration)+2,0]) # Add one frame for last second and 0 note
    # --------------------------------------------------------------------
    # Return the list notes[i] = [time, notes/sec]
    # --------------------------------------------------------------------
    return notes

# ----------------------------------------------------------
# Generate 1 frame
# ----------------------------------------------------------

def video(tps,txte,my_video,txte1,foldername,font="CMY Bright",color="white",fontsize=100,notes="NOTES/SEC: ",total="TOTAL: "):
    """
    :param tps: clip start time
    :param txte: text of the clip, basically the number of notes per second
    :param my_video: video on which to add the text
    :param txte1: text of the clip, basically the total of the notes played
    :param foldername: name of the folder in which to save the clip
    :return: A ".mp4" video with all of the above in the correct folder.
    Add the new video to the global list of video created.
    """

    # --------------------------------------------------------------------
    # Adding text (notes/sec on the left side, total notes on the right)
    # --------------------------------------------------------------------

    my_text  = mp.TextClip(notes + txte, font = font, color = color, fontsize = fontsize).set_position((10,0))
    my_text1 = mp.TextClip(total + txte1,font = font, color = color, fontsize = fontsize).set_position((10,fontsize*1.2))
    # --------------------------------------------------------------------
    # Save the video
    # --------------------------------------------------------------------
    final = mp.CompositeVideoClip([my_video, my_text,my_text1])
    save_as = foldername + "/partial_video_output_" + str(tps) + ".mp4"
    final.subclip(tps,tps+1).write_videofile(save_as, fps = 1, codec ="libx264")
    # --------------------------------------------------------------------
    # Add the new video into the global clips list
    # --------------------------------------------------------------------
    global clips
    clips.append(mp.VideoFileClip(save_as))

# ----------------------------------------------------------
# Generate full video
# ----------------------------------------------------------
def video1(filename,foldername,fontsize,note,total, w=1000,h=250,colorbg=(0,0,0),colortxt="white",font="CMU Bright",videooutput="/final_video_output.mp4"):
    """
    :param filename: name of the .mid file to analyze.
    :param foldername: name of the folder in which to save the clip
    :param videoname: output file name of the video
    :return: "This is so long" if it succeeds, it never crashes.
    Write the output video into the "foldername" folder.
    """
    # --------------------------------------------------------------------
    # Import some globals variables
    # --------------------------------------------------------------------
    global clips,avancement,avancement1,t,duration
    # --------------------------------------------------------------------
    # Generate the notes list with notes/sec and tot count
    # --------------------------------------------------------------------
    notes = midifile(filename)
    # --------------------------------------------------------------------
    # I don't play music, I don't care about audio=True
    # --------------------------------------------------------------------
    #my_video = mp.VideoFileClip(videoname,audio=False).resize((w,h))
    my_video = mp.ColorClip((w,h),color=colorbg)
    # --------------------------------------------------------------------
    # Creating every single seconds of the video
    # --------------------------------------------------------------------
    notes_counter = 0 # Initialize the total notes counter
    for i in range (len(notes)): # 'for' loops for life

        # I've try to make a progress bar but...
        # ... it works only when the file is corrupt
        procent = ((i+1)/(len(notes)))*100
        procent = "{}% of partial videos were generated".format(procent)
        advancement.configure(text=procent) #
        # Generate 1 frame of the video
        tps = int(notes[i][0])                  # When
        txte = str(notes[i][1])                 # Notes/sec
        notes_counter += notes[i][1]            # Total
        # Create video
        video(tps,txte,my_video,str(notes_counter),foldername,font,colortxt,fontsize,note,total)

    final_clip = concatenate_videoclips(clips)
    # --------------------------------------------------------------------
    # Writing the final video
    # --------------------------------------------------------------------
    videooutput = foldername + videooutput
    final_clip.write_videofile(videooutput,fps=25)
    for i in range(len(notes)):
        tps = int(notes[i][0])
        save_as = foldername + "/partial_video_output_" + str(tps) + ".mp4"
        os.remove(save_as)
    clips = []
    # --------------------------------------------------------------------
    # Small texts to celebrate all this shit
    # --------------------------------------------------------------------
    advancement.configure(text="Rendering done",fg="green")
    advancement1.configure(text="Video save as "+str(videooutput),fg="green")
    tpstot = time.time() - t # Because speed is important
    finished = "This was soooooooooooooooooooooo long: "+ str(tpstot)+ " seconds,\n wich is " +str(round((tpstot / duration) * 100, 2))+"% the length of the original video."
    advancement2 = Label(text=finished,fg="green")
    advancement2.grid(column=1,row=9)
    advancement2.configure(text=finished,fg="green")

# --------------------------------------------------------------------
# Basic visual interface
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Init Tkinter
# --------------------------------------------------------------------
window = Tk()
window.title("Notes/secondes from midi files")
window.geometry("820x450")
# --------------------------------------------------------------------
# Initialize global filename, videoname & foldername
# --------------------------------------------------------------------
filename   = ""
foldername = ""
fontsize = 100
w = int(fontsize*5)
h = int(fontsize*2.5)
colorbg = (0,0,0)
colortxt = "white"
font = "CMU Bright"
notes = "NOTES/SEC: "
total = "TOTAL: "
videooutput = "/final_video_output.mp4"
# --------------------------------------------------------------------
# 4 buttons, 4 fonctions
# --------------------------------------------------------------------

def clicked():
    """
    :return: global filename
    """
    global filename
    filename = askopenfilename(title="Choose your midi file",filetypes=[('Midi file', '.mid')])

    if len(filename)>0: #checks if there is a file selected
        open.configure(text="File successfully opened",fg="green")
        open02.configure(text= str(filename)+" file opened.")

    return filename


def clicked1():
    """
    :return: global foldername
    """
    global foldername
    foldername = askdirectory(title="Choose an output folder")

    if len(foldername)>0: #checks if there is a folder selected
        open2.configure(text="Folder successfully opened",fg="green")
        open22.configure(text= str(foldername) +" folder opened.")

    return foldername

def clicked2():
    """
    :return: successfully created video
    """
    global foldername,filename,w,h,colorbg,colortxt,font,fontsize,notes,total,videooutput
    # Because speed is important (I know, I don't return or print time, but it's OK.)
    t = time.time()
    if int(getfontsize1.get())>0:
       fontsize = int(getfontsize1.get())
    if len(getfont1.get()) > 0:
        font = getfont1.get()
    if len(getcolor1.get()) >0:
        colortxt = getcolor1.get()
    if len(getnotes1.get()) >0:
        notes = getnotes1.get()
    if len(gettotal1.get())>0:
        total = gettotal1.get()
    if len(getvideooutput.get())>0:
        videooutput = "/"+ getvideooutput.get() + ".mp4"
    w = int(fontsize*10)
    h = int(fontsize*2.5)
    video1(filename,foldername,fontsize,notes,total, w, h, colorbg,colortxt,font,videooutput)
    openfolder = Button(window, text="Open folder",command = clicked3)
    openfolder.grid(column=1,row=11)
    openfile4 = Button(window, text="Launch file", command=clicked4)
    openfile4.grid(column=1, row=13)
    return foldername

def clicked3():
    global foldername, videooutput
    filepath = foldername
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))
    openfolder = Label(window,text="Folder succesfully opened",fg='green')
    openfolder.grid(column=1,row=12)
def clicked4():
    global foldername, videooutput
    filepath = foldername + videooutput
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))
    openfolder = Label(window, text="File succesfully launched", fg='green')
    openfolder.grid(column=1, row=14)
# --------------------------------------------------------------------
# Configure texts and buttons of the Tkinter window
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Midi file
# --------------------------------------------------------------------
open02 = Label(window,text="")
open02.grid(column=1,row=1)
open = Label(window,text="  No midi file opened  ",fg="red")
open.grid(column=0,row=0)
openfile = Button(window,text="Choose your midi file",command=clicked)
openfile.grid(column=1,row=0)
# --------------------------------------------------------------------
# Output folder
# --------------------------------------------------------------------
open22 = Label(window,text="")
open22.grid(column=1,row=3)
open2 = Label(window,text="  No folder selected    ",fg="red")
open2.grid(column=0,row=2)
openfile2 = Button(window,text="Choose an output folder",command=clicked1)
openfile2.grid(column=1,row=2)
# --------------------------------------------------------------------
# Render the video
# --------------------------------------------------------------------
openfile3 = Button(window,text="Render the video",command=clicked2)
openfile3.grid(column=1,row=4)
# --------------------------------------------------------------------
# ... progress bar ...
# --------------------------------------------------------------------
advancement = Label(window,text="0%",fg="red")
advancement.grid(column=1,row=5)
advancement1 = Label(window,text=" "*70 + "0%" + " "*70,fg="red")
advancement1.grid(column=1,row=6)
# --------------------------------------------------------------------
# color, font
# --------------------------------------------------------------------
getfontsize = Label(window,text="Fontsize")
getfontsize.grid(column=2,row=0)
getfontsize1 = Entry(window)
getfontsize1.insert(0,"100")
getfontsize1.grid(column=3,row=0)
getcolor = Label(window,text="Text color")
getcolor.grid(column=2,row=1)
getcolor1 = Entry(window)
getcolor1.insert(0,'White')
getcolor1.grid(column=3,row=1)
getfont = Label(window,text="Font")
getfont.grid(column=2,row=2)
getfont1 = Entry(window)
getfont1.insert(0,"CMU Bright")
getfont1.grid(column=3,row=2)
getnotes = Label(window,text="Text notes/secondes")
getnotes.grid(column=2,row=3)
getnotes1 = Entry(window)
getnotes1.insert(0,"NOTES/SEC: ")
getnotes1.grid(column=3,row=3)
gettotal = Label(window,text="Text total")
gettotal.grid(column=2,row=4)
gettotal1 = Entry(window)
gettotal1.insert(0,"TOTAL: ")
gettotal1.grid(column=3,row=4)
getvideooutput = Label(window,text="Video output name")
getvideooutput.grid(column=2,row=5)
getvideooutput = Entry(window)
getvideooutput.insert(0,"final_video_output")
getvideooutput.grid(column=3,row=5)
# --------------------------------------------------------------------
# And of course...
# --------------------------------------------------------------------
window.mainloop()