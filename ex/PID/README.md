This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **PID_ex1** project into IDE.
The aim of this exercise is to practice acquired FreeRTOS skills 
and implement PID controller. The exercise involves:
- decomposition of system into separate FreeRTOS,
- communication between tasks using different synchronization 
mechanisms,
- implementation of PID controller.

More information about FreeRTOS can be found in [FreeRTOSMastering] 
and [FreeRTOSManual].

## DC motor simulator

This task comes with a additional board -- a DC motor simulator. 
The DC motor simulator is a low pass filter which 
mimics a real DC motor. 
|DC motor simulator|Connector   |MCU description|
|--|--|--|
|GND               |GND         |Ground         |
|IN                |**DAC1**    |MCU DAC output |
|OUT               |**ADC1**    |MCU ADC input  |

Refer to [board schematic](https://github.com/wdomski/ARClab/blob/develop/boards/NUCLEO64-Board.pdf) 
for connection diagram.

## MCU configuration

The ADC1 is configured in such a way that the 
conversion is triggered by software. The conversion can be started 
in interrupt mode (all necessary interrupts are already enabled).

The DAC1 peripheral is also configured.

## PID

PID is a regulator which is a sum of three terms: 
proportional, integral and derivative. 
PID algorithm accepts as input two values: the desired value 
and the measured value. Based on those two values it calculates 
current error which is a difference between them.

```
e = dv - mv
```

PID output can be defined with following simplified formula

```
u = Kp * e + Ki * e_sum + Kd * e_diff
```
where
- *u* is the PID output, a control signal applied to the 
control object,
- *Kp* is the proportional coefficient,
- *Ki* is the integral coefficient,
- *Kd* is the derivative coefficient,
- *e* is current error calculated as difference between 
the desired and the measured value,
- *e_sum* is the error sum. Sum of all previous errors 
which were present in the system from the start of PID 
controller.
- *e_diff* is the error derivative. Usually, it can be 
calculated as difference between current error and 
error from previous iteration.

The *Ki* and *Kd* should be scaled with time -- which 
is the period with which the control loop operates.

Implement PID controller in *pid.c* and in corresponding 
*pid.h* header file.

More about PID controllers can be read in [PID].

## Task 1

This exercise goal is to implement a PID controller for 
a DC motor. Instead of a real motor a DC motor simulator is 
used which is a simple RC circuit.

This task should be implemented with four FreeRTOS tasks:
- **measure** -- a task responsible for reading measured value 
using ADC. The measured value is sent to **control** task.
- **user** -- a task which implements the user interface. The 
user should be able to change desired value in range of 
[0,4000] with step 500 (see example of an output). 
The task sends the desired value to **control** thread.
User can input following values '0', '1', ..., '8' where
'0' is translated to 0 desired value while 8 is translated 
to 4000 desired value. Other values entered by the user 
via serial port should be ignored.
- **control** -- a task which uses a PID controller. Based on the 
measured value (**mv**) and the desired value (**dv**) calculates 
the control signal (**cs**). This task directly 
controls DAC output with control signal. 12-bit 
DAC resolution can be used instead of 8-bit.
- **communication** -- a task which sends via *printf()*
information about the measured value, the desired value 
and the control signal.

Following table shows the frequency of each task:

|Task name     | Frequency [Hz]|
|--|--|
|measure       | 100 |
|control       | 100 |
|communication | 2   |
|user          | 10  |

The FreeRTOS time grain is set to 1 ms.

The synchronization mechanism for tasks can be freely chosen. 
It can involve mutexes, queues and/or event groups.

Following items should be present in the finished exercise:
- initialization of all peripherals,
- serial port configuration,
- proper implementation of PID controller,
- proper implementation of all four tasks,
- proper implementation of synchronization between tasks,
- tuned PID controller for the DC motor simulation.

Below you can see an example of an output:
```
Starting!
mv:    0, dv: 1000, cs: 4095
mv:  938, dv: 1000, cs: 1197
mv:  983, dv: 1000, cs: 1064
mv:  991, dv: 1000, cs: 1070
mv:  996, dv: 1000, cs: 1064
mv:  999, dv: 1000, cs: 1057
mv:  999, dv: 1000, cs: 1063
mv: 1000, dv: 1000, cs: 1059
mv: 1726, dv: 4000, cs: 4095
mv: 2600, dv: 4000, cs: 4095
mv: 3136, dv: 4000, cs: 4095
mv: 3471, dv: 4000, cs: 4095
mv: 3678, dv: 4000, cs: 4095
mv: 3805, dv: 4000, cs: 4095
mv: 3885, dv: 4000, cs: 4095
mv: 2423, dv:    0, cs:    0
mv: 1493, dv:    0, cs:    0
mv:  921, dv:    0, cs:    0
mv:  566, dv:    0, cs:    0
mv:  351, dv:    0, cs:    0
mv:  215, dv:    0, cs:    0
mv:  474, dv: 1000, cs: 1217
mv:  735, dv: 1000, cs: 1176
mv:  870, dv: 1000, cs: 1121
mv:  937, dv: 1000, cs: 1087
mv:  581, dv:  500, cs:    0
mv:  400, dv:  500, cs:  453
mv:  435, dv:  500, cs:  583
mv:  468, dv:  500, cs:  571
mv:  484, dv:  500, cs:  568
mv:  408, dv:    0, cs:    0
mv:  246, dv:    0, cs:    0
mv:  147, dv:    0, cs:    0
mv:   84, dv:    0, cs:    0
mv:   48, dv:    0, cs:    0
mv:   23, dv:    0, cs:    0
mv:   10, dv:    0, cs:    0
mv:    0, dv:    0, cs:    0
mv:    0, dv:    0, cs:    0
mv:    0, dv:    0, cs:    0
```

# Useful functions

Start ADC conversion in interrupt mode.
```C
HAL_ADC_Start_IT();
```

Start ADC.
```C
HAL_ADC_Start();
```

Start ADC in DMA mode, measurement treated as buffer 
of length equal to 1 sample.
```C
HAL_ADC_Start_DMA();
```

Start TIM in time base mode with interrupts:
```C
HAL_TIM_Base_Start_IT(&htim6);
```

Callback function called when the ADC measurement is ready.
```C
HAL_ADC_ConvCpltCallback();
```

Returns last measured value.
```C
HAL_ADC_GetValue();
```

Enable reception on UART in interrupt mode.
```C
HAL_UART_Receive_IT();
```

Callback function called when data was received by UART.
```C
HAL_UART_RxCpltCallback();
```

Get current number of ticks measured since 
MCU start (in this exercise 1 tick = 1 [ms])
```C
HAL_GetTick();
```

Redirection of *printf()* function output to serial port 
can be done with redefinition of *_write()* function.
Also include **stdio.h**.

```C
int _write(int file, char *ptr, int len) {
	HAL_UART_Transmit(&huart2, (uint8_t *) ptr, len, 50);
	return len;
}
```

## FreeRTOS related

### Mutexes

Create a mutex. This function returns a mutex:
```C
xSemaphoreCreateMutex();
```

Take (lock) mutex:
```C
xSemaphoreTake();
```

Give (unlock) mutex:
```C
xSemaphoreGive();
```

### Event Groups

Create an Event Group:
```C
xEventGroupCreate();
```

Set bits in an Event Group:
```C
xEventGroupSetBits();
```

Wait for bits to be set:
```C
xEventGroupWaitBits();
```

### Queues

Create a queue:
```C
xQueueCreate(numberOfItems, sizeOfItem);
```

Check how meny items is currently in queue:
```C
uxQueueMessagesWaiting();
```

Receive an item from queue:
```C
xQueueReceive();
```

Send item to queue:
```C
xQueueSendToBack();
```

Check the item without taking it out from queue:
```C
xQueuePeek();
```

### Task related

Create a task **example** with  **exampleTask** function which 
implements the task:
```C
xTaskCreate(exampleTask, "example", configMINIMAL_STACK_SIZE * 4, NULL, 3, NULL);
```

Start scheduler:
```C
vTaskStartScheduler();
```

General look of a task:
```C
void exampleTask(void * args) {

	for (;;) {

	}
}
```

General look of a periodic task with period of 100 [ms]:
```C
void exampleTask(void * args) {
	TickType_t xLastWakeTime;
	xLastWakeTime = xTaskGetTickCount();
	
	for (;;) {
		vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
	}
}
```


