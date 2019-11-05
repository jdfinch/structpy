
from abc import ABC, abstractmethod
from structpy.graph.node import Node

class Net:

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




