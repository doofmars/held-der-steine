from moviepy.editor import *
from PIL import Image
import multiprocessing as mp
import concurrent.futures
import numpy as np # for numerical operations
import subprocess, os, platform

#Youtuber target url
youtube_url = 'https://www.youtube.com/user/HeldderSteine'

#File pahts, flags and output
source_dir = 'source'
work_dir = 'work'
loaded_flag = 'loaded'
output = 'my_stack.mp4'
black_image = 'black.png'

#Length of all clips
start = 0
stop = 10
#Video sync related
audiopeak = 0.015
frames_per_second = 25
buffer_duration = 2
#Number of videos in mosaic
videoX = 19
videoY = 19
#640x360
xDimension = 160
yDimension = 90
# Data holder
videos = []
work = []
count = 0
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

def prepare_file(filename):
    input_video = VideoFileClip(source_dir + '/' + filename).resize(width=xDimension).subclip(start, stop)
    concatenate_videoclips([blank, input_video]).subclip(volume_mark(input_video), stop + buffer_duration).write_videofile(work_dir + '/' + filename, verbose=False)
    try:
        input_video.audio.reader.close_proc()
        input_video.reader.close()
    except Exception as e:
        pass
    
    try:
        input_video.close()
    except Exception as e:
        print('Failed to close video, %s/%s'% (work_dir, filename))
        
    return filename

#Start downloading using youtube-dl
if not os.path.exists(source_dir + '/' + loaded_flag):
    open(source_dir + '/' + loaded_flag, 'a').close()
    os.system('youtube-dl -o "'+source_dir+'/%(upload_date)s_%(id)s.%(ext)s" -f worst ' + youtube_url)
else:
    print('Source files already downloaded')
    
#Prepare workdir
try:
    os.mkdir(work_dir)
except FileExistsError:
    print('Wokrdir already exists')

#Create blank video as buffer before videos
img = Image.new('RGB', (xDimension, yDimension))
img.save(work_dir + '/' + black_image)
blank = ImageClip(work_dir + '/' + black_image, duration=buffer_duration)

#Iterate over source files, add black offset and sync timing to first noise in video. Save into workdir
for file in sorted(os.listdir(source_dir), reverse=True):
    filename = os.fsdecode(file)
    if filename.endswith('.mp4'): 
        count = count + 1
        
        if os.path.exists(work_dir + '/' + filename):
            print('%s/%s already exists, #%d'% (work_dir, filename, count))
        else:
            print('Perpare file: %s/%s, #%d'% (source_dir, filename, count))
            work.append(filename)
        
        if count > (videoX * videoY):
            print('Preparation done')
            break

with concurrent.futures.ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
    future_prepare_file = {executor.submit(prepare_file, filename): filename for filename in work}
    for future in concurrent.futures.as_completed(future_prepare_file):
        future_processed_filename = future_prepare_file[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%s generated an exception: %s' % (future_processed_filename, exc))
        else:
            print('Processed %s' % (data))
    
    
# pool.apply(prepare_file, args=(filename))
        
#Iterate over workdir files, position clips and put into holding array
for file in sorted(os.listdir(work_dir), reverse=True):
    filename = os.fsdecode(file)
    if filename.endswith('.mp4'):
        print('Load file: %s/%s (%i,%i)' % (work_dir, filename, x, y))
        videos.append(VideoFileClip(work_dir + '/' + filename).set_position((x * xDimension, y * yDimension)))
        
        if x < videoX - 1:
            x = x + 1
        else: 
            x = 0
            y = y + 1
            if y >= videoY:
                print("Reached end of area")
                break
    
#final_clip = clips_array([[video0, video1, video2, video3], [video4, video5, video6, video7]])
#final_clip.resize(width=1920).write_videofile("my_stack.mp4")

#Composite clips and render out
CompositeVideoClip(videos, size=(xDimension*(videoX),yDimension*(videoY))).resize(width=1920).write_videofile(output)

# Finally open rendered video
if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', os.path.join(os.path.abspath(''), output)))
elif platform.system() == 'Windows':    # Windows
    os.startfile(os.path.join(os.path.abspath(''), output))
else:                                   # linux variants
    subprocess.call(('xdg-open', os.path.join(os.path.abspath(''), output)))