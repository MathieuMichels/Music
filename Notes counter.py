# ----------------------------------------------------------
# import some packages
# ----------------------------------------------------------
from mido import MidiFile                         # Open midi files
import moviepy.editor as mp                       # Video editor
from moviepy.editor import concatenate_videoclips # Merging videos
import time                                       # Because speed is important
from tkinter import *                             # Visual interface
from tkinter.filedialog import *                  # Easy file opening
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
    print("The song has a duration of {} seconds, which is {} minutes and {} seconds..\n\n".format(duration, minutes,
                                                                                                   secondes))
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
def video(tps,txte,my_video,txte1,foldername):
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
    # video settings (size & time)
    # --------------------------------------------------------------------

    w, h = my_video.size
    my_video = my_video.subclip(tps,tps+1)

    # --------------------------------------------------------------------
    # Adding text (notes/sec on the left side, total notes on the right)
    # --------------------------------------------------------------------

    my_text = mp.TextClip(txte, font ="Times New Roman", color ="white", fontsize = 100)
    txt_col = my_text.on_color(size=(my_video.w + my_text.w, my_text.h + 5), color=(0, 0, 0), pos=(6,"center"), col_opacity=0.6)
    txt_mov = txt_col.set_pos(lambda t: (max(int(360), int(360)), max(int(540), int(540))))
    my_text1 = mp.TextClip(txte1, font="Times New Roman", color="white", fontsize=100)
    txt_col1 = my_text1.on_color(size=(my_video.w + my_text.w, my_text.h + 5), color=(0, 0, 0), pos=(6, "center"), col_opacity=0.6)
    txt_mov1 = txt_col1.set_pos(lambda t: (max(int(960), int(960)), max(int(540), int(540))))

    # --------------------------------------------------------------------
    # Save the video
    # --------------------------------------------------------------------
    final = mp.CompositeVideoClip([my_video, txt_mov,txt_mov1])
    save_as = foldername + "/partial_video_output_" + str(tps) + ".mp4"
    final.subclip(tps,tps+1).write_videofile(save_as, fps = 1, codec ="libx264")

    # --------------------------------------------------------------------
    # Add the new video into the global clips list
    # --------------------------------------------------------------------
    global clips
    clips.append(save_as)

# ----------------------------------------------------------
# Generate full video
# ----------------------------------------------------------
def video1(filename,foldername,videoname):
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
    my_video = mp.VideoFileClip(videoname,audio=False)
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
        video(tps,txte,my_video,str(notes_counter),foldername)

    # Initialize concatenate video
    final_clip = concatenate_videoclips([mp.VideoFileClip(clips[0])])
    # --------------------------------------------------------------------
    # Concatenate the differents clips to create the final video
    # --------------------------------------------------------------------
    for i in range(len(clips)):
        # Again, I've try to make a progress bar but...
        # ... it works only when the file is corrupt
        procent1 = ((i+1)/(len(notes)))*100
        procent11 = "{}% 5% of video merge initialization is complete".format(procent1)
        advancement1.configure(text=procent11)
        # Merge the video with the previous merging
        final_clip = concatenate_videoclips([final_clip,mp.VideoFileClip(clips[i])])
    # --------------------------------------------------------------------
    # Writing the final video
    # --------------------------------------------------------------------
    videooutput = foldername + "/final_video_output.mp4"
    final_clip.write_videofile(videooutput,fps=25)
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
window.geometry("700x250")
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
    :return: global videoname
    """
    global videoname

    videoname = askopenfilename(title="Choose the black video",filetypes=[('Video file', '.mp4')])

    if len(videoname)>0: #checks if there is a file selected

        open1.configure(text="Video successfully opened",fg="green")
        open12.configure(text= str(videoname) + " video opened.")

    return videoname

def clicked2():
    """
    :return: global foldername
    """
    global foldername
    foldername = askdirectory(title="Choose an output folder")

    if len(foldername)>0: #checks if there is a folder selected
        open2.configure(text="Folder successfully opened",fg="green")
        open22.configure(text= str(foldername) +" folder opened.")

    return foldername

def clicked3():
    """
    :return: successfully created video
    """
    global foldername,filename,videoname,t
    # Because speed is important (I know, I don't return or print time, but it's OK.)
    t = time.time()
    video1(filename,foldername,videoname)
    return foldername

# --------------------------------------------------------------------
# Initialize global filename, videoname & foldername
# --------------------------------------------------------------------
filename   = ""
videoname  = ""
foldername = ""
# --------------------------------------------------------------------
# Configure texts and buttons of the Tkinter window
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Midi file
# --------------------------------------------------------------------
open02 = Label(window,text="")
open02.grid(column=1,row=1)
open = Label(window,text="No files opened",fg="red")
open.grid(column=0,row=0)
openfile = Button(window,text="Choose your midi file",command=clicked)
openfile.grid(column=1,row=0)
# --------------------------------------------------------------------
# Black video
# --------------------------------------------------------------------
open12 = Label(window,text="")
open12.grid(column=1,row=3)
open1 = Label(window,text="No files opened",fg="red")
open1.grid(column=0,row=2)
openfile1 = Button(window,text="Choose the black video",command=clicked1)
openfile1.grid(column=1,row=2)
# --------------------------------------------------------------------
# Output folder
# --------------------------------------------------------------------
open22 = Label(window,text="")
open22.grid(column=1,row=5)
open2 = Label(window,text="No files opened",fg="red")
open2.grid(column=0,row=4)
openfile2 = Button(window,text="Choose an output folder",command=clicked2)
openfile2.grid(column=1,row=4)
# --------------------------------------------------------------------
# Render the video
# --------------------------------------------------------------------
openfile3 = Button(window,text="Render the video",command=clicked3)
openfile3.grid(column=1,row=6)
# --------------------------------------------------------------------
# ... progress bar ...
# --------------------------------------------------------------------
advancement = Label(window,text="0%",fg="red")
advancement.grid(column=1,row=7)
advancement1 = Label(window,text="0%",fg="red")
advancement1.grid(column=1,row=8)
# --------------------------------------------------------------------
# And of course...
# --------------------------------------------------------------------
window.mainloop()