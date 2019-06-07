from standard.graph.graph import Graph
from abc import ABC, abstractmethod

class Frontier(ABC):
    """
    Abstract class representing the frontier of a traversal, search, or
    exploration
    """

    @abstractmethod
    def pop(self, element):
        """
        Removes and returns the next element to be considered in the frontier
        """
        pass

    @abstractmethod
    def complete(self):
        """
        Returns a bool representing whether the 
        """
        pass

    def __bool__(self):
        return self.complete()

    

