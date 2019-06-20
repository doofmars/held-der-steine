from moviepy.editor import *
import os

directory = os.fsencode('source/Minifigures')

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".mp4"): 
         print(filename)
         continue
     else:
         continue


start = 0
stop = 1

video0 = VideoFileClip( 'source/Minifigures/20141004_QwvV2zfCL68.mp4').subclip(start, stop)
video1 = VideoFileClip( 'source/Minifigures/20150903_syT1qPR_nYI.mp4').subclip(start, stop)
video2 = VideoFileClip( 'source/Minifigures/20170517_-OsKQIMf0ls.mp4').subclip(start, stop)
video3 = VideoFileClip( 'source/Minifigures/20170517_DnCd7KEJNmU.mp4').subclip(start, stop)
video4 = VideoFileClip( 'source/Minifigures/20170806_MXXPJ-oJlTY.mp4').subclip(start, stop)
video5 = VideoFileClip( 'source/Minifigures/20180112_ySMTFt9rftg.mp4').subclip(start, stop)
video6 = VideoFileClip( 'source/Minifigures/20180417_XUbxc-Qt1a8.mp4').subclip(start, stop)
video7 = VideoFileClip( 'source/Minifigures/20180928_Ss69gFLHNqQ.mp4').subclip(start, stop)
video8 = VideoFileClip( 'source/Minifigures/20190202_ldz23LoNhQo.mp4').subclip(start, stop)
video9 = VideoFileClip( 'source/Minifigures/20190414_qYLp4K4LpdA.mp4').subclip(start, stop)
video10 = VideoFileClip('source/Minifigures/20190504_bJCIbEw-JGk.mp4').subclip(start, stop)

#final_clip = clips_array([[video0, video1, video2, video3], [video4, video5, video6, video7]])
#final_clip.resize(width=1920).write_videofile("my_stack.mp4")

CompositeVideoClip([video0, video1.set_position((640, 0)), video2.set_position((0, 360))], size=(1280,720)).write_videofile("my_stack.mp4")
