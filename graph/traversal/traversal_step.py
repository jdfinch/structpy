
class _TraversalStep:

    @staticmethod
    def init_frontier(traversal):
        return

class _ArcTraversalStep(_TraversalStep):

    @staticmethod
    def init_frontier(traversal):
        for i in range(len(traversal.frontier())):
            next(traversal)

class TraversalStep:

    class Nodes(_TraversalStep):

        def __init__(self, node):
            self._node = node

        def node(self):
            return self._node

        def value(self):
            return self.node()

        def next_steps(self, graph):
            for n in graph.targets(self._node):
                yield TraversalStep.Nodes(n)

        def __str__(self):
            return '<TraversalStep.Nodes ' \
                   + str(self._node) \
                   + '>'

        def __repr__(self):
            return str(self)

    class Arcs(_ArcTraversalStep):

        def __init__(self, node, source=None):
            self._node = node
            self._source = source

        def node(self):
            return self._node

        def source(self):
            return self._source

        def value(self):
            return self._source, self._node

        def next_steps(self, graph):
            for n in graph.targets(self._node):
                yield TraversalStep.Arcs(n, self._node)

        def __str__(self):
            return '<TraversalStep.Arcs ' \
                   + ', '.join([str(x) for x in (self._source, self._node)]) \
                   + '>'

        def __repr__(self):
            return str(self)

    class LabeledArcs(_ArcTraversalStep):

        def __init__(self, node, source=None, source_label=None):
            self._node = node
            self._source = source
            self._source_label = source_label

        def node(self):
            return self._node

        def source(self):
            return self._source

        def label(self):
            return self._source_label

        def value(self):
            return self._source, self._node, self._source_label

        def next_steps(self, graph):
            for n in graph.targets(self._node):
                label = graph.label(self._node, n)
                yield TraversalStep.LabeledArcs(n, self._node, label)

        def __str__(self):
            return '<TraversalStep.LabeledArcs ' \
                   + ', '.join([str(x) for x in (self._source, self._node, self._source_label)]) \
                   + '>'

        def __repr__(self):
            return str(self)