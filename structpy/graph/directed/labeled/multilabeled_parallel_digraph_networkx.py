from structpy import implementation
import networkx as nx
from structpy.graph.directed.labeled.multilabeled_parallel_digraph_spec import MultiLabeledParallelDigraphSpec


@implementation(MultiLabeledParallelDigraphSpec)
class MultiLabeledParallelDigraphNX:

    __id_count__ = 0
    @classmethod
    def get_id(cls):
        cls.__id_count__ += 1
        return cls.__id_count__

    def __init__(self, edges=None, nodes=None):
        self._nx = nx.MultiDiGraph()
        self._edges = {}
        if nodes is not None:
            self._nx.add_nodes_from(nodes)
        if edges is not None:
            for source, target, label, id in edges:
                self.add(source, target, label, id)

    def has(self, node=None, target=None, label=None, edge_id=None):
        if target is None and label is None and edge_id is None:
            return node in self._nx
        elif label is None and edge_id is None:
            return node in self._nx and target in self._nx[node]
        elif target is None and edge_id is None and label is not None:
            return label in {l for s, t, l, i in self.out_edges(node)}
        elif edge_id is None and node is not None and target is not None and label is not None:
            return label in {l for s, t, l, i in self.edges(node, target, label)}
        elif edge_id is not None and node is None:
            return edge_id in self._edges
        else:
            return self.has(edge_id=edge_id) and self._edges[edge_id] == (node, target, label)

    def targets(self, source, label=None):
        if label is None:
            out_edges = self._nx.out_edges(source)
            return {target for source, target in out_edges}
        else:
            out_edges = self._nx.out_edges(source, data=True)
            return {target for source, target, data in out_edges if data['label'] == label}

    def sources(self, target, label=None):
        if label is None:
            in_edges = self._nx.in_edges(target)
            return {source for source, target in in_edges}
        else:
            in_edges = self._nx.in_edges(target, data=True)
            return {source for source, target, data in in_edges if data['label'] == label}

    def labels(self, source=None, target=None):
        if target is None and source is None:
            return {l for s, t, l, i in self.out_edges(source)}
        elif source is None:
            return {l for s, t, l, i in self.in_edges(target)}
        else:
            return {l for s, t, l, i in self.edges(source, target)}

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
        if self.has(source):
            out_edges = self._nx.out_edges(source, keys=True)
            if label is None:
                return {(s, t, self._nx[s][t][i]['label'], i) for s, t, i in out_edges}
            else:
                return {(s, t, self._nx[s][t][i]['label'], i) for s, t, i in out_edges
                        if self._nx[s][t][i]['label'] == label}
        else:
            return set()

    def in_edges(self, target, label=None):
        if self.has(target):
            in_edges = self._nx.in_edges(target, keys=True)
            if label is None:
                return {(s, t, self._nx[s][t][i]['label'], i) for s, t, i in in_edges}
            else:
                return {(s, t, self._nx[s][t][i]['label'], i) for s, t, i in in_edges
                        if self._nx[s][t][i]['label'] == label}
        else:
            return set()

    def source(self, edge_id):
        return self._edges[edge_id][0]

    def target(self, edge_id):
        return self._edges[edge_id][1]

    def label(self, edge_id):
        return self._edges[edge_id][2]

    def signature(self, edge_id):
        return self._edges[edge_id]

    def nodes(self):
        return set(self._nx.nodes())

    def edges(self, node=None, target=None, label=None):
        if node is None and target is None and label is None:
            return {(s, t, l, i) for i, (s, t, l) in self._edges.items()}
        elif target is None and label is None:
            edges = self.in_edges(node)
            edges.update(self.out_edges(node))
            return edges
        elif node is None and target is None:
            return {(s, t, l, i) for i, (s, t, l) in self._edges.items() if l == label}
        elif label is None:
            return {(node, target, self._nx[node][target][i]['label'], i) for i in self._nx[node][target]}
        else:
            return {(s, t, l, i) for s, t, l, i in self.out_edges(node, label=label)
                    if t == target}

    def add(self, node, target=None, label=None, edge_id=None):
        self._nx.add_node(node)
        if target is not None and label is not None:
            self._nx.add_node(target)
            if edge_id is None:
                edge_id = MultiLabeledParallelDigraphNX.get_id()
            if edge_id in self._edges:
                raise KeyError('Edge edge_id {} already exists.'.format(edge_id))
            self._nx.add_edge(node, target, label=label, key=edge_id)
            self._edges[edge_id] = (node, target, label)
            return edge_id
        elif (target is not None and label is None) or (target is None and label is not None):
            raise Exception('Both target and label must be specified to add an edge.')

    def remove(self, node=None, target=None, label=None, edge_id=None):
        if target is None and label is None and edge_id is None:
            self._nx.remove_node(node)
        elif target is not None and label is not None and edge_id is not None:
            del self._edges[edge_id]
            self._nx.remove_edge(node, target, key=edge_id)
        elif label is None and edge_id is None:
            for s, t, l, i in self.edges(node, target):
                self.remove(edge_id=i)
        elif edge_id is None:
            to_remove = self.edges(node, target, label)
            for _, _, _, edge_id in to_remove:
                del self._edges[edge_id]
                self._nx.remove_edge(node, target, edge_id)
        else:
            node, target, label = self._edges[edge_id]
            del self._edges[edge_id]
            self._nx.remove_edge(node, target, edge_id)

    def set(self, old, new):
        for out_edge in self.out_edges(old):
            self.remove(*out_edge)
            self.add(new, *out_edge[1:])
        for in_edge in self.in_edges(old):
            self.remove(*in_edge)
            self.add(in_edge[0], new, in_edge[2:])
        self.remove(old)

    def set_label(self, label, edge_id=None):
        source, target = self._edges[edge_id][:2]
        self._edges[edge_id] = (source, target, label)
        self._nx[source][target][edge_id]['label'] = label

if __name__ == '__main__':
    print(MultiLabeledParallelDigraphSpec.verify(MultiLabeledParallelDigraphNX))