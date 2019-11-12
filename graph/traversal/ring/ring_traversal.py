
from structpy.graph.traversal.traversal import Traversal
from structpy.graph.traversal.frontier.queue import Queue


class RingTraversal(Traversal):

    arcs = None
    labeled_arcs = None

    def __init__(self, graph, start, depth=None):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        self._frontier.add((start, 0))
        self._max_depth = depth
        self._ring_traverser = _SingleRingTraversal

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        depth = self._frontier.peek()[-1]
        if self._max_depth is not None and depth > self._max_depth:
            raise StopIteration
        return self._ring_traverser(
            self._frontier,
            self._visited,
            depth,
            self._graph
        )

class _SingleRingTraversal(RingTraversal):

    def __init__(self, frontier, visited, depth, graph):
        self._graph = graph
        self._frontier = frontier
        self._visited = visited
        self._current_depth = depth

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        n, d = self._frontier.peek()
        if d > self._current_depth:
            raise StopIteration
        self._frontier.get()
        for target in self._graph.targets(n):
            if target not in self._visited:
                self._visited.add(target)
                self._frontier.add((target, d+1))
        return n

class RingArcTraversal(RingTraversal):

    def __init__(self, graph, start, depth=None):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        self._ring_traverser = _SingleRingArcTraversal
        self._max_depth = depth
        for target in self._graph.targets(start):
            if target not in self._visited:
                self._frontier.add((start, target, 0))
                self._visited.add(target)

class _SingleRingArcTraversal(RingArcTraversal):

    def __init__(self, frontier, visited, depth, graph):
        self._graph = graph
        self._frontier = frontier
        self._visited = visited
        self._current_depth = depth

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        source, n, d = self._frontier.peek()
        if d > self._current_depth:
            raise StopIteration
        self._frontier.get()
        for target in self._graph.targets(n):
            if target not in self._visited:
                self._visited.add(target)
                self._frontier.add((n, target, d+1))
        return source, n

class RingLabeledArcTraversal(RingTraversal):

    def __init__(self, graph, start, depth=None):
        Traversal.__init__(self, graph, start)
        self._frontier = Queue()
        self._ring_traverser = _SingleRingLabeledArcTraversal
        self._max_depth = depth
        for target in self._graph.targets(start):
            if target not in self._visited:
                label = self._graph.label(start, target)
                self._frontier.add((start, target, label, 0))
                self._visited.add(target)

class _SingleRingLabeledArcTraversal(RingLabeledArcTraversal):

    def __init__(self, frontier, visited, depth, graph):
        self._graph = graph
        self._frontier = frontier
        self._visited = visited
        self._current_depth = depth

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        source, n, l, d = self._frontier.peek()
        if d > self._current_depth:
            raise StopIteration
        self._frontier.get()
        for target in self._graph.targets(n):
            if target not in self._visited:
                label = self._graph.label(n, target)
                self._visited.add(target)
                self._frontier.add((n, target, label, d+1))
        return source, n, l

RingTraversal.arcs = RingArcTraversal
RingTraversal.labeled_arcs = RingLabeledArcTraversal
