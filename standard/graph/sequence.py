import standard.graph.tree as tree

class Sequence(tree.Tree):
    """
    A linear, complete ordering of nodes, where ordering is represented by
    arc direction
    """

    def top(self):
        """
        Returns the last node, or None if the sequence is empty
        """
        raise NotImplementedError()

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
