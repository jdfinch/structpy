
from structpy.graph.flex.flex_forest import FlexForest
from structpy.graph.core.tree import Tree

class FlexTree(FlexForest, Tree):

    def __init__(self, root):
        FlexForest.__init__(self)
        self._root = root
        self.add_node(self._root)

    def root(self):
        return self._root