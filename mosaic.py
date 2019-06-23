from moviepy.editor import *
import subprocess, os, platform

#Youtuber target url
youtube_url = 'https://www.youtube.com/user/HeldderSteine'

#File pahts, flags and output
source_dir = 'source'
work_dir = 'work'
loaded_flag = 'loaded'
output = 'my_stack.mp4'

#Length of all clips
start = 0
stop = 10
#Number of videos in mosaic
videoX = 10
videoY = 10
#640x360
xDimension = 320
yDimension = 180
# Data holder
videos = []
x = 0
y = 0

#Start downloading using youtube-dl
if not os.path.exists(source_dir + '/' + loaded_flag):
    open(source_dir + '/' + loaded_flag, 'a').close()
    os.system('youtube-dl -o "'+source_dir+'/%(upload_date)s_%(id)s.%(ext)s" -f worst ' + youtube_url)
else:
	print('Source files already downloaded')

#Iterate over files, position and put into holding array
for file in sorted(os.listdir(source_dir), reverse=True):
    filename = os.fsdecode(file)
    if filename.endswith(".mp4"): 
        print("%s/%s (%i,%i)" % (source_dir, filename, x, y))
        video = VideoFileClip(source_dir + "/" + filename).resize(width=xDimension).subclip(start, stop).set_position((x * xDimension, y * yDimension))
        videos.append(video)
        if x < videoX - 1:
            x = x + 1
        else: 
            x = 0
            y = y + 1
            if y >= videoY:
                print("reached end of area")
                break
    else:
        continue

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