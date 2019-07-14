import numpy as np # for numerical operations
from moviepy.editor import VideoFileClip, concatenate
import speech_recognition as sr
import os

framerate = 100
temp_file = 'temp.wav'

if not os.path.exists(temp_file):
	clip = VideoFileClip("source/20190619_2-pXg_U27dw.mp4").subclip(0, 10)
	clip.audio.write_audiofile(temp_file)

r = sr.Recognizer()
audioFile = sr.AudioFile(temp_file)
with audioFile as source:
	audio = r.record(source)
	decoder = r.recognize_sphinx(audio, language='de-DE', show_all=False)
	print(decoder)
	

