This course is prepared by Wojciech Domski.
All rights reserved.

# Prerequisites

Remember to add *printf()* redirection.
Also do not forget to turn off optimization and 
set parallel build e.g. for 8 simultaneous threads.
Create a launch debug configuration that 
will only flash the MCU without entering debug mode.

# Task 1

Import **FreeRTOS_ex1** project into IDE.
The aim of this exercise is to show how to implement tasks in 
FreeRTOS. The exercise involves:
- periodic task creation,
- starting FreeRTOS scheduler, 
- communication between tasks using mutexes,
- communication using events via Event Groups.

**This exercise contains three sub-exercises.**

The ADC1 for **ADC2** connector is configured in such a way 
a software conversion launch is required. 
Further exercises may require changes to the imported project.
It is required to start a timer TIM6 (1Hz frequency) in time 
base mode with interrupts and start ADC1 peripheral 
(without interrupts or DMA).

Moreover, **TIMER3** connector was configured so it 
generates a square wave with frequency of 1/3Hz ~= 0.33Hz.
**TIMER3** connector is connected with **ADC2** connector
through low-pass filter.

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
- start PWM generation for TIM1, channel 3 for **TIMER3** connector,
- start ADC1,
- write code that will read measured data from ADC periodically,
- print data via redirected printf(), both measurement and 
local time in milliseconds.

**In this exercise do not implement FreeRTOS tasks.**

Sample output from serial console:
```
Starting!             
ADC: 1341, time: 1002 
ADC: 2996, time: 2005 
ADC: 2045, time: 3008 
ADC:  782, time: 4011 
ADC: 2789, time: 5014 
ADC: 1944, time: 6017 
ADC:  779, time: 7020 
ADC: 2788, time: 8023 
ADC: 1922, time: 9026 
ADC:  808, time: 10029
ADC: 2796, time: 11032
ADC: 1903, time: 12035
ADC:  835, time: 13038
ADC: 2807, time: 14041
ADC: 1887, time: 15044
ADC:  864, time: 16047
ADC: 2819, time: 17050
```

Can you explain why the square wave is deformed and 
we are observing values other than minimum and maximum?

## Subtask 2

Subtask 2 is an extension to subtask 1 where FreeRTOS 
capabilities are used.

In this exercise you have to fill out following gaps:
- include all necessary headers **stdio.h**, **FreeRTOS.h**,
**task.h**, **semphr.h** (in this order),
- start PWM generation for TIM1, channel 3 for **TIMER3** connector,
- start TIM6 in time base mode, no interrupts,
- start ADC1 without interrupts,
- create a mutex,
- create two tasks described above,
- start FreeRTOS scheduler,
- implement printf() redirection to serial port,
- implement **measure** task as a periodic one, period = 1000 [ms],
- implement **comm** task as a periodic one, period = 1000 [ms],
- print data via redirected printf(), both measurement and 
local time in milliseconds.

Below you can see an example of an output:
```
Starting!             
ADC:    0, time: 1    
ADC: 1460, time: 1001 
ADC: 1465, time: 2001 
ADC: 3040, time: 3001 
ADC: 2067, time: 4001 
ADC:  769, time: 5001 
ADC: 2781, time: 6001 
ADC: 1967, time: 7001 
ADC:  731, time: 8001 
ADC: 2765, time: 9001 
ADC: 1962, time: 10001
ADC:  728, time: 11001
ADC: 2765, time: 12001
ADC: 1960, time: 13001
ADC:  730, time: 14001
ADC: 2766, time: 15001
```

Do you see some difference? Maybe some discrepancy or lack of it?
What have caused it and can you explain why?

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
- reconfigure project so TIM6 can generate interrupts,
- reconfigure project so ADC1 is triggered not by software but 
via event from TIM6,
- start PWM generation for TIM1, channel 3 for **TIMER3** connector,
- create global variable for holding Event Group,
- create Event Group,
- in **measure** task set a flag (bit 0) in Event group,
- in **comm** task use appropriate API for waiting for 
an event. **Wait only for 400 [ms]**,
- make additional appropriate alterations to the code,
- print data via redirected printf(), both measurement and 
local time in milliseconds.

Below you can see an example of an output:
```
Starting!            
ADC: 2069, time: 1   
no event             
no event             
ADC: 2074, time: 1001
no event             
no event             
ADC: 3274, time: 2001
no event             
no event             
ADC: 2159, time: 3001
no event             
no event             
ADC:  802, time: 4001
no event             
no event             
ADC: 2795, time: 5001
no event             
no event             
ADC: 1978, time: 6001
no event             
no event             
ADC:  733, time: 7001
no event             
no event             
ADC: 2767, time: 8001
no event             
```

# Task 2

Import **FreeRTOS_ex2** project into IDE.
The aim of this exercise is to show how to implement tasks in 
FreeRTOS. The exercise involves:
- periodic task creation,
- starting FreeRTOS scheduler, 
- communication between tasks using mutexes,
- communication using queues in different modes.

**This exercise contains three subexercises.**

The ADC1 is configured in such a way that the 
conversion is triggered by TIM6. It is required to 
start a timer TIM6 in time base mode with interrupts 
and start ADC1 peripheral in DMA mode. This configuration 
allows for completely CPU-free periodic measurement of 
analog signal.

Additional changes to the project are required:
- enable interrupts on TIM6,
- select trigger event as Update Event for TIM6,
- select trigger source for ADC1,
- configure DMA for ADC1 in circular mode,
- enable DMA transfers on ADC completed conversion.

It is required to start a timer TIM6 (1Hz frequency) in time 
base mode with interrupts and start ADC1 peripheral 
(without interrupts or DMA).

Moreover, **TIMER3** connector was configured so it 
generates a square wave with frequency of 1/3Hz ~= 0.33Hz.
**TIMER3** connector is connected with **ADC2** connector
through low-pass filter.

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
- start PWM generation for TIM1, channel 3 for **TIMER3** connector,
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
```C
HAL_ADC_Start_IT(&hadc1);
```

Start ADC.
```C
HAL_ADC_Start(&hadc1);
```

Start ADC in DMA mode, measurement treated as buffer 
of length equal to 1 sample.
```C
HAL_ADC_Start_DMA(&hadc1, (uint32_t *) &measurement, 1);
```

Start TIM in time base mode with interrupts:
```C
HAL_TIM_Base_Start_IT(&htim6);
```

Callback function called when the ADC measurement is ready.
```C
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc);
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


