This course is prepared by Wojciech Domski.
All rights reserved.

# File description

- **inputOutputDecoupling.py** - main exercise file containing `effector_trajectory_generator_3d()` (desired end-effector trajectory with derivatives) and `model_ode()` (3R manipulator ODE with input-output decoupling controller) with TODO placeholders to be filled by students
- **simulator.py** - contains `Simulator` class responsible for running the ODE integration and collecting simulation data
- **run.py** - script to run the input-output decoupling exercise; configures manipulator parameters, runs the simulation and plots results
- **requirements.txt** - Python dependencies

# Task 1
Run run.py script and observe how joint trajectory is changing.
Can you explain it?

You can use below to observe the joint trajectory:
```Python
plt.plot(sim_data['time'], sim_data['out_qr_d0'])
```

# Task 2
Introduce friction in manipulator joints using Tustin friction model. You 
need to calculate proper elements for **T** vector.
Use tips in inputOutputDecoupling.py to introduce the friction model.

Run run.py script and observe how joint trajectory is changing.
Can you explain it?

# Task 3
Implement input-output decoupling algorithm.
Use tips in code to calculate **F** and **G** describing the 
affine system. Calculate errors **e**, **e_d1** and after that calculate 
the new input to the system **v**. Calculate inverse of matrix **G** and 
define it as **Ginv**. Finally, calculate control input vector **u**.
All necessary formulas for above you will find in the inputOutputDecoupling.py 
script comments.

Also remember to calculate 1st and 2nd derivative for 
desired end-effector trajectory in function *effector_trajectory_generator_3d*.
Do not change the desired trajectory functions, just calculate 
1st and 2nd derivative for provided functions.

Is everything working as expected? If not what can be the problem and how 
you can fix it?

# Useful informations

## Plotting

To plot errors calculated as difference between real and desired 
end-effector trajectory you can use following
```Python
plt.plot(sim_data['time'], additional['k'][0,:] - additional['qchd'][0,:],
         sim_data['time'], additional['k'][1,:] - additional['qchd'][1,:],
         sim_data['time'], additional['k'][2,:] - additional['qchd'][2,:])
```

Similarly, you can plot real vs. desired trajectory in 3D:
```Python
ax = plt.subplot(projection='3d')
ax.plot(additional['k'][0,:], additional['k'][1,:], additional['k'][2,:], 'r')
ax.plot(additional['qchd'][0,:], additional['qchd'][1,:], additional['qchd'][2,:], 'b')
```

Finally, to observe joint trajectory:
```Python
plt.plot(sim_data['time'], sim_data['out_qr_d0'])
```

## Data structures

There are two data structures important for analysis of simulation results:
- sim_data
- additional

**sim_data** has following fields:
- **time** time series,
- **out_qr_d1** q' (manipulator joint velocities),
- **out_qr_d0** q (manipulator joint positions).

**additional** has following fields:
- **qchd** desired end-effector trajectory,
- **qchd_d1** desired end-effector trajectory (velocities),
- **qchd_d2** desired end-effector trajectory (accelerations),
- **dets** selected determinants,
- **k** real end-effector trajectory. 
