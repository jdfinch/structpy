from standard.graph.frontiers.queue import Queue
from standard.graph.frontiers.frontier import Frontier

class MemQueue(Queue, Frontier):
    """
    Frontier for breadth-first traversal search
    """

    def __init__(self, iterable):
        Queue.__init__(self, iterable)
        self.visited = set(iterable)
    
    def add(self, element):
        if element not in self.visited:
            Queue.add(self, element)
            self.visited.add(element)

    
