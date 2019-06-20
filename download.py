import os
import sys
from pytube import YouTube
from pytube import Playlist

playlist = Playlist('https://www.youtube.com/watch?v=OTuuNXpp3LE&list=PLtQoBfL4IptTmMtyFyGvh1XSOsM_3R3Oq')
print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(playlist)

exit()

path = os.path.abspath('')
yt = YouTube("https://www.youtube.com/watch?v=tr9_NDVYoJc")
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=path+'\\source')