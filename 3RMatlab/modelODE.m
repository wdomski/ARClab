function [ output_args, additional ] = modelODE( t, input_args, parameters )
    
    %get input values

    %manipulator joint position
        qr_d1 = input_args(1:3);
        q_d1 = qr_d1;
    %manipulator joint velocities
        qr = input_args(4:6); 
        q = qr;

    m1 = parameters.m1;
    m2 = parameters.m2;
    m3 = parameters.m3;
    mc = parameters.mc;

    l1 = parameters.l1;
    l2 = parameters.l2;
    l3 = parameters.l3;

    a = parameters.a;
    b = parameters.b;
    c = parameters.c;
    
    g = parameters.g;
    
    Tv = parameters.Tv;
    Ts = parameters.Ts;  
    Tk = parameters.Tk;      

    Kp = parameters.Kp;
    Kd = parameters.Kd;
    
    %test START
    %test STOP

    %calculate position of the end-effector
    xch = ...
    a + l1*cos(qr(1)) - l2*(sin(qr(1))*sin(qr(2)) - cos(qr(1))*cos(qr(2))) - l3*cos(qr(3))*(sin(qr(1))*sin(qr(2)) - cos(qr(1))*cos(qr(2)));
    ych = ...
    b + l1*sin(qr(1)) + l2*(cos(qr(1))*sin(qr(2)) + cos(qr(2))*sin(qr(1))) + l3*cos(qr(3))*(cos(qr(1))*sin(qr(2)) + cos(qr(2))*sin(qr(1)));
    zch = ...
    c + l3*sin(qr(3));
    xch_d1 = ...
    - l3*(cos(qr(3))*(cos(qr(1))*sin(qr(2))*qr_d1(1) + cos(qr(2))*sin(qr(1))*qr_d1(1) + cos(qr(1))*sin(qr(2))*qr_d1(2) + cos(qr(2))*sin(qr(1))*qr_d1(2)) - sin(qr(3))*(sin(qr(1))*sin(qr(2)) - cos(qr(1))*cos(qr(2)))*qr_d1(3)) - l2*(cos(qr(1))*sin(qr(2))*qr_d1(1) + cos(qr(2))*sin(qr(1))*qr_d1(1) + cos(qr(1))*sin(qr(2))*qr_d1(2) + cos(qr(2))*sin(qr(1))*qr_d1(2)) - l1*sin(qr(1))*qr_d1(1);
    ych_d1 = ...
    l3*(cos(qr(3))*(cos(qr(1))*cos(qr(2))*qr_d1(1) + cos(qr(1))*cos(qr(2))*qr_d1(2) - sin(qr(1))*sin(qr(2))*qr_d1(1) - sin(qr(1))*sin(qr(2))*qr_d1(2)) - sin(qr(3))*(cos(qr(1))*sin(qr(2)) + cos(qr(2))*sin(qr(1)))*qr_d1(3)) + l2*(cos(qr(1))*cos(qr(2))*qr_d1(1) + cos(qr(1))*cos(qr(2))*qr_d1(2) - sin(qr(1))*sin(qr(2))*qr_d1(1) - sin(qr(1))*sin(qr(2))*qr_d1(2)) + l1*cos(qr(1))*qr_d1(1);
    zch_d1 = ...
    l3*cos(qr(3))*qr_d1(3);


    %calculate dynamics
    M = ...
    [[(l1^2*m1)/3 + l1^2*m2 + l1^2*m3 + (l2^2*m2)/3 + l2^2*m3 + (l3^2*m3*cos(qr(3))^2)/3 + l1*l2*m2*cos(qr(2)) + 2*l1*l2*m3*cos(qr(2)) + l2*l3*m3*cos(qr(3)) + l1*l3*m3*cos(qr(2))*cos(qr(3)), (l2^2*m2)/3 + l2^2*m3 + (l3^2*m3*cos(qr(3))^2)/3 + (l1*l2*m2*cos(qr(2)))/2 + l1*l2*m3*cos(qr(2)) + l2*l3*m3*cos(qr(3)) + (l1*l3*m3*cos(qr(2))*cos(qr(3)))/2, -(l1*l3*m3*sin(qr(2))*sin(qr(3)))/2]; [(l2^2*m2)/3 + l2^2*m3 + (l3^2*m3*cos(qr(3))^2)/3 + (l1*l2*m2*cos(qr(2)))/2 + l1*l2*m3*cos(qr(2)) + l2*l3*m3*cos(qr(3)) + (l1*l3*m3*cos(qr(2))*cos(qr(3)))/2, (l2^2*m2)/3 + l2^2*m3 + (l3^2*m3*cos(qr(3))^2)/3 + l2*l3*m3*cos(qr(3)), 0]; [-(l1*l3*m3*sin(qr(2))*sin(qr(3)))/2, 0, (l3^2*m3)/3]];
    C = ...
    [[- qr_d1(2)*((l1*l2*m2*sin(qr(2)))/2 + l1*l2*m3*sin(qr(2)) + (l1*l3*m3*cos(qr(3))*sin(qr(2)))/2) - qr_d1(3)*((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2 + (l1*l3*m3*cos(qr(2))*sin(qr(3)))/2), - qr_d1(1)*((l1*l2*m2*sin(qr(2)))/2 + l1*l2*m3*sin(qr(2)) + (l1*l3*m3*cos(qr(3))*sin(qr(2)))/2) - qr_d1(2)*((l1*l2*m2*sin(qr(2)))/2 + l1*l2*m3*sin(qr(2)) + (l1*l3*m3*cos(qr(3))*sin(qr(2)))/2) - qr_d1(3)*((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2 + (l1*l3*m3*cos(qr(2))*sin(qr(3)))/2), - qr_d1(1)*((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2 + (l1*l3*m3*cos(qr(2))*sin(qr(3)))/2) - qr_d1(2)*((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2 + (l1*l3*m3*cos(qr(2))*sin(qr(3)))/2) - (l1*l3*m3*cos(qr(3))*sin(qr(2))*qr_d1(3))/2]; [qr_d1(1)*((l1*l2*m2*sin(qr(2)))/2 + l1*l2*m3*sin(qr(2)) + (l1*l3*m3*cos(qr(3))*sin(qr(2)))/2) - ((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(3), -((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(3), - ((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(1) - ((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(2)]; [((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(2) + qr_d1(1)*((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2 + (l1*l3*m3*cos(qr(2))*sin(qr(3)))/2), ((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(1) + ((l3^2*m3*cos(qr(3))*sin(qr(3)))/3 + (l2*l3*m3*sin(qr(3)))/2)*qr_d1(2), 0]];
    D = ...
    [[0]; [0]; [-(g*l3*m3*cos(qr(3)))/2]];
    J = ...
    [[- l1*sin(qr(1)) - l2*sin(qr(1) + qr(2)) - l3*cos(qr(3))*sin(qr(1) + qr(2)), - l2*sin(qr(1) + qr(2)) - l3*cos(qr(3))*sin(qr(1) + qr(2)), -l3*sin(qr(3))*cos(qr(1) + qr(2))]; [l1*cos(qr(1)) + l2*cos(qr(1) + qr(2)) + l3*cos(qr(3))*cos(qr(1) + qr(2)), l2*cos(qr(1) + qr(2)) + l3*cos(qr(3))*cos(qr(1) + qr(2)), -l3*sin(qr(3))*sin(qr(1) + qr(2))]; [0, 0, l3*cos(qr(3))]];
    J_d1 = ...
    [[- l3*(cos(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - sin(qr(3))*sin(qr(1) + qr(2))*qr_d1(3)) - l2*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - l1*cos(qr(1))*qr_d1(1), - l3*(cos(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - sin(qr(3))*sin(qr(1) + qr(2))*qr_d1(3)) - l2*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)), l3*(sin(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - cos(qr(3))*cos(qr(1) + qr(2))*qr_d1(3))]; [- l3*(sin(qr(3))*cos(qr(1) + qr(2))*qr_d1(3) + cos(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))) - l2*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - l1*sin(qr(1))*qr_d1(1), - l3*(sin(qr(3))*cos(qr(1) + qr(2))*qr_d1(3) + cos(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))) - l2*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)), - l3*cos(qr(3))*sin(qr(1) + qr(2))*qr_d1(3) - l3*sin(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))]; [0, 0, -l3*sin(qr(3))*qr_d1(3)]];
    P = ...
    [[l3*(sin(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - cos(qr(3))*cos(qr(1) + qr(2))*qr_d1(3))*qr_d1(3) - qr_d1(1)*(l3*(cos(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - sin(qr(3))*sin(qr(1) + qr(2))*qr_d1(3)) + l2*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) + l1*cos(qr(1))*qr_d1(1)) - qr_d1(2)*(l3*(cos(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) - sin(qr(3))*sin(qr(1) + qr(2))*qr_d1(3)) + l2*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)))]; [- qr_d1(2)*(l3*(sin(qr(3))*cos(qr(1) + qr(2))*qr_d1(3) + cos(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))) + l2*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))) - (l3*cos(qr(3))*sin(qr(1) + qr(2))*qr_d1(3) + l3*sin(qr(3))*cos(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)))*qr_d1(3) - qr_d1(1)*(l3*(sin(qr(3))*cos(qr(1) + qr(2))*qr_d1(3) + cos(qr(3))*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2))) + l2*sin(qr(1) + qr(2))*(qr_d1(1) + qr_d1(2)) + l1*sin(qr(1))*qr_d1(1))]; [-l3*sin(qr(3))*qr_d1(3)^2]];
    B = ...
    [[1, 0, 0]; [0, 1, 0]; [0, 0, 1]];
    T = ...
    [[0]; [0]; [0]];
    %calculate friction in manipulator joints
    %use Tustin model with Tv, Ts and Tk coefficients
    %velocities for each joints are in vector q_d1

    %generate trajectory for end effector    
    %remember to calculate 1st and 2nd derivative of desired end-effector
    %trajectory
    [qchd, qchd_d1, qchd_d2] = effectorTrajectoryGenerator3D(t, parameters);

        MInv = M^-1;

    %     y'' = P - J M^-1 C q' + J M^-1 u
    %     F = P - J M^-1 C q' - J M^-1 D - J M^-1 T
    %     G = J M^-1
    %     v = qd'' - Kd e' - Kp e
    %     u = G^-1 * (v - F)
    
        detJ = det(J);

        %calculate F
        F = zeros(3,1);
        %calculate G
        G = zeros(3,3);

        qch = [xch; ych; zch];
        qch_d1 = [xch_d1; ych_d1; zch_d1];
        
        %e = qch - qchd;
        %e' = qch' - qchd';

        %calculate errors: e and e'
        %for e' keep e_d1 notation
        e = zeros(3,1);
        e_d1 = zeros(3,1);

        %calculate new input to the system v
        v = zeros(3,1);

        detG = det(G);
        %calculate inverse of G as below
        %Ginv = G^-1;

        %calculate control input u
        u = zeros(3,1);
        
        %calculate state
        qr_d2 = MInv * (B * u - C * q_d1 - D - T);   

    dets = [detG; detJ];            
        
    output_args = zeros(6,1);
    output_args(1:3) = qr_d2;
    output_args(4:6) = qr_d1;
    
    additional.qchd = qchd;
    additional.qchd_d1 = qchd_d1;
    additional.qchd_d2 = qchd_d2;
    additional.dets = dets;
    additional.k = qch;  

end

