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
**adc_channels** array.

In this task you have to fill out following gaps:

- implement the corresponding callback function for ADC measurement,
- implement state machine which carries for measurement and 
communication flow,
- introduce periodical flow of measurement,
- periodically display which channels was measured and what value 
it holds.

Use following function to change actively measured channel 
on specific rank. You should chose proper ADC peripheral, 
rank (always set to *ADC_REGULAR_RANK_1*) and 
channel (from above table).
```C
LL_ADC_REG_SetSequencerRanks(adc, rank, channel);
```

# Task 2

Import **ADC_ex2** project into IDE.
The aim of this exercise is to show how to implement tasks in 
FreeRTOS. The exercise involves:
- periodic task creation,
- starting FreeRTOS scheduler, 
- communication between tasks using mutexes,
- communication using events via Event Groups.

You have to connect two pins with a wire. Pin PA0 (analog input) 
and PC13 (blue button). Connect those two ports 
while the dev board is not connected to power!
Use the leaflet given out during classes to identify the 
MCU pins.
Before proceeding further inform teacher about the connection 
and ask for permission to proceed further.

**This exercise contains three subexercises.**

The ADC1 is configured in such a way that the 
conversion is triggered by TIM6. It is required to 
start a timer TIM6 in time base mode with interrupts 
and start ADC1 peripheral (without interrupts or DMA).

There should be created two tasks:
- **measure**, a task responsible for reading measurements 
from ADC and storing it in memory. This task 
should be a periodic one with period equal to 1000 [ms],
- **comm** prints measured value via serial ports 
and determines if a button was pushed or not. This task 
should be a periodic one with period equal to 1000 [ms].

More information about FreeRTOS can be found in [FreeRTOSMastering] 
and [FreeRTOSManual].

## Subtask 1

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**,
- start TIM6 in time base mode with interrupts,
- start ADC1,
- write code that will read measured data from ADC periodically.

**In this exercise do not implement FreeRTOS tasks.**

Below you can see an example of an output:
```
4029, released
4035, released
4031, released
4031, released
0, pushed
0, pushed
4031, released
0, pushed
0, pushed
4029, released
4029, released
```

## Subtask 2

Subtask 2 is an extension to subtask 1 where FreeRTOS 
capabilities are used.

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**, **FreeRTOS.h**,
**task.h**, **semphr.h** (in this order),
- start TIM6 in time base mode with interrupts,
- start ADC1,
- create a mutex,
- create two tasks described above,
- start FreeRTOS scheduler,
- implement printf() redirection to serial port,
- implement **measure** task as a periodic one, period = 1000 [ms],
- implement **comm** task as a periodic one, period = 1000 [ms].

Below you can see an example of an output:
```
4036, released
4030, released
4031, released
4036, released
0, pushed
0, pushed
4024, released
4031, released
4031, released
0, pushed
4031, released
4030, released
```

## Subtask 3

Subtask 3 is a modification of Subtask 2 where 
instead of periodically calling **comm** task an 
event group is used instead. A mutex is 
still being used for data synchronization. 
The **comm** task should be only waked up when 
the measurement is ready to process.

Find proper API for handling Event Groups in [FreeRTOSManual].

In this exercise you have to fill out following gaps:
- include **event_groups.h** header file,
- create global variable for holding Event Group,
- create Event Group,
- in **measure** task set a flag (bit 0) in Event group,
- in **comm** task use appropriate API for waiting for 
an event. **Wait only for 400 [ms]**,
- make additional appropriate alterations to the code.

Below you can see an example of an output:
```
4029, released
no event
no event
4031, released
no event
no event
4031, released
no event
no event
4031, released
no event
no event
0, pushed
no event
no event
4031, released
no event
no event
```

# Task 3

Import **ADC_ex3** project into Atollic TrueSTUDIO.
The aim of this exercise is to show how to implement tasks in 
FreeRTOS. The exercise involves:
- periodic task creation,
- starting FreeRTOS scheduler, 
- communication between tasks using mutexes,
- communication using queues in different modes.

You have to connect two pins with a swire. Pin PA0 (analog input) 
and PC13 (blue button). Connect those two ports 
while the dev board is not connected to power!
Use the leaflet given out during classes to identify the 
MCU pins.
Before proceeding further inform teacher about the connection 
and ask for permission to proceed further.

**This exercise contains three subexercises.**

The ADC1 is configured in such a way that the 
conversion is triggered by TIM6. It is required to 
start a timer TIM6 in time base mode with interrupts 
and start ADC1 peripheral in DMA mode. This configuration 
allows for completely CPU-free periodic measurement of 
analog signal.

There should be created two tasks:
- **measure**, a task responsible for reading measurements 
from ADC and storing it in memory. 
- **comm** prints measured value via serial ports 
and determines if a button was pushed or not. 

More information about FreeRTOS can be found in [FreeRTOSMastering] 
and [FreeRTOSManual].

## Subtask 1

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**,
- start TIM6 in time base mode with interrupts,
- start ADC1 in DMA mode,
- write code that will prints measured data periodically, 
period should be equal to 1000 [ms].

**In this exercise do not implement FreeRTOS tasks.**

Below you can see an example of an output:
```
Measured 4029
Measured 4035
Measured 4031
Measured 4031
Measured 0
Measured 0
Measured 4031
Measured 0
Measured 0
Measured 4029
Measured 4029
```

## Subtask 2

Subtask 2 is an extension to subtask 1 where FreeRTOS 
capabilities are used.

The aim of this exercise is to implement a queue 
of size equal to 15 samples of uint16_t type. 
Two tasks should be created **measure** and **comm**.
Task **measure** should be made periodical with period 
equal to 300 [ms] (not ticks).
Task **comm** should be also periodical but depending 
on the number of items inside the queue it should change.
If there are more than 12 samples the **comm** task 
should have period equal to 100 [ms] while 
the queue has less than 4 items inside the period should 
be equal to 500 [ms]. This feature should be implemented 
as a hysteresis. In other words, if the queue is almost 
empty items should be pulled slowly while 
the queue is almost full the items should be pulled 
quickly.

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**, **FreeRTOS.h**,
**task.h**, **semphr.h**, **queue.h** (in this order),
- start TIM6 in time base mode with interrupts,
- start ADC1 in DMA mode,
- create a mutex to share a **queueError** variable between tasks,
- create a queue (15 samples of uint16_t),
- create two tasks described above,
- start FreeRTOS scheduler,
- implement printf() redirection to serial port,
- implement **measure** task as a periodic one,
- implement **comm** task as a periodic one,
- implement *proper* communication between **measure** and **comm** 
using created mutex and queue.

Three values should be printed via **comm** task:
- current time expressed in ticks,
- ADC value,
- queue size,
- queueError (flag).

Flag can be assigned with four values (implement as 
enumeration type QueueStatus):
- QueueOK (0) when a item was successfully sent to queue,
- QueueWriteProblem (1) when there was a problem during sending 
an item to the queue,
- QueueEmpty (2) queue was empty,
- QueueCantRead (3) an item could not be received from 
the queue.

Identify each state of the queue and print corresponding 
information.

Below you can see an example of an output:
```
Starting!
time: 0, measured value: 0, queue size 0, error 2
time: 500, measured value: 0, queue size 2, error 0
time: 1000, measured value: 0, queue size 3, error 0
time: 1500, measured value: 0, queue size 3, error 0
time: 2000, measured value: 0, queue size 4, error 0
time: 2500, measured value: 4035, queue size 5, error 0
time: 3000, measured value: 4035, queue size 5, error 0
time: 3500, measured value: 4035, queue size 6, error 0
time: 4000, measured value: 4036, queue size 7, error 0
time: 4500, measured value: 4036, queue size 7, error 0
time: 5000, measured value: 4036, queue size 8, error 0
time: 5500, measured value: 4036, queue size 9, error 0
time: 6000, measured value: 4036, queue size 9, error 0
time: 6500, measured value: 4036, queue size 10, error 0
time: 7000, measured value: 4036, queue size 11, error 0
time: 7500, measured value: 4035, queue size 11, error 0
time: 8000, measured value: 4035, queue size 12, error 0
time: 8500, measured value: 4035, queue size 13, error 0
time: 8600, measured value: 4035, queue size 12, error 0
time: 8700, measured value: 4035, queue size 11, error 0
time: 8800, measured value: 4035, queue size 11, error 0
time: 8900, measured value: 4036, queue size 10, error 0
time: 9000, measured value: 4036, queue size 9, error 0
time: 9100, measured value: 4036, queue size 9, error 0
time: 9200, measured value: 4036, queue size 8, error 0
time: 9300, measured value: 4035, queue size 7, error 0
time: 9400, measured value: 4035, queue size 7, error 0
time: 9500, measured value: 4035, queue size 6, error 0
time: 9600, measured value: 4035, queue size 5, error 0
time: 9700, measured value: 4035, queue size 5, error 0
time: 9800, measured value: 4035, queue size 4, error 0
time: 9900, measured value: 4037, queue size 3, error 0
time: 10400, measured value: 4037, queue size 4, error 0
time: 10900, measured value: 4037, queue size 5, error 0
time: 11400, measured value: 4037, queue size 5, error 0
time: 11900, measured value: 4035, queue size 6, error 0
time: 12400, measured value: 4035, queue size 7, error 0
time: 12900, measured value: 4035, queue size 7, error 0
time: 13400, measured value: 4035, queue size 8, error 0
time: 13900, measured value: 4035, queue size 9, error 0
time: 14400, measured value: 4035, queue size 9, error 0
time: 14900, measured value: 4035, queue size 10, error 0
time: 15400, measured value: 4035, queue size 11, error 0
time: 15900, measured value: 4035, queue size 11, error 0
time: 16400, measured value: 4035, queue size 12, error 0
time: 16900, measured value: 4035, queue size 13, error 0
time: 17000, measured value: 4035, queue size 12, error 0
time: 17100, measured value: 4035, queue size 11, error 0
time: 17200, measured value: 4035, queue size 11, error 0
time: 17300, measured value: 4035, queue size 10, error 0
time: 17400, measured value: 4035, queue size 9, error 0
time: 17500, measured value: 4035, queue size 9, error 0
time: 17600, measured value: 4035, queue size 8, error 0
time: 17700, measured value: 4035, queue size 7, error 0
time: 17800, measured value: 4035, queue size 7, error 0
time: 17900, measured value: 4035, queue size 6, error 0
time: 18000, measured value: 4035, queue size 5, error 0
time: 18100, measured value: 4035, queue size 5, error 0
time: 18200, measured value: 4035, queue size 4, error 0
time: 18300, measured value: 4035, queue size 3, error 0
time: 18800, measured value: 4035, queue size 4, error 0
```

## Subtask 3

Subtask 3 is an extension to subtask 1 where FreeRTOS 
capabilities are used.

The aim of this exercise is to implement a queue 
of size equal to 1 sample of QueueMessages type. 
This implementation is called mail box where 
message is broadcasted to the listeners.

Two tasks should be created **measure** and **comm**.
In addition to **measure** and **comm** a callback from 
ADC completed conversion should be implemented 
where an **adc_flag** should be set to 
one and the LED should be toggled.

Task **measure** should be made periodical with period 
equal to 300 [ms] (not ticks). However, only when 
there was a completed conversion (**adc_flag == 1**)
it should send a message through the queue 
(overwrite it with a new message), either 
**QueueMsgNewData** or **QueueMsgNewDataChange**. 
The message should switch to notify listening task 
of change.

Task **comm** should be also periodical with 
period equal to 1000 [ms].
The **comm** task should only peek the value 
stored in the queue. 

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**, **FreeRTOS.h**,
**task.h**, **semphr.h**, **queue.h** (in this order),
- start TIM6 in time base mode with interrupts,
- start ADC1 in DMA mode,
- implement ADC callback,
- create a mutex to share a **queueError** variable between tasks,
- create a queue (1 samples of QueueMessages),
- create two tasks described above,
- start FreeRTOS scheduler,
- implement printf() redirection to serial port,
- implement **measure** task as a periodic one, period = 300 [ms],
- implement **comm** task as a periodic one, period = 1000 [ms],
- implement *proper* communication between **measure** and **comm** 
using created mutex and queue.

Three values should be printed via **comm** task:
- current time expressed in ticks,
- ADC value,
- queue message,
- queueError (flag).

Flag can be assigned with four values (QueueStatus):
- QueueOK (0) when a item was successfully sent to queue,
- QueueWriteProblem (1) when there was a problem during sending 
an item to the queue,
- QueueEmpty (2) queue was empty,
- QueueCantRead (3) an item could not be received from 
the queue.

The queue message type should be assigned with one of three 
values (implement as enumeration type QueueMessages):
- QueueMsgNoData (0) there is no data, 
- QueueMsgNewData (1) new data available, 
- QueueMsgNewDataChange (2) new data available, same as 
QueueMsgNewData but allows to discover if there was a 
new portion of data.

Identify each state and message of the queue and print corresponding 
information.

Below you can see an example of an output:
```
Starting!
time: 0, measured value: 0, queue msg 0, error 0
time: 2000, measured value: 4036, queue msg 1, error 0
time: 3000, measured value: 4036, queue msg 2, error 0
time: 4000, measured value: 4036, queue msg 1, error 0
time: 5000, measured value: 4036, queue msg 2, error 0
time: 6000, measured value: 0, queue msg 1, error 0
time: 7000, measured value: 4035, queue msg 2, error 0
time: 8000, measured value: 4036, queue msg 1, error 0
time: 9000, measured value: 4036, queue msg 2, error 0
time: 10000, measured value: 0, queue msg 1, error 0
time: 11000, measured value: 0, queue msg 2, error 0
time: 12000, measured value: 4036, queue msg 1, error 0
time: 13000, measured value: 4035, queue msg 2, error 0
time: 14000, measured value: 4035, queue msg 1, error 0
time: 15000, measured value: 4035, queue msg 2, error 0
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


