
from abc import ABC, abstractmethod
from structpy.graph.traversal.traversal_step import TraversalStep

from structpy.graph.traversal.traversal_step import Step


class Frontier(ABC):

    def __init__(self, graph):
        self.graph = graph
        self.transforms = []
        self.successors = lambda g, step: g.targets(step.node)
        self.output = lambda step: step.node

    def start(self, *initials):
        for initial in initials:
            step = Step(initial)
            for transform in self.transforms:
                for t_step in transform(self.graph, step):
                    self.add(t_step)
        return self

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def add(self, step):
        pass

    def expand(self, step):
        for successor in self.successors(self.graph, step):
            for transform in self.transforms:
                for t_step in transform(self.graph, successor):
                    self.add(t_step)

    def done(self):
        return len(self) > 0

    #############################################################

    def arcs(self):
        return self

    def memoried(self):

        return self


