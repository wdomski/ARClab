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

- **ADC** contains exercises related to the Analog 
Digital Converter peripheral.

# Course outline

## Laboratory 1

OSH training.

Introduction to the laboratory classes.

## Laboratory 2

Introduction to solving ordinary differential equations 
with ODE solver in Matlab. 

Exercise **3RMatlab**

## Laboratory 3

Introduction to GPIO peripheral in MCUs.
Exercises from **GPIO** directory, tasks 1, 2 & 3. 

## Laboratory 4

Working with timers, ADC and DAC. 
Concepts of interrupts and callback functions.
State machines.

Exercises from **TIM**, tasks 1 & 2.

Exercise from **ADC**, task 1.

Exercise from **DAC**, task 1.

## Laboratory 5

Introduction to FreeRTOS. Basic concepts, task 
and task synchronisation.

Exercise from **ADC**, task 2.

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

# Additional materials

Description of the development board can be found in [UM1724], 
while the information about the MCU at this board can be found in [STM32L476xx]. 
The detailed description of the STM32L4x5 and STM32L4x6 MCUs along 
with its registers description is in [RM0351].

In [UM1884] detailed description of HAL API and LL API can be found. 
Information about automatic code generation using STM32CubeMX software 
can be found in [UM1718].

User manual for STM Studio software can be found in [UM1025].

Mentioned files can be found at [st.com](https://www.st.com) or at [edu.domski.pl](https://edu.domski.pl/kursy/advanced-robot-control/arc-laboratory/)

# Literature

- [STM32L476xx] ST, Ultra-low-power Arm® Cortex®-M4 32-bit MCU+FPU, 100DMIPS, up to 1MB Flash, 128 KB SRAM, USB OTG FS, LCD, ext. SMPS, STM32L476xx, Datasheet, 2018.

- [UM1884] ST, Description of STM32L4/L4+ HAL and low-layer drivers, User manual, UM1884, 2017.

- [UM1724] ST, STM32 Nucleo-64 boards, User manual, UM1724, 2017.

- [UM1718] ST, STM32CubeMX for STM32 configuration and initialization C code generation, User Manual, UM1718, 2019.

- [RM0351] ST, STM32L4x5 and STM32L4x6 advanced Arm®-based 32-bit MCUs, Reference manual, RM0351, 2018.

- [UM1025] ST, Getting started with STM-STUDIO, User manual, UM1025, 2013.





















