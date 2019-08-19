import os
import csv
from sesecpyGeneral import *

class sesecpyExperiment():
    def __init__(self):
        self.sesFilePath = []
        self.mbFilesPath = []

    def initialSettings(self):

        #####GLOBAL SETTINGS TO EDIT FOR EXPERIMENT#####################################################################

        #set the SES file
        #self.sesFilePath = "C:\\Users\\win10\\SES_MB\\SES_Feedback.jsonsestree"
        #self.sesFilePath = "/home/linux/SES_MB/SES_Feedback.jsonsestree"
        pathOfThisScript = os.path.dirname(os.path.abspath(__file__))
        #native
        sesFilePathNative = os.path.join(pathOfThisScript, "Example\\FeedbackControl_native\\Feedback.jsonsestree")
        pathOfMbSimulink = os.path.join(pathOfThisScript, "Example\\FeedbackControl_native\\MB_Simulink")
        pathOfMbOpenModelica = os.path.join(pathOfThisScript, "Example\\FeedbackControl_native\\MB_OpenModelica")
        pathOfMbDymola = os.path.join(pathOfThisScript, "Example\\FeedbackControl_native\\MB_Dymola")
        #FMI
        sesFilePathFMI = os.path.join(pathOfThisScript, "Example\\FeedbackControl_FMI\\Feedback.jsonsestree")
        pathOfMbFMI = os.path.join(pathOfThisScript, "Example\\FeedbackControl_FMI")
        #set dictionaries
        self.sesFilePath = {"native": sesFilePathNative, "FMI": sesFilePathFMI}
        self.mbFilesPath = {"Simulink": pathOfMbSimulink, "OpenModelica": pathOfMbOpenModelica, "Dymola": pathOfMbDymola, "FMI": pathOfMbFMI}

        #delete the PES and FPES after they are not needed anymore
        deletePES = True
        deleteFPES = True
        #delete the created models after the simulation run (ignored when using FMI)
        deleteModelsAfterSimulation = True

        ################################################################################################################

        #now return
        return self.sesFilePath, self.mbFilesPath, deletePES, deleteFPES, deleteModelsAfterSimulation


    def nextState(self, resultfile, simulationNumber):
        goalsMet = False
        sesvars = ""
        pesFilePath = ""
        fpesFilePath = ""
        simulator = ""
        interface = ""
        appendConfig = ""
        overallResults = ""

        #####TO EDIT FOR EXPERIMENT#####################################################################################
        # Analyze the result and find out, whether the goal is met. If the goal is not met, set the new sesvars.

        #read the resultfile
        def readResults(resultfile):
            res = []
            with open(resultfile, 'r') as resfile:
                reader = csv.reader(resfile, delimiter=";")
                for row in reader:  # separated by semicolon -> so the different simulation runs of one structure variant are separated here
                    if reader.line_num == 1:  # first line: the file
                        for rw in row:
                            if rw != "":
                                res.append([rw.split(',')[0]])
                    else:  # all other lines
                        for rw in range(len(row)):
                            if row[rw] != "":
                                res[rw].append(row[rw].split(','))
            return res

        #check if the goals are met -> 5% overshoot at maximum, 15 seconds settling time
        def goalsAreMet(res):
            goalsMet = True         #stays True, when the goals are met
            overallResults = ""     #string with the overall results -> when the goals are met
            for rs in res:
                for r in rs:
                    try:
                        if (float(r[3]) > 0.05) or (float(r[0]) > 15 and abs(float(r[3])) > 0.005):  # we allow 0.5 percent overshoot after 15 seconds
                            goalsMet = False
                    except:
                        pass
                if goalsMet:  # if the goals are met, set the overall results and break
                    overallResults = str(rs[0])
                    break
            return goalsMet, overallResults

        #here the function begins

        #check the simulation results (of course not for the first simulation run and only if there is a resultfile)
        if simulationNumber > 0 and resultfile != "":
            res = readResults(resultfile)
            goalsMet, overallResults = goalsAreMet(res)

        #if the goals are not met, set new SESvars and configuration depending on the simulator -> there are three simulators
        if not goalsMet:
            #default values
            feedforward = 0
            simulator = "Simulink"
            interface = "native"
            solverToUse = "ode45"

            #decide for a simulator and a solver and feedforward -> depending on the simulation number
            if (simulationNumber + 1) % 3 == 1:
                if (simulationNumber + 1) / 3 <= 1:
                    feedforward = 0
                else:
                    feedforward = 1
                simulator = "Simulink"
                solverToUse = "ode45"
            elif (simulationNumber + 1) % 3 == 2:
                if (simulationNumber + 1) / 3 <= 1:
                    feedforward = 0
                else:
                    feedforward = 1
                simulator = "OpenModelica"
                solverToUse = "dassl"
            elif (simulationNumber + 1) % 3 == 0:
                if (simulationNumber + 1) / 3 <= 1:
                    feedforward = 0
                else:
                    feedforward = 1
                simulator = "Dymola"
                solverToUse = "dassl"

            #set the SES variable settings -> as Python list in a string
            sesvars = '[feedforward=' + str(feedforward) + ', mysim="' + str(simulator) + '", myinterface="' + str(interface) + '"]'

            #calculate the new names for PES and FPES files based on the SESvar settings
            sesecpyGeneralObj = sesecpyGeneral

            #select the sesfile depending on the interface
            if interface == "native":
                sesFilePath = self.sesFilePath.get("native")
            else:
                sesFilePath = self.sesFilePath.get("FMI")

            pesFilePath, fpesFilePath = sesecpyGeneralObj.findPESFPESNames(sesecpyGeneral, sesFilePath, sesvars, simulationNumber)

            #add lines in the config.txt for the simulator parameterization -> build the string to append to the config.txt
            starttime = 0               #tstart for the simulation
            solver = str(solverToUse)   #the solver to take -> it needs to be supported by the simulator
            stoptime = 50               #tfinal for the simulation
            maxstep = 0.1               #maximum stepsize for the solver
            exectype = "sequential"     #the type of the execution in SESEuPy: sequential or parallel
            nsigana = ["sourceSys.y","sourceDist.y","addDist.y"]           #names of the signals to analyze in the result

            appendConfig = "STARTTIME: "+str(starttime)+"\nSOLVER: "+solver+"\nSTOPTIME: "+str(stoptime)+"\nMAXSTEP: "+str(maxstep)+"\nEXECTYPE: "+exectype+"\nNSIGANA: "+str(nsigana)

        ################################################################################################################

        #now return
        return goalsMet, sesvars, pesFilePath, fpesFilePath, simulator, interface, appendConfig, overallResults