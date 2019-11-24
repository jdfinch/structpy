
def Database(graph_cls):

    class _GraphDatabase(graph_cls):

        def __init__(self, arcs=None):
            graph_cls.__init__(self)
            self._node_data = {n: {} for n in self.nodes()}
            self._arc_data = {(s, t): {} for s, t, _ in self.arcs()}
            if arcs is not None:
                for arc in arcs:
                    self.add(*arc)

        def add_node(self, node):
            graph_cls.add_node(self, node)
            self._node_data[node] = {}

        def add_arc(self, source, target, label=None):
            if label is None:
                graph_cls.add_arc(self, source, target)
            else:
                graph_cls.add_arc(self, source, target, label)
            self._arc_data[(source, target)] = {}

        def remove_node(self, node):
            graph_cls.remove_node(self, node)
            del self._node_data[node]

        def remove_arc(self, source, target):
            graph_cls.remove_arc(self, source, target)
            del self._arc_data[(source, target)]

        def data(self, node):
            return self._node_data[node]

        def arc_data(self, source, target):
            return self._arc_data[(source, target)]

    return _GraphDatabase

