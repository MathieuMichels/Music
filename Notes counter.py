from mido import MidiFile
import moviepy.editor as mp
from moviepy.editor import concatenate_videoclips
import time
from tkinter import *
from tkinter.filedialog import *
t = time.time()
duree = 0
def midifile(filename):
    mid = MidiFile(filename)
    mididict = []
    for i in mid:
        if i.type == 'note_on' or i.type == 'note_off' or i.type == 'time_signature':
            mididict.append(i.dict())
    mem1=0
    mem2=[]
    mem3=[]
    for i in mididict:
        time = i['time'] + mem1
        i['time'] = time
        mem1 = i['time']
        if i['type'] == 'note_on' and i['velocity'] == 0:
            i['type'] = 'note_off'
        if i['type'] == 'note_on':
            mem2.append(i['time'])
        if i['type'] == 'note_off':
            mem3.append(i['time'])

    #print("Number of notes:", len(mem2))
    global duree
    duree = max(mem2)
    minutes = duree//60
    secondes = duree - (minutes*60)
    #print("Le morceau dure {} secondes, soit {} minutes et {} secondes.".format(duree,minutes,secondes))
    #print("mem2",mem2)
    for i in range(len(mem2)-1):
        mem2[i] = int(mem2[i])
    for i in range(len(mem3)-1):
        mem3[i] = int(mem3[i])
    print(len(mem2))
    #print(len(mem1))
    print(len(mem3))

    notes = [[0,0]]

    for i in range(int(duree)+1):
        notes.append([i+1,mem2.count(i)])
    #print(notes)
    notes.append([int(duree)+2,0])
    print(notes)
    print(len(notes))
    return notes
#midifile("Release/variation.mid")
def video(tps,txte,my_video,txte1,foldername):

    """Ouverture du fichier"""

    w, h = my_video.size #infos sur la taille de la vidéo (largeur, hauteur)
    my_video = my_video.subclip(tps,tps+1)

    my_text = mp.TextClip(txte, font ="Times New Roman", color ="white", fontsize = 100)
    txt_col = my_text.on_color(size=(my_video.w + my_text.w, my_text.h + 5), color=(0, 0, 0), pos=(6,"center"), col_opacity=0.6)
    txt_mov = txt_col.set_pos(lambda t: (max(int(360), int(360)), max(int(540), int(540))))
    my_text1 = mp.TextClip(txte1, font="Times New Roman", color="white", fontsize=100)
    txt_col1 = my_text1.on_color(size=(my_video.w + my_text.w, my_text.h + 5), color=(0, 0, 0), pos=(6, "center"),
                               col_opacity=0.6)
    txt_mov1 = txt_col1.set_pos(lambda t: (max(int(960), int(960)), max(int(540), int(540))))
    final = mp.CompositeVideoClip([my_video, txt_mov,txt_mov1])

    lieu = foldername
    lieu += "/partial_video_output_"
    lieu += str(tps)
    lieu += ".mp4"
    final.subclip(tps,tps+1).write_videofile(lieu, fps = 1, codec ="libx264")

    global clips
    clips.append(lieu)

clips = []
def video1(filename,foldername,videoname):

    global clips,avancement,avancement1,t,duree
    notes = midifile(filename)
    my_video = mp.VideoFileClip(videoname,audio=False)
    txte1=0
    for i in range (len(notes)):
        procent = ((i+1)/(len(notes)))*100
        procent01 = "{}% of partial videos were generated".format(procent)
        avancement.configure(text=procent01)
        tps = int(notes[i][0])
        txte = str(notes[i][1])
        txte1 += notes[i][1]
        video(tps,txte,my_video,str(txte1),foldername)
    #print(clips)

    final_clip = concatenate_videoclips([mp.VideoFileClip(clips[0])])
    for i in range(len(clips)):
        procent1 = ((i+1)/(len(notes)))*100
        procent11 = "{}% 5% of video merge initialization is complete".format(procent1)
        avancement1.configure(text=procent11)
        final_clip = concatenate_videoclips([final_clip,mp.VideoFileClip(clips[i])])
    videooutput = foldername + "/final_video_output.mp4"
    final_clip.write_videofile(videooutput,fps=25)
    avancement.configure(text="Rendering done",fg="green")
    avancement1.configure(text="Video save as "+str(videooutput),fg="green")
    tpstot = time.time() - t
    fini = "This is soooooooooooooooooooooo long: "+ str(tpstot)+ " seconds,\n wich is " +str(round((tpstot / duree) * 100, 2))+"% the length of the original video."
    avancement2 = Label(text=fini,fg="green")
    avancement2.grid(column=1,row=9)
    avancement2.configure(text=fini,fg="green")




window = Tk()
window.title("Notes/secondes from midi files")
window.geometry("700x250")

filename=""
def clicked():
    global filename
    filename = askopenfilename(title="Choisissez votre fichier midi",
                               filetypes=[('Midi file', '.mid')])
    if len(filename)>0:
        ouvert.configure(text="Fichier correctement ouvert",fg="green")
        ouvert02.configure(text="Fichier "+str(filename)+" ouvert.")
    return filename
ouvert02 = Label(window,text="")
ouvert02.grid(column=1,row=1)
ouvert = Label(window,text="Aucun fichier ouvert",fg="red")
ouvert.grid(column=0,row=0)
ouvrirfichier = Button(window,text="Choisissez votre fichier midi",command=clicked)
ouvrirfichier.grid(column=1,row=0)
avancement = Label(window,text="")
avancement.grid(column=1,row=7)
avancement1 = Label(window,text="")
avancement1.grid(column=1,row=8)
videoname = ""
def clicked1():
    global videoname
    videoname = askopenfilename(title="Choisissez une vidéo noire",filetypes=[('Video file', '.mp4')])
    if len(videoname)>0:
        ouvert1.configure(text="Fichier correctement ouvert",fg="green")
        ouvert12.configure(text="Fichier " + str(videoname) + " ouvert.")
    return videoname
ouvert12 = Label(window,text="")
ouvert12.grid(column=1,row=3)
ouvert1 = Label(window,text="Aucun fichier ouvert",fg="red")
ouvert1.grid(column=0,row=2)
ouvrirfichier1 = Button(window,text="Choisissez une vidéo noire",command=clicked1)
ouvrirfichier1.grid(column=1,row=2)

foldername = ""
def clicked2():
    global foldername
    foldername = askdirectory(title="Choisissez un dossier de sortie")
    if len(foldername)>0:
        ouvert2.configure(text="Dossier correctement ouvert",fg="green")
        ouvert22.configure(text="Dossier "+str(foldername)+" ouvert.")
    return foldername
ouvert22 = Label(window,text="")
ouvert22.grid(column=1,row=5)
ouvert2 = Label(window,text="Aucun fichier ouvert",fg="red")
ouvert2.grid(column=0,row=4)
ouvrirfichier2 = Button(window,text="Choisissez un dossier de sortie",command=clicked2)
ouvrirfichier2.grid(column=1,row=4)

def clicked3():
    global foldername,filename,videoname,t
    t = time.time()
    video1(filename,foldername,videoname)
    return foldername


ouvrirfichier3 = Button(window,text="Rendre la vidéo",command=clicked3)
ouvrirfichier3.grid(column=1,row=6)

window.mainloop()