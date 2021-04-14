function [ qchd, qchd_d1, qchd_d2 ] = effectorTrajectoryGenerator3D( t, parameters)
%effectorTrajectoryGenerator
%generates prime function, first and second derivative for
%end effector trajectory

    w = 0.015 * 2 * pi;
    k = 0.5;
    dx = 2.3;
    dy = 0.1;
    dz = 0.0;
    
    qchd = [k*cos(w*t)+dx; k*sin(w*t)+dy; 0.1*k*cos(w*t)+dz];
    qchd_d1 = [-w * k*sin(w*t); w * k*cos(w*t); - 0.1 * w * k*sin(w*t)];
    qchd_d2 = [-w * w * k*cos(w*t); -w * w * k*sin(w*t); -0.1 * w * w * k*cos(w*t)];
    
end

