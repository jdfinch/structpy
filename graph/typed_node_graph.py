
from abc import ABC, abstractmethod
from structpy.graph.core.graph import Graph

class TypedNodeGraph(Graph, ABC):

    @abstractmethod
    def node_type(self, node):
        """
        Returns the type of node
        """
        pass
