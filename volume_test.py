import numpy as np # for numerical operations
from moviepy.editor import VideoFileClip, concatenate


# test out the get volume function

clip = VideoFileClip("source/20190619_2-pXg_U27dw.mp4").subclip(0, 10)

step = 1/25
cut = lambda i: clip.audio.subclip(i,i+step).to_soundarray(fps=200)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in np.arange(0,int(clip.audio.duration),step)] 

maximum = 0
for i, v in enumerate(volumes, start=0):
	if v > maximum:
		print("%f -> %i"%(v,i))
		maximum = v
