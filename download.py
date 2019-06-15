import os
import sys
from pytube import YouTube

path = os.path.abspath('')
url = 'https://www.youtube.com/watch?v=gQrkvZeE3Uc'
yt = YouTube("https://www.youtube.com/watch?v=n06H7OcPd-g")
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first().download(output_path=path+'\\source')