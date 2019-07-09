
from  structpy.graph.core.point_forest import PointForest

class PointTree(PointForest):
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

    def remove_node(self, node):
        """
        Remove a node without deleting all of its descendents
        :param node: node to remove
        :return: None
        """
        parent = self.parent(node)
        for epi in list(self.epis(node)):
            self.replace_pro(node, epi, parent)
            self.remove_node(node)

    def delete(self, node):
        """
        Remove a node and all its descendents
        :param node: node to remove
        :return: None
        """
        #problems: need to implement traverse
        for node in list(self.traverse(node)):
            self.remove_node(node)

    def path(self, node, sequence_cls=None):
        """
        Returns a Sequence starting at the root of the tree and ending
        at `node`

        `sequence_cls`: the type of `Sequence` to use
        """
        p = [n for n in self.traverse_reverse(node)]
        p.reverse()
        return sequence_cls(p)

    def traverse(self, start):
        """
        Traverse the tree, starting at node `start`
        """
        yield start
        for epi in self.epis(start):
            yield from self.traverse(epi)

    def traverse_reverse(self, start):
        """
        Traverse the tree in reverse, starting at node `start`
        """
        yield start
        while start is not self.root():
            start = self.parent(start)
            yield start