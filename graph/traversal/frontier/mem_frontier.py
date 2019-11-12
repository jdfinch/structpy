
from structpy.graph.traversal.frontier.frontier import Frontier


class MemFrontier(Frontier):

    def __init__(self, frontier, visited=None):
        self._frontier = frontier
        if visited is None:
            self._visited = {x.node() for x in self._frontier}
        else:
            self._visited = visited
            for item in self._frontier:
                self._visited.add(item.node())
        self._step = frontier.step()

    def add(self, item):
        node = item.node()
        if node not in self._visited:
            self._visited.add(node)
            self._frontier.add(item)

    def get(self):
        return self._frontier.get()

    def __len__(self):
        return len(self._frontier)
