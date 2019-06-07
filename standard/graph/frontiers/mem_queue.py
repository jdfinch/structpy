from standard.graph.frontiers.queue import Queue
from standard.graph.frontiers.frontier import Frontier

class MemQueue(Queue, Frontier):
    """
    Frontier for breadth-first traversal
    """

    def __init__(self, iterable):
        Queue.__init__(self, iterable)
        self.visited = set(iterable)
    
    def add(self, node):
        """
        Adds an element to the MemQueue, but only if it has never been added
        before. This is implemented using a visited set
        """
        if node not in self.visited:
            Queue.add(self, node)
            self.visited.add(node)

    
