from moviepy.editor import *
from moviepy.audio.fx.all import *
from PIL import Image
import multiprocessing as mp
import concurrent.futures
import numpy as np # for numerical operations
import subprocess, os, platform

#File pahts, flags and output
work_dir = 'work'
offset_row_dir = 'rowoff'

#Length of all clips
start = 0
stop = 17
#Video sync related
frames_per_second = 25
buffer_duration = 3
audiopeak = 0
#Number of videos in mosaic
videoX = 5
videoY = 5
#640x360
xDimension = 160
yDimension = 90
# Data holder
videos = []
x = 0
y = 0

#Lambda helper to get a cut of the clip as soundarray and calculate the mean volume of it
cut = lambda i, clip: clip.audio.subclip(i,i+1/frames_per_second).to_soundarray(fps=2000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())

def volume_mark(clip):
    for i in np.arange(0,int(clip.audio.duration), 1/frames_per_second): 
        current = volume(cut(i, clip))
        if current >= audiopeak:
            print("Sync peak at %f -> %f for %s"%(i, current, filename))
            return i

#Prepare workdir
try:
    os.mkdir(work_dir)
except FileExistsError:
    print('Wokrdir already exists')
try:
    os.mkdir(work_dir + '/' + offset_row_dir)
except FileExistsError:
    print('Rowdir already exists')
    
#Iterate over workdir files, position clips and generate videos per row to preserve memory
for ap in np.arange(0.01, 0.2, 0.01):
    audiopeak = ap
    for file in sorted(os.listdir(work_dir), reverse=True):
        filename = os.fsdecode(file)
        if filename.endswith('.mp4'):
            row_output = '%s/%s/r_%02d_%f.mp4'% (work_dir, offset_row_dir, y, audiopeak)
            if not os.path.exists(row_output):
                print('Load file: %s/%s (%i,%i)' % (work_dir, filename, x, y))
                input_video = VideoFileClip(work_dir + '/' + filename)
                input_video = audio_normalize(input_video)
                videos.append(input_video.subclip(volume_mark(input_video) - buffer_duration, stop).set_position((x * xDimension, 0)))
                
            if x < videoX - 1:
                x = x + 1
            else: 
                if os.path.exists(row_output):
                    print('Row already exists, %s'% (row_output))
                else:
                    print('Render row: %s'% (row_output))
                    CompositeVideoClip(videos, size=(xDimension*(videoX),yDimension)).subclip(2.5, stop).write_videofile(row_output)
                    for video in videos:
                        try:
                            video.audio.reader.close_proc()
                            video.reader.close()
                        except Exception as e:
                            pass
                        
                        try:
                            video.close()
                        except Exception as e:
                            print('Failed to close video, %s/%s'% (work_dir, filename))
                    video = []
                x = 0
                print("Reached end of area")
                break



print('Rows generated')