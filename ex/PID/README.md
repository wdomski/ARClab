This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **PID_ex1** project into Atollic TrueSTUDIO.
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
mimics a real DC motor. Before proceeding further 
calculate the frequency for which the filter will attenuate to 
half its original power. This will allow to select 
proper values for PID controller. Each board has necessary 
parameters written at its top.

You have to connect the DC motor with the dev board. 

|DC motor simulator|Nucleo board|Description    |
|--|--|--|
|GND               |GND         |Ground         |
|IN                |PA4         |MCU DAC output |
|OUT               |PA0         |MCU ADC input  |

Connect DC motor simulator  
while the dev board is disconnected from power!
Use the leaflet given out during classes to identify the 
MCU pins.
Before proceeding further inform teacher about the connection 
and ask for permission to proceed further.

## MCU configuration

The ADC1 is configured in such a way that the 
conversion is triggered by software. The conversion can be started 
in interrupt mode (all necessary interrupts are already enabled).

The DAC1 peripheral is also configured.

Also interrupts from EXTI are enabled to facilitate the 
implementation of the user interface (switch button).

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

Implement PID controller in pid.c and in corresponding 
pid.h header file.

More about PID controllers can be read in [PID].

## Task 1

This exercise's goal is to implement a PID controller for 
a DC motor. Instead of a real motor a DC motor simulator is 
used which is a simple RC circuit.

This task should be implemented with four FreeRTOS tasks:
- **measure** -- a task responsible for reading measured value 
using ADC. The measured value is sent to **control** task.
- **user** -- a task which implements the user interface. The 
user should be able to change desired value in range of 
[0,4000] with step 400 (see example of an output). 
The task sends the desired value to **control** thread.
- **control** -- a task which uses a PID controller. Based on the 
measured value (**mv**) and the desired value (**dv**) calculates 
the control signal (**cs**). This task directly 
controls DAC output with control signal. 12-bit 
DAC resolution can be used instead of 8-bit.
- **communication** -- a task which sends via printf 
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

Also add visualization of:
- the desired value,
- the measured value,
- the control signal,
- the error between the desired value and the measured value.

Following items should be present in the finished exercise:
- proper implementation of PID controller,
- proper implementation of all four tasks,
- proper implementation of synchronization between tasks,
- tunned PID controller for the DC motor simulation,
- calculate frequency for RC circuit (DC motor simulator),
- visualization of all necessary signals.

Below you can see an example of an output:
```
Starting!
mv:0,dv:1000,cs:4095
mv:894,dv:1000,cs:1043
mv:944,dv:1000,cs:1067
mv:968,dv:1000,cs:1090
mv:984,dv:1000,cs:1079
mv:996,dv:1000,cs:1048
mv:993,dv:1000,cs:1086
mv:996,dv:1000,cs:1079
mv:999,dv:1000,cs:1067
mv:1000,dv:1000,cs:1062
mv:999,dv:1000,cs:1071
mv:998,dv:1000,cs:1076
mv:1221,dv:1500,cs:3053
mv:1503,dv:1500,cs:1623
mv:1506,dv:1500,cs:1575
mv:1705,dv:2000,cs:3684
mv:2006,dv:2000,cs:2135
mv:2010,dv:2000,cs:2067
mv:2346,dv:2500,cs:3548
mv:2518,dv:2500,cs:2601
mv:2634,dv:3000,cs:4095
mv:3032,dv:3000,cs:3189
mv:3034,dv:3000,cs:3037
mv:3345,dv:3500,cs:4095
mv:3557,dv:3500,cs:3677
mv:3582,dv:4000,cs:4095
mv:3747,dv:4000,cs:4095
mv:3843,dv:4000,cs:4095
mv:3898,dv:4000,cs:4095
mv:3931,dv:4000,cs:4095
mv:2362,dv:0,cs:0
mv:1399,dv:0,cs:0
mv:830,dv:0,cs:0
mv:496,dv:0,cs:0
mv:292,dv:0,cs:0
mv:172,dv:0,cs:0
mv:103,dv:500,cs:0
mv:178,dv:500,cs:584
mv:554,dv:1000,cs:2593
mv:920,dv:1000,cs:1141
mv:1186,dv:1500,cs:3072
mv:1486,dv:1500,cs:1631
mv:1498,dv:1500,cs:1577
mv:1502,dv:1500,cs:1554
mv:1501,dv:1500,cs:1560
mv:1503,dv:1500,cs:1547
mv:1497,dv:1500,cs:1583
```

# Useful functions

Start ADC conversion in interrupt mode.
- HAL_ADC_Start_IT(&hadc1);

Start ADC.
- HAL_ADC_Start(&hadc1);

Start ADC in DMA mode, measurement treated as buffer 
of length equal to 1 sample.
- HAL_ADC_Start_DMA(&hadc1, (uint32_t *) &measurement, 1);

Start TIM in time base mode with interrupts:
- HAL_TIM_Base_Start_IT(&htim6);

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

## FreeRTOS related

### Mutexes

Create a mutex. This function returns a mutex:
- xSemaphoreCreateMutex();

Take (lock) mutex:
- xSemaphoreTake();

Give (unlock) mutex:
- xSemaphoreGive();

### Event Groups

Create an Event Group:
- xEventGroupCreate();

Set bits in an Event Group:
- xEventGroupSetBits();

Wait for bits to be set:
- xEventGroupWaitBits();

### Queues

Create a queue:
- xQueueCreate(numberOfItems, sizeOfItem);

Check how meny items is currently in queue:
- uxQueueMessagesWaiting();

Receive an item from queue:
- xQueueReceive();

Send item to queue:
- xQueueSendToBack();

Check the item without taking it out from queue:
- xQueuePeek();

### Task related

Create a task **example** with  **exampleTask** function which 
implements the task:
- xTaskCreate(exampleTask, "example", configMINIMAL_STACK_SIZE * 4, NULL, 3, NULL);

Start scheduler:
- vTaskStartScheduler();

General look of a task:
```
void exampleTask(void * args) {

	for (;;) {

	}
}
```

General look of a periodic task with period of 100 [ms]:
```
void exampleTask(void * args) {
	TickType_t xLastWakeTime;
	xLastWakeTime = xTaskGetTickCount();
	
	for (;;) {
		vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
	}
}
```


