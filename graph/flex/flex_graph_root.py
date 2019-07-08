
from structpy.graph import FlexGraph

class FlexGraphRoot(FlexGraph):
    """
    Nodes are represented as tuples (value, offset)
    """

    def __init__(self):
        self._root = None
        FlexGraph.__init__(self)

    def add_root(self, root):
        self._root = root
        self.add_node(root)

    def get_root(self):
        return self._root