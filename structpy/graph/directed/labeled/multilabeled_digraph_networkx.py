
from structpy import implementation

import networkx as nx
from structpy.graph.directed.labeled.multilabeled_digraph_spec import MultiLabeledDigraphSpec


@implementation(MultiLabeledDigraphSpec)
class MultiLabeledDigraphNX(nx.MultiDiGraph):

    def __init__(self, edges=None, nodes=None):
        super(MultiLabeledDigraphNX, self).__init__()
        if nodes is not None:
            for node in nodes:
                self.add(node)
        if edges is not None:
            for source, target, label in edges:
                self.add(source, target, label)

    def add(self, node, target=None, label=None):
        self.add_node(node)
        if target is not None and label is not None:
            self.add_node(target)
            self.add_edge(node, target, edge=label, key=label)
        elif (target is not None and label is None) or (target is None and label is not None):
            raise Exception('Both target and label must be specified, if one is')

    def has(self, node, target=None, label=None):
        if target is None and label is None:
            return node in self
        elif label is None:
            return target in self[node]
        elif target is None:
            return len(self.out_edges(node, label)) > 0
        else:
            return (node, target, label) in self.out_edges(node)

    def nodes(self):
        return set(super().nodes())

    def targets(self, source, label=None):
        if label is None:
            out_edges = super().out_edges(source)
            return set([target for source, target in out_edges])
        else:
            out_edges = super().out_edges(source, data=True)
            return set([target for source, target, data in out_edges if data['edge']==label])

    def sources(self, target, label=None):
        if label is None:
            in_edges = super().in_edges(target)
            return set([source for source, target in in_edges])
        else:
            in_edges = super().in_edges(target, data=True)
            return set([source for source, target, data in in_edges if data['edge']==label])

    def neighbors(self, node, label=None):
        if label is None:
            neighbors = self.sources(node)
            neighbors.update(self.targets(node))
            return neighbors
        else:
            neighbors = self.sources(node, label)
            neighbors.update(self.targets(node, label))
            return neighbors

    def out_edges(self, source, label=None):
        if label is None:
            out_edges = super().out_edges(source, data=True)
            return set([(source, target, data['edge']) for source, target, data in out_edges])
        else:
            out_edges = super().out_edges(source, data=True)
            return set([(source, target, data['edge']) for source, target, data in out_edges
                        if data['edge']==label])

    def in_edges(self, target, label=None):
        if label is None:
            in_edges = super().in_edges(target, data=True)
            return set([(source, target, data['edge']) for source, target, data in in_edges])
        else:
            in_edges = super().in_edges(target, data=True)
            return set([(source, target, data['edge']) for source, target, data in in_edges
                        if data['edge']==label])

    def edges(self, node=None, label=None):
        if node is None and label is None:
            return set(super().edges(data='edge'))
        elif label is None:
            edges = self.in_edges(node)
            edges.update(self.out_edges(node))
            return edges
        elif node is None:
            return set([edge for edge in super().edges(data='edge') if edge[2]==label])
        else:
            edges = self.in_edges(node, label)
            edges.update(self.out_edges(node, label))
            return edges

    def remove(self, node, target=None, label=None):
        if target is None and label is None:
            self.remove_node(node)
        elif target is not None and label is not None:
            test = self.get_edge_data(node, target)
            self.remove_edge(node, target, key=label)
        elif label is None:
            self.get_edge_data(node, target)
            raise Exception('edge label must be specified')

    def set(self, node, target, old_label=None, new_label=None):
        if old_label is None and new_label is None:
            old_edges = self.edges(node)
            self.remove(node)
            for old_source, old_target, old_label in old_edges:
                if old_source == node:
                    self.add(target, old_target, old_label)
                elif old_target == node:
                    self.add(old_source, target, old_label)
        elif old_label is not None and new_label is not None:
            self.remove(node, target, old_label)
            self.add(node, target, new_label)


if __name__ == '__main__':
    print(MultiLabeledDigraphSpec.verify(MultiLabeledDigraphNX))