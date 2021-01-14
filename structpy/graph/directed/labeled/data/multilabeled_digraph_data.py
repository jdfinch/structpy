
from structpy import implementation
from structpy.graph.directed.labeled.data.multilabeled_digraph_data_spec import MultiLabeledDigraphDataSpec
from structpy.graph.directed.labeled.multilabeled_digraph_networkx import MultiLabeledDigraphNX
from collections import defaultdict
from structpy.collection import Attributes


@implementation(MultiLabeledDigraphDataSpec)
class MultiLabeledDigraphDataNX(MultiLabeledDigraphNX):

    def __init__(self, edges=None, nodes=None):
        MultiLabeledDigraphNX.__init__(self, edges, nodes)
        self.node_data = defaultdict(Attributes)
        self.edge_data = defaultdict(Attributes)
        if isinstance(edges, dict):
            for k, v in edges.items():
                self.edge_data[k]().update(v)
        if isinstance(nodes, dict):
            for k, v in nodes.items():
                self.node_data[k]().update(v)

    def data(self, node, target=None, label=None):
        if label is None:
            return self.node_data[node]
        else:
            return self.edge_data[node, target, label]


if __name__ == '__main__':
    print(MultiLabeledDigraphDataSpec.verify(MultiLabeledDigraphDataNX))