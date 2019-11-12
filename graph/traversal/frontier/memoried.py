
from structpy.graph.traversal.frontier.frontier_composition import FrontierComposition


def Memoried(frontier_cls, visited=None):

    class MemoriedFrontier(frontier_cls):

        def __init__(self, *args, **kwargs):
            self._visited = set()
            frontier_cls.__init__(self, *args, **kwargs)
            if visited is None:
                self._visited = {x.node() for x in self}
            else:
                self._visited = visited
                for item in self:
                    self._visited.add(item.node())

        def add(self, item):
            node = item.node()
            if node not in self._visited:
                self._visited.add(node)
                frontier_cls.add(self, item)

    return MemoriedFrontier

