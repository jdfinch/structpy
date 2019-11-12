
from structpy.graph.traversal.frontier.frontier import Frontier
from collections import deque

class Queue(Frontier, deque):

    def __init__(self, *args, **kwargs):
        deque.__init__(self)
        Frontier.__init__(self, *args, **kwargs)

    add = deque.appendleft

    get = deque.pop

    def __len__(self):
        return deque.__len__(self)

    def peek(self):
        return self[-1]