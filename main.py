#Experiment Control
#The Experiment Control consists of an experiment independent and an experiment dependent part.
#This is the startscript managing the call of both.

import os
import platform
import shutil
from sesecpyExperiment import *
from sesecpyGeneral import *


#define the python call (python / python3) and variables depending on the OS
system = platform.system()
if system == "Windows":
    pythoncall = "python"
    dirSep = "\\"
else:
    pythoncall = "python3"
    dirSep = "/"

#set directories
#get the current directory of this script and split it
sesecpyPathParts = os.path.dirname(os.path.realpath(__file__)).split(dirSep)
#set the directory for the infrastructure -> it is one directory up of the directory of this script
infrastructurePath = dirSep.join(sesecpyPathParts[:-1])

#create objects
sesecpyExperimentObject = sesecpyExperiment
sesecpyGeneralObject = sesecpyGeneral

#initial settings -> experiment specific
sesFilePath, mbFilespath, deletePES, deleteFPES, deleteModelsAfterSimulation = sesecpyExperimentObject.initialSettings(sesecpyExperiment)

#begin the loop -> as long as the goals are not met -> execute in loop
loopCounter = 0
loopMax = 10
goalsMet = False
interface = ""
addedMbFiles = []
resultfile = ""
errorOcc = False
overallResults = ""
while loopCounter < loopMax and not goalsMet and not errorOcc:

    #calculate the next SESvars -> experiment specific
    goalsMet, sesvars, pesFilePath, fpesFilePath, simulator, interface, appendConfig, overallResults = sesecpyExperimentObject.nextState(sesecpyExperiment, resultfile, loopCounter)  # the loopCounter is the simulation number

    #select the sesfile depending on the interface -> only do in the first loop, then it is set
    if loopCounter == 0 and interface == "native":
        sesFilePath = sesFilePath.get("native")
    elif loopCounter == 0 and interface == "FMI":
        sesFilePath = sesFilePath.get("FMI")

    #execute the prune, flatten, build and execute toolchain if the goals are not met yet -> general
    if not goalsMet:

        if interface == "native":   #for the native interface -> copy the MB depending on the simulator
            usedMB = mbFilespath.get(simulator)
        else:                       #for FMI -> copy the only MB (for all simulators)
            usedMB = mbFilespath.get(interface)
        for hfile in os.listdir(usedMB):
            hfilepathname = os.path.join(usedMB, hfile)
            newhfilepathname = os.path.join(os.path.split(sesFilePath)[0], hfile)
            try:
                if os.path.isdir(hfilepathname):
                    shutil.copytree(hfilepathname, newhfilepathname)
                else:
                    shutil.copyfile(hfilepathname, newhfilepathname)
            except:
                print("Error copying the MB file(s) in the directory with the SES file!")
            addedMbFiles.append(newhfilepathname)

        resultfile = sesecpyGeneralObject.executeToolchain(sesecpyGeneral, infrastructurePath, pythoncall, sesFilePath, sesvars, pesFilePath, fpesFilePath, deletePES, deleteFPES, deleteModelsAfterSimulation, appendConfig)
        if resultfile == "":
            errorOcc = True

        #remove the copied MB from the directory containing the FPES
        # -> for the native interface (in the next loop maybe there are other MB files for a different simulator necessary, which can have the same name)
        # -> for FMI it is always the same MB -> do not remove
        if interface == "native":
            for addedMbFile in addedMbFiles:
                if os.path.exists(addedMbFile):
                    if os.path.isdir(addedMbFile):
                        shutil.rmtree(addedMbFile)
                    else:
                        os.remove(addedMbFile)

    loopCounter += 1

#calculate overall results -> experiment specific
if not goalsMet and loopCounter == loopMax and not errorOcc:
    print("Finished. The goal could not be met in " + str(loopMax) + " steps or another error occurred. Please look at the output in the command window.")
elif goalsMet and not errorOcc:
    print("Finished. The goal is met with:\n" + overallResults)
elif errorOcc:
    print("An error occurred.")