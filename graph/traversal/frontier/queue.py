
from structpy.graph.traversal.frontier.frontier import Frontier
from collections import deque

class Queue(deque, Frontier):

    def __init__(self, graph, *initials):
        deque.__init__(self)
        Frontier.__init__(self, graph, *initials)

    add = deque.appendleft

    get = deque.pop

    def __str__(self):
        return 'FrontierQueue(' + ', '.join([str(x) for x in self]) + ')'

    def __repr__(self):
        return str(self)
