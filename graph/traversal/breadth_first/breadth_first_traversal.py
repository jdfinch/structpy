
from structpy.graph.traversal.traversal import Traversal
from structpy.graph.traversal.frontier.queue import Queue

class BreadthFirstArcTraversal(Traversal):

    def __init__(self, graph, start):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        for target in self._graph.targets(start):
            self._frontier.add((start, target))

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        arc = self._frontier.get()
        source, target = arc
        for next_target in self._graph.targets(target):
            if next_target not in self._visited:
                self._visited.add(next_target)
                self._frontier.add((target, next_target))
        return arc

class BreadthFirstLabeledArcTarversal(Traversal):

    def __init__(self, graph, start):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        for target in self._graph.targets(start):
            label = self._graph.label(start, target)
            self._frontier.add((start, target, label))

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        arc = self._frontier.get()
        source, target, label = arc
        for next_target in self._graph.targets(target):
            if next_target not in self._visited:
                label = self._graph.label(target, next_target)
                self._visited.add(next_target)
                self._frontier.add((target, next_target, label))
        return arc

class BreadthFirstBoundedTraversal(Traversal):

    def __init__(self, graph, start, depth):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        self._frontier.add((start, 0))
        self._depth = depth

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        n, d = self._frontier.get()
        if d < self._depth:
            for target in self._graph.targets(n):
                if target not in self._visited:
                    self._visited.add(target)
                    self._frontier.add((target, d+1))
        return n

class BreadthFirstTraversal(Traversal):
    arcs = BreadthFirstArcTraversal
    labeled_arcs = BreadthFirstLabeledArcTarversal
    bounded = BreadthFirstBoundedTraversal

    def __init__(self, graph, start):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        self._frontier.add(start)

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        n = self._frontier.get()
        for target in self._graph.targets(n):
            if target not in self._visited:
                self._visited.add(target)
                self._frontier.add(target)
        return n
