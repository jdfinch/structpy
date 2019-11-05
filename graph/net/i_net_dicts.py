
from structpy.graph.net.net import Net
from structpy.language.simple import each

class INetDicts(Net):

    def __init__(self, other_labeled_graph=None):
        """
        *_sources_labels_targets* : `dict<source: dict<label: set<target>>>`

        *_targets_labels_sources* : `dict<target: dict<label: set<source>>>`

        *_sources_target_label* : `dict<source: dict<target: label>>`
        """
        self._sources_labels_targets = {}
        self._targets_labels_sources = {}
        self._sources_target_label = {}
        if other_labeled_graph is not None:
            for arc in other_labeled_graph.arcs():
                self.add_arc(*arc)

    def nodes(self):
        return self._sources_labels_targets.keys()

    def add_node(self, node):
        self._sources_labels_targets[node] = {}
        self._targets_labels_sources[node] = {}
        self._sources_target_label[node] = {}

    def add_arc(self, source, target, label):
        if label not in self._sources_labels_targets[source]:
            self._sources_labels_targets[source][label] = set()
        self._sources_labels_targets[source][label].add(target)
        if label not in self._targets_labels_sources[target]:
            self._targets_labels_sources[target][label] = set()
        self._targets_labels_sources[target][label].add(source)
        self._sources_target_label[source][target] = label

    def remove_node(self, node):
        sources = self.sources(node)
        targets = self.targets(node)
        for source in sources:
            self.remove_arc(source, node)
        for target in targets:
            self.remove_arc(node, target)
        del self._sources_target_label[node]
        del self._targets_labels_sources[node]
        del self._sources_labels_targets[node]

    def remove_arc(self, source, target):
        label = self.label(source, target)
        self._sources_labels_targets[source][label].remove(target)
        if not self._sources_labels_targets[source][label]:
            del self._sources_labels_targets[source][label]
        self._targets_labels_sources[target][label].remove(source)
        if not self._targets_labels_sources[target][label]:
            del self._targets_labels_sources[target][label]
        del self._sources_target_label[source][target]

    def targets(self, source, label=None):
        if label is None:
            targets = set()
            for label in self._sources_labels_targets[source]:
                targets.update(self._sources_labels_targets[source][label])
            return targets
        else:
            return set(self._sources_labels_targets[source][label])

    def sources(self, target, label=None):
        if label is None:
            sources = set()
            for label in self._targets_labels_sources[target]:
                sources.update(self._targets_labels_sources[target][label])
            return sources
        else:
            return set(self._targets_labels_sources[target][label])

    def label(self, source, target):
        return self._sources_target_label[source][target]

    def arcs(self):
        arcs = set()
        for source in self._sources_target_label:
            for target in self._sources_target_label[source]:
                label = self._sources_target_label[source][target]
                arcs.add((source, target, label))
        return arcs

    def has_arc(self, source, target, label=None):
        if label is None:
            return target in self._sources_target_label[source]
        else:
            tl = self._sources_target_label[source]
            return target in tl and tl[target] == label
