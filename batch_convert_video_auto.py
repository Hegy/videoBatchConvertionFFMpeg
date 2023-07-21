#handler.py
import os
# import ctypes
import sys
import subprocess
import pkg_resources
import configparser
import datetime

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


def move_file(source_path, destination_path):
    try:
        os.rename(source_path, destination_path)
        print(f"File moved successfully from '{source_path}' to '{destination_path}'.")
    except FileNotFoundError:
        print("Error: The source file was not found.")
    except PermissionError:
        print("Error: You don't have permission to move the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def checkIfConfigFileExists(configFileName):
    if not os.path.exists(configFileName):
        # Create default ini file
        config = configparser.ConfigParser()
        # 'ffmpegPath':'C:\ffmpeg', 
        
        config['Folders'] = {'output_folder':'C:\\VIDEO', 'processed_folder':'SOURCE_FINISHED', 'create_new_folder_for_each_batch':'True', 'path_to_ffdshow':'C:\\ffmpeg\\bin\\ffmpeg.exe'}
        config['Encoding'] = {'default_parameters':'-c:v libx265 -b 1200K -c:a aac'} 
        config['UserInput'] = {'ask_for_parameters':'False'}
        config['FileOperations'] = {'move_original':'True', 'copy_timedate':'True'}
        config['UI'] = {'play_finish_sound':'False', 'open_output_folder':'False', 'keep_console_on_finish':'True'}
        
        with open(configFileName, 'w') as f:
            config.write(f)

        os.startfile(configFile)


if __name__ == "__main__":
    print("hello!")
    # MessageBox = ctypes.windll.user32.MessageBoxW
    
    configFile = 'settings.ini'
    
    checkIfConfigFileExists(configFile)
    
    config = configparser.ConfigParser()
    config.read(configFile)
    
    try:
        outputFolderName = config['Folders']['output_folder']
        processedFolderName = config['Folders']['processed_folder']
        createNewFolderForEachBatch = config['Folders']['create_new_folder_for_each_batch']
        pathToFfdshow = config['Folders']['path_to_ffdshow']
        defaultParameters = config['Encoding']['default_parameters']
        askForParameters = config['UserInput']['ask_for_parameters']
        moveOriginalFile = config['FileOperations']['move_original']
        copyTimeDateToOutputFile = config['FileOperations']['copy_timedate']
        playFinishSound = config['UI']['play_finish_sound']
        openOutputFolder = config['UI']['open_output_folder']
        keepConsoleOnFinish = config['UI']['keep_console_on_finish']

        # print("outputFolderName", outputFolderName) 
        # print("processedFolderName", processedFolderName)
        # print("createNewFolderForEachBatch", createNewFolderForEachBatch)
        # print("defaultParameters", defaultParameters) 
        # print("askForParameters", askForParameters)
        # print("moveOriginalFile", moveOriginalFile)
        # print("copyTimeDateToOutputFile", copyTimeDateToOutputFile)
        # print("playFinishSound", playFinishSound)
        # print("openOutputFolder", openOutputFolder)
        
    except Exception as e:
        print(f"An error occurred. Parameter not set: {e}")
        os.startfile(configFile)
        input("Press Enter to exit...")

    list = sys.argv[1:]

    if askForParameters == 'True':
        print("askForParameters", askForParameters)
        presetName, params = promtUser()
    else:
        params = defaultParameters
    
    batchFolderName = ""
    if createNewFolderForEachBatch == 'True':
        batchFolderName = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        # >>> datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        # '10:36AM on July 23, 2010'

    for inputFile in list:

        fileNameWPath, fileExtension = os.path.splitext(inputFile)
        filePath = os.path.split(inputFile)[0]
        fileNameExt = os.path.split(inputFile)[1]

        # outputFolderPath = filePath + "\\" + outputFolderName + "\\" + batchFolderName
        outputFolderPath = outputFolderName + "\\" + batchFolderName
        outputFilePathNameExtension = outputFolderPath + "\\" + fileNameExt # + "\\" + fileExtension

        os.makedirs(outputFolderPath, exist_ok=True)  # succeeds even if directory exists.
        os.makedirs(filePath + "\\" + processedFolderName, exist_ok=True)  # succeeds even if directory exists.
        
        # print("os.path.split(inputFile)[0]", os.path.split(inputFile)[0]) # os.path.split(inputFile)[0] C:\Temp\DEL\vid_test_auto_convert
        # print("os.path.split(inputFile)[1]", os.path.split(inputFile)[1]) # os.path.split(inputFile)[1] videoplayback.mp4
        # print("fileNameWPath+fileExtension", fileNameWPath+fileExtension)
        print("fileNameWPath", fileNameWPath)
        print(list.index(inputFile)+1, '/', len(list), os.path.split(inputFile)[1])

        # commandLine = 'ffmpeg.exe -nostdin -i "' + inputFile + '" ' + params + ' "' + fileNameWPath + presetName + '.mp4"'
        commandLine = pathToFfdshow + ' -nostdin -i "' + inputFile + '" ' + params + ' "' + outputFilePathNameExtension
        # MessageBox(None, commandLine, 'Window title', 0)
        run_command(commandLine)

        if copyTimeDateToOutputFile == 'True':
            # get original file properties
            fileProperties = os.stat(inputFile)
            # modify atime and mtime (access time and modify time)
            os.utime(outputFilePathNameExtension, (fileProperties.st_mtime, fileProperties.st_mtime))
        
        if moveOriginalFile == 'True':
            # moving original file
            destination_file = filePath + "\\" + processedFolderName + "\\" + fileNameExt
            move_file(inputFile, destination_file)
        
    # MessageBox(None, "END", 'Window title', 0)
    if playFinishSound == 'True':
        os.system("rundll32.exe cmdext.dll,MessageBeepStub")
        # print(os.path.split(inputFile)[0])
        # input("Press Enter to continue...")
    if openOutputFolder == 'True':
        os.system(f'explorer "{outputFolderPath}"')
    if keepConsoleOnFinish == 'True':
        input("All files processed. Press Enter to exit...")
