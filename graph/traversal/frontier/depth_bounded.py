
from structpy.graph.traversal.frontier.frontier_composition import FrontierComposition
from sys import maxsize

def DepthBounded(frontier_cls, depth):

    class DepthBoundedFrontier(frontier_cls):

        def __init__(self, *args, **kwargs):
            self._depth = 0
            self._max_depth = depth
            frontier_cls.__init__(self, *args, **kwargs)

        def add(self, item):
            if self._depth <= self._max_depth:
                frontier_cls.add(self, (item, self._depth))

        def get(self):
            item, d = frontier_cls.get(self)
            self._depth = d + 1
            return item

    return DepthBoundedFrontier

