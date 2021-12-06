import os
import sys
import time
import requests


while True:
    print("program is starting")
    path = os.walk("../stlFiles")
    for dirpath, dirnames, filenames in path:
        for filename in filenames:
            if not filename.endswith(".stl"):
                continue
            gcodeFilename = filename.replace(".stl", ".gcode")
            timerFilename = filename.replace(".stl", ".txt")
            if not os.path.exists("../gcodeFiles/" + gcodeFilename):
                commandSlicer = "./slic3r ../stlFiles/" + filename + " --output ../gcodeFiles/" + gcodeFilename
                os.system(commandSlicer)
            if not os.path.exists("../gcodeFiles/" + timerFilename):    
                commandTimer = "./utils/estimate-gcode-time.pl ../gcodeFiles/" + gcodeFilename + " ../gcodeFiles/" + timerFilename 
                os.system(commandTimer)
                # time.sleep(10)
                with open("../gcodeFiles/" + timerFilename) as f:
                    with open("../gcodeFiles/" + gcodeFilename) as file_gcode:
                    
                        estimation = f.readline()
                        print(int(estimation))
                        url = 'http://143.244.182.58:4000/api/quotations/' + timerFilename.replace(".txt", "")
                        files=[
                            ('gcodeFile',(gcodeFilename, file_gcode,'application/octet-stream'))
                        ]
                        myobj = {'filename': filename, 'estimation': int(estimation),}
                        x = requests.post(url, files=files)
                        x = requests.post(url, json = myobj)
                        print(x)
                    
    print("finish...")
    time.sleep(10)

