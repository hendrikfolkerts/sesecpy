INTRODUCTION

The software SESEcPy has been developed by the research group Computational
Engineering and Automation (CEA) at Wismar University of Applied Sciences.
The software implements an Experiment Control according to the System Entity
Structure / Model Base (SES/MB) infrastructure introduced for automatic
execution of simulation experiments.
Please read the documentation for further information. A comprehensive
introduction to the SES/MB theory is given in the documentation of the SES
modeling tool SESToPy.
The software is written in Python3.
It was tested with the simulation softwares Matlab R2018a (for Simulink),
OpenModelica 1.12.0 and Dymola 2018.

EXECUTE

Copy SESToPy, SESMoPy, SESEuPy, and SESEcPy in one directory like shown below.

SESMB_Infrastructure
    |
     - SESEcPy
    |
     - SESEuPy
    |
     - SESMoPy
    |
     - SESToPy

Copy the directory SESMB_Infrastructure in your home folder, e.g. C:\Users\<Username>
Go in the SESEcPy folder. 
The program can be executed from source. Python3 needs to be installed and the
program can be started with the command:
- in Windows: python main.py
- in Linux: python3 main.py

CHANGELOG


ToDo, Known Bugs, Notes


LICENSE


HOW TO CITE

Folkerts, H., Pawletta, T., Deatcu, C., and Hartmann, S. (2019). A Python Framework for
Model Specification and Automatic Model Generation for Multiple Simulators. In: Proc. of
ASIM Workshop 2019 - ARGESIM Report 57, ASIM Mitteilung AM 170. ARGESIM/ASIM Pub.
TU Vienna, Austria, 02/2019, 69-75. (Print ISBN 978-3-901608-06-3)