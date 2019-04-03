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

Below you can see an example of an output:
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

# Task 2

Import **ADC_ex2** project into Atollic TrueSTUDIO.
The aim of this exercise is to show how to implement tasks in 
FreeRTOS. The exercise involves:
- periodic task creation,
- starting FreeRTOS scheduler, 
- communication between tasks using mutexes.

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

In this excercise you have to fill out following gaps:
- include all necessary headers **stdio.h**, **FreeRTOS.h**,
**task.h**, **semphr.h** (in this order),
- start TIM6 in time base mode with interrupts,
- start ADC1,
- create a mutex,
- create two tasks described above,
- start FreeRTOS scheduler,
- implement printf() redirection to serial port,
- implement **measure** task as a periodic one,
- implement **comm** task as a periodic one.

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

More information about FreeRTOS can be found in [FreeRTOSMastering] 
and [FreeRTOSManual].

# Useful functions

Start ADC conversion in interrupt mode.
- HAL_ADC_Start_IT(&hadc1);

Start ADC.
- HAL_ADC_Start(&hadc1);

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

Create mutex. This function returns a mutex:
- xSemaphoreCreateMutex();

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


