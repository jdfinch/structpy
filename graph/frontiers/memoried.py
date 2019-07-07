from abc import ABC, abstractmethod
from structpy.graph.frontiers.frontier import Frontier
from structpy.graph.frontiers.stack import Stack
from structpy.graph.frontiers.queue import Queue
from structpy.graph.frontiers.search_tree import SearchTree

class MemoriedFrontier(Frontier, ABC):
    """
    Frontier that keeps track of nodes that have been added and filters out
    added nodes if they appear in this set of previously visited nodes
    """

    def __init__(self):
        self.visited = set()

    @abstractmethod
    def _add_memoried(self, pro, epi=None, arc=None):
        """
        Implement this function to add element to the collection,
        assuming it should be added

        Memoried will automatically ignore (not add) elements that have 
        been added before at any point in the object's lifetime
        """
        pass

    def add(self, pro, epi=None, arc=None):
        """
        Add an node `epi` to the Memoried collection, but not if it has ever
        been added before. Memoried maintains a set of visited nodes to 
        filter out visited nodes from being added
        """
        if epi is None and pro not in self.visited:
            self._add_memoried(pro)
            self.visited.add(pro)
        elif epi is not None and epi not in self.visited:
            self._add_memoried(epi)
            self.visited.add(epi)

    def add_node(self, node):
        if node not in self.visited:
            self._add_memoried(node)
            self.visited.add(node)

def Memoried(frontier):
    """
    Creates and returns a new class of type MemoriedFrontier that also
    inherits from cls

    `cls`: a Frontier class pointer
    """

    class NewMemoriedFrontier(MemoriedFrontier, frontier):
        """
        Generated class for a Frontier that remembers and filters out
        previously added nodes
        """

        def __init__(self, *args, **kwargs):
            MemoriedFrontier.__init__(self)
            frontier.__init__(self, *args, **kwargs)
        

        def _add_memoried(self, pro, epi=None, arc=None):
            return frontier.add(self, pro, epi, arc)

        def __str__(self):
            return 'Mem' + frontier.__str__(self)

    return NewMemoriedFrontier

MemStack = Memoried(Stack)
MemQueue = Memoried(Queue)
