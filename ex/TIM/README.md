This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **TIM_ex1** project into IDE.
The aim of this exercise is to show how the simple PWM 
output signal can be used to change the 
brightness of a LED. Use connector **TIMER4** 
to which a LED diode is connected.

In this task you have to fill out following gaps:

- start PWM generation,
- implement callback for UART incoming transmission,
- adjust brightness according to user input,
- update the PWM duty signal every time user sends data.

User can send
|Value|PWM duty|
|-|-|
|0| 0   %|
|1| 25  %|
|2| 50  %|
|3| 75  %|
|4| 100 %|

Any other value sent by user should be ignored and appropriate 
information should be outputted on serial interface.

Every time when a change in PWM duty occurs 
the MCU should send appropriate information via 
serial port (use **printf()** redirection).

# Task 2

Import **TIM_ex2** project into IDE.
The aim of this exercise is to show how the Input Capture 
mode works. This application counts time (in timer [us])
between level changes. The information is passed to 
serial output via redirection of **printf()** function.

For this use **TIMER1** connector configured as Input Capture 
and **TIMER5** configured as GPIO output. This is possible because 
these two connectors are connected, refer to 
[board schematic](https://github.com/wdomski/ARClab/blob/develop/boards/NUCLEO64-Board.pdf).

Familiarize with the configuration of the project, 
in particular timer configuration for **TIMER1** 
and deduce the time resolution with which the 
input signal is measured. This will be needed to print proper 
value of ms on serial interface.

Below you can see example of an output:

```
Time since last button press: 1019 [ms]
Time since last button press: 5234 [ms]
Time since last button press: 3621 [ms]
Time since last button press: 1169 [ms]
Time since last button press: 5203 [ms]
Time since last button press: 4371 [ms]
```

The change of state of the **TIMER5** should only occur 
when user sends *t* for toggle via serial interface.

In this task you have to fill out following gaps:

- capture the input capture event, store time and reset counter, 
this can be done in Callback function,

- implement callback from UART to get user input,

- inform user about time since last press event.

You have to connect two pins with a wire. Pin PA0 (timer input 
capture) and PC13 (blue button). Connect those two ports 
while the dev board is not connected to power!
Use the leaflet given out during classes to identify the 
MCU pins.
Before proceeding further inform teacher about the connection 
and ask for permission to proceed further.

During the implementation use provided variables: **flag** and **time**.

# Useful functions

Set desired duty of a PWM on selected channel.
```C
__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);
```

Start PWM signal generation on selected channel.
```C
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
```

Returns current number of ticks counted by a timer.
```C
__HAL_TIM_GET_COMPARE(&htim2, TIM_CHANNEL_1);
```

Reset counter register of selected timer with desired value.
```C
__HAL_TIM_SET_COUNTER(&htim2, 0);
```

Start Timer in Input Capture mode with interrupts.
```C
HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
```

Redefine following callback function from Input Capture
```C
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim);
```

Start UART in interrupt mode
```C
HAL_UART_Receive_IT();
```

Redefine incoming transmission callback for UART
```C
HAL_UART_RxCpltCallback();
```

Redirection of **printf()** function output to serial port 
can be done with redefinition of **_write()** function.
Also include **stdio.h**.

```
int _write(int file, char *ptr, int len) {
	HAL_UART_Transmit(&huart2, (uint8_t *) ptr, len, 50);
	return len;
}
```

# Additional materials

Description of the development board can be found in [UM1724], 
while the information about the MCU at this board can be found in [STM32L476xx]. 
The detailed description of the STM32L4x5 and STM32L4x6 MCUs along 
with its registers description is in [RM0351].

In [UM1884] detailed description of HAL API and LL API can be found. 
Information about automatic code generation using STM32CubeMX software 
can be found in [UM1718].

Mentioned files can be found at [st.com](https://www.st.com) or at [edu.domski.pl](https://edu.domski.pl/kursy/advanced-robot-control/arc-laboratory/)

# Literature

- [STM32L476xx] ST, Ultra-low-power Arm® Cortex®-M4 32-bit MCU+FPU, 100DMIPS, up to 1MB Flash, 128 KB SRAM, USB OTG FS, LCD, ext. SMPS, STM32L476xx, Datasheet, 2018.

- [UM1884] ST, Description of STM32L4/L4+ HAL and low-layer drivers, User manual, UM1884, 2017.

- [UM1724] ST, STM32 Nucleo-64 boards, User manual, UM1724, 2017.

- [UM1718] ST, STM32CubeMX for STM32 configuration and initialization C code generation, User Manual, UM1718, 2019.

- [RM0351] ST, STM32L4x5 and STM32L4x6 advanced Arm®-based 32-bit MCUs, Reference manual, RM0351, 2018.



