This course is prepared by Wojciech Domski.
All rights reserved.

# Task 1

Compile and run **GPIO_ex1** project.
The goal of this project is to familiarize students with 
workflow of creating an embedded solution for 
STM32 MCUs. 

First a project with a STM32CubeMX application is created then 
the code is generated from this project. Next, the 
generated project is imported into Atollic TrueSTUDIO IDE 
where it is configured. Basic configuration considers:

- turning off optimization (-O0),
- using all CPU cores to speed up compilation e.g. (-j 16),
- creating a launch configuration which only load 
the application without entering debugging.

Also, *printf()* output is redirected with redefinition of 
*_write()* function to use USART (serial port) as output.
This allows to display some log data to a serial terminal 
which can turn out to be helpful.

Moreover, during the class a simple debugging session 
will be presented. It will involve checking the 
state of variables, moving around code in step mode, 
pausing and resuming session.

# Task 2

Compile and run **GPIO_ex2** project.
The goal is to familiarize students with changing 
state of a digital output.
The effect can be observed on dev board where 
a LED diode wil change its state (turned on or off).

# Task 3

Create a project or use an existing one (**GPIO_ex1** or **GPIO_ex2**)
to write a program which will read digital input state (button) 
and toggle LED every time when a button is pressed. 

Implement debouncing procedure. This procedure should 
not introduce any delay to the system (busy waits, etc.) 
but should be time dependent. 

The application should work as follows.
When a button is pressed it immediately changes current 
state of the LED. During hold and after release the LED 
state should not change.


# Useful functions

Reading digital input state
- HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin);

Toggling digital output state
- HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);

Delay measured in [ms] (busy wait)
- HAL_Delay(1000);

Get current number of ticks measured since 
MCU start (in this exercise 1 tick = 1 [ms])
- HAL_GetTick();

Setting digital output to low/high
- HAL_GPIO_WritePin( LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
- HAL_GPIO_WritePin( LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);

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



