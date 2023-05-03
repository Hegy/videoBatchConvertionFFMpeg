#handler.py
import os
import ctypes
import sys
import subprocess
import pkg_resources

required = {'inquirer', 'tqdm'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import inquirer
from progress import Progress

def promtUser():
    ffmpegParameters = {'_1200K_H265_aac':'-c:v libx265 -b 1200K -c:a aac', 
                        '_2880K_H265_aac':'-c:v libx265 -b 2880K -c:a aac', 
                        '_6000K_H265_aac':'-c:v libx265 -b 6000K -c:a aac', 
                        '*':'',
                        '_ultrafast_1200K_H265_aac':'-c:v libx265 -b 1200K -preset ultrafast -c:a aac', 
                        '_1280x720_1200K_H265_aac':'-s 1280x720 -c:v libx265 -b 1200K -c:a aac',
                        '_1920x1080_1200K_H265_aac':'-s 1920x1080 -c:v libx265 -b 1200K -c:a aac',
                        '_1920x1080_2880K_H265_aac':'-s 1920x1080 -c:v libx265 -b 2880K -c:a aac',
                        '_1920x1080_6000K_H265_aac':'-s 1920x1080 -c:v libx265 -b 6000K -c:a aac',
                        '_1080x1920_6000K_H265_aac':'-s 1080x1920 -c:v libx265 -b 6000K -c:a aac',
                        '_deinterlace_1200K_H265_aac':'-vf yadif -c:v libx265 -b 1200K -c:a aac',
                        }

    #  Для HD-video 1280×720 < -b 2550K >, для Full-HD 1920×1080 < -b 5760K >
    questions = [
      inquirer.List('parameters',
                    message="What parameters do you need?",
                    choices=[*ffmpegParameters], 
                    carousel=True,
                ),
    ]
    answers = inquirer.prompt(questions)

    # print (answers["parameters"])
    # print(ffmpegParameters[answers["parameters"]])
    return answers["parameters"], ffmpegParameters[answers["parameters"]]

def run_command(command):
    """ Run the command, capture output and send it to the
        Progress Object. """
    progress = Progress()
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8'
        )
    for line in process.stdout:
        # line = line.decode('utf-8')
        progress.show_progress(line.strip())
    exit_code = process.wait()
    if exit_code:
        progress.clear()
        if not progress.verbose:
            print(progress.stdout_log)
    progress.cleanup()


if __name__ == "__main__":
    print("hello!")
    MessageBox = ctypes.windll.user32.MessageBoxW
    
    list = sys.argv[1:]

    presetName, params = promtUser()

    for inputFile in list:
        
        fileNameWPath, fileExtension = os.path.splitext(inputFile)
        stinfo = os.stat(inputFile)

        print(fileNameWPath+fileExtension)
        print(list.index(inputFile)+1, '/', len(list), os.path.split(inputFile)[1])

        commandLine = 'ffmpeg.exe -nostdin -i "' + inputFile + '" ' + params + ' "' + fileNameWPath + presetName + '.mp4"'
        # MessageBox(None, commandLine, 'Window title', 0)
        run_command(commandLine)
        
        # Modifying atime and mtime
        os.utime(fileNameWPath + presetName + '.mp4', (stinfo.st_mtime, stinfo.st_mtime))

    # MessageBox(None, "END", 'Window title', 0)
    # os.system("start C:\Windows\Media\Alarm03.wav")
    os.system("rundll32.exe cmdext.dll,MessageBeepStub")
    print(os.path.split(inputFile)[0])
    input("Press Enter to continue...")
    os.system(f'explorer "{os.path.split(inputFile)[0]}"')
    

# ---------------------------
# Window title
# ---------------------------
# ffmpeg C:\Dell\MVI_2062.MOV -c:v libx265 -b 2880K -c:a aac C:\Dell\00000001_2880K_H265_aac.mp4
                            # -c:v libx265 -b 1200K -c:a aac
# ---------------------------
# ОК   
# ---------------------------



# os.system("pause")
# print ("The full path for this file is %s!" % sys.argv[1])
# os.system("pause")


#"C:\Users\1\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\pythonw.exe" "C:\Temp\ffmpeg_mp4.py" "%1"

# import sys
# import tkinter as tk
# from tkinter import filedialog

# root = tk.Tk()
# # root.withdraw()
# # specify size of window.
# root.geometry("250x170")
 
# # Create text widget and specify size.
# T = Text(root, height = 5, width = 52)
 
# # Create label
# l = Label(root, text = "Fact of the Day")
# l.config(font =("Courier", 14))
 
# Fact = """A man can be arrested in
# Italy for wearing a skirt in public."""
 
# # Create button for next text.
# b1 = Button(root, text = "Next", )
 
# # Create an Exit button.
# b2 = Button(root, text = "Exit",
            # command = root.destroy)
 
# l.pack()
# T.pack()
# b1.pack()
# b2.pack()
 
# # Insert The Fact.
# T.insert(tk.END, Fact)
 
# tk.mainloop()
# # file_path = filedialog.askopenfilename()

# # def hello(a):
    # # print ("hello and that's your sum:", a)

# # a = int(sys.argv[1])
# # hello(a)
# If you type : py main.py 1 5
# It should give you "hello and that's your sum:6"
