
from abc import ABC, abstractmethod
from structpy.graph.traversal.traversal_step import TraversalStep

from structpy.graph.traversal.traversal_step import Step
from structpy.language import Mechanic


class Frontier(ABC):

    def __init__(self, graph):
        self.graph = graph
        self.transforms = []
        self.successors = lambda g, step: g.targets(step.node)
        self.output = lambda step: step.node

    def start(self, *initials):
        initials = [Step(x) for x in initials]
        for transform in self.transforms:
            old_initials = list(initials)
            initials = list()
            for i in range(len(old_initials)):
                step = old_initials[i]
                for t_step in transform(self.graph, step):
                    initials.append(t_step)
        for initial in initials:
            self.add(initial)
        return self

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def add(self, step):
        pass

    def expand(self, step):
        successors = self.successors(self.graph, step)
        for transform in self.transforms:
            old_initials = list(successors)
            successors = list()
            for i in range(len(old_initials)):
                successor = old_initials[i]
                for t_step in transform(self.graph, successor, step):
                    successors.append(t_step)
        for successor in successors:
            yield successor

    def done(self):
        return len(self) > 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.done():
            raise StopIteration
        step = self.get()
        for next_step in self.expand(step):
            self.add(next_step)
        return self.output(step)

    #############################################################

    def arcs(self):
        return self

    def memoried(self):
        @Mechanic(visited=set())
        def remember(this, graph, step, prev=None):
            if step.node not in this.visited:
                this.visited.add(step.node)
                yield step
        self.transforms.append(remember)
        return self


