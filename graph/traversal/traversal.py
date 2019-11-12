
from abc import ABC, abstractmethod

class Traversal(ABC):

    def __init__(self, graph, start):
        self._graph = graph
        self._visited = {start}

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class _TraversalStep:

    def __init__(self, node, source=None, source_label=None, level=0):
        self._node = node
        self._source = source
        self._source_label = source_label
        self._level = level

    def node(self):
        return self._node

    def value(self):
        return self.node()

    def next_steps(self, graph):
        for n in graph.targets(self._node):
            label = graph.label(self._node, n)
            yield _TraversalStep(n, self._node, label, self._level + 1)

class _Traversal:

    def __init__(self, graph, frontier):
        self._graph = graph
        self._frontier = frontier
        self._step = self._frontier.step()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        item = self._frontier.get()
        for following in item.next_steps(self._graph):
            self._frontier.add(following)
        return item.value()
