
from structpy import implementation
from structpy.graph.undirected.unlabeled.undigraph_spec import UndigraphSpec


@implementation(UndigraphSpec)
class Undigraph:

    def __init__(self, arcs=None):
        self.arcs = {}

    def add_node(self, node):
        pass


if __name__ == '__main__':
    print(UndigraphSpec.verify(Undigraph))