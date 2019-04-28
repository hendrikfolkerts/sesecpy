import os
import csv
from sesecpyGeneral import *

class sesecpyExperiment():
    def __init__(self):
        self.sesvars = ""

    def initialSettings(self):

        #####TO EDIT FOR EXPERIMENT#####################################################################################
        #set the SES file
        #self.sesFilePath = "C:\\Users\\win10\\SES_MB\\SES_Feedback.jsonsestree"
        #self.sesFilePath = "/home/linux/SES_MB/SES_Feedback.jsonsestree"
        self.sesFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example\\Feedback.jsonsestree")

        #set the initial SES variable settings -> as Python list in a string
        self.sesvars = "[feedforward=0]"

        #delete the PES and FPES after they are not needed anymore
        deletePES = True
        deleteFPES = True
        #delete the created models after the simulation run
        deleteModelsAfterSimulation = True

        #add lines in the config.txt for the simulator parameterization
        starttime = 0               #tstart for the simulation
        solver = "dassl"            #the solver to take -> it needs to be supported by the simulator
        stoptime = 50               #tfinal for the simulation
        maxstep = 0.1               #maximum stepsize for the solver
        exectype = "parallel"       #the type of the execution in SESEuPy: sequential or parallel
        nsigana = ["sourceSys.y","sourceDist.y","addDist.y"]           #names of the signals to analyze in the result
        ################################################################################################################

        #set the initial PES and FPES files
        sesecpyGeneralObj = sesecpyGeneral
        pesFilePath, fpesFilePath = sesecpyGeneralObj.findPESFPESNames(sesecpyGeneral, self.sesFilePath, self.sesvars)

        #build the string to append to the config.txt
        appendConfig = "STARTTIME: "+str(starttime)+"\nSOLVER: "+solver+"\nSTOPTIME: "+str(stoptime)+"\nMAXSTEP: "+str(maxstep)+"\nEXECTYPE: "+exectype+"\nNSIGANA: "+str(nsigana)

        #now return
        return self.sesFilePath, self.sesvars, pesFilePath, fpesFilePath, deletePES, deleteFPES, deleteModelsAfterSimulation, appendConfig

    def nextState(self, resultfile):
        goalsMet = False    #set to True, when the goals are met
        overallResults = "" #string with the overall results -> when the goals are met

        #####TO EDIT FOR EXPERIMENT#####################################################################################
        # Analyze the result and find out, whether the goal is met. If the goal is not met, set the new sesvars.

        #read the resultfile
        res = []
        with open(resultfile, 'r') as resfile:
            reader = csv.reader(resfile, delimiter=";")
            for row in reader:  #seperated by semicolon -> so the different simulation runs of one structure variant are seperated here
                if reader.line_num == 1:    #first line: the file
                    for rw in row:
                        if rw != "":
                            res.append([rw.split(',')[0]])
                else:   #all other lines
                    for rw in range(len(row)):
                        if row[rw] != "":
                            res[rw].append(row[rw].split(','))

        #check if the goals are met -> 5% overshoot at maximum, 15 seconds settling time
        goalsMet = True
        for rs in res:
            for r in rs:
                try:
                    if (float(r[1]) > 0.05) or (float(r[0]) > 15 and int(r[1]) > 0.005):  #we allow 0.5 percent overshoot after 15 seconds
                        goalsMet = False
                except:
                    pass
            if goalsMet:    #if the goals are met, set the overall results and break
                overallResults = str(rs[0])
                break

        #if the goals are not met, set the new sesvars
        if not goalsMet:
            self.sesvars = "[feedforward=1]"

        ################################################################################################################

        #set the new PES and FPES files
        sesecpyGeneralObj = sesecpyGeneral
        pesFilePath, fpesFilePath = sesecpyGeneralObj.findPESFPESNames(sesecpyGeneral, self.sesFilePath, self.sesvars)

        #now return
        return goalsMet, self.sesvars, pesFilePath, fpesFilePath, overallResults