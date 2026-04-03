from abc import ABCMeta
from abc import abstractmethod
import numpy as np

class Model:
    __metaclass__ = ABCMeta
    
    def __init__(self, state: np.array, dt: float) -> None:
        self._state = state     # vehicle state
        self._dt = dt           # time step
        
    @abstractmethod
    def step(self, u: np.array):
        pass
    
    @property
    def n(self):
        return len(self.state)
    
    @property
    @abstractmethod
    def m(self):
        pass
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state   
