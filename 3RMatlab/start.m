%calculate

%clear;
clearvars -except tEnd 

if exist('tEnd', 'var') == 0
    tEnd = 100;
end

disp('Initializing random number generator');
rng(123456789);

Pi = pi;

m1 = 1;
m2 = 1;
m3 = 1;
mc = m1 + m2 + m3;

l1 = 1;
l2 = 1;
l3 = 1;

a = 0;
b = 0;
c = 0;

g = -10;

Tv = 0.01;
Ts = 0.01;
Tk = 5;

Kp = 10 * eye(3);
Kd = 50 * eye(3);

%define initial conditions for the manipulator
init_qr_d1 = [0; 0; 0];
init_qr = [0; 0; 0.0];

qr1 = init_qr(1);
qr2 = init_qr(2);
qr3 = init_qr(3);

qr = init_qr;

%set sample time for to workspace blocks
sample_time = 0.25;

%parameters for the model
parameters.m1 = m1;
parameters.m2 = m2;
parameters.m3 = m3;
parameters.mc = mc;

parameters.l1 = l1;
parameters.l2 = l2;
parameters.l3 = l3;

parameters.a = a;
parameters.b = b;
parameters.c = c;

parameters.g = g;

parameters.Tv = Tv;
parameters.Ts = Ts;
parameters.Tk = Tk;

parameters.Kp = Kp;
parameters.Kd = Kd;

disp('Starting ...');

    ic = zeros(3+3,1);
    ic(1:3) = init_qr_d1;
    ic(4:6) = init_qr;
    
    modelName = 'modelODE';
    modelNameFun = str2func(modelName);

    opts = odeset('RelTol',1e-6,'AbsTol',1e-6);
    opts = odeset(opts,'OutputFcn','odeplot');
    [t, youtput] = ode45(@(t,y) modelNameFun(t,y,parameters), [0:sample_time:tEnd], ic, opts);
    
    tLength = length(t);
    additional.qchd = zeros(3,tLength);
    additional.qchd_d1 = zeros(3,tLength);
    additional.qchd_d2 = zeros(3,tLength);
    additional.dets = zeros(2,tLength);
    additional.k = zeros(3,tLength);  
    for i = 1:tLength
        [~, additionalNew] = modelNameFun(t(i), youtput(i,:)', parameters);
        additional.qchd(:,i) = additionalNew.qchd;
        additional.qchd_d1(:,i) = additionalNew.qchd_d1;
        additional.qchd_d2(:,i) = additionalNew.qchd_d2;
        additional.dets(:,i) = additionalNew.dets;
        additional.k(:,i) = additionalNew.k;          
    end    
    
    sim_data.time = [0:sample_time:tEnd];
    sim_data.out_qr_d1 = youtput(:,1:3);
    sim_data.out_qr_d0 = youtput(:,4:6);




