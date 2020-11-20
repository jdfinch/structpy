

from structpy import implementation
from structpy.graph.directed.labeled.labeled_digraph_spec import LabeledDigraphSpec

from structpy.map import Himap, Hifunction

from itertools import chain


@implementation(LabeledDigraphSpec)
class LabeledDigraph:

    def __init__(self, edges=None, nodes=None):
        self._labels = Hifunction(1)
        self._targets = Himap(1)
        self._nodes = set()
        if nodes is not None:
            for node in nodes:
                self.add(node)
        if edges is not None:
            for source, target, label in edges:
                self.add(source, target, label)

    def add(self, node, target=None, label=None):
        self._nodes.add(node)
        if target is not None:
            self._nodes.add(target)
            if (node, label) in self._targets:
                self._targets[node, label].add(target)
            else:
                self._targets[node, label] = [target]
            self._labels[node, target] = label

    def remove(self, node, target=None):
        if target is None:
            for source in self.sources(node):
                self.remove(source, node)
            for target in self.targets(node):
                self.remove(node, target)
            self._nodes.remove(node)
            self._targets.pop(node, default=0)
            self._labels.pop(node, default=0)
            self._targets.codomain.pop(node, default=0)
            self._labels.codomain.pop(node, default=0)
        else:
            label = self._labels[node, target]
            del self._labels[node, target]
            self._targets[node, label].remove_bipredicate(target)
            if not self._targets[node, label]:
                del self._targets[node, label]

    def has(self, node, target=None, label=None):
        if target is None and label is None:
            return node in self._nodes
        elif label is None:
            return node in self._nodes and target in self._labels[node]
        elif target is None:
            return node in self._nodes and label in self._targets[node]
        else:
            return node in self._nodes and (node, target) in self._labels and \
                   self._labels[node, target] == label

    def targets(self, source, label=None):
        if label is None:
            return set(self._targets[source].values()) if source in self._targets else set()
        else:
            return set(self._targets.get(source, label, default=tuple())) \
                if (source, label) in self._targets else set()

    def sources(self, target, label=None):
        if label is None:
            return set(self._targets.codomain[target].values()) \
                if target in self._targets.codomain else set()
        else:
            return set(self._targets.codomain.get(target, label, default=tuple())) \
                if (target, label) in self._targets.codomain else set()

    def neighbors(self, node, label=None):
        return self.sources(node, label) | self.targets(node, label)

    def out_edges(self, source, label=None):
        if label is None:
            return set([(s, t, l) for s, l, t in self._targets[source].items()]) \
                if source in self._targets else set()
        else:
            return set([(source, target, label) for target in
                        self._targets.get(source, label, default=tuple())]) \
                if (source, label) in self._targets else set()

    def in_edges(self, target, label=None):
        if label is None:
            return set([(s, t, l) for t, l, s in self._targets.codomain[target].items()]) \
                if target in self._targets.codomain else set()
        else:
            return set([(source, target, label) for source in
                        self._targets.codomain.get(target, label, default=tuple())]) \
                if (target, label) in self._targets.codomain else set()

    def nodes(self):
        return set(self._nodes)

    def edges(self, node=None, label=None):
        if node is None and label is None:
            return set(self._labels.items())
        elif label is None:
            return self.in_edges(node) | self.out_edges(node)
        elif node is None:
            return set([(s, t, l) for l, t, s in self._labels.codomain.items()])
        else:
            return self.in_edges(node, label) | self.out_edges(node, label)


if __name__ == '__main__':
    print(LabeledDigraphSpec.verify(LabeledDigraph))