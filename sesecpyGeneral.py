import os
import subprocess
from os.path import splitext

class sesecpyGeneral():
    # this is the toolchain which needs to be executed independent of the experiment
    def executeToolchain(self, infrastructurePath, pythoncall, sesFilePath, sesvars, pesFilePath, fpesFilePath, deletePES, deleteFPES, deleteModelsAfterSimulation, appendConfig):
        #call pruning and flattening
        print("1. Execute SESToPy")
        #go in the SESToPy directory
        os.chdir(os.path.join(infrastructurePath, "SESToPy"))
        #call pruning
        print("Deriving the PES")
        #ret = subprocess.check_output([pythoncall, "main.py", "-p", sesFilePath, sesvars, "-o", pesFilePath], shell=True)
        #ret = ret.decode("utf-8")
        ret = self.executeSubprocess(self, [pythoncall, "main.py", "-p", sesFilePath, sesvars, "-o", pesFilePath])
        ret = "\r\n".join(ret)
        #call flattening if pruning was successful
        if "OK - The pruning is done successfully." in ret:
            print("The pruning process of the SES\n" + sesFilePath + "\nhas finished. The PES is saved in the file:\n" + pesFilePath + "\n")
            #call flattening
            print("Deriving the FPES")
            #ret = subprocess.check_output([pythoncall, "main.py", "-f", pesFilePath, "-o", fpesFilePath], shell=True)
            #ret = ret.decode("utf-8")
            ret = self.executeSubprocess(self, [pythoncall, "main.py", "-f", pesFilePath, "-o", fpesFilePath])
            ret = "\r\n".join(ret)
            if "OK - The flattening is done successfully." in ret:
                if deletePES:
                    os.remove(pesFilePath)
                print("The flattening process of the PES\n" + pesFilePath + "\nhas finished. The FPES is saved in the file:\n" + fpesFilePath + "\n")
                #call modelbuilding
                print("2. Execute SESMoPy")
                #go in the SESMoPy directory
                os.chdir(os.path.join(infrastructurePath, "SESMoPy"))
                #call SESMoPy
                print("Building the model(s)")
                #ret = subprocess.check_output([pythoncall, "main.py", "-b", fpesFilePath], shell=True)
                #returnv = ret.decode("utf-8")
                ret = self.executeSubprocess(self, [pythoncall, "main.py", "-b", fpesFilePath])
                returnv = "\r\n".join(ret)
                if "OK - The model(s) was/were created in " in returnv:
                    if deleteFPES:
                        os.remove(fpesFilePath)
                    modelfolder = "".join([i for i in returnv.split("\n") if i.startswith('MODELFOLDER: ')])[13:-1]  # get the line beginning with MODELFOLDER: and extract it, alternative way see below when extracting RESULTFILE:
                    print("The modelbuilding process has finished. Models are placed in the directory\n" + modelfolder + "\n")
                    if modelfolder[0] in ["'", '"']:    #remove " or ' at beginning and end of the modelfolder's path
                        modelfolder = modelfolder[1:-1]
                    #extend the configuration
                    conffile = os.path.join(modelfolder, "config.txt")
                    with open(conffile, "a") as fileobject:
                        fileobject.write(appendConfig)
                    print("Extended the simulation configuration file.\n")
                    #call execution unit
                    print("3. Execute SESEuPy")
                    #go in the SESEuPy directory
                    os.chdir(os.path.join(infrastructurePath, "SESEuPy"))
                    #call SESEuPy
                    print("Executing the model(s). This can take some time.")
                    if deleteModelsAfterSimulation:
                        dmas = "True"
                    else:
                        dmas = "False"
                    #subprocess call -> output of subprocess can only be seen afterwards
                    #ret = subprocess.check_output([pythoncall, "main.py", modelfolder, dmas], shell=True)
                    #returnv = ret.decode("utf-8")
                    #resultfile = returnv[returnv.find("RESULTFILE: ")+12:-2]
                    #print("The execution process has finished.\nThe output is:\n" + returnv + "\nResults are placed in the file\n" + resultfile + "\n")
                    #subprocess call -> output of subprocess can be seen directly
                    returnv = self.executeSubprocess(self, [pythoncall, "main.py", modelfolder, dmas])
                    returnv = "\r\n".join(returnv)
                    resultfile = returnv[returnv.find("RESULTFILE: ")+12:]
                    print("\nThe execution process has finished. Results are placed in the file\n" + resultfile + "\n")
                    return resultfile
                else:
                    #do nothing if the model(s) could not be built
                    print(returnv)
                    print("Models of the FPES\n" + fpesFilePath + "\ncould not be built. Please look in your command output for error messages. Is the call of SESMoPy correct? See documentation if you are unsure!")
                    return "", returnv
            else:
                #do nothing if the PES could not be flattened
                print(ret)
                print("The PES\n" + pesFilePath + "\ncould not be flattened. Please look in your command output for error messages. Is the call of SESToPy correct? See documentation if you are unsure!")
                return "", ret
        else:
            #do nothing if the SES could not be pruned
            print(ret)
            print("The SES\n" + sesFilePath + "\ncould not be pruned with the SES variables\n" + sesvars + ". Please look in your command output for error messages. Is the call of SESToPy correct? See documentation if you are unsure!")
            return "", ret

    #calculate the path and filenames of PES and FPES based on the SES and the sesvars
    def findPESFPESNames(self, sesFilePath, sesvars):
        sesFilePathParts = sesFilePath.split("\\")
        baseSESFilePath = "\\".join(sesFilePathParts[:-1])
        sesFileName = sesFilePathParts[-1]
        sesvars = sesvars[1:-1] #prepare the SES variables for updating the PES name
        sesvarlist = sesvars.split(",")
        pesFileName = splitext(sesFileName)[0] + "_p_" + "_".join(sesvarlist) + ".jsonsestree"
        pesFileName = pesFileName.replace("=", "e")
        fpesFileName = splitext(pesFileName)[0] + "_f" + ".jsonsestree"
        pesFilePath = os.path.join(baseSESFilePath, pesFileName)
        fpesFilePath = os.path.join(baseSESFilePath, fpesFileName)
        return pesFilePath, fpesFilePath

    #directly output a line of a subprocess call in the command as soon as it is printed by the subprocess
    def executeSubprocess(self, command):
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1)
        lines_iterator = iter(popen.stdout.readline, b"")
        subprocessLines = []
        while popen.poll() is None:
            for line in lines_iterator:
                nline = line.rstrip()
                line = nline.decode("latin")
                subprocessLines.append(line)
                print(line, end="\r\n", flush=True)  # yield line
        return subprocessLines