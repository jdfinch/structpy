
from abc import ABC, abstractmethod
from structpy.graph.traversal.traversal_step import TraversalStep


class Frontier(ABC):

    def __init__(self, *initials, step=None):
        if step is not None:
            self._step = step
        else:
            self._step = TraversalStep.Nodes
        for initial in initials:
            self.add(self._step(initial))

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def add(self, item):
        pass

    def step(self):
        return self._step

    @abstractmethod
    def __len__(self):
        pass

    def __bool__(self):
        return len(self) > 0

