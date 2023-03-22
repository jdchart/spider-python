
videoPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network/media/Dancing_Philosophy_Solos_improvises.mp4"
outPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network/media/Dancing_Philosophy_Solos_improvisesRESIZE.mp4"


from moviepy.editor import *

videoClip = VideoFileClip(videoPath)

clip_with_borders = videoClip.margin(top=0, bottom=702, left=0, right=0, color=(255, 255, 255))
# BVorders msut be even for some reason


clip_with_borders.write_videofile(outPath)