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
to write a program which will digital input state (button) 
and toggle LED every time when a button is pressed.

