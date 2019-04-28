#Experiment Control
#The Experiment Control consists of an experiment independent and an experiment dependent part.
#This is the startscript managing the call of both.

import os
import platform
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
sesFilePath, sesvars, pesFilePath, fpesFilePath, deletePES, deleteFPES, deleteModelsAfterSimulation, appendConfig = sesecpyExperimentObject.initialSettings(sesecpyExperiment) #initialize variables (experiment specific)

#begin the loop -> as long as the goals are not met -> execute in loop
goalsMet = False
loopCounter = 0
loopMax = 10
overallResults = ""
while not goalsMet and loopCounter < loopMax:
    #execute the prune, flatten, build and execute toolchain -> general
    resultfile = sesecpyGeneralObject.executeToolchain(sesecpyGeneral, infrastructurePath, pythoncall, sesFilePath, sesvars, pesFilePath, fpesFilePath, deletePES, deleteFPES, deleteModelsAfterSimulation, appendConfig)
    #calculate the next SESvars -> experiment specific
    goalsMet, sesvars, pesFilePath, fpesFilePath, overallResults = sesecpyExperimentObject.nextState(sesecpyExperiment, resultfile)
    loopCounter += 1

#calculate overall results -> experiment specific
if not goalsMet and loopCounter == loopMax:
    print("Finished. The goal could not be met in " + str(loopMax) + " steps or another error occurred. Please look at the output in the command window.")
else:
    print("Finished. The goal is met with:\n" + overallResults)