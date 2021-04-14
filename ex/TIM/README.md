This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **TIM_ex1** project into Atollic TrueSTUDIO.
The aim of this exercise is to show how the simple PWM 
output signal can be used to change the 
brightness of a LED.

In this task you have to fill out following gaps:

- implement debouncing,
- start PWM generation,
- update the PWM duty signal every time a button is pressed.

Every time when a change in PWM duty occurs 
the MCU should send appropriate information via 
serial port (use printf() redirection).

# Task 2

Import **TIM_ex2** project into Atollic TrueSTUDIO.
The aim of this exercise is to show how the Input Capture 
mode works. This application counts time (in timer [us])
between button press events. The information is passed to 
serial output via redirection of *printf()* function.

Below you can see example of an output:

```
Time since last button press: 1019 [ms]
Time since last button press: 6 [ms]
Time since last button press: 5234 [ms]
Time since last button press: 3 [ms]
Time since last button press: 3621 [ms]
Time since last button press: 1169 [ms]
Time since last button press: 4 [ms]
Time since last button press: 5203 [ms]
Time since last button press: 4371 [ms]
```

Can you see something interesting?

In this task you have to fill out following gaps:

- capture the input capture event, store time and reset counter, 
this can be done in Callback function,
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
- __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);

Start PWM signal generation on selected channel.
- HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);

Returns current number of ticks counted by a timer.
- __HAL_TIM_GET_COMPARE(&htim2, TIM_CHANNEL_1);

Reset counter register of selected timer with desired value.
- __HAL_TIM_SET_COUNTER(&htim2, 0);

Start Timer in Input Capture mode with interrupts.
- HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);

Redefine following callback function from Input Capture
```
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
}
```

Redirection of printf() function output to serial port 
can be done with redefinition of _write() function.
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


