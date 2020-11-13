

from structpy import implementation
from structpy.graph.directed.labeled.labeled_digraph_spec import LabeledDigraphSpec

from structpy.map import Himap


@implementation(LabeledDigraphSpec)
class LabeledDigraph:

    def __init__(self, edges=None, nodes=None):
        self.edges = Himap(1)
        self.nodes = Himap(1)
        if nodes is not None:
            for node in nodes:
                self.add(node)
        if edges is not None:
            for source, target, label in edges:
                self.add(source, target, label)

    def add(self, node, target=None, label=None):
        if target is None:
            self.nodes[node] = {}
        else:
            if not node in self.nodes:
                self.nodes[node] = {}
                self.edges[node] = {}
            if not label in self.nodes[node]:
                self.nodes[node, label] = {}
            if not target in self.edges[node]:
                self.edges[node, target] = {}
            self.nodes[node, label].add(target)
            self.edges[node, target].add(label)

    def has(self, node, target=None, label=None):
        if target is None and label is None:
            return node in self.nodes
        elif label is None:
            return node in self.edges and target in self.edges[node]
        elif target is None:
            return node in self.nodes and label in self.nodes[node]
        else:
            return node in self.nodes and target in self.edges[node] and \
                   self.edges[node, target] == label


if __name__ == '__main__':
    print(LabeledDigraphSpec.verify(LabeledDigraph))