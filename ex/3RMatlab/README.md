This course is prepared by Wojciech Domski.
All rights reserved.

# Task 1
Run start.m script and observe how joint trajectory is changing.
Can you explain it?

You can use below to observe the joint trajectory:
```Matlab
plot(sim_data.time,sim_data.out_qr_d0)
```

# Task 2
Introduce friction in manipulator joints using Tustin friction model. You 
need to calculate proper elements for **T** vector.
Use tips in modelODE.m to introduce the friction model.

Run start.m script and observe how joint trajectory is changing.
Can you explain it?

# Task 3
Implement input-output decoupling algorithm.
Use tips in code to calculate **F** and **G** describing the 
affine system. Calculate errors **e**, **e_d1** and after that calculate 
the new input to the system **v**. Calculate inverse of matrix **G** and 
define it as **GInv**. Finally, calculate control input vector **u**.
All necessary formulas for above you will find in the modelODE.m script 
comments.

Also remember to calculate 1st and 2nd derivative for 
desired end-effector trajectory in file *effectorTrajectoryGenerator3D*.
Do not change the desired trajectory functions, just calculate 
1st and 2nd derivative for provided functions.

Is everything working as expected? If not what can be the problem and how 
you can fix it?

# Useful informations

## Plotting

To plot errors calculated as difference between real and desired 
end-effector trajectory you can use following
```Matlab
plot(sim_data.time,additional.k(1,:)-additional.qchd(1,:),sim_data.time,additional.k(2,:)-additional.qchd(2,:),sim_data.time,additional.k(3,:)-additional.qchd(3,:))
```

Similarly, you can plot real vs. desired trajectory in 3D:
```Matlab
plot3(additional.k(1,:),additional.k(2,:),additional.k(3,:),additional.qchd(1,:),additional.qchd(2,:),additional.qchd(3,:))
```

Finally, to observe joint trajectory:
```Matlab
plot(sim_data.time,sim_data.out_qr_d0)
```

## Data structures

There two data structures important for analysis of simulation results:
- sim_data
- additional

**sim_data** has following fields:
- **time** time series,
- **out_qr_d1** q' (manipulator joint velocities),
- **out_qr_d0** q' (manipulator joint positions).

**additional** has following fields:
- **qchd** desired end-effector trajectory,
- **qchd_d1** desired end-effector trajectory (velocities),
- **qchd_d2** desired end-effector trajectory (accelerations),
- **dets** selected determinants,
- **k** real end-effector trajectory. 



























