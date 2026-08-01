from abc import ABCMeta
from abc import abstractmethod
import numpy as np
from scipy.integrate import solve_ivp

class Simulator:
    __metaclass__ = ABCMeta
        
    def __init__(self, model, dt=0.01) -> None:
        self._model = model
        self._stats = {}
        self._dt = dt
        
    @abstractmethod
    def step(self, t, state):
        pass
        
    def run(self, start: np.array, T: float, dt: float, trajectory):
        self.T = T
        self.dt = dt
        self._trajectory = trajectory
        
        startTime = 0
        self._stats = {'t': [startTime], 
                 'next': 0}
        
        solver = solve_ivp(self.step, [0, T], start, method='RK45', 
                           rtol=1e-3, atol=1e-6, t_eval=list(np.arange(startTime,T+self._dt,self._dt)))
        
        return self._stats, solver
