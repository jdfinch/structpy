
from structpy.graph.traversal.frontier.frontier import Frontier

class Stack(Frontier, list):

    add = list.append

    get = list.pop

    def peek(self):
        return self[-1]
