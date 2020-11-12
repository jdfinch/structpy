

from structpy import implementation
from structpy.graph.directed.labeled.labeled_digraph_spec import LabeledDigraphSpec

from structpy.map import Himap, Bimap


@implementation(LabeledDigraphSpec)
class LabeledDigraph:

    def __init__(self, edges=None, nodes=None):
        self.edges = Bimap()
        self.nodes = Himap(1)

    def add(self, node, target=None, label=None):
        if target is None:
            self.nodes[node]
