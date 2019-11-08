
from structpy.graph.labeled_digraph import LabeledDigraph


class Net(LabeledDigraph):

    class Node:

        def __init__(self, value=None, **targets):
            self._node_value = value
            self._targets_label = {}
            self._labels_targets = {}
            self._labels_sources = {}
            for target, label in targets:
                self.add(target, label)

        def targets(self, label=None):
            if label is None:
                return self._targets_label.keys()
            else:
                return self._labels_targets[label]

        def label(self, target):
            return self._targets_label[target]

        def sources(self, label=None):
            if label is None:
                sources = set()
                for sset in self._labels_sources.values():
                    sources.update(sset)
                return sources
            else:
                return self._labels_sources[label]

        def add(self, target, label):
            self._targets_label[target] = label
            if label not in self._labels_targets:
                self._labels_targets[label] = set()
            self._labels_targets[label].add(target)
            if label not in target._labels_sources:
                target._labels_sources[label] = set()
            target._labels_sources[label].add(self)

        def remove(self, target):
            label = self._targets_label[target]
            target._labels_sources[label].remove(self)
            if not target._labels_sources[label]:
                del target._labels_sources[label]
            del self._targets_label[target]
            self._labels_targets[label].remove(target)
            if not self._labels_targets[label]:
                del self._labels_targets[label]

        def delete(self):
            for source in self.sources():
                source.remove(self)
            for target in self.targets():
                self.remove(target)

    def __init__(self):
        self._nodes = set()

    def nodes(self):
        return self._nodes

    def add_node(self, node):
        self._nodes.add(node)

    def add_arc(self, source, target, label):
        source.add(target, label)

    def remove_node(self, node):
        node.delete()
        self._nodes.remove(node)

    def remove_arc(self, source, target):
        source.remove(target)

    def targets(self, source, label=None):
        return source.targets(label)

    def label(self, source, target):
        return source.label(target)

    def sources(self, target, label=None):
        return target.sources(label)


