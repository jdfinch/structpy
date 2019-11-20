
from structpy.graph.labeled_digraph.map_data_digraph import MapDataDigraph


class MapDatabaseDigraph(MapDataDigraph):

    def __init__(self, arcs=None):
        MapDataDigraph.__init__(self, arcs)
        self._arc_data = {(s, t): {} for s, t, _ in self.arcs()}

    def add_arc(self, source, target, label):
        MapDataDigraph.add_arc(self, source, target, label)
        self._arc_data[(source, target)] = {}

    def remove_arc(self, source, target):
        MapDataDigraph.remove_arc(self, source, target)
        del self._arc_data[(source, target)]

    def arc_data(self, source, target):
        return self._arc_data[(source, target)]

