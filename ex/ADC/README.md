This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **ADC_ex1** project into IDE.
The aim of this exercise is to show how basic ADC 
measurement with interrupts works.
The ADC conversion is triggered by software. Two 
ADC channels were configured for **ADC3** and **ADC4** 
connectors, both for ADC1 peripheral. 

Below a table was presented to which ADC peripherals 
and channels connectors were attached.

|Connector|Peripheral|Channel    |
|-|-|-|
|**ADC3** | ADC1     | Channel 4 |
|**ADC4** | ADC1     | Channel 13|

Implement a state machine which draft is included in 
*main.c* file. Following states are available:
- ADC_Idle (currently there is no conversion)
- ADC_Converting (ADC is measuring the analog signal)
- ADC_Ready (ADC measurement is ready)

The measurement should be triggered every one second. 
For this use **HAL_GetTick()**. Do not introduce explicit 
delays.

During the implementation use provided variables: 
- **flag** to discover if IRQ was handled, 
- **measurement** holds measurement, 
- **last_time** is time in ms of last measurement, 
- **adc_channels** an array holding ADC channels, use 
**measured_channel** to move through available ADC channels,
- **measured_channel** currently measured channel, an index of 
**adc_channels** array, can be used to identify currently 
measured channel.

In this task you have to fill out following gaps:

- implement the corresponding callback function for ADC measurement,
- implement state machine which carries for measurement and 
communication flow,
- introduce periodical flow of measurement,
- periodically display which channels was measured and what value 
it holds.

The ADC is set to perform scanning conversion. 
After each conversion the interrupt is being fired. 
The order of channels in ranks defines the order of interrupts. 
First channel (**ADC3** connector) to be measured is assigned to 
rank no. 1 and the second one (**ADC4** connector) is 
assigned to rank no. 2.

# Useful functions

Start ADC conversion in interrupt mode.
```C
HAL_ADC_Start_IT(&hadc1);
```

Start TIM in time base mode with interrupts:
```C
HAL_TIM_Base_Start_IT(&htim6);
```

Callback function called when the ADC measurement is ready.
```C
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc);
```

Returns last measured value.
```C
measurement = HAL_ADC_GetValue(&hadc1);
```

Get current number of ticks measured since 
MCU start (in this exercise 1 tick = 1 [ms])
```C
HAL_GetTick();
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




