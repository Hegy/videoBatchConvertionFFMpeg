# videoBatchConvertionFFMpeg
MS Windows Right click batch video conversion using ffmpeg

You can add this to your context menu using two different ways

(recommended)
1) Put a batch_convert_video.py file or link to this file into shell:sendto folder

or

2) You can also add custom context menu on right click for with Default Program Editor http://defaultprogramseditor.com/

# Require

python
https://www.python.org/downloads/windows/

ffprogress 
https://github.com/Hegy/ffprogress/releases

FFMpeg https://ffmpeg.org/
direct link for win build https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z

# Instalaltion

1) download and install python if not exists
2) download and extract ffmpeg into C:\ffmpeg
3) download and extraxt FFProgress into C:\ffmpeg\FFProgress


add variables to path ???
  C:\ffmpeg\bin


4) place link to the file C:\ffmpeg\FFProgress\batch_convert_video.py into sendto folder (win+R -> shell:sendto)
