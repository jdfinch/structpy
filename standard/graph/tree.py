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

    def parent(self, node):
        """
        Return the parent (pro) of the `node`
        """
        for pro in self.pros(node):
            return pro

    def path(self, node, sequence_cls=None):
        """
        Returns a Sequence starting at the root of the tree and ending
        at `node`

        `sequence_cls`: the type of `Sequence` to use
        """
        p = [n for n in self.traverse_reverse(node)]
        p.reverse()
        return sequence_cls(p)

    def traverse_reverse(self, start):
        """
        Traverse the sequence in reverse, starting at node `start`
        """
        yield start
        while start is not self.root():
            start = self.parent(start)
            yield start
