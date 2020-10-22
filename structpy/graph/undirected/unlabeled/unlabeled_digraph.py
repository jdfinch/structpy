
from structpy import implementation
from structpy.graph.undirected.unlabeled.unlabeled_digraph_spec import UnlabeledDigraphSpec


@implementation(UnlabeledDigraphSpec)
class UnlabeledDigraph:

    def __init__(self, arcs=None):
        self.arcs = {}

    def add_node(self, node):
        pass


if __name__ == '__main__':
    print(UnlabeledDigraphSpec.verify(UnlabeledDigraph))