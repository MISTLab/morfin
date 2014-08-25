#MORFIN- MIST Lab Orbital Radiation Fault INjector 11/08/2014

Author:Vedant

This project provides an estimate of the fault rates for Xilinx FPGA. The script has the capabilities to predict and inject single bit faults

##Dependencies:

The script has been written for Python 2.7 and has been tested for Windows 7, Spyder, but it should also work for other operating systems.

The project makes use of the following modules available for python:

- Selenium
- sgp4
- Spacepy
- ConfigParser
- csv
- time
- multiprocessing
- os
- math
- numpy
- scipy
- serial
- random

The FPGA under test needs to have the SEM core provided by Xilinx: http://www.xilinx.com/products/intellectual-property/SEM.htm

The user will need to provide a clock of 50Hz for the operation for the SEM core and one for determining the baud rate for the UART(it is advisable for the UART to run at the highest baud-rate possible i.e 115200).

The user needs to have an account at :https://creme.isde.vanderbilt.edu/CREME-MC/ , to use the CREME96 model.

##Instructions:

- Copy all the files(inputs.ini,Morfin.py and data.csv) in the project to the script directory of python.

- To specify you mission and simulation parameters use the inputs.ini file. The file is well commented to specify all the inputs.

- Make sure that the system has access to the Internet in case you are running the simulation for a given set of parameters for the first time, as the program needs to access the internet to generate at least 2 data-points for the Fault Injector to work. If LUT data already exists in the data.csv file then internet access is not necessary.

- Make sure that the FPGA under test has the SEM core programmed into it. working at the correct frequency and setup for correct UART communication rate.

- Ensure that the FPGA is connected to the system before starting the Simulator, also define the correct USB communication port in the inputs.ini file

- To use the Selenium module for python make sure that the module is included properly and that you have the driver for whichever browser the usser would like to use(The code has been tested for Chromedriver and the native Firefox Driver, although PhantomJS can also be used for an headless operation)

- Make sure that during run-time the user does not interact with Chrome or Firefox window used by Selenium.

- Once all above conditions have been satisfied, the user can run the script. 


##Outputs:

- The Simulator displays the Memory address of the fault simulated and the mission time when the fault was encountered.

- The code has been currently configured to use the CRC auto repair function in the SEM core to revert the Bit flip, although it can be turned off by passing the character "d"(present in the code as a commented line Line 463). This feature can be used to test other scrubbers.(the CRC auto repair only corrects Single Upsets in the FPGA,  more complicated scrubbers should be used to correct Multiple Bit errors)


##Note:

- Please make sure the folder name assigned in the inputs.ini file does not already exist in you CREME96 account, if not the program might experience errors during run-time.

- The Spacepy library returns some wrong values for certain data, this will be improved in the new versions of the module but the functions using spacepy library functions have functionality to handle these errors.

- It is recommended to use Chrome for Selenium so as to provide a GUI to debug in case of errors from the CREME96 website (occasionally occurs, best way to deal with this is the wait for some time and run the program later), Chrome is considerably faster then most other GUI browsers.

- There is a probability that the SEU is generated in the SEM core itself and this would cause problems in the FPGA to simulate further faults or to communicate with the system on the other end of the UART.(Although this is extremely rare as the area occupied by the Core is negligible, during tests this failure wasn't experienced until 10,000 faults were simulated)

- If the code stops after a few faults have been injected it is because the communication between the FPGA and the Desktop/PC has been lost, this may be because of the reason stated above.