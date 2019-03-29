This course is prepared by Wojciech Domski.
All rights reserved.

This is a repository for Advanced Robot Control laboratory classes 
at Wrocław University of Science and Technology.

To read more about the course go to [Course Web Site](https://edu.domski.pl/kursy/advanced-robot-control/)

The ARClab repository is divided into separate directories. 
Each directory contains materials necessary for laboratory classes.

# Table of content:

- **3RMatlab** is a set of scripts written in Matlab for 3R rigid manipulator. 
The goal of this class it to implement input-output decoupling for 
this object. The simulation is run using ODE solver instead of a 
Simulink diagram.

- **GPIO** contains two exercises for STM32 MCU. Those 
exercises involve GPIO manipulation using a button to read 
data from digital input, and a LED to write digital output.

# Troubleshooting

- If the Atollic TrueSTUDIO displays a message that 
the ST-Link programmer is not available make sure that 
is not used in ST-Link Utility and all debug sessions 
are terminated.

- If the Atollic TrueSTUDIO shows a message that there 
is no application available for flashing the MCU 
make sure that the path to the Toolchain is correct.
You can change it in *Properties -> C/C++ Build -> 
Settings -> Toolchain Version -> Fixed toolchain location*.

Change the path 

C:\Program Files (x86)\Atollic\TrueSTUDIO for STM32 **X.Y.Z**\ARMTools\bin

where **X.Y.Z** should be replaced with currently installed version of 
Atollic TrueSTUDIO.




















