from abc import ABCMeta
from abc import abstractmethod
import numpy as np

class Obstacle:
    __metaclass__ = ABCMeta
    
    def __init__(self, safe_margin=0.2) -> None:
        self._safe_margin = safe_margin
    
    @abstractmethod
    def distance(self, point: np.array):
        return 0
    
    @abstractmethod
    def inside(self, point: np.array):
        return False
    
    @abstractmethod
    def inside_safe(self, point: np.array):
        return False    
    
    @abstractmethod
    def plotType(self):
        return ""  
    
    @property
    def safe_margin(self):
        return self._safe_margin  
