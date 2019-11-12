
from structpy.graph.traversal.frontier.frontier_composition import FrontierComposition


class Memoried(FrontierComposition):

    def __init__(self, frontier, visited=None):
        FrontierComposition.__init__(self, frontier)
        if visited is None:
            self._visited = {x.node() for x in self._frontier}
        else:
            self._visited = visited
            for item in self._frontier:
                self._visited.add(item.node())

    def add(self, item):
        node = item.node()
        if node not in self._visited:
            self._visited.add(node)
            self._frontier.add(item)



