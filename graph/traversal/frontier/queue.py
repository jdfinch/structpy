
from structpy.graph.traversal.frontier.frontier import Frontier
from collections import deque

class Queue(Frontier, deque):

    def __init__(self, *initials, step=None):
        deque.__init__(self)
        Frontier.__init__(self, *initials, step=step)

    add = deque.appendleft

    get = deque.pop

    def __len__(self):
        return deque.__len__(self)

    def __str__(self):
        return 'FrontierQueue(' + ', '.join([str(x) for x in self]) + ')'

    def __repr__(self):
        return str(self)
