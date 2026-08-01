from abc import ABCMeta
from abc import abstractmethod
import numpy as np
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial

from model import Model
from simulator import Simulator

class UnicycleModel(Model):
    def __init__(self, state: np.array, dt: float, e=0.1) -> None:
        # state is vehicle state: x, y, theta
        super().__init__(state, dt)
        self._e = e
            
    def step(self, u: np.array):
        K = np.array([[np.cos(self.state[2]), 0],
                      [np.sin(self.state[2]), 0],
                      [0                    , 1]])
        dx = np.matmul(K, u)
        self._state = self._state + dx * self._dt
        
        return self._state
        
    @property
    def m(self):
        return 2
    
    @property
    def e(self):
        return self._e
    
    @property
    def h(self):
        e = self._e
        x = self._state[0]
        y = self._state[1]
        theta = self._state[2]
        # TODO: implement linearisation functions h(q)
        # For dynamic linearisation delta = pi/2
        # h1 = x + e * cos(theta + pi/2)
        # h2 = y + e * sin(theta + pi/2)
        # Simplify using trigonometric identities:
        # cos(theta + pi/2) = -sin(theta)
        # sin(theta + pi/2) = cos(theta)
        h = np.array([0, 0])
        return h       
        

def trajectory_generator_square(t, dt=1):
    if type(t) != np.ndarray:
        # TODO: generate square trajectory
        # with e.g. piece wise approach
        h = np.array([0, 0])
        h_d1 = np.array([0, 0])    
        h_d2 = np.array([0, 0])
    else:
        # do not change below code of this function
        h = np.zeros((2, len(t)))
        h_d1 = np.zeros((2, len(t)))
        h_d2 = np.zeros((2, len(t)))
        for i in range(len(t)):
            h[:,i], h_d1[:,i], h_d2[:,i] = trajectory_generator_square(t[i])
        
    return h, h_d1, h_d2


def trajectory_generator_hexagon(t, side=0.4):
    if type(t) != np.ndarray:
        # TODO: generate hexagonal trajectory
        # A regular hexagon has 6 sides, each of length 'side'.
        # The time to traverse one side is 'side' (unit speed).
        # Total period = 6 * side.
        # The exterior angle between consecutive sides is pi/3.
        # For each segment k (k=0..5), the direction angle is k * pi/3.
        # Use piece-wise linear segments with constant velocity
        # along each side.
        h = np.array([0, 0])
        h_d1 = np.array([0, 0])
        h_d2 = np.array([0, 0])
    else:
        # do not change below code of this function
        h = np.zeros((2, len(t)))
        h_d1 = np.zeros((2, len(t)))
        h_d2 = np.zeros((2, len(t)))
        for i in range(len(t)):
            h[:,i], h_d1[:,i], h_d2[:,i] = trajectory_generator_hexagon(t[i])

    return h, h_d1, h_d2


def trajectory_generator_circle(t, w=np.pi * 0.4, offset=0.2, A=1.0):
    h = np.array([A*np.cos(t*w + offset), A*np.sin(t*w + offset)])
    # TODO: calculate first and second derivative
    h_d1 = np.array([t, t])    
    h_d2 = np.array([t, t])
    return h, h_d1, h_d2


class SimulatorDynamics(Simulator):
    def __init__(self, model, dt=0.01) -> None:
        self._model = model
        self._stats = {}
        self._dt = dt
        
    def step(self, t, state):
        h = state[0:2]
        h_d1 = state[2:4]
        q = state[4:7]     # x, y, theta
        chi1 = state[7]    # extended state: chi1 = v - e*omega
        
        theta = q[2]
        e = self._model.e
        
        self._model.state = q
        
        # TODO: construct the dynamic decoupling matrix Kd
        # Kd is a 2x2 matrix that depends on theta and chi1.
        # It was derived during the lecture by differentiating 
        # h(q) twice and grouping the terms w.r.t. 
        # new inputs w1 and w2.
        # h'' = Kd @ w
        Kd = np.array([[1, 0],
                       [0, 1]])
        detKd = np.linalg.det(Kd)
        
        Kd_inv = np.linalg.inv(Kd)
        
        hd, hd_d1, hd_d2 = self._trajectory(t)
        
        Kp = 200
        Kd_gain = 20
        
        # TODO: calculate errors and their first derivative
        eh = np.zeros((2))
        eh_d1 = np.zeros((2))
        
        # TODO: introduce new input to the system (PD with feedforward)
        # v_new = hd_d2 - Kp * eh - Kd_gain * eh_d1
        v_new = np.zeros((2))
        # TODO: calculate control signals w = [w1, w2]
        # using dynamic decoupling: w = Kd_inv @ v_new
        # w1 = dchi1/dt, w2 = omega
        w = np.zeros((2))
        
        w1 = w[0]  # = dchi1/dt
        w2 = w[1]  # = omega
        
        # TODO: calculate real unicycle control signals
        # omega comes directly from w2
        # linear velocity: vel = chi1 + e * omega
        # (derived from chi1 = v - e*omega)
        omega = 0
        vel = 0
        
        # TODO: calculate h second derivative h''
        # h_d2 = Kd @ w
        h_d2 = np.zeros((2))
        
        # TODO: calculate state derivatives for the ODE
        # q_d1: unicycle kinematics [vel*cos(theta), vel*sin(theta), omega]
        # chi1_d1: derivative of extended state = w1
        q_d1 = np.zeros((3))
        chi1_d1 = 0
        
        new_state = np.concatenate([h_d1, h_d2, q_d1, [chi1_d1]])
        
        if t >= self._stats['next']:
            self._stats['next'] = t + self._dt
            print(f"t: {t:.2f}, "
                    f"e_h: {eh}, h: {h}, hd: {hd}, "
                    f"x: {q[0]:.2f}, y: {q[1]:.2f}, theta: {q[2]:.2f}, "
                    f"chi1: {chi1:.4f}, detKd: {detKd:.6f}")
        
        return np.array(new_state)
