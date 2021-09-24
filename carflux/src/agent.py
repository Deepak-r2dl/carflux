"""
The agent class for Pacman
"""

from abc import ABC, abstractmethod

class Agent(ABC):
    
    # Probably a bit risque.
    def __init__(self,**kwargs):
        for k, v in kwargs.items():
            setattr(self,k,v)
        super().__init__()
    
    @abstractmethod
    # Observe world. Encode neighbourhood filter if needbe
    def perceive(self):
        pass
    
    @abstractmethod
    # update internal states, optional
    def update_state(self):
        pass
    
    @abstractmethod
    # react to world settings
    def react(self):
        pass
    
    @abstractmethod
    # communicate observable state,
    def communicate(self):
        pass