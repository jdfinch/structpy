
from structpy.graph.labeled_digraph.map_digraph import MapDigraph


class MapDataDigraph(MapDigraph):

    def __init__(self, arcs=None):
        MapDigraph.__init__(self, arcs)
        self._node_data = {n: {} for n in self.nodes()}

    def add_node(self, node):
        MapDigraph.add_node(self, node)
        self._node_data[node] = {}

    def remove_node(self, node):
        MapDigraph.remove_node(self, node)
        del self._node_data[node]

    def data(self, node):
        return self._node_data[node]