import structpy.graph.core.tree as tree
from structpy.graph.core.point_tree import PointTree

class PointSequence(PointTree):
    """

    """

    def __init__(self, iterable=None):
        set_root = False
        self._nodes = set()
        for e in iterable:
            if not set_root:
                self._root = e
                set_root = True
            self.add_node(e)
            self._top = e

    def top(self):
        """
        Returns the last node, or None if the sequence is empty
        """
        return self._top

    def child(self, node):
        """
        Returns the child (epi) of node
        """
        for epi in self.epis(node):
            return epi

    def node_at(self, index):
        """
        Returns the node at a certain index, where the root is index 0
        """
        i = 0
        node = self.root()
        while i < index:
            node = self.child(node)
            i += 1
        return node

    def traverse(self, start=None):
        """
        Traverse the sequence in the forward direction, starting at node `start`
        """
        if start is None:
            start = self.root()
        yield start
        while start is not self.top():
            start = self.child(start)
            yield start

    def traverse_reverse(self, start=None):
        """
        Traverse the sequence in reverse, starting at node `start`
        """
        if start is None:
            start = self.top()
        tree.Tree.traverse_reverse(self, start)