This course is prepared by Wojciech Domski.
All rights reserved.

# File description

- **model.py** - contains `Model` base class which defines the interface for all dynamic models (state, step, number of inputs/outputs)
- **simulator.py** - contains `Simulator` base class responsible for running ODE integration (`solve_ivp`) and collecting simulation data
- **dynamicLin.py** - main exercise file containing `UnicycleModel` (unicycle kinematics), trajectory generators (`trajectory_generator_circle`, `trajectory_generator_hexagon`), and `SimulatorDynamics` (dynamic linearisation based controller) with TODO placeholders to be filled by students
- **run.py** - script to run the dynamic linearisation exercise; creates the model, selects trajectory generator, runs the simulation and plots results

# Dynamic linearisation concept

Dynamic linearisation extends the state vector with an additional 
variable $\chi_1 = v - e \omega$, where $v$ is linear velocity 
and $\omega$ is angular velocity. The key benefit compared to 
static linearisation is that dynamic linearisation allows 
tracking of orientation. However, the system must be constantly 
on the move ($\chi_1 \neq 0$).

For the unicycle with $\delta = \frac{\pi}{2}$ the linearising 
functions are:
- $h_1 = x - e \sin(\theta)$
- $h_2 = y + e \cos(\theta)$

The dynamic decoupling matrix is:

$$K_d = \begin{bmatrix} \cos\theta & -\chi_1 \sin\theta \\ \sin\theta & \chi_1 \cos\theta \end{bmatrix}$$

with $\det K_d = \chi_1 \neq 0$.

The control law is:
$$w = K_d^{-1}(\ddot{h}_d - K_1 \dot{e}_h - K_0 e_h)$$

where $w = [w_1, w_2]^T$, $w_1 = \dot{\chi}_1$, $w_2 = \omega$.

The real control signals are: $\omega = w_2$ and 
$v = \chi_1 + e \omega$.

# Task 1 -- just drive
Given provided example in *dynamicLin.py* Python file provide implementation
for dynamic linearisation algorithm, and implementation of the Unicycle's 
kinematic model.

## Dynamic linearisation algorithm

To implement dynamic linearisation algorithm focus on 
*SimulatorDynamics.step()* method. In this method a code block marked 
with TODO placeholder was provided. It contains 
steps which have to be filled. These steps are mainly 
responsible for constructing the dynamic decoupling matrix 
and calculating state derivatives.

The entire template for dynamic linearisation calculation was provided and 
it is only necessary to fill the gaps.

During this task you need to implement everything but:
- desired trajectory represented as *trajectory_generator_circle*,
- control algorithm, including error calculation, *v_new* and *w*.

Apply constant control signals equal to 0.1 for both w1 and w2.

## Results

After a successful implementation the real trajectory 
should show a curved path because constant angular velocity 
(w2 = 0.1) was applied while the velocity parameter chi1 grows 
linearly (w1 = 0.1).

Change the initial pose (only orientation) to see if 
the real trajectory angle corresponds to the initial 
conditions.

# Task 2 -- follow a circle

The scope of this task is to implement circular 
trajectory and control law.

## Circular trajectory

Finish implementation of *trajectory_generator_circle()* 
function by providing first and second derivative.

## Control law

Calculate the new input *v_new* as PD controller with correction 
(feedforward from desired trajectory second derivative).
Calculate the control signal *w* using the inverse of the 
dynamic decoupling matrix $K_d$.

## Results

Now, a desired trajectory should look like a circle. 
If the control algorithm was properly implemented 
the real (realized) trajectory should also be circular 
in shape.

As initial condition use 
```
start = np.array([0.1, 0.1, np.pi/2*0.1])
```

The chi1 subplot should show that the extended state 
variable remains nonzero throughout the simulation, 
confirming that the system is always in motion.

# Task 3 -- follow a hexagon

The task is to provide a desired hexagonal trajectory.
This can be implemented as a partially admissible 
trajectory consisting of admissible sections (straight 
lines). A regular hexagon has 6 sides.

The default side length is 0.4. The trajectory generator 
function *trajectory_generator_hexagon()* accepts a 
parametric *side* argument.

For each segment $k$ ($k = 0, \ldots, 5$) the direction 
angle is $k \cdot \frac{\pi}{3}$. The velocity along 
each side has unit magnitude, so the time to traverse 
one side equals *side*. The total period is $6 \cdot$ *side*.

In *run.py* the following code has to be changed:
```
    # TODO chose trajectory generator
    trajectory_generator = trajectory_generator_circle
```
into
```
    # TODO chose trajectory generator
    trajectory_generator = trajectory_generator_hexagon
```

Now, the *trajectory_generator_hexagon()* function can be 
implemented inside *dynamicLin.py*.

## Results

Now, a desired trajectory should look like a hexagon. 
Also, the real trajectory should look like a hexagon.

Observe the chi1 plot to verify that the system 
maintains nonzero velocity throughout the trajectory.
