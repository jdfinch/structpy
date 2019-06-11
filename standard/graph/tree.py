import standard.graph.dag as dag
from abc import ABC

class Tree(dag.Dag, ABC):
    """
    """

    def __init__(self, root=None):
        self._root = root
        self.add_node(root)
    
    def root(self):
        """
        Returns the root of this Tree

        Default implementation: returns `self._root`
        """
        return self._root