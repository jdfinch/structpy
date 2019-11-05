
from abc import ABC, abstractmethod
from structpy.graph.node import Node
from structpy.graph.labeled_digraph.labeled_digraph import LabeledDigraph

class Net(LabeledDigraph):

    @abstractmethod
    def nodes(self):
        """

        """
        pass

    @abstractmethod
    def add_node(self, node):
        """

        """
        pass

    @abstractmethod
    def add_arc(self, source, target, label):
        """

        """
        pass

    @abstractmethod
    def remove_node(self, node):
        """

        """
        pass

    @abstractmethod
    def remove_arc(self, source, target):
        """

        """
        pass

    @abstractmethod
    def targets(self, source, label=None):
        """

        """
        pass

    @abstractmethod
    def label(self, source, target):
        """

        """
        pass

    @abstractmethod
    def sources(self, target, label=None):
        """

        """
        pass

    def arcs(self):
        """

        """
        return NotImplementedError()

    def len_nodes(self):
        """

        """
        return len(self.nodes())

    def len_arcs(self):
        """

        """
        return len(self.arcs())

    def node(self, node_value):
        """

        """
        return Node(node_value, self)

    def add(self, node, target=None, label=None):
        if target is None and not self.has_node(node):
            self.add_node(node)

    def has_node(self, node):
        return node in self.nodes()

    def has_arc(self, source, target, label=None):
        if label is None:
            for s, t, l in self.arcs():
                if s == source and t == target:
                    return True
            return False
        else:
            return (source, target, label) in self.arcs()
