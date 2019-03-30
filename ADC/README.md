This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **ADC_ex1** project into Atollic TrueSTUDIO.
The aim of this exercise is to show how basic ADC 
measurement with interrupts works.
The ADC conversion is triggered by software. When the 
converted digital value is ready an interrupt is rosed.
Corresponding callback function is called then called.

To imitate analog signal digital signal from blue pushbutton 
is connected to the analog input.

Below you can see example of an output:
```
Measured value = 4031
Measured value = 0
Measured value = 4034
Measured value = 4034
Measured value = 0
Measured value = 0
Measured value = 4031
Measured value = 4031
Measured value = 4032
```
Can you explain it?

You have to connect two pins with a wire. Pin PA0 (analog input) 
and PC13 (blue button). Connect those two ports 
while the dev board is not connected to power!
Use the leaflet given out during classes to identify the 
MCU pins.
Before proceeding further inform teacher about the connection 
and ask for permission to proceed further.

Implement a simple state machine which draft is included in 
*main.h* file. Following states are available:
- ADC_Idle (currently there is no conversion)
- ADC_Converting (ADC is measuring the analog signal)
- ADC_Ready (ADC measurement is ready)

The measurement should be triggered every one second. 
For this use **HAL_GetTick()**. Do not introduce explicit 
delays.

During the implementation use provided variables: **flag**, **measurement** 
and **lasttime**.

In this task you have to fill out following gaps:

- implement the corresponding callback function for ADC measurement,
- implement state machine which carries for measurement and 
communication flow,
- introduce periodical flow of measurement.


# Useful functions

Start ADC conversion in interrupt mode.
- HAL_ADC_Start_IT(&hadc1);

Callback function called when the ADC measurement is ready.
- void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc);

Returns last measured value.
- measurement = HAL_ADC_GetValue(&hadc1);

Get current number of ticks measured since 
MCU start (in this exercise 1 tick = 1 [ms])
- HAL_GetTick();

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



