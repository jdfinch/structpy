
from structpy.graph.traversal.frontier.frontier import Frontier


class FrontierComposition(Frontier):

    def __init__(self, frontier):
        self._frontier = frontier
        self._step = frontier.step()

    def __len__(self):
        return len(self._frontier)

    def __str__(self):
        return str(self._frontier)

    def __repr__(self):
        return str(self)

    def step(self):
        return self._frontier.step()

    def add(self, item):
        self._frontier.add(item)

    def get(self):
        return self._frontier.get()
