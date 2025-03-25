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

- **StaticLin** is a set of scripts written in Python for 
trajectory tracking task executed by unicycle mobile platform.
The goal is accomplished via static linearization. It is considered 
both for dynamics and kinematics of the mobile platform.

- **MPC** contains task about Model Predictive Control.
MPC algorithm is used for controlling a unicycle to follow a 
desired trajectory.

- **GPIO** contains two exercises for STM32 MCU. Those 
exercises involve GPIO manipulation using a button to read 
data from digital input, and a LED to write digital output.

- **ADC** contains exercises related to the Analog 
Digital Converter peripheral. 

- **DAC** contains exercises related to the Digital Analog 
Converter (DAC).

- **TIM** exercises related to counters.

- **FreeRTOS** contains exercises related to 
FreeRTOS where tasks, mutexes, event groups and queues 
are being used.

- **PID** implementation of PID regulator for FreeRTOS.

# Course outline

## Laboratory -- OSH

OSH training.

Introduction to the laboratory classes.

## Laboratory -- 3R manipulator in Matlab

Introduction to solving ordinary differential equations 
with ODE solver in Matlab. 

Exercise **3RMatlab**

## Laboratory -- Static linearization for unicycle

Introduction to solving ordinary differential equations 
with SciPy in Python. A unicycle mobile platform is 
a control object. The objective is to track an 
admissible trajectory (circle) and inadmissible 
trajectory square. This trajectory tracking task has to be 
realized both for dynamics and kinematics models of a unicycle 
mobile platform.

Exercise **StaticLin**

## Laboratory -- Model Predictive Control

Trajectory planning for Unicycle and Ackerman models 
using MPC. 
Additionally, round and rectangular obstacles are being 
considered. Exercise in Python using, numpy, scipy and 
matplotlib.

Exercise **MPC**

## Laboratory -- GPIO

Introduction to GPIO peripheral in MCUs.
Exercises from **GPIO** directory, tasks 1, 2 & 3. 

## Laboratory -- ADC & DAC

Working with timers, ADC and DAC. 
Concepts of interrupts and callback functions.
State machines.

Exercises from **TIM**, tasks 1 & 2.

Exercise from **ADC**, task 1.

Exercise from **DAC**, task 1.

## Laboratory -- mutexes and event groups in FreeRTOS

Introduction to FreeRTOS. Basic concepts, creation of tasks 
and task synchronization. Usage of mutexes to synchronize 
data between tasks. Also Event Groups are being used to 
send a notification about events.

Exercises from **FreeRTOS**, task 1 (all subtasks).

## Laboratory -- mailbox and FIFO queues in FreeRTOS

Introduction to FreeRTOS. Task synchronization using 
mutexes and queues. Queues are handled in two ways. 
First usage of queues is based on storing 
data in a queue with limited number of samples. 
A queue is being used as a FIFO queue.
Second usage is based on mailbox where a queue 
can only hold a single sample. This behaviour is 
useful for broadcasting current state to multiple number 
of tasks.

Exercises from **FreeRTOS**, task 2 (all subtasks).

## Laboratory -- PID in FreeRTOS

Implementation of a PID controller for a DC motor simulator 
using FreeRTOS. As a DC motor simulator a low-pass filter 
build from resistor and compensator is being used.

Exercises from **PID**, task 1.

# Remote work

All development boards used during laboratory are available 
via remote server. Connection to this remote server is done using 
a secure SSH connection. Moreover, there are different services 
available and access to these services is done via port tunnelling.

Below a glance on dev boards available through out the course.

![LEDs on](https://github.com/wdomski/ARClab/blob/develop/images/boards_off.jpg "Dev boards with LEDs turned on")

![LEDs off](https://github.com/wdomski/ARClab/blob/develop/images/boards_on.jpg "Dev boards with LEDs turned off")

## RemoteLab

Remote work is possible due to RemoteLab infrastructure. 
A demonstration video as well as description of RemoteLab 
capabilities is available at [RemoteLab](https://blog.domski.pl/remotelab-can-now-plot-data-in-real-time/).

**Please watch the video since it will answer most common questions.**

## Available services

Each server can host multiple number of services 
to which following can be included:

- **OpenOCD server** allows to remotely control development boards. 
Thanks to this service remote debug session can be started.
Access to a specific dev board is available on port number 
3000 + *id* where *id* is the number of a board.

- **state server** allows to inspect current state of each 
dev board. It delivers a web interface though which 
a board can be *restarted*, *halted* and *resumed*. 
Also the **OpenOCD server** for specified board can be 
restarted. The web interface is available at 8000 port number.

- **video streaming server** delivers a real-time visual feedback 
to all boards used during laboratory class. It can be used 
to e.g. examine if a LED diode is turned on or not. 
The server is available via web service at 8000 port number.

## Servers

There are three servers available 
which are run on Raspberry Pi. SSH ports to each 
server were collected in a table below.

| Server | Primary port number |Secondary port number | Debug service |Status server | Video streaming |
|---|---|---|---|---|---|
|aries           | 2201      | 2301                 |x|x|x|
|taurus          | 2202      | 2302                 |x|x| |
|eridanus        | 2203      | 2303                 |x|x|x|

If server at primary SSH port number is not reachable 
please use secondary port number.

## Boards

For remote work following boards are available:
- Nucleo-L476RG,
- Nucleo-L452RE,
- STM32L476G-Disco,
- STM32F429I-DISC1.

Each board has a set of features. In other words, the 
set of features describes which connectors (depicted 
in schematic) are available. Status server allows to 
verify which set of features is supported by 
a particular board.

The schematic is available 
[here](https://github.com/wdomski/ARClab/blob/wd/boards/NUCLEO64-Board.pdf).


## SSH connection 

For Linux users following command is sufficient
```Bash
ssh LOGIN@DOMAIN -p 2201 -L 3001:localhost:3001 -L 8000:localhost:8000
```

Above will connect to aries (because of 2201 port number) and 
three tunnels will be created:
- OpenOCD service will be available for board with *id* = 1 
because port number is 3000 + *id*,
- **video streaming** and **status server** will be available at localhost:8000.

Please mind the port numbers.

For Windows user a PuTTY can be used. 
The tunnelled ports can be set via menu depicted in below 
figure

![PuTTY configuration](https://github.com/wdomski/ARClab/blob/develop/images/putty.png "PuTTY configuration") 

## Serial port

Most of the dev boards are equipped with a serial port. 
On each server a **minicom** program is available. 
It delivers a console interface for serial port. 
Each dev board has a unique device through which the 
serial interface is available. Please mind that the 
device can change over time. To identify current 
device number please refer to description of 
specific dev board available through **status server** service.

```Bash
minicom --device /dev/ttySomeDevice0
```

Default configuration allows to open a session with following 
serial communication parameters (115200, 8N1):
- 115200 baud, transmission rate,
- 8 bits of data,
- N no parity control,
- 1, a single stop bit.

In order to close *minicom* **Ctrl+a** followed by **x** 
has to be entered.

### Easier alternative

It is much easier to use build in serial console via web interface. 
In order to do so select *Serial* link which will open serial console 
connected to appropriate development board.

This console also offers real-time plotting of received data. 
However, data needs to be sent in a specific format.

More details how to work with real-time plotting can be found here:
[Real-time plotting](https://blog.domski.pl/remotelab-can-now-plot-data-in-real-time/)

# Troubleshooting

- If an error about erasing Flash memory appear during 
debug session start please reset dev board via **status server**.

# Additional materials

Description of the development board can be found in [UM1724], 
while the information about the MCU at this board can be found in [STM32L476xx]. 
The detailed description of the STM32L4x5 and STM32L4x6 MCUs along 
with its registers description is in [RM0351].

In [UM1884] detailed description of HAL API and LL API can be found. 
Information about automatic code generation using STM32CubeMX software 
can be found in [UM1718].

User manual for STM Studio software can be found in [UM1025].

More information about FreeRTOS can be found in [FreeRTOSMastering].
Details about API of FreeRTOS can be found in [FreeRTOSManual].

Mentioned files can be found at [st.com](https://www.st.com) or at 
[edu.domski.pl](https://edu.domski.pl/en/courses/advanced-robot-control/arc-laboratory/)

# Literature

- [STM32L476xx] ST, Ultra-low-power Arm® Cortex®-M4 32-bit MCU+FPU, 100DMIPS, 
up to 1MB Flash, 128 KB SRAM, USB OTG FS, LCD, ext. SMPS, STM32L476xx, 
Datasheet, 2018.

- [UM1884] ST, Description of STM32L4/L4+ HAL and low-layer drivers, 
User manual, UM1884, 2017.

- [UM1724] ST, STM32 Nucleo-64 boards, User manual, UM1724, 2017.

- [UM1718] ST, STM32CubeMX for STM32 configuration and initialization C code 
generation, User Manual, UM1718, 2019.

- [RM0351] ST, STM32L4x5 and STM32L4x6 advanced Arm®-based 32-bit MCUs, 
Reference manual, RM0351, 2018.

- [UM1025] ST, Getting started with STM-STUDIO, User manual, UM1025, 2013.

- [FreeRTOSMastering] R. Barry, Mastering the FreeRTOS™ Real Time Kernel, 
Real Time Engineers Ltd., 2016.

- [FreeRTOSManual] Amazon Web Services, The FreeRTOS™ Reference Manual, 
API Functions and Configuration Options, Amazon.com Inc., 2017.

- [PID] K. J. Åström and T. Hägglund, PID Controllers: Theory, Design, 
and Tuning, 1995, Instrument Society of America


















