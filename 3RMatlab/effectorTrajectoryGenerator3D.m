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
    
    %caclulate first and second derivative based on the qchd vector
    qchd_d1 = [0; 0; 0];
    qchd_d2 = [0; 0; 0];
    
end

