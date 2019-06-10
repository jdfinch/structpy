from standard.graph.graph import Graph
from abc import ABC, abstractmethod

class Frontier(Graph, ABC):
    """
    Abstract class representing the frontier of a traversal, search, or
    exploration

    When adding to the frontier, call `.add(pro, epi)` or 
    `.add(pro, epi, arc)`, where `pro` is the expanded node, `epi` is the node
    to add, and `arc` is an optional arc value from `pro` to `epi`
    """

    def __init__(self, iterable):
        for e in iterable:
            self.add(e)

    @abstractmethod
    def pop(self, element):
        """
        Removes and returns the next element to be considered in the frontier
        """
        pass

    @abstractmethod
    def complete(self):
        """
        Returns a bool representing whether the frontier is done changing
        state
        """
        pass

    def __bool__(self):
        return self.complete()

    

