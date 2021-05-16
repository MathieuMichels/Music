# Music
## Midi file - Note speed

I've always wanted to add a note and note / second counter to my videos, but I couldn't find any software to do this, or a tutorial on how to do it. 
So I took my very poor knowledge of python to achieve this. I first tried by connecting python to Adobe Premiere Pro with Pymiere, 
but the text handling with this system is horrible. Finally I decided to create a separate video as explained below.

I hope it can help a few.

PS: I would like to go from the "per second" version to something more instantaneous. For example, which updates every 10th of a second. 
Or even ideally every time a note is played. 
But I haven't figured out how to do it yet. If anyone knows, I'm interested 😉.

Actually, I found [something that can do what I whant](https://github.com/hccdy/midi-counter-gen), but it's in C#, 
I don't know C# yet, and I've found an issue in his code: instantaneous speed and the total is exactly twice as high as the reality ....



--------------------------------------------------------
### How to run the script for the first time 
In this project you will find a "Notes counter.py" file.

This small python script generates videos based on a midi file and displays the number of notes per second as well as the total.

To use the script, you will first need to install a few packages:

* mido      ```  pip install mido    ```
* moviepy   ```  pip install moviepy ```
* time      ```  pip install time    ```
* tkinter   ```  pip install tkinter ```
* ffmpeg    ```  pip install ffmpeg  ```

### How to use the script
When it's done, you can run the "Notes counter.py" file. This will open a Tkinter window. 
You have to select 3 differents things:
  * the midi file you want to analyze,
  * the video on wich you want to add the text ([you can download my black video](https://github.com/mathieumichels/Music/blob/master/blackvideo.mp4), 
  but you can also make your own video.)
  * an output folder
  
Pay attention to the fact that the output folder will contain s+1 videos with s the length in second of your midi file. 
s+1 because of one per second of video + 1 for the final output.

### Information on the final video
The final video is save as "final_video_output.mp4" in the output folder. 
So, this is an '.mp4' file. 

In this video, you'll have on the left side the notes/sec counter and on the right side the total note counter. 

If you want to change the font, you can do it at line 95 and 98 by changing ```font="CMU Bright"```.

On my computer, it takes about 110 - 140% of the video's time to create the final video. 
It's not fast at all, but like I said I'm not a computer genius, so if some people feel motivated to help me optimize this stuff, I'm interested 😉
