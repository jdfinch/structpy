
from structpy import implementation
from structpy.graph.undirected.unlabeled.undigraph_spec import UndigraphSpec


@implementation(UndigraphSpec)
class UndigraphRaw:

    def __init__(self, arcs=None):
        self.arcs = {}



if __name__ == '__main__':
    print(UndigraphSpec.__verify__(UndigraphRaw))