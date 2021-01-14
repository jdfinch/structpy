
from structpy import implementation
from structpy.graph.directed.labeled.data.multilabeled_parallel_digraph_data_spec import MultiLabeledParallelDigraphDataSpec
from structpy.graph.directed.labeled.multilabeled_parallel_digraph_networkx import MultiLabeledParallelDigraphNX
from structpy.collection.attributes import Attributes
from collections import defaultdict


@implementation(MultiLabeledParallelDigraphDataSpec)
class MultiLabeledParallelDigraphDataNX(MultiLabeledParallelDigraphNX):

    def __init__(self, edges=None, nodes=None):
        MultiLabeledParallelDigraphNX.__init__(self, edges, nodes)
        self.node_data = defaultdict(Attributes)
        self.edge_data = defaultdict(Attributes)
        if isinstance(edges, dict):
            for k, v in edges.items():
                self.edge_data[k]().update(v)
        if isinstance(nodes, dict):
            for k, v in nodes.items():
                self.node_data[k]().update(v)

    def data(self, node, target=None, label=None, id=None):
        if label is None:
            return self.node_data[node]
        else:
            return self.edge_data[node, target, label, id]


if __name__ == '__main__':
    print(MultiLabeledParallelDigraphDataSpec.verify(MultiLabeledParallelDigraphDataNX))