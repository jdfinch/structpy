
from structpy.graph.labeled_digraph import MapDatabaseDigraph as Graph
from enum import Enum

class _Model(Enum):
    PULL = 0
    PUSH = 1

class ModelGraph(Graph):

    def __init__(self, arcs=None):
        Graph.__init__(self, arcs)
        self._update = None # dict<node: update>
        self.clear_update()

    def clear_update(self):
        self._update = {node: +node for node in self.nodes()}

    def add_pull(self, node, function_ptr):
        self.data(node)[_Model.PULL] = function_ptr

    def add_push(self, node, function_ptr):
        self.data(node)[_Model.PUSH] = function_ptr

    def pull_update(self, node):
        pass

