# videoBatchConvertionFFMpeg
MS Windows Right click batch video conversion using ffmpeg

You can add this to your context menu using two different ways

(recommended)
1) Put a batch_convert_video.py file or link to this file into shell:sendto folder

or

2) You can also add custom context menu on right click for with Default Program Editor http://defaultprogramseditor.com/

# Require

python
https://www.python.org/downloads/

ffprogress 
https://github.com/Hegy/ffprogress/releases

FFMpeg https://ffmpeg.org/
direct link for win build https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z

file from this project "batch_convert_video_auto.py"
https://github.com/Hegy/videoBatchConvertionFFMpeg/releases/tag/videoBatchConvertionFFMpeg


# Instalaltion

1) download and install python if not exists
2) download and extract ffmpeg into C:\ffmpeg (full path to exe should be like this "C:\ffmpeg\bin\ffmpeg.exe") (Or set up path in ini file on the first run)
3) download and extraxt FFProgress into C:\ffmpeg\FFProgress
4) download and extract file batch_convert_video_auto.py into C:\ffmpeg\FFProgress
5) place link to the file C:\ffmpeg\FFProgress\batch_convert_video_auto.py into sendto folder (win+R -> shell:sendto)
