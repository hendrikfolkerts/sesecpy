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

This application is licensed under GNU GPLv3.

HOW TO CITE

Folkerts, H., Deatcu, C., Pawletta, T., Hartmann, S. (2019). Python-Based eSES/MB
Framework: Model Specification and Automatic Model Generation for Multiple Simulators.
SNE - Simulation Notes Europe Journal, ARGESIM Pub. Vienna, SNE 29(4)2019, 207-215.
(DOI: 10.11128/sne.29.tn.10497),(Selected EUROSIM 2019 Postconf. Publ.)

Folkerts, H., Pawletta, T., Deatcu, C., and Hartmann, S. (2019). A Python Framework for
Model Specification and Automatic Model Generation for Multiple Simulators. In: Proc. of
ASIM Workshop 2019 - ARGESIM Report 57, ASIM Mitteilung AM 170. ARGESIM/ASIM Pub.
TU Vienna, Austria, 02/2019, 69-75. (Print ISBN 978-3-901608-06-3)

Folkerts, H., Pawletta, T., Deatcu, T. (2019). An Integrated Modeling,
Simulation and Experimentation Environment in Python Based on SES/MB and DEVS.
Proc. of the 2019 Summer Simulation Conference, ACM Digital Lib.,
2019 July 22-24, Berlin, Germany, 12 pages.